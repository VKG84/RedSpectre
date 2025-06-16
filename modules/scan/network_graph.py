import subprocess
import xml.etree.ElementTree as ET
import networkx as nx

def extract_graph_from_nmap(target):
    xml_file = "/tmp/nmap_scan.xml"
    try:
        subprocess.run(["nmap", "-sV", "-oX", xml_file, target], check=True)
        tree = ET.parse(xml_file)
        root = tree.getroot()

        G = nx.Graph()

        for host in root.findall('host'):
            address = host.find('address').get('addr')
            G.add_node(address)

            for port in host.findall(".//port"):
                portid = port.get("portid")
                service = port.find("service")
                if service is not None:
                    service_name = service.get("name")
                    G.add_node(f"{address}:{portid} ({service_name})")
                    G.add_edge(address, f"{address}:{portid} ({service_name})")

        return G
    except Exception as e:
        raise RuntimeError(f"Erreur dans l'extraction du graphe : {e}")
