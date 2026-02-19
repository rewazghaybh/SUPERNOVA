from terminal_output import display_terminal_report
from json_report import save_to_json


REMEDIATION_MAP = {
    "ftp_anon": "Disable anonymous login in /etc/vsftpd.conf.",
    "smb_guest": "Disable guest access and enforce SMB signing.",
    "http_no_tls": "Enable HTTPS and redirect all HTTP traffic to port 443.",
    "telnet_enabled": "Disable Telnet and use SSH for secure communication."
}

def start_reporting(raw_data):
   
 
    for host in raw_data.get('hosts', []):
        for v in host.get('vulnerabilities', []):
         
            score = v.get('severity_score', 0)
            if score >= 9.0: v['severity_label'] = "Critical"
            elif score >= 7.0: v['severity_label'] = "High"
            elif score >= 4.0: v['severity_label'] = "Medium"
            else: v['severity_label'] = "Low"

         
            ctype = v.get('check_type')
            v['remediation'] = REMEDIATION_MAP.get(ctype, "Consult security best practices.")

 
    display_terminal_report(raw_data)
    save_to_json(raw_data)


if __name__ == "__main__":
    example_data = {
        "scan_info": {"target_scope": "192.168.1.0/24", "start_time": "2026-02-16 21:00", "team_name": "SUPERNOVA"},
        "hosts": [{
            "ip": "192.168.1.10", "status": "Up",
            "vulnerabilities": [{
                "port": 21, "service": "FTP", "cve_id": "CVE-1999-0497", 
                "severity_score": 9.8, "check_type": "ftp_anon", 
                "description": "Anonymous FTP allowed", "evidence": "Logged in as 'anonymous'"
            }]
        }]
    }
    start_reporting(example_data)
