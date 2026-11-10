import json
import random
import requests
import os
from datetime import datetime

def fetch_ips():
    try:
        response = requests.get('https://raw.githubusercontent.com/ircfspace/endpoint/refs/heads/main/ip.json', timeout=10)
        data = response.json()
        return data
    except Exception as e:
        return {
            "ipv4": ["162.159.192.23:859", "162.159.192.178:4500", "162.159.193.1:1701", "162.159.195.2:2408"],
            "ipv6": ["[2606:4700:d1::9f62:b405:88e4:858e]:7152", "[2606:4700:d0::a29f:c001]:1701"]
        }

def generate_config(ip_port, index, ip_version):
    base = f"warp://{ip_port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4&&detour=warp://{ip_port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4#etofot-WoW-{ip_version}-{index}"
    return base

def update_config_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'src', 'templates', 'config_template.txt')
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read().strip()

    ips = fetch_ips()
    
    ipv4_pool = ips.get('ipv4', [])
    ipv6_pool = ips.get('ipv6', [])

    sample_ipv4_count = min(4, len(ipv4_pool))
    sample_ipv6_count = min(2, len(ipv6_pool))

    ipv4_list = random.sample(ipv4_pool, sample_ipv4_count) if sample_ipv4_count > 0 else []
    ipv6_list = random.sample(ipv6_pool, sample_ipv6_count) if sample_ipv6_count > 0 else []
    
    configs = []
    idx = 1
    for ip in ipv4_list:
        configs.append(generate_config(ip, idx, "IPv4"))
        idx += 1
    for ip in ipv6_list:
        configs.append(generate_config(ip, idx, "IPv6"))
        idx += 1
    
    final_config = template + "\n\n" + "\n\n".join(configs) + "\n"
    
    output_path = os.path.join(base_dir, 'config.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_config)
    print(f"Successfully generated {len(configs)} configs in {output_path}")

if __name__ == "__main__":
    update_config_file()
