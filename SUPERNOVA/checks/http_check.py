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
            
        s.close()
        
    except Exception as e:
        result["error"] = str(e)

    return result