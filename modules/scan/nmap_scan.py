import subprocess

def run_nmap_scan(target, mode="standard"):
    if mode == "rapide":
        cmd = ["nmap", "-T4", "-F", target]
    elif mode == "agressif":
        cmd = ["nmap", "-T5", "-A", "-p-", "--reason", "--osscan-guess", target]
    else:  # standard
        cmd = ["nmap", "-T4", "-sV", "-sC", target]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        return result.stdout
    except Exception as e:
        return f"[Erreur Nmap] {e}"
