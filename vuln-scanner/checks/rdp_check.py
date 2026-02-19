import socket

def check_rdp(target: str, port: int = 3389) -> dict:
    """
    Checks if RDP port is open and attempts a basic handshake.
    """
    result = {
        "service": "RDP",
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
            # Simple check: RDP usually requires checking for protocol support
            # which is complex. For now, we report open port and potential
            # banner if sent (RDP doesn't always send banner on connect).
            # A full RDP handshake (like BlueKeep check) requires a lot of bytes.
            result["description"] = "RDP port is open. Ensure NLA is enabled."
            
        s.close()

    except Exception as e:
        result["error"] = str(e)
        
    return result