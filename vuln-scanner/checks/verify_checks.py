import threading
import socket
import time
import sys
import os

# Add project root to path so we can import checks
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from checks.runner import CheckRunner
from checks.network_checks import check_ftp, check_telnet
from checks.web_checks import check_http

def mock_ftp_server(port, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', port))
    s.listen(1)
    s.settimeout(1)
    
    while not stop_event.is_set():
        try:
            conn, addr = s.accept()
            conn.sendall(b"220 Mock FTP Server\r\n")
            while True:
                data = conn.recv(1024)
                if not data: break
                if b"USER anonymous" in data:
                    conn.sendall(b"331 Please specify the password.\r\n")
                elif b"PASS" in data:
                    conn.sendall(b"230 Login successful.\r\n")
                elif b"QUIT" in data:
                    conn.sendall(b"221 Goodbye.\r\n")
                    break
            conn.close()
        except socket.timeout:
            continue
        except Exception as e:
            print(f"FTP Mock Error: {e}")
    s.close()

def mock_http_server(port, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', port))
    s.listen(1)
    s.settimeout(1)

    while not stop_event.is_set():
        try:
            conn, addr = s.accept()
            data = conn.recv(1024)
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Server: MockHTTPServer/1.0\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "Hello, World!"
            )
            conn.sendall(response.encode())
            conn.close()
        except socket.timeout:
            continue
        except Exception as e:
            print(f"HTTP Mock Error: {e}")
    s.close()

def mock_telnet_server(port, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', port))
    s.listen(1)
    s.settimeout(1)

    while not stop_event.is_set():
        try:
            conn, addr = s.accept()
            conn.sendall(b"Welcome to Mock Telnet\r\nLogin: ")
            conn.close()
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Telnet Mock Error: {e}")
    s.close()

def run_tests():
    stop_event = threading.Event()
    
    # Start Mocks
    ftp_port = 2121
    http_port = 8080
    telnet_port = 2323
    
    t_ftp = threading.Thread(target=mock_ftp_server, args=(ftp_port, stop_event))
    t_http = threading.Thread(target=mock_http_server, args=(http_port, stop_event))
    t_telnet = threading.Thread(target=mock_telnet_server, args=(telnet_port, stop_event))
    
    t_ftp.start()
    t_http.start()
    t_telnet.start()
    
    print("Started mock servers...")
    time.sleep(1) # Wait for servers to start
    
    try:
        print("\n--- Testing Individual Checks ---")
        
        print("\n[FTP Check]")
        ftp_res = check_ftp('127.0.0.1', ftp_port)
        print(ftp_res)
        if ftp_res.get("vulnerable"):
            print("SUCCESS: FTP Anonymous Login Detected")
        else:
            print("FAILURE: FTP Anonymous Login NOT Detected")
        
        print("\n[HTTP Check]")
        http_res = check_http('127.0.0.1', http_port)
        print(http_res)
        if http_res.get("vulnerable"):
             print("SUCCESS: HTTP Unencrypted Service Detected")
        else:
             print("FAILURE: Vulnerability NOT Detected")

        print("\n[Telnet Check]")
        print(check_telnet('127.0.0.1', telnet_port))
        
        print("\n--- Testing CheckRunner ---")
        runner = CheckRunner()
        # Note: Runner runs with default ports so we might likely see closed ports 
        # unless we modify runner to accept custom ports or we mock std ports (requires admin).
        # But we can verify it runs without error.
        results = runner.run_all('127.0.0.1')
        for res in results:
            print(f"Check: {res.get('check_name')} - Status: {res.get('status')}")

    finally:
        stop_event.set()
        t_ftp.join()
        t_http.join()
        t_telnet.join()
        print("\nMock servers stopped.")

if __name__ == "__main__":
    run_tests()
