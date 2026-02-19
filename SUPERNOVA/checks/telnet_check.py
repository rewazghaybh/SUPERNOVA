import socket

def check_telnet(target: str, port: int = 23) -> dict:
    """
    Checks for Telnet service and grabs banner.
    Telnet is inherently insecure (cleartext).
    """
    result = {
        "service": "Telnet",
        "port": port,
        "status": "Closed",
        "vulnerable": False,
        "description": "Port is closed"
    }

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        code = s.connect_ex((target, port))
        
        if code == 0:
            result["status"] = "Open"
            result["vulnerable"] = True # Telnet is always a risk
            result["description"] = "Telnet service detected (Cleartext protocol)."
            
            try:
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                result["banner"] = banner
            except:
                pass
                
        s.close()

    except Exception as e:
        result["error"] = str(e)
        
    return result