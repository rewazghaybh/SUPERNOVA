import socket

def check_http(target: str, port: int = 80) -> dict:
    """
    Checks HTTP service and grabs banner.
    """
    result = {
        "service": "HTTP",
        "port": port,
        "status": "Closed",
        "description": "Port is closed"
    }

    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        code = s.connect_ex((target, port))
        
        if code == 0:
            result["status"] = "Open"
            
            # Send simple HTTP GET
            request = f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode())
            
            response = s.recv(4096).decode('utf-8', errors='ignore')
            
            # Extract Server header if present
            server_header = "Unknown"
            status_line = response.split('\r\n')[0] if response else "No Response"
            
            for line in response.split('\r\n'):
                if line.lower().startswith('server:'):
                    server_header = line.split(':', 1)[1].strip()
                    break
            
            result["banner"] = server_header
            result["description"] = f"HTTP Server found: {server_header}. Status: {status_line}"
            
            # Check if using HTTP (not HTTPS)
            if port == 80 or not result.get("ssl", False):  # Simplified assumption for this check
                 result["vulnerable"] = True
                 result["description"] += " - Unencrypted HTTP service detected."
            
    except Exception as e:
        result["error"] = str(e)
    finally:
        if s:
            s.close()

    return result

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

    s = None
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

    except Exception as e:
        result["error"] = str(e)
    finally:
        if s:
            s.close()

    return result
