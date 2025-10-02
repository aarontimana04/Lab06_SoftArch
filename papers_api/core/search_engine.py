import math
from collections import Counter, defaultdict
from .models import Paper
def _tokenize(text:str):
    return [t.lower() for t in ''.join([c if c.isalnum() else ' ' for c in text]).split() if t]
def build_index():
    docs = Paper.objects.all()
    N = docs.count() or 1
    df = Counter(); tokens_by_doc = {}
    for d in docs:
        tokens = _tokenize(f"{d.title} {d.abstract} {d.keywords}")
        tokens_by_doc[d.id] = tokens
        for t in set(tokens): df[t]+=1
    return N, df, tokens_by_doc
def search(query, limit=10, offset=0):
    q_tokens = _tokenize(query)
    if not q_tokens: return [], 0
    N, df, tokens_by_doc = build_index()
    scores = defaultdict(float)
    for doc_id, tokens in tokens_by_doc.items():
        tf = Counter(tokens)
        for t in q_tokens:
            idf = math.log((N+1) / (1 + df.get(t,0))) + 1.0
            scores[doc_id] += (tf.get(t,0) * idf)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total = len(ranked)
    sliced = ranked[offset:offset+limit]
    return sliced, total
