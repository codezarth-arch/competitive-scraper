import time
import threading
from src.database import get_connection
from src.scraper import fetch_page_content
from src.diff import calculate_text_diff

def analyze_keywords(content: str) -> str:
    """
    Identifica palavras-chave críticas no conteúdo extraído.
    """
    text_lower = content.lower()
    if "esgotado" in text_lower or "indisponível" in text_lower:
        return "⚠️ Produto Esgotado / Indisponível"
    elif "promoção" in text_lower or "oferta" in text_lower or "desconto" in text_lower:
        return "⚡ Oferta / Promoção Detetada"
    elif "frete grátis" in text_lower:
        return "📦 Frete Grátis Ativo"
    return "Alteração Estrutural de Preço/Conteúdo"

def run_automated_check():
    print("[MONITOR] A iniciar verificação periódica de concorrentes...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, url, css_selector FROM targets")
        targets = cursor.fetchall()
        
        for target in targets:
            target_id = target["id"]
            name = target["name"]
            url = target["url"]
            css_selector = target["css_selector"]
            
            new_content = fetch_page_content(url, css_selector)
            if not new_content:
                continue
                
            cursor.execute(
                "SELECT content FROM snapshots WHERE target_id = ? ORDER BY captured_at DESC LIMIT 1",
                (target_id,)
            )
            last_snapshot = cursor.fetchone()
            
            if last_snapshot:
                old_content = last_snapshot["content"]
                diff = calculate_text_diff(old_content, new_content)
                
                if diff["additions"] > 0 or diff["deletions"] > 0:
                    cursor.execute(
                        "INSERT INTO snapshots (target_id, content) VALUES (?, ?)",
                        (target_id, new_content)
                    )
                    
                    # Analisa palavras-chave para qualificar o alerta
                    keyword_insight = analyze_keywords(new_content)
                    alert_msg = f"[{keyword_insight}] em '{name}'"
                    
                    cursor.execute(
                        "INSERT INTO alerts (target_id, message, severity) VALUES (?, ?, ?)",
                        (target_id, alert_msg, "warning")
                    )
                    
                    conn.commit()
                    print(f"[MONITOR] {alert_msg}")
            else:
                cursor.execute(
                    "INSERT INTO snapshots (target_id, content) VALUES (?, ?)",
                    (target_id, new_content)
                )
                conn.commit()
        
        conn.close()
        print("[MONITOR] Verificação periódica concluída com sucesso.")
    except Exception as e:
        print(f"[MONITOR] Erro durante a execução automática: {e}")

def schedule_background_monitoring(interval_seconds: int = 300):
    def wrapper():
        while True:
            run_automated_check()
            time.sleep(interval_seconds)
            
    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
    print(f"[MONITOR] Agendador em segundo plano ativado (Intervalo: {interval_seconds}s).")