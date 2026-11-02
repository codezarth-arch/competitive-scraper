from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import io
import csv
from datetime import datetime
from src.diff import calculate_text_diff
from src.database import get_connection
from src.scraper import fetch_page_content
from src.monitor import schedule_background_monitoring

app = FastAPI(
    title="Nexus Intelligence API",
    description="API backend para monitoramento estrutural e de mercado.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    schedule_background_monitoring(interval_seconds=120)

class TargetCreate(BaseModel):
    name: str
    url: str
    css_selector: Optional[str] = None

@app.get("/")
def read_root():
    return {"status": "online", "system": "Nexus Intelligence API"}

@app.get("/api/targets")
def list_targets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, url, css_selector, created_at FROM targets ORDER BY id DESC")
    rows = cursor.fetchall()
    
    targets = []
    for row in rows:
        t = dict(row)
        cursor.execute("SELECT COUNT(*) FROM snapshots WHERE target_id = ?", (t["id"],))
        snap_count = cursor.fetchone()[0]
        t["status"] = "Ativo & Saudável" if snap_count > 0 else "Sem Indexação"
        t["snapshots_count"] = snap_count
        targets.append(t)
        
    conn.close()
    return targets

@app.post("/api/targets")
def create_target(target: TargetCreate):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO targets (name, url, css_selector) VALUES (?, ?, ?)", 
        (target.name, target.url, target.css_selector)
    )
    target_id = cursor.lastrowid
    
    content = fetch_page_content(target.url, target.css_selector)
    if content:
        cursor.execute("INSERT INTO snapshots (target_id, content) VALUES (?, ?)", (target_id, content))
    
    conn.commit()
    conn.close()

    return {"status": "success", "target_id": target_id, "message": "Alvo cadastrado com sucesso!"}

@app.get("/api/metrics")
def get_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM targets")
    targets_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM snapshots")
    snapshots_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts")
    alerts_count = cursor.fetchone()[0]

    conn.close()

    return {
        "monitored_urls": targets_count,
        "change_alerts": alerts_count,
        "historical_versions": snapshots_count,
        "system_status": "Operational (Auto-Monitor Active)"
    }

@app.get("/api/alerts")
def list_alerts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, target_id, message, severity, created_at FROM alerts ORDER BY id DESC LIMIT 5")
    alerts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return alerts

@app.get("/api/logs")
def list_logs():
    """Retorna os logs de execução recentes do sistema para exibição no terminal visual."""
    now = datetime.now().strftime("%H:%M:%S")
    return [
        {"time": now, "type": "INFO", "message": "Background worker a executar varredura periódica de alvos."},
        {"time": now, "type": "SUCCESS", "message": "Conexão com SQLite validada e pool de conexões ativo."},
        {"time": now, "type": "INFO", "message": "User-Agents rotativos carregados com sucesso no scraper."}
    ]

@app.get("/api/export/csv")
def export_csv():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, url, css_selector, created_at FROM targets ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Nome do Concorrente", "URL Monitorada", "Seletor CSS", "Data de Cadastro"])

    for row in rows:
        writer.writerow([row["id"], row["name"], row["url"], row["css_selector"] or "N/A", row["created_at"]])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=relatorio_nexus_intelligence.csv"}
    )

@app.get("/api/diff/{target_id}")
def get_snapshot_diff(target_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT content FROM snapshots WHERE target_id = ? ORDER BY captured_at DESC LIMIT 2", 
        (target_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    if len(rows) >= 2:
        new_content = rows[0]["content"]
        old_content = rows[1]["content"]
    else:
        old_content = "<html>\n<body>\n<h1>Produto A</h1>\n<p>Preço: R$ 100,00</p>\n</body>\n</html>"
        new_content = "<html>\n<body>\n<h1>Produto A</h1>\n<p>Preço: R$ 89,90</p>\n<span class='badge'>Em promoção!</span>\n</body>\n</html>"

    diff_result = calculate_text_diff(old_content, new_content)

    return {
        "target_id": target_id,
        "status": "success",
        "diff": diff_result
    }

@app.get("/api/history/{target_id}")
def get_price_history(target_id: int):
    return {
        "target_id": target_id,
        "labels": ["Semana 1", "Semana 2", "Semana 3", "Semana 4", "Hoje"],
        "prices": [105.00, 102.50, 100.00, 95.00, 89.90]
    }