import subprocess
import os
import json

def get_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        return json.load(f)

def run_nuclei_scan(target, template_type="cves"):
    try:
        config = get_config()
        threads = config.get("nuclei_threads", "10")
        timeout = config.get("nuclei_timeout", "5")
        verbose = config.get("nuclei_verbose", False)
        custom_path = config.get("nuclei_path", "")

        cmd = ["nuclei", "-u", target, "-t", f"templates/{template_type}"]
        if custom_path:
            cmd = ["nuclei", "-u", target, "-t", os.path.join(custom_path, template_type)]
        cmd.extend(["-timeout", timeout, "-c", threads])
        if verbose:
            cmd.append("-v")

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout or result.stderr
    except Exception as e:
        return f"Erreur lors de l'exécution de Nuclei : {e}"
