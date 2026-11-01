# ⚡ Nexus Intelligence — Competitive Scraper

> **Sistema de Monitoramento Estrutural e de Mercado Automatizado**  
> Aplicação full-stack para captura, versionamento e análise de alterações em páginas web concorrentes em tempo real.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Architecture](https://img.shields.io/badge/Scale-Small_to_Medium-emerald?style=for-the-badge)

---

## 📌 Sobre o Projeto

O **Nexus Intelligence** é um *competitive scraper* desenvolvido com arquitetura desacoplada. Ele realiza varreduras periódicas em alvos estruturados na web, armazena *snapshots* históricos de dados e identifica discrepâncias em tempo real através de uma API de alta performance.

Design construído sob a paleta **Obsidian / Dark Mode**, priorizando princípios modernos de UI/UX, psicologia das cores e visualização limpa de métricas.

---

## 🏗️ Arquitetura do Sistema

O projeto adota uma convenção clara de diretórios e separação de responsabilidades (Backend RESTful + Frontend Dashboard):

```text
10_competitive-scraper/
├── 20_frontend/
│   └── 30_index.html        # Dashboard visual em Tailwind CSS & JS
├── 20_src/
│   ├── 30_api.py            # Endpoints FastAPI para leitura de métricas
│   ├── 30_database.py       # Persistência ACID e gestão de Snapshots em SQLite
│   ├── 30_monitor.py        # Loop de verificação periódica de alvos
│   └── 30_scraper.py        # Engine de captura e parse (BeautifulSoup4)
├── 20_data/
│   └── 30_scraper.db        # Banco de dados relacional SQLite
└── 30_requirements.txt      # Dependências da aplicação