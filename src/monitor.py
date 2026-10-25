# src/monitor.py
from src.database import get_db_connection

class ChangeMonitor:
    def __init__(self):
        pass

    def check_and_store(self, url, scraper_result):
        """Compara o hash atual com o histórico e gerencia o versionamento e alertas."""
        if not scraper_result["success"]:
            print(f"[ERRO] Falha ao acessar {url}: {scraper_result['error']}")
            return

        current_hash = scraper_result["content_hash"]
        raw_html = scraper_result["raw_html"]

        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Busca a última versão registrada para esta URL
            cursor.execute(
                'SELECT content_hash FROM page_versions WHERE url = ? ORDER BY id DESC LIMIT 1',
                (url,)
            )
            last_record = cursor.fetchone()

            if last_record is None:
                # Primeira verificação: cria a Baseline
                cursor.execute(
                    'INSERT INTO page_versions (url, content_hash, raw_html) VALUES (?, ?, ?)',
                    (url, current_hash, raw_html)
                )
                print(f"[INFO] Baseline criada para a URL: {url}")
                
            elif last_record['content_hash'] != current_hash:
                # Mudança detectada: salva nova versão e envia alerta
                cursor.execute(
                    'INSERT INTO page_versions (url, content_hash, raw_html) VALUES (?, ?, ?)',
                    (url, current_hash, raw_html)
                )
                
                cursor.execute(
                    'INSERT INTO alerts (url, change_type, description) VALUES (?, ?, ?)',
                    (url, 'Mudança Estrutural', f'Alteração detectada na estrutura de: {url}')
                )
                print(f"[ALERTA] Mudança estrutural registrada para: {url}")
            else:
                print(f"[OK] Sem alterações relevantes em: {url}")