#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rich.console import Console
from colorama import init
import http.server, socketserver, datetime, http.cookies, uuid, json, platform, psutil, socket, logging, traceback, requests, os

init(autoreset=True)
console = Console()

PORT = 8000

def api_location(ip: str | None = None):
    url = "http://ip-api.com/json/" + (ip or "") + "?lang=tr"
    try:
        r = requests.get(url, timeout=4)
        if r.ok and r.json().get("status") == "success":
            d = r.json()
            return {"ip": d.get("query"), "country": d.get("country"), "city": d.get("city"), "latitude": d.get("lat"), "longitude": d.get("lon"), "isp": d.get("isp")}
    except Exception:
        pass
    return None

SERVER_LOCATION = api_location()

TITLE_ASCII = """
 █████╗ ██████╗ ██╗██╗   ██╗ █████╗      ██╗      ██████╗  ██████╗ 
██╔══██╗██╔══██╗██║██║   ██║██╔══██╗     ██║     ██╔═══██╗██╔════╝ 
███████║██████╔╝██║██║   ██║███████║     ██║     ██║   ██║██║  ███╗
██╔══██║██╔══██╗██║╚██╗ ██╔╝██╔══██║██   ██║     ██║   ██║██║   ██║
██║  ██║██║  ██║██║ ╚████╔╝ ██║  ██║╚█████╔╝     ╚██████╔╝╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝ ╚════╝       ╚═════╝  ╚═════╝ 
"""

MENU_CLEAR = "cls" if os.name == "nt" else "clear"
TOOL_RUN_MSG = f"[bold green]Yeni bir terminal açın ve çalıştırın:[/bold green] [yellow]cloudflared tunnel --url http://localhost:{PORT}[/yellow]\n[red]Olmazsa:[/red] [yellow]pkg install cloudflared[/yellow]"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
HTML_STYLE = "font-family:monospace;background:#0d1117;color:#c9d1d9;text-align:center;margin-top:20vh"

class AdvancedLogHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            hdr = self.headers.get
            client_ip = hdr("CF-Connecting-IP") or hdr("X-Real-IP") or (hdr("X-Forwarded-For").split(",")[0].strip() if hdr("X-Forwarded-For") else None) or self.client_address[0]
            cookies = http.cookies.SimpleCookie(hdr("Cookie"))
            uid_cookie = cookies.get("user_id")
            if not uid_cookie:
                uid = uuid.uuid4()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Set-Cookie", f"user_id={uid}; Path=/")
                self.end_headers()
                self.wfile.write(f"<html><body style='{HTML_STYLE}'><h1>Hoş Geldin!</h1><p>Çerez oluşturuldu &#127850;</p></body></html>".encode("utf-8"))
            else:
                uid = uid_cookie.value
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<html><body style='{HTML_STYLE}'><h1>Tekrar Hoş Geldin! &#127881;</h1></body></html>".encode("utf-8"))

            log_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "user_id": str(uid),
                "session_id": str(uuid.uuid4()),
                "ip_address": client_ip,
                "client_location": api_location(client_ip),
                "server_location": SERVER_LOCATION,
                "user_agent": hdr("User-Agent"),
                "referer": hdr("Referer"),
                "accept_language": hdr("Accept-Language"),
                "connection": hdr("Connection"),
                "dnt": hdr("DNT", "N/A"),
                "system_info": {
                    "platform": platform.platform(),
                    "cpu_count": psutil.cpu_count(logical=False),
                    "ram_total": psutil.virtual_memory().total
                },
                "network_info": {
                    "hostname": socket.gethostname(),
                    "remote_port": self.client_address[1]
                }
            }

            log_msg = json.dumps(log_data, indent=4, ensure_ascii=False)
            print(log_msg)
            logging.info(log_msg)

        except Exception as e:
            logging.error(f"{e}\n{traceback.format_exc()}")
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<html><body style='{HTML_STYLE};color:#ff5555'><h1>500 Hata</h1></body></html>".encode("utf-8"))

def show_menu():
    os.system(MENU_CLEAR)
    console.print(f"[bold cyan]{TITLE_ASCII}[/bold cyan]")
    console.print("[bold yellow]1 → Tool'u Çalıştır 🚀[/bold yellow]")

def handle_menu():
    show_menu()
    while True:
        choice = console.input("[white]Seçim (1): [/white]").strip()
        if choice == "1":
            console.print(TOOL_RUN_MSG)
            break
        console.print("[red]Geçersiz seçim![/red]")

def run_server():
    with socketserver.TCPServer(("", PORT), AdvancedLogHandler) as httpd:
        console.print(f"[green]Sunucu {PORT} portunda...[/green]")
        httpd.serve_forever()

if __name__ == "__main__":
    handle_menu()
    run_server()
