from rest_framework import viewsets, views, permissions
from rest_framework.response import Response
from django.db import transaction
from .models import Author, Paper, Subscription, Log
from .serializers import AuthorSerializer, PaperSerializer, SubscriptionSerializer, LogSerializer
from .search_engine import search as engine_search
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all().order_by('-created_at')
    serializer_class = PaperSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        paper = serializer.save()
        Log.objects.create(level='INFO', event='PAPER_CREATED', paper=paper, details=f'URL={paper.url}')
        return paper
class SubscriptionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        sub, _ = Subscription.objects.get_or_create(user=request.user)
        return Response(SubscriptionSerializer(sub).data)
    def post(self, request):
        action = request.query_params.get('action')
        sub, _ = Subscription.objects.get_or_create(user=request.user)
        if action == 'start_trial':
            sub.status='TRIAL'; sub.auto_renew=False; sub.save()
            Log.objects.create(level='INFO', event='TRIAL_STARTED', user=request.user)
            return Response(SubscriptionSerializer(sub).data)
        if action == 'pay':
            sub.status='ACTIVE'; sub.auto_renew=True; sub.save()
            Log.objects.create(level='INFO', event='PAYMENT_SUCCESS', user=request.user)
            return Response(SubscriptionSerializer(sub).data)
        if action == 'cancel':
            sub.status='CANCELED'; sub.auto_renew=False; sub.save()
            Log.objects.create(level='INFO', event='SUBSCRIPTION_CANCELED', user=request.user)
            return Response(SubscriptionSerializer(sub).data)
        return Response({'detail':'action inválida'}, status=400)
class SearchView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        q = request.query_params.get('q','')
        page = int(request.query_params.get('page',1))
        size = int(request.query_params.get('page_size',10))
        offset=(page-1)*size
        ranked, total = engine_search(q, limit=size, offset=offset)
        results = []
        for doc_id, score in ranked:
            p = Paper.objects.get(id=doc_id)
            results.append({'paper_id':p.id,'title':p.title,'score':round(score,3),'url':p.url})
        Log.objects.create(level='INFO', event='SEARCH', user=request.user, details=f'q={q}')
        return Response({'total':total,'page':page,'page_size':size,'results':results})
class DownloadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, paper_id):
        try:
            p = Paper.objects.get(id=paper_id)
        except Paper.DoesNotExist:
            return Response({'detail':'paper not found'}, status=404)
        p.downloads += 1; p.save(update_fields=['downloads'])
        Log.objects.create(level='INFO', event='DOWNLOAD', user=request.user, paper=p, details=f'id={p.id}')
        return Response({'download_url': p.url or f'https://example.org/papers/{p.id}.pdf'})
class OverviewView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        total_papers=Paper.objects.count()
        total_authors=Author.objects.count()
        last_searches=list(Log.objects.filter(event='SEARCH').order_by('-created_at').values('details','created_at')[:10])
        return Response({'total_papers':total_papers,'total_authors':total_authors,'last_searches':last_searches})
class LogsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        logs=Log.objects.all().order_by('-created_at')[:100]
        return Response(LogSerializer(logs, many=True).data)
class ScrapeRunView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        from collections import Counter
        import re
        searches = Log.objects.filter(event='SEARCH').values_list('details', flat=True)
        terms=[]
        for s in searches:
            m=re.search(r"q=(.*)", s or "")
            if m: terms.extend(m.group(1).split())
        cnt=Counter([t.lower() for t in terms if t])
        created=[]
        with transaction.atomic():
            for term, n in cnt.most_common(5):
                title=f"Auto-generated paper about {term}"
                p = Paper.objects.create(title=title, abstract=f"This paper discusses {term}.", keywords=term)
                created.append(p.id)
        Log.objects.create(level='INFO', event='SCRAPE_RUN', user=request.user, details=f'created={len(created)}')
        return Response({'created_ids': created})
