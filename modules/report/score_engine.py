import re

def compute_security_score(recon, scan, nuclei):
    score = 100
    recommendations = []

    # Analyse du scan réseau
    open_ports = len(re.findall(r"open", scan))
    if open_ports > 10:
        score -= 20
        recommendations.append("Réduire le nombre de ports ouverts exposés au public.")
    elif open_ports > 5:
        score -= 10
        recommendations.append("Vérifier la nécessité des services ouverts.")

    # Analyse des vulnérabilités
    critical = len(re.findall(r'\[critical\]', nuclei, re.IGNORECASE))
    high = len(re.findall(r'\[high\]', nuclei, re.IGNORECASE))
    score -= critical * 10
    score -= high * 5

    if critical > 0:
        recommendations.append("Corriger immédiatement les vulnérabilités critiques.")
    if high > 0:
        recommendations.append("Évaluer et corriger les vulnérabilités de niveau élevé.")

    # Analyse WHOIS
    if "Registrar" in recon or "Creation Date" in recon:
        score -= 5
        recommendations.append("Protéger les informations WHOIS si non anonymisées.")

    score = max(0, score)
    return score, recommendations
