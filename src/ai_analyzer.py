def generate_market_insight(target_name: str, old_price: float, new_price: float) -> str:
    """
    Simula um analisador inteligente de mercado que processa variações de preço 
    e gera um resumo executivo acionável para tomada de decisão.
    """
    diff_value = new_price - old_price
    percentage = (diff_value / old_price) * 100 if old_price > 0 else 0
    
    if diff_value < 0:
        return (f"📉 Alerta de Competitividade: O concorrente '{target_name}' reduziu o preço em "
                f"{abs(percentage):.1f}% (de R$ {old_price:.2f} para R$ {new_price:.2f}). "
                f"Recomendação: Avaliar impacto na margem e considerar ajuste tático.")
    elif diff_value > 0:
        return (f"📈 Oportunidade de Mercado: O concorrente '{target_name}' aumentou o preço em "
                f"{percentage:.1f}% (de R$ {old_price:.2f} para R$ {new_price:.2f}). "
                f"Recomendação: Oportunidade para capturar parcela de mercado com o preço atual.")
    else:
        return f"⚖️ Estabilidade: O concorrente '{target_name}' manteve o preço estável em R$ {new_price:.2f}."