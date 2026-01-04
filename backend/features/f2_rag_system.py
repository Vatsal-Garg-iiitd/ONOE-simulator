"""
Feature 2: RAG (Retrieval-Augmented Generation) System
Queries Constitution and Kovind Report for evidence
"""
import json
from typing import List, Dict
from pathlib import Path

class RAGSystem:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.constitution_data = None
        self.kovind_data = None
        self.load_documents()
    
    def load_documents(self):
        """Load Constitution and Kovind Report excerpts"""
        try:
            with open(self.data_dir / "constitution_excerpts.json", "r") as f:
                self.constitution_data = json.load(f)
            
            with open(self.data_dir / "kovind_report_excerpts.json", "r") as f:
                self.kovind_data = json.load(f)
        except Exception as e:
            print(f"Error loading RAG documents: {e}")
            self.constitution_data = {"articles": {}}
            self.kovind_data = {"excerpts": []}
    
    def query_constitution(self, article_number: int) -> Dict:
        """Query Constitution for specific article"""
        article_key = str(article_number)
        if article_key in self.constitution_data.get("articles", {}):
            article = self.constitution_data["articles"][article_key]
            return {
                "source": f"Constitution of India - Article {article_number}",
                "page_number": None,
                "quote": article["text"],
                "context": article["context"],
                "relevance_score": 1.0
            }
        return None
    
    def query_kovind_report(self, article_number: int) -> List[Dict]:
        """Query Kovind Report for relevant excerpts"""
        results = []
        relevance_map = {
            82: "article_82",
            83: "articles_83_172",
            85: "article_85",
            172: "articles_83_172",
            174: "article_174",
            356: "article_356",
            "82A": "article_82A"
        }
        
        target_relevance = relevance_map.get(article_number, "")
        
        for excerpt in self.kovind_data.get("excerpts", []):
            if target_relevance in excerpt.get("relevance", ""):
                results.append({
                    "source": f"Kovind Committee Report - Page {excerpt['page']}",
                    "page_number": excerpt["page"],
                    "quote": excerpt["quote"],
                    "relevance_score": 0.95
                })
        
        # Special handling for Article 356 - add statistics
        if article_number == 356:
            for excerpt in self.kovind_data.get("excerpts", []):
                if "article_356_statistics" in excerpt.get("relevance", ""):
                    results.append({
                        "source": f"Kovind Committee Report - Page {excerpt['page']}",
                        "page_number": excerpt["page"],
                        "quote": excerpt["quote"],
                        "relevance_score": 1.0
                    })
        
        return results
    
    def query_documents(self, article_number: int, query: str = None) -> List[Dict]:
        """
        Main query method - searches both Constitution and Kovind Report
        Returns list of evidence with sources and quotes
        """
        evidence = []
        
        # Get Constitution text
        const_result = self.query_constitution(article_number)
        if const_result:
            evidence.append(const_result)
        
        # Get Kovind Report excerpts
        kovind_results = self.query_kovind_report(article_number)
        evidence.extend(kovind_results)
        
        return evidence

# Singleton instance
rag_system = RAGSystem()
