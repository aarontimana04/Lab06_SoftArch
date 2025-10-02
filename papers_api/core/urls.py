from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, PaperViewSet, SubscriptionView, SearchView, DownloadView, OverviewView, LogsView, ScrapeRunView
router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'papers', PaperViewSet, basename='papers')
urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/check/', SubscriptionView.as_view()),
    path('subscriptions/', SubscriptionView.as_view()),
    path('search/', SearchView.as_view()),
    path('download/<int:paper_id>/', DownloadView.as_view()),
    path('overview/', OverviewView.as_view()),
    path('logs/', LogsView.as_view()),
    path('scrape/run/', ScrapeRunView.as_view()),
]
