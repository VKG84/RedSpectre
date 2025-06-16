import os

def load_targets_from_file(filepath):
    try:
        with open(filepath, "r") as f:
            targets = [line.strip() for line in f if line.strip()]
        return targets
    except Exception as e:
        return f"Erreur de chargement du fichier : {e}"
