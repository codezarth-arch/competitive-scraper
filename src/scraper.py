# src/scraper.py
import requests
from bs4 import BeautifulSoup
import hashlib
import re

class WebScraper:
    def __init__(self, timeout=10):
        self.timeout = timeout
        # Headers simulando um navegador real para evitar bloqueios básicos
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    def fetch_and_clean(self, url):
        """Faz o request HTTP e limpa elementos voláteis do HTML para evitar falsos positivos."""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            raw_html = response.text
            cleaned_html = self._clean_volatile_content(raw_html)
            content_hash = hashlib.sha256(cleaned_html.encode('utf-8')).hexdigest()
            
            return {
                "success": True,
                "raw_html": raw_html,
                "cleaned_html": cleaned_html,
                "content_hash": content_hash,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "raw_html": None,
                "cleaned_html": None,
                "content_hash": None,
                "error": str(e)
            }

    def _clean_volatile_content(self, html_content):
        """Remove elementos dinâmicos que mudam sozinhos (scripts, meta tags, etc)."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove tags que causam ruído na análise estrutural
        for element in soup(["script", "style", "noscript", "meta"]):
            element.decompose()
            
        text_content = soup.get_text(separator=' ', strip=True)
        
        # Limpa padrões de data e hora dinâmicos do texto
        cleaned_text = re.sub(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}', '', text_content)
        
        return cleaned_text