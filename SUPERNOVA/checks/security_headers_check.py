import socket

def check_security_headers(target: str, port: int = 80) -> dict:
    """
    Checks for missing security headers.
    """
    result = {
        "service": "HTTP Headers",
        "port": port,
        "status": "Skipped", # Default if port closed
        "vulnerable": False,
        "description": "Port closed"
    }

    important_headers = [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Strict-Transport-Security", # HSTS
        "Content-Security-Policy"
    ]
    
    missing_headers = []

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        code = s.connect_ex((target, port))
        
        if code == 0:
            result["status"] = "Checked"
            
            request = f"HEAD / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode())
            
            response = s.recv(4096).decode('utf-8', errors='ignore')
            
            headers_found = []
            for line in response.split('\r\n'):
                if ':' in line:
                    key = line.split(':')[0].strip()
                    headers_found.append(key.lower())
            
            for header in important_headers:
                if header.lower() not in headers_found:
                    missing_headers.append(header)
            
            if missing_headers:
                result["vulnerable"] = True
                result["description"] = f"Missing security headers: {', '.join(missing_headers)}"
            else:
                result["description"] = "All checked security headers are present."

        s.close()

    except Exception as e:
        result["error"] = str(e)

    return result