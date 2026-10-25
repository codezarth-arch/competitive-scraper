# src/main.py
from src.database import init_db
from src.scraper import WebScraper
from src.monitor import ChangeMonitor

# URLs de teste para monitoramento
TARGET_URLS = [
    "https://httpbin.org/html",
]

def main():
    print("=== Iniciando Coleta do Scraper ===")
    init_db()
    
    scraper = WebScraper()
    monitor = ChangeMonitor()
    
    for url in TARGET_URLS:
        print(f"Verificando: {url}...")
        result = scraper.fetch_and_clean(url)
        monitor.check_and_store(url, result)
        
    print("=== Processo Finalizado ===")

if __name__ == "__main__":
    main()