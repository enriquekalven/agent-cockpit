import math
import re
from typing import Any, Dict, List


class BM25Engine:
    """
    Python implementation of the weighted BM25 algorithm for Cockpit Context retrieval.
    Inspired by Andrew Ng's Context Hub.
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_count = 0
        self.avg_dl = 0
        self.doc_freqs = {}
        self.idf = {}
        self.corpus = []
        self.field_weights = {
            "name": 3.0,
            "tags": 2.0,
            "description": 1.0,
            "content": 0.5
        }

    def tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def build_index(self, docs: List[Dict[str, Any]]):
        self.corpus = docs
        self.doc_count = len(docs)
        total_dl = 0
        
        # Calculate doc frequencies for IDF
        for doc in docs:
            # Combine all fields into a single token stream for basic IDF, 
            # but we'll score fields individually later.
            combined_text = f"{doc.get('name', '')} {doc.get('description', '')} {' '.join(doc.get('tags', []))} {doc.get('content', '')}"
            tokens = self.tokenize(combined_text)
            total_dl += len(tokens)
            
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.doc_freqs[token] = self.doc_freqs.get(token, 0) + 1
        
        self.avg_dl = total_dl / self.doc_count if self.doc_count > 0 else 0
        
        # Calculate IDF
        for token, freq in self.doc_freqs.items():
            self.idf[token] = math.log((self.doc_count - freq + 0.5) / (freq + 0.5) + 1.0)

    def score_field(self, query_tokens: List[str], field_text: str, weight: float) -> float:
        tokens = self.tokenize(field_text)
        if not tokens:
            return 0.0
            
        tf = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
            
        score = 0.0
        dl = len(tokens)
        
        for q in query_tokens:
            if q not in tf:
                continue
            
            f = tf[q]
            idf = self.idf.get(q, 0)
            
            # BM25 Formula
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * (dl / self.avg_dl)) if self.avg_dl > 0 else f + self.k1
            score += idf * (numerator / denominator)
            
        return score * weight

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []
            
        scores = []
        for _, doc in enumerate(self.corpus):
            total_score = 0.0
            total_score += self.score_field(query_tokens, doc.get("name", ""), self.field_weights["name"])
            total_score += self.score_field(query_tokens, doc.get("description", ""), self.field_weights["description"])
            total_score += self.score_field(query_tokens, " ".join(doc.get("tags", [])), self.field_weights["tags"])
            total_score += self.score_field(query_tokens, doc.get("content", ""), self.field_weights["content"])
            
            if total_score > 0:
                scores.append((total_score, doc))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scores[:limit]]
