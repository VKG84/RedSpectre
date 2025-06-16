from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
from .score_engine import compute_security_score

def generate_global_report(results_dict, output_file="rapport_global.html"):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template("report_template_global.html")

    scored_data = []
    for target, data in results_dict.items():
        recon = data.get("recon", "")
        scan = data.get("scan", "")
        nuclei = data.get("nuclei", "")
        score, recommendations = compute_security_score(recon, scan, nuclei)
        scored_data.append({
            "target": target,
            "scan": scan,
            "recon": recon,
            "nuclei": nuclei,
            "score": score,
            "recommendations": recommendations
        })

    report_html = template.render(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        results=scored_data
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_html)
    return output_file
