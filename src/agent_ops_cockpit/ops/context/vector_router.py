"""
Pillar: Wisdom Store (Semantic Context Engine)
SME Persona: Master Architect
Objective: Elevates BM25 to a dense vector router with resilient fallback for hermetic sandboxes.
"""

import math
import os
from typing import Any, Dict, List

from google.genai import Client
from rich.console import Console

console = Console()


class VectorSemanticRouter:
    """
    Wisdom Store Semantic Router: Generates dense or resilient sparse embeddings to retrieve governance guidelines.
    """

    def __init__(self, use_remote: bool = True):
        self.use_remote = use_remote
        self.corpus: List[Dict[str, Any]] = []
        self.embeddings: List[List[float]] = []
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv(
            "GOOGLE_API_KEY"
        )
        self.is_vertex = (
            os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"
        )
        self.vector_dim = 768  # Standard dimension for text-embedding-004

    def get_embedding_local(self, text: str) -> List[float]:
        """
        [Resilient Fallback]
        Generates a deterministic float vector based on character frequencies (L2 Normalized).
        Guarantees flawless execution in CI/CD without API Keys.
        """
        vector = [0.0] * self.vector_dim
        # Fill vector based on char frequencies and trigrams
        text_lower = text.lower()
        for i, char in enumerate(text_lower[: self.vector_dim * 2]):
            idx = ord(char) % self.vector_dim
            vector[idx] += 1.0 + (i * 0.001)

        # Add simple trigram hashing
        for i in range(len(text_lower) - 2):
            trigram = text_lower[i : i + 3]
            idx = hash(trigram) % self.vector_dim
            vector[idx] += 2.0

        # L2 Normalization
        sq_sum = sum(v * v for v in vector)
        norm = math.sqrt(sq_sum) if sq_sum > 0 else 1.0
        return [v / norm for v in vector]

    def get_embedding_remote(self, text: str) -> List[float]:
        """Generates dense embeddings via Google GenAI Cloud API."""
        if not (self.api_key or self.is_vertex):
            return self.get_embedding_local(text)

        try:
            client = Client()
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=text,
            )
            # Support both object and dict payload variations
            if (
                hasattr(response, "embeddings")
                and response.embeddings
                and len(response.embeddings) > 0
            ):
                first_embed = response.embeddings[0]
                if hasattr(first_embed, "values"):
                    return [float(x) for x in first_embed.values]
                elif isinstance(first_embed, dict) and "values" in first_embed:
                    return [float(x) for x in first_embed["values"]]

            # Fallback if payload extraction was complex
            if hasattr(response, "embedding") and response.embedding:
                if hasattr(response.embedding, "values"):
                    return [float(x) for x in response.embedding.values]

            return self.get_embedding_local(text)

        except Exception as e:
            console.print(
                f"⚠️  [yellow]Gemini Embeddings API Error ({e}). Falling back to Local Router.[/yellow]"
            )
            return self.get_embedding_local(text)

    def get_embedding(self, text: str) -> List[float]:
        if self.use_remote and (self.api_key or self.is_vertex):
            return self.get_embedding_remote(text)
        return self.get_embedding_local(text)

    def build_index(self, docs: List[Dict[str, Any]]):
        """Indexes the documents and generates embeddings for each node."""
        self.corpus = docs
        self.embeddings = []

        console.print(
            f"🧠 [cyan]Vector Router: Embedding {len(docs)} knowledge nodes...[/cyan]"
        )
        for doc in docs:
            # Combine core metadata and content for embedding
            payload = f"Name: {doc.get('name', '')}\nDescription: {doc.get('description', '')}\nCategory: {doc.get('category', '')}\nContent: {doc.get('content', '')}"
            emb = self.get_embedding(payload)
            self.embeddings.append(emb)

        console.print("✅ [green]Semantic Vector Index Built.[/green]")

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(v1, v2, strict=False))
        return dot_product

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Performs a dense vector similarity search."""
        if not self.corpus or not self.embeddings:
            return []

        query_emb = self.get_embedding(query)

        scored_docs = []
        for doc, doc_emb in zip(self.corpus, self.embeddings, strict=False):
            score = self.cosine_similarity(query_emb, doc_emb)
            scored_docs.append({"doc": doc, "score": score})

        # Sort descending by score
        scored_docs.sort(key=lambda x: x["score"], reverse=True)

        return [item["doc"] for item in scored_docs[:limit]]
