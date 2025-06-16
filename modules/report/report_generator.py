from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
from .score_engine import compute_security_score

def generate_report(target, recon, scan, nuclei, output_file="rapport.html"):
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template("report_template.html")

    score, recommendations = compute_security_score(recon, scan, nuclei)

    report_html = template.render(
        target=target,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        recon=recon,
        scan=scan,
        nuclei=nuclei,
        score=score,
        recommendations=recommendations
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_html)
    return output_file
