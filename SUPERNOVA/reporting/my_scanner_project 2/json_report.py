import json
from colorama import Fore, Style

def save_to_json(full_data, filename="scan_results.json"):
    try:
        with open(filename, 'w') as f:
            json.dump(full_data, f, indent=4)
        print(f"{Fore.GREEN}[+] Report successfully saved to {filename}")
    except Exception as e:
        print(f"{Fore.RED}[-] Failed to save JSON: {e}")
