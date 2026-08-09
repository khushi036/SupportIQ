import os
import glob
from typing import List, Dict, Any
from backend.models.schemas import SourceCitation

class KnowledgeRAGRetriever:
    """
    Lightweight, deterministic RAG Retriever for SupportIQ Knowledge Base.
    Indexes policy markdown documents and scores query relevance using term frequency & keyword matching.
    Returns source citations with titles, file excerpts, and confidence scores.
    """
    
    def __init__(self, knowledge_dir: str = None):
        if knowledge_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            knowledge_dir = os.path.join(base_dir, "knowledge")
            
        self.documents = []
        self._load_documents(knowledge_dir)

    def _load_documents(self, knowledge_dir: str):
        md_files = glob.glob(os.path.join(knowledge_dir, "*.md"))
        for filepath in md_files:
            filename = os.path.basename(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            title = filename.replace(".md", "").replace("_", " ").title()
            # Extract first heading if present
            lines = content.split("\n")
            for line in lines:
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    break
                    
            self.documents.append({
                "filename": filename,
                "title": title,
                "content": content,
                "path": filepath
            })

    def search(self, query: str, top_k: int = 2) -> List[SourceCitation]:
        query_words = set(query.lower().split())
        scored_docs = []

        for doc in self.documents:
            content_lower = doc["content"].lower()
            score = 0.0
            matched_snippets = []

            # Scoring heuristics
            for word in query_words:
                if len(word) > 3 and word in content_lower:
                    score += 0.25
                    
            # Check domain keyword boosts
            if any(k in query.lower() for k in ["ship", "track", "where", "delivery", "arrive", "carrier"]) and "shipping" in doc["filename"]:
                score += 0.55
            elif any(k in query.lower() for k in ["refund", "return", "damaged", "broken"]) and "returns" in doc["filename"]:
                score += 0.55
            elif any(k in query.lower() for k in ["cancel", "cancellation", "stop order"]) and "cancellation" in doc["filename"]:
                score += 0.55
            elif any(k in query.lower() for k in ["warranty", "guarantee", "repair", "defect"]) and "warranty" in doc["filename"]:
                score += 0.55
            elif any(k in query.lower() for k in ["payment", "bank", "failed", "deducted", "upi"]) and "payment" in doc["filename"]:
                score += 0.55

            if score > 0:
                # Find best paragraph snippet
                paragraphs = [p.strip() for p in doc["content"].split("\n\n") if p.strip()]
                best_p = paragraphs[0] if paragraphs else doc["content"][:200]
                for p in paragraphs:
                    if any(w in p.lower() for w in query_words if len(w) > 3):
                        best_p = p
                        break

                scored_docs.append({
                    "title": doc["title"],
                    "filename": doc["filename"],
                    "relevance_score": min(round(0.65 + score * 0.3, 2), 0.98),
                    "excerpt": best_p[:250] + ("..." if len(best_p) > 250 else "")
                })

        scored_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        citations = []
        for d in scored_docs[:top_k]:
            citations.append(SourceCitation(
                title=d["title"],
                filename=d["filename"],
                relevance_score=d["relevance_score"],
                excerpt=d["excerpt"]
            ))

        return citations

# Global RAG Instance
rag_retriever = KnowledgeRAGRetriever()
