# ⚡ Nexus Intelligence — Scraper Competitivo com IA

> **Sistema de Monitoramento Estrutural, Análise de Mercado e Inteligência Executiva Automatizada**  
> Aplicação full-stack desacoplada para captura, versionamento histórico, geração de alertas e síntese de inteligência de mercado via IA em tempo real.

![Python](https://img.shields.io/badge/PYTHON-3.14-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FASTAPI-009688?style=for-the-badge&logo=fastapi)
![Tailwind CSS](https://img.shields.io/badge/TAILWIND_CSS-38B2AC?style=for-the-badge&logo=tailwind-css)
![SQLite](https://img.shields.io/badge/SQLITE-003B57?style=for-the-badge&logo=sqlite)
![AI Engine](https://img.shields.io/badge/AI_ENGINE-ENABLED-8A2BE2?style=for-the-badge)
![Scale](https://img.shields.io/badge/SCALE-LARGE-brightgreen?style=for-the-badge)

---

## 📌 Sobre o Projeto

O **Nexus Intelligence** é uma plataforma de inteligência competitiva e monitoramento web projetada sob arquitetura desacoplada e modular. O sistema realiza varreduras periódicas em alvos configurados, calcula divergências estruturais via diffing, persiste o histórico em banco relacional SQLite e utiliza um **motor de IA generativa** para emitir resumos executivos acionáveis sobre movimentações de mercado.

A interface foi desenvolvida sob o conceito **Obsidian / Dark Mode**, priorizando princípios modernos de UI/UX corporativo, ausência de elementos poluídos, navegação otimizada e acessibilidade multi-dispositivo.

---

## 🚀 Funcionalidades Principais

* **Monitoramento Autônomo em Background:** Loop assíncrono em segundo plano para varredura contínua de alvos.
* **Isolamento por Seletores CSS:** Capacidade de focar na extração exata de blocos HTML/Texto (preços, títulos, status de estoque).
* **Análise Executiva com IA:** Geração automática de relatórios resumidos em linguagem natural sobre oscilações de preços e estratégias recomendadas.
* **Dashboard Multi-Alvos:** Tabela interativa para controle individual de saúde, contagem de versões e análise profunda por alvo.
* **Gráficos Evolutivos em Tempo Real:** Renderização de histórico de preços por linha do tempo utilizando Chart.js.
* **Alertas Inteligentes & Logs em Tempo Real:** Terminal visual para acompanhamento das requisições e registro de anomalias detectadas.
* **Exportação Executiva em CSV:** Download instantâneo da base inteira de alvos e métricas em formato padronizado.
* **Anti-Blocking Strategy:** Mecanismo integrado de rotação de User-Agents no scraper.

---

## 🛠️ Arquitetura e Tecnologias

* **Backend:** Python 3.14 + FastAPI (Uvicorn)
* **Frontend:** HTML5, Tailwind CSS (CDN), Chart.js
* **Banco de Dados:** SQLite3 (Local Persistence)
* **Extração & Automação:** Requests, BeautifulSoup4, Background Tasks
* **Controle de Versão:** Git / GitHub

---

## ⚙️ Como Executar o Projeto

1. **Ative o ambiente virtual (`.venv`):**
   ```powershell
   .\.venv\Scripts\Activate.ps1