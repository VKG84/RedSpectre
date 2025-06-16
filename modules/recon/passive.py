import socket
import whois

def passive_recon(target):
    result = f"Reconnaissance passive pour {target}\n"
    try:
        # WHOIS info
        whois_info = whois.whois(target)
        result += f"\n[WHOIS]\n"
        for key, value in whois_info.items():
            result += f"{key}: {value}\n"
    except Exception as e:
        result += f"Erreur WHOIS: {e}\n"

    try:
        # Reverse DNS
        ip = socket.gethostbyname(target)
        hostname = socket.gethostbyaddr(ip)
        result += f"\n[Reverse DNS]\nIP: {ip}\nHostname: {hostname[0]}\n"
    except Exception as e:
        result += f"Erreur DNS inverse: {e}\n"

    return result
