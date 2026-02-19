from colorama import Fore, Style, init

init(autoreset=True)

def display_terminal_report(full_data):
    metadata = full_data.get('scan_info', {})
    hosts = full_data.get('hosts', [])

   
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE}{Style.BRIGHT}          VULNERABILITY SCANNER - FINAL REPORT")
    print(f"{Fore.CYAN}{'='*70}")
    print(f"{Fore.WHITE}Target Scope: {metadata.get('target_scope', 'N/A')}")
    print(f"{Fore.WHITE}Scan Time   : {metadata.get('start_time', 'N/A')}")
    print(f"{Fore.WHITE}Team Name   : {metadata.get('team_name', 'N/A')}")
    print(f"{Fore.CYAN}{'='*70}\n")

    for host in hosts:
        ip = host.get('ip')
        status = host.get('status', 'Unknown').lower()

        if status == 'down':
            print(f"{Fore.RED}[!] Target Host: {ip} is DOWN")
            continue

        print(f"{Fore.YELLOW}{Style.BRIGHT}[+] Target Host: {ip}")
        print(f"{Fore.WHITE}{'-'*50}")

        for v in host.get('vulnerabilities', []):
           
            sev = v.get('severity_label', 'Low')
            color = Fore.RED if sev in ['Critical', 'High'] else Fore.YELLOW
            
            print(f"    {color}[{sev}] {Fore.WHITE}Port: {v.get('port')} ({v.get('service')})")
            print(f"    {Fore.WHITE}ID: {v.get('cve_id')} | Score: {v.get('severity_score')}")
            print(f"    {Fore.WHITE}Description: {v.get('description')}")
            print(f"    {Fore.CYAN}Evidence: {v.get('evidence')}") 
            print(f"    {Fore.GREEN}Remediation: {v.get('remediation')}") 
            print(f"    {Fore.WHITE}{'-'*20}")

    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"Scan Summary: Found {len(hosts)} host(s).")
