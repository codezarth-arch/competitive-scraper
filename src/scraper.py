import urllib.request
import urllib.error
import html.parser
import random

# Lista de User-Agents legítimos para simular diferentes navegadores reais e evitar bloqueios
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.2210.91'
]

class SimpleHTMLSelector(html.parser.HTMLParser):
    def __init__(self, target_tag, target_class=None):
        super().__init__()
        self.target_tag = target_tag.lower()
        self.target_class = target_class
        self.inside_target = False
        self.extracted_text = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == self.target_tag:
            if not self.target_class:
                self.inside_target = True
            else:
                attr_dict = dict(attrs)
                classes = attr_dict.get('class', '').split()
                if self.target_class in classes:
                    self.inside_target = True

    def handle_endtag(self, tag):
        if tag.lower() == self.target_tag and self.inside_target:
            self.inside_target = False

    def handle_data(self, data):
        if self.inside_target:
            cleaned = data.strip()
            if cleaned:
                self.extracted_text.append(cleaned)

def extract_element_text(html_content: str, tag: str = "body", css_class: str = None) -> str:
    parser = SimpleHTMLSelector(tag, css_class)
    parser.feed(html_content)
    return " ".join(parser.extracted_text)

def fetch_page_content(url: str, css_selector: str = None) -> str:
    """
    Realiza o download do HTML utilizando um User-Agent rotativo aleatório 
    e filtra o elemento via seletor CSS, caso especificado.
    """
    selected_agent = random.choice(USER_AGENTS)
    headers = {
        'User-Agent': selected_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            
            if css_selector and "." in css_selector:
                tag, class_name = css_selector.split(".", 1)
                filtered = extract_element_text(html_content, tag, class_name)
                return filtered if filtered else html_content
                
            return html_content
    except Exception as e:
        print(f"[SCRAPER] Erro ao aceder {url} com o agente {selected_agent[:30]}...: {e}")
        return ""