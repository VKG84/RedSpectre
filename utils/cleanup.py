import os
import shutil
import subprocess
import glob

def secure_delete(file_path):
    try:
        if os.path.exists(file_path):
            subprocess.run(["shred", "-u", "-n", "3", file_path], check=True)
            return f"✔️ Fichier supprimé en toute sécurité : {file_path}"
        return f"⚠️ Fichier introuvable : {file_path}"
    except Exception as e:
        return f"Erreur lors de la suppression sécurisée : {file_path} - {e}"

def clean_redspectre_traces():
    deleted = []

    # Nettoyage des fichiers générés
    extensions = ["*.html", "*.xml", "*.nmap", "*.log"]
    for pattern in extensions:
        for filepath in glob.glob(pattern):
            try:
                os.remove(filepath)
                deleted.append(f"✔️ Supprimé : {filepath}")
            except Exception as e:
                deleted.append(f"❌ Erreur : {filepath} - {e}")

    # Historique bash/zsh
    for hist_file in ["~/.bash_history", "~/.zsh_history"]:
        path = os.path.expanduser(hist_file)
        try:
            with open(path, "w") as f:
                f.write("")
            deleted.append(f"✔️ Vider historique : {path}")
        except Exception as e:
            deleted.append(f"❌ Erreur vidage : {path} - {e}")

    # Journaux système (si root)
    logs = ["/var/log/auth.log", "/var/log/syslog"]
    for log in logs:
        if os.path.exists(log) and os.access(log, os.W_OK):
            try:
                with open(log, "w") as f:
                    f.write("")
                deleted.append(f"✔️ Vider : {log}")
            except Exception as e:
                deleted.append(f"⚠️ Non nettoyé : {log} - {e}")

    return deleted
