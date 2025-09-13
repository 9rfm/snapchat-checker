import requests
import random
import string
import time
from colorama import Fore, init
init(autoreset=True)

class SnapchatChecker:
    def __init__(self):
        self.checked = 0
        self.user = ""
        self.available = 0
        self.unavailable = 0
        self.deleted = 0
        self.run = True
        self.target_available = 1005
        self.proxies = None
        self.proxymod = None
        self.proxy_type = None
        self.P = []
        
        print(f"{Fore.CYAN}===== Snapchat Username Checker =====")
        
        self.proxymod = input("Use proxies? (p)aid/(f)ree/(n)o: ").strip().lower()
        if self.proxymod == "p":
            self.proxy_type = input("Proxy type:\n1. http ip:port\n2. socks4\n3. socks5\n4. user:pass@host:port\n5. host:port:user:pass\n6. ip:port:user:pass\n7. user:pass:host:port\nEnter choice (1-7): ").strip()
            proxy_file = input("Enter proxy file path: ").strip()
            try:
                with open(proxy_file, 'r') as file:
                    self.P = [line.strip() for line in file if line.strip()]
                    if not self.P:
                        print(f"{Fore.RED}No valid proxies found in file. Continuing without proxy.")
                        self.proxymod = "n"
                    else:
                        print(f"{Fore.GREEN}Loaded {len(self.P)} proxies.")
            except FileNotFoundError:
                print(f"{Fore.RED}Proxy file not found. Continuing without proxy.")
                self.proxymod = "n"
            except Exception as e:
                print(f"{Fore.RED}Error loading proxy: {str(e)}. Continuing without proxy.")
                self.proxymod = "n"
        elif self.proxymod == "f":
            print(f"{Fore.GREEN}Will use free proxies from public sources.")
        else:
            print(f"{Fore.YELLOW}Continuing without proxy.")
            self.proxymod = "n"
        
        self.mode = input(f"Choose mode:\n1. Check from file\n2. Check random usernames\n3. Check specific username\n4. Check with semi-username patterns\nEnter choice (1-4): ").strip()
        
        if self.mode == "1":
            self.file_path = input("Enter file path containing usernames: ").strip()
            self.usernames = self.load_usernames()
        elif self.mode == "2":
            self.length = int(input("Enter username length: ").strip())
            self.count = int(input("Enter number of usernames to check (or press Enter for unlimited until 1005 available): ").strip() or 0)
        elif self.mode == "3":
            self.username = input("Enter username to check: ").strip()
        elif self.mode == "4":
            self.count = int(input("Enter number of usernames to check (or press Enter for unlimited until 1005 available): ").strip() or 0)
        else:
            print(f"{Fore.RED}Invalid choice. Exiting.")
            exit()
            
        self.start()
    
    def load_usernames(self):
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}File not found. Exiting.")
            exit()
    
    def generate_random_username(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(self.length))
    
    def generate_semi_usernames(self):
        chars = string.ascii_lowercase + string.digits
        patterns = [
            lambda: f"{random.choice(chars)}_{random.choice(chars)}{random.choice(chars)}",
            lambda: f"{random.choice(chars)}-{random.choice(chars)}{random.choice(chars)}",
            lambda: f"{random.choice(chars)}_{random.choice(chars)}",
            lambda: f"{random.choice(chars)}-{random.choice(chars)}"
        ]
        return random.choice(patterns)()
    
    def proxynew(self):
        if self.proxymod == "p":
            self.mode = "Paid Proxy"
            if not self.P:
                print(f"{Fore.RED} No proxies available in the list")
                return None
                
            self.proxy = random.choice(self.P)
            if self.proxy_type == '1':
                self.proxymode = "http ip:port"
                return {
                    'http': f'http://{self.proxy}',
                    'https': f'http://{self.proxy}'
                }
            elif self.proxy_type == '2':
                self.proxymode = "socks4"
                return {
                    'http': f'socks4://{self.proxy}',
                    'https': f'socks4://{self.proxy}'
                }
            elif self.proxy_type == '3':
                self.proxymode = "socks5"
                return {
                    'http': f'socks5://{self.proxy}',
                    'https': f'socks5://{self.proxy}'
                }
            elif self.proxy_type == '4':
                self.proxymode = "user:pass@host:port"
                return {
                    'http': f'http://{self.proxy}',
                    'https': f'http://{self.proxy}'
                }
            elif self.proxy_type == '5':
                self.proxymode = "host:port:user:pass"
                host_port, user_pass = self.proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{host_port}',
                    'https': f'http://{user}:{password}@{host_port}'
                }
            elif self.proxy_type == '6':
                self.proxymode = "ip:port:user:pass"
                ip_port, user_pass = self.proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{ip_port}',
                    'https': f'http://{user}:{password}@{ip_port}'
                }
            elif self.proxy_type == '7':
                self.proxymode = "user:pass:host:port"
                user_pass, host_port = self.proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{host_port}',
                    'https': f'http://{user}:{password}@{host_port}'
                }
        elif self.proxymod == "f":
            self.mode = "Free proxy"
            proxy = self.get_free_proxy()
            if proxy:
                return {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
        return None
    
    def get_free_proxy(self):
        sources = [
            "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt",
            "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&timeout=20000",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
        ]
        
        for source in sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxies = [p.strip() for p in response.text.splitlines() if ":" in p]
                    if "api.proxyscrape.com" in source:
                        proxies = [p.replace("http://", "") for p in proxies if p.startswith("http://")]
                    if proxies:
                        return random.choice(proxies)
            except:
                continue
        return None
    
    def check_username(self, username):
        max_retries = 3
        retry_delay = 2
        
        if self.proxymod in ["p", "f"]:
            self.proxies = self.proxynew()
        
        for attempt in range(max_retries):
            try:
                self.user = username
                url = "https://aws.api.snapchat.com/loq/suggest_username_v3"
                data = {"requested_username": self.user}
                headers = {
                    "User-Agent": "Snapchat/12.43.0.32 (Agile_Client_Error; Android 11; gzip)",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "*/*"
                }
                
                response = requests.post(url, data=data, headers=headers, proxies=self.proxies)
                with open("res.txt", "a", encoding="utf-8") as file:
                    file.write(f"[{self.user}] {response.text}\n")

                if f'"requested_username":"{self.user}","status_code":"OK"' in response.text:
                    self.available += 1
                    with open("available_snapchat.txt", "a", encoding="utf-8") as file:
                        file.write(f"{self.user}\n")
                elif f'"{self.user} is already taken!"' in response.text and '"status_code":"TAKEN"' in response.text:
                    self.unavailable += 1
                elif f'{self.user} is currently unavailable!' in response.text and '"status_code":"DELETED"' in response.text:
                    self.deleted += 1
                else:
                    self.unavailable += 1
                
                self.checked += 1
                break  
                
            except Exception as e:
                if self.proxymod in ["p", "f"] and attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}[RETRY] {username}: {str(e)}. Switching proxy...")
                    self.proxies = self.proxynew()
                    time.sleep(1) 
                elif attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}[RETRY] {username}: {str(e)}. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2 
                else:
                    print(f"{Fore.YELLOW}[ERROR] {username}: {str(e)} after {max_retries} attempts")
    
    def print_status(self):
        print(f"\r{Fore.CYAN}Checked: {self.checked} | {Fore.GREEN}Available: {self.available} | {Fore.RED}Unavailable: {self.unavailable} | {Fore.YELLOW}Deleted: {self.deleted} | {Fore.MAGENTA} username :{self.user}", end='', flush=True)
    
    def start(self):
        print(f"{Fore.CYAN}Starting username checker...")
        
        try:
            if self.mode == "1":
                for username in self.usernames:
                    if not self.run or self.available >= self.target_available:
                        break
                    self.check_username(username)
                    self.print_status()
                    time.sleep(random.uniform(1.5, 3.0))
                print(f"\n{Fore.YELLOW}All usernames checked from file.")
                
            elif self.mode == "2":
                checked = 0
                while (self.count == 0 or checked < self.count) and self.run and self.available < self.target_available:
                    username = self.generate_random_username()
                    self.check_username(username)
                    checked += 1
                    self.print_status()
                    time.sleep(random.uniform(1.5, 3.0))
                if self.count > 0:
                    print(f"\n{Fore.YELLOW}Completed checking {self.count} random usernames.")
                else:
                    print(f"\n{Fore.GREEN}Target of {self.target_available} available usernames reached!")
                    
            elif self.mode == "3":
                self.check_username(self.username)
                self.print_status()
                print("\nUsername check completed.")
                
            elif self.mode == "4":
                checked = 0
                while (self.count == 0 or checked < self.count) and self.run and self.available < self.target_available:
                    username = self.generate_semi_usernames()
                    self.check_username(username)
                    checked += 1
                    self.print_status()
                    time.sleep(random.uniform(1.5, 3.0)) 
                
                if self.count > 0:
                    print(f"\n{Fore.YELLOW}Completed checking {self.count} random usernames.")
                else:
                    print(f"\n{Fore.GREEN}Target of {self.target_available} available usernames reached!")
                
        except KeyboardInterrupt:
            self.run = False
            print(f"\n{Fore.YELLOW}Interrupted by user. Stopping...")
        
        print(f"\n{Fore.CYAN}Final Results:")
        print(f"{Fore.CYAN}Checked: {self.checked} | {Fore.GREEN}Available: {self.available} | {Fore.RED}Unavailable: {self.unavailable} | {Fore.YELLOW}Deleted: {self.deleted}")
        
        if self.available > 0:
            print(f"{Fore.GREEN}Available usernames saved in available_snapchat.txt")

if __name__ == "__main__":
    SnapchatChecker()