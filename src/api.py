# src/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import get_db_connection, init_db

app = FastAPI(title="Competitive Scraper API", version="1.0.0")

# Permite acesso do front-end à API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/api/stats")
def get_stats():
    """Retorna estatísticas gerais do sistema."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT url) as total_urls FROM page_versions")
        urls_count = cursor.fetchone()["total_urls"]
        
        cursor.execute("SELECT COUNT(*) as total_alerts FROM alerts")
        alerts_count = cursor.fetchone()["total_alerts"]
        
        cursor.execute("SELECT COUNT(*) as total_versions FROM page_versions")
        versions_count = cursor.fetchone()["total_versions"]
        
        return {
            "monitored_urls": urls_count,
            "total_alerts": alerts_count,
            "total_versions": versions_count,
            "system_status": "Online"
        }

@app.get("/api/alerts")
def get_alerts():
    """Retorna os alertas registrados."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, change_type, description, created_at FROM alerts ORDER BY id DESC LIMIT 20")
        return [dict(row) for row in cursor.fetchall()]

@app.get("/api/versions")
def get_versions():
    """Retorna o histórico de versões."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, content_hash, created_at FROM page_versions ORDER BY id DESC LIMIT 20")
        return [dict(row) for row in cursor.fetchall()]