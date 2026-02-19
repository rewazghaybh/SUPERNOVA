import socket

def check_ftp(target: str, port: int = 21) -> dict:
    """
    Checks for anonymous FTP login and grabs the banner.
    """
    result = {
        "service": "FTP",
        "port": port,
        "status": "Closed",
        "vulnerable": False,
        "description": "Port is closed"
    }

    try:
        # 1. Connect and Grab Banner
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        code = s.connect_ex((target, port))
        
        if code != 0:
            s.close()
            return result
        
        result["status"] = "Open"
        try:
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            result["banner"] = banner
        except:
            result["banner"] = "No banner"

        # 2. Check Anonymous Login
        s.sendall(b"USER anonymous\r\n")
        response_user = s.recv(1024).decode('utf-8', errors='ignore')
        
        s.sendall(b"PASS anonymous@\r\n")
        response_pass = s.recv(1024).decode('utf-8', errors='ignore')
        
        if "230" in response_pass:  # 230 User logged in, proceed.
            result["vulnerable"] = True
            result["description"] = "Anonymous FTP login allowed (Code 230)."
        else:
            result["description"] = "Anonymous login disabled."
            
        s.close()

    except Exception as e:
        result["error"] = str(e)
        result["description"] = f"Error during check: {e}"

    return result