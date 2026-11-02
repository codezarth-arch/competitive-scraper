import difflib

def calculate_text_diff(old_text: str, new_text: str) -> dict:
    """
    Compara duas strings (ex: conteúdo HTML ou texto de snapshots) 
    e retorna as diferenças detalhadas linha a linha.
    """
    if not old_text:
        old_text = ""
    if not new_text:
        new_text = ""

    # Divide os textos em linhas para análise detalhada
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    # Gera o diff usando a biblioteca nativa difflib
    diff = list(difflib.unified_diff(
        old_lines, 
        new_lines, 
        fromfile='snapshot_anterior', 
        tofile='snapshot_atual', 
        lineterm=''
    ))

    added_count = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
    removed_count = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))

    return {
        "has_changes": len(diff) > 0,
        "added_lines": added_count,
        "removed_lines": removed_count,
        "diff_details": diff
    }