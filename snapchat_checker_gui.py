import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
import requests
import random
import sys
import ctypes
import string
import time
from colorama import Fore, init
from dataclasses import dataclass
def hidecmd():
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class SnapchatCheckerGUI:
    def __init__(self, root):
        hidecmd()
        self.root = root
        self.root.title("Snapchat Username Checker")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        try:
            self.root.iconbitmap("shadow.ico")
        except Exception:
            pass
        
        self.bg_color = "#2c3e50" 
        self.fg_color = "#2c3e50"  
        self.accent_color = "#3498db"  
        self.success_color = "#2ecc71"  
        self.error_color = "#e74c3c"  
        self.warning_color = "#f39c12"  
        
        self.checked = 0
        self.available = 0
        self.unavailable = 0
        self.deleted = 0
        self.run = False
        self.target_available = 1005
        self.proxies = None
        self.proxymod = "n"
        self.proxy_type = None
        self.P = []
        self.mode = "1"
        self.usernames = []
        self.count = 0
        self.length = 5
        self.username = ""
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.settings_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.results_tab, text="Results")
        
        self.setup_settings_tab()
        
        self.setup_results_tab()
        
        self.status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    
    def setup_settings_tab(self):
        proxy_frame = ttk.LabelFrame(self.settings_tab, text="Proxy Settings")
        proxy_frame.pack(fill=tk.X, padx=10, pady=5)
        
        mode_frame = ttk.LabelFrame(self.settings_tab, text="Check Mode")
        mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        options_frame = ttk.LabelFrame(self.settings_tab, text="Options")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons_frame = ttk.Frame(self.settings_tab)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.proxy_var = tk.StringVar(value="n")
        ttk.Label(proxy_frame, text="Use proxies:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(proxy_frame, text="No", variable=self.proxy_var, value="n", command=self.toggle_proxy_options).grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(proxy_frame, text="Paid", variable=self.proxy_var, value="p", command=self.toggle_proxy_options).grid(row=0, column=2, padx=5, pady=5)
        ttk.Radiobutton(proxy_frame, text="Free", variable=self.proxy_var, value="f", command=self.toggle_proxy_options).grid(row=0, column=3, padx=5, pady=5)
        
        self.proxy_type_frame = ttk.Frame(proxy_frame)
        self.proxy_type_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E, padx=5, pady=5)
        self.proxy_type_frame.grid_remove()
        
        self.proxy_type_var = tk.StringVar(value="1")
        ttk.Label(self.proxy_type_frame, text="Proxy type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="HTTP (ip:port)", variable=self.proxy_type_var, value="1").grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="SOCKS4", variable=self.proxy_type_var, value="2").grid(row=0, column=2, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="SOCKS5", variable=self.proxy_type_var, value="3").grid(row=0, column=3, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="user:pass@host:port", variable=self.proxy_type_var, value="4").grid(row=1, column=0, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="host:port:user:pass", variable=self.proxy_type_var, value="5").grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="ip:port:user:pass", variable=self.proxy_type_var, value="6").grid(row=1, column=2, padx=5, pady=5)
        ttk.Radiobutton(self.proxy_type_frame, text="user:pass:host:port", variable=self.proxy_type_var, value="7").grid(row=1, column=3, padx=5, pady=5)
        
        self.proxy_file_frame = ttk.Frame(proxy_frame)
        self.proxy_file_frame.grid(row=2, column=0, columnspan=4, sticky=tk.W+tk.E, padx=5, pady=5)
        self.proxy_file_frame.grid_remove()
        
        ttk.Label(self.proxy_file_frame, text="Proxy file:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.proxy_file_var = tk.StringVar()
        ttk.Entry(self.proxy_file_frame, textvariable=self.proxy_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.proxy_file_frame, text="Browse", command=self.browse_proxy_file).grid(row=0, column=2, padx=5, pady=5)
        
        self.mode_var = tk.StringVar(value="1")
        ttk.Label(mode_frame, text="Check mode:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="Check from file", variable=self.mode_var, value="1", command=self.toggle_mode_options).grid(row=0, column=1, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="Check random usernames", variable=self.mode_var, value="2", command=self.toggle_mode_options).grid(row=0, column=2, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="Check specific username", variable=self.mode_var, value="3", command=self.toggle_mode_options).grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(mode_frame, text="Check with semi-username patterns", variable=self.mode_var, value="4", command=self.toggle_mode_options).grid(row=1, column=2, padx=5, pady=5)
        
        self.file_frame = ttk.Frame(mode_frame)
        self.file_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(self.file_frame, text="Username file:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_path_var = tk.StringVar()
        ttk.Entry(self.file_frame, textvariable=self.file_path_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.file_frame, text="Browse", command=self.browse_username_file).grid(row=0, column=2, padx=5, pady=5)
        
        self.random_frame = ttk.Frame(mode_frame)
        self.random_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        self.random_frame.grid_remove()
        
        ttk.Label(self.random_frame, text="Username length:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.length_var = tk.StringVar(value="5")
        ttk.Entry(self.random_frame, textvariable=self.length_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.random_frame, text="Number to check (0 for unlimited):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.count_var = tk.StringVar(value="100")
        ttk.Entry(self.random_frame, textvariable=self.count_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.specific_frame = ttk.Frame(mode_frame)
        self.specific_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        self.specific_frame.grid_remove()
        
        ttk.Label(self.specific_frame, text="Username to check:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(self.specific_frame, textvariable=self.username_var, width=30).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.semi_frame = ttk.Frame(mode_frame)
        self.semi_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        self.semi_frame.grid_remove()
        
        ttk.Label(self.semi_frame, text="Number to check (0 for unlimited):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.semi_count_var = tk.StringVar(value="100")
        ttk.Entry(self.semi_frame, textvariable=self.semi_count_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(options_frame, text="Target available usernames:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.target_var = tk.StringVar(value="1005")
        ttk.Entry(options_frame, textvariable=self.target_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.start_button = ttk.Button(buttons_frame, text="Start Checking", command=self.start_checking)
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.stop_button = ttk.Button(buttons_frame, text="Stop", command=self.stop_checking, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_button = ttk.Button(buttons_frame, text="Save Results", command=self.save_results)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def setup_results_tab(self):
        stats_frame = ttk.Frame(self.results_tab)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(stats_frame, text="Checked:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.checked_label = ttk.Label(stats_frame, text="0")
        self.checked_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Available:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.available_label = ttk.Label(stats_frame, text="0")
        self.available_label.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Unavailable:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.unavailable_label = ttk.Label(stats_frame, text="0")
        self.unavailable_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Deleted:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.deleted_label = ttk.Label(stats_frame, text="0")
        self.deleted_label.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(stats_frame, text="Progress:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(stats_frame, variable=self.progress_var, length=400)
        self.progress_bar.grid(row=2, column=1, columnspan=3, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(self.results_tab, text="Results:").pack(anchor=tk.W, padx=10, pady=5)
        self.results_text = scrolledtext.ScrolledText(self.results_tab, width=80, height=20)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        available_frame = ttk.LabelFrame(self.results_tab, text="Available Usernames")
        available_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.available_text = scrolledtext.ScrolledText(available_frame, width=80, height=10)
        self.available_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def toggle_proxy_options(self):
        if self.proxy_var.get() == "p":
            self.proxy_type_frame.grid()
            self.proxy_file_frame.grid()
        elif self.proxy_var.get() == "f":
            self.proxy_type_frame.grid_remove()
            self.proxy_file_frame.grid_remove()
        else: 
            self.proxy_type_frame.grid_remove()
            self.proxy_file_frame.grid_remove()
    
    def toggle_mode_options(self):
        self.file_frame.grid_remove()
        self.random_frame.grid_remove()
        self.specific_frame.grid_remove()
        self.semi_frame.grid_remove()
        
        mode = self.mode_var.get()
        if mode == "1":
            self.file_frame.grid()
        elif mode == "2":
            self.random_frame.grid()
        elif mode == "3":
            self.specific_frame.grid()
        elif mode == "4":
            self.semi_frame.grid()
    
    def browse_proxy_file(self):
        filename = filedialog.askopenfilename(title="Select Proxy File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            self.proxy_file_var.set(filename)
    
    def browse_username_file(self):
        filename = filedialog.askopenfilename(title="Select Username File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            self.file_path_var.set(filename)
    
    def load_usernames(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            self.log_message(f"File not found: {file_path}", "error")
            return []
        except Exception as e:
            self.log_message(f"Error loading file: {str(e)}", "error")
            return []
    
    def generate_random_username(self, length):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    
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
            if not self.P:
                self.log_message("No proxies available in the list", "error")
                return None
                
            proxy = random.choice(self.P)
            
            if self.proxy_type == '1':
                return {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
            elif self.proxy_type == '2':
                return {
                    'http': f'socks4://{proxy}',
                    'https': f'socks4://{proxy}'
                }
            elif self.proxy_type == '3':
                return {
                    'http': f'socks5://{proxy}',
                    'https': f'socks5://{proxy}'
                }
            elif self.proxy_type == '4':
                return {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
            elif self.proxy_type == '5':
                host_port, user_pass = proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{host_port}',
                    'https': f'http://{user}:{password}@{host_port}'
                }
            elif self.proxy_type == '6':
                ip_port, user_pass = proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{ip_port}',
                    'https': f'http://{user}:{password}@{ip_port}'
                }
            elif self.proxy_type == '7':
                user_pass, host_port = proxy.split(':', 1)
                user, password = user_pass.split(':', 1)
                return {
                    'http': f'http://{user}:{password}@{host_port}',
                    'https': f'http://{user}:{password}@{host_port}'
                }
        elif self.proxymod == "f":
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
                    self.log_message(f"[AVAILABLE] {username}", "success")
                    self.available_text.insert(tk.END, f"{username}\n")
                    self.available_text.see(tk.END)
                elif f'"{self.user} is already taken!"' in response.text and '"status_code":"TAKEN"' in response.text:
                    self.unavailable += 1
                    self.log_message(f"[TAKEN] {username}", "unavailable")
                elif f'{self.user} is currently unavailable!' in response.text and '"status_code":"DELETED"' in response.text:
                    self.deleted += 1
                    self.log_message(f"[DELETED] {username}", "deleted")
                else:
                    self.unavailable += 1
                    self.log_message(f"[UNKNOWN] {username}: {response.text}", "unavailable")
                
                self.checked += 1
                self.update_stats()
                break  
                
            except Exception as e:
                if self.proxymod in ["p", "f"] and attempt < max_retries - 1:
                    self.log_message(f"[RETRY] {username}: {str(e)}. Switching proxy...", "warning")
                    self.proxies = self.proxynew()
                    time.sleep(1)  
                elif attempt < max_retries - 1:
                    self.log_message(f"[RETRY] {username}: {str(e)}. Retrying in {retry_delay}s...", "warning")
                    time.sleep(retry_delay)
                    retry_delay *= 2 
                else:
                    self.log_message(f"[ERROR] {username}: {str(e)} after {max_retries} attempts", "error")
    
    def update_stats(self):
        self.checked_label.config(text=str(self.checked))
        self.available_label.config(text=str(self.available))
        self.unavailable_label.config(text=str(self.unavailable))
        self.deleted_label.config(text=str(self.deleted))
        
        if self.count > 0:
            progress = min(100, (self.checked / self.count) * 100)
            self.progress_var.set(progress)
        elif self.target_available > 0:
            progress = min(100, (self.available / self.target_available) * 100)
            self.progress_var.set(progress)
        
        self.status_bar.config(text=f"Checked: {self.checked} | Available: {self.available} | Unavailable: {self.unavailable} | Deleted: {self.deleted} | Current: {self.user}")
        
        self.root.update_idletasks()
    
    def log_message(self, message, level="info"):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        if level == "error":
            tag = "error"
            color = "#e74c3c" 
        elif level == "warning":
            tag = "warning"
            color = "#f39c12"  
        elif level == "success":
            tag = "success"
            color = "#2ecc71"  
        elif level == "unavailable":
            tag = "unavailable"
            color = "#95a5a6"  
        elif level == "deleted":
            tag = "deleted"
            color = "#f1c40f"
        else:
            tag = "info"
            color = "#3498db" 
        
        self.results_text.insert(tk.END, log_message)
        self.results_text.tag_add(tag, f"end-{len(log_message)+1}c", "end-1c")
        self.results_text.tag_config(tag, foreground=color)
        
        self.results_text.see(tk.END)
    
    def start_checking(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.checked = 0
        self.available = 0
        self.unavailable = 0
        self.deleted = 0
        self.run = True
        
        self.results_text.delete(1.0, tk.END)
        self.available_text.delete(1.0, tk.END)
        
        for tag, color in [("error", "#e74c3c"), ("warning", "#f39c12"), ("success", "#2ecc71"), 
                          ("info", "#3498db"), ("unavailable", "#95a5a6"), ("deleted", "#f1c40f")]:
            self.results_text.tag_config(tag, foreground=color)
        
        self.proxymod = self.proxy_var.get()
        self.proxy_type = self.proxy_type_var.get() if self.proxymod == "p" else None
        self.mode = self.mode_var.get()
        self.target_available = int(self.target_var.get())
        
        if self.proxymod == "p":
            proxy_file = self.proxy_file_var.get()
            try:
                with open(proxy_file, 'r') as file:
                    self.P = [line.strip() for line in file if line.strip()]
                    if not self.P:
                        self.log_message("No valid proxies found in file. Continuing without proxy.", "error")
                        self.proxymod = "n"
                    else:
                        self.log_message(f"Loaded {len(self.P)} proxies.", "info")
            except FileNotFoundError:
                self.log_message("Proxy file not found. Continuing without proxy.", "error")
                self.proxymod = "n"
            except Exception as e:
                self.log_message(f"Error loading proxy: {str(e)}. Continuing without proxy.", "error")
                self.proxymod = "n"
        
        self.check_thread = threading.Thread(target=self.check_thread_function)
        self.check_thread.daemon = True
        self.check_thread.start()
    
    def check_thread_function(self):
        try:
            self.log_message("Starting username checker...", "info")
            
            if self.mode == "1":
                file_path = self.file_path_var.get()
                self.usernames = self.load_usernames(file_path)
                if not self.usernames:
                    self.log_message("No usernames loaded from file.", "error")
                    self.stop_checking()
                    return
                
                self.log_message(f"Loaded {len(self.usernames)} usernames from file.", "info")
                for username in self.usernames:
                    if not self.run or self.available >= self.target_available:
                        break
                    self.check_username(username)
                    time.sleep(random.uniform(1.5, 3.0))  
                self.log_message("All usernames checked from file.", "info")
                
            elif self.mode == "2":  
                self.length = int(self.length_var.get())
                self.count = int(self.count_var.get())
                checked = 0
                
                while (self.count == 0 or checked < self.count) and self.run and self.available < self.target_available:
                    username = self.generate_random_username(self.length)
                    self.check_username(username)
                    checked += 1
                    time.sleep(random.uniform(1.5, 3.0))  
                
                if self.count > 0:
                    self.log_message(f"Completed checking {self.count} random usernames.", "info")
                else:
                    self.log_message(f"Target of {self.target_available} available usernames reached!", "success")
                    
            elif self.mode == "3":  
                username = self.username_var.get()
                if not username:
                    self.log_message("No username specified.", "error")
                    self.stop_checking()
                    return
                
                self.check_username(username)
                self.log_message("Username check completed.", "info")
                
            elif self.mode == "4":
                self.count = int(self.semi_count_var.get())
                checked = 0
                
                while (self.count == 0 or checked < self.count) and self.run and self.available < self.target_available:
                    username = self.generate_semi_usernames()
                    self.check_username(username)
                    checked += 1
                    time.sleep(random.uniform(1.5, 3.0)) 
                
                if self.count > 0:
                    self.log_message(f"Completed checking {self.count} semi-pattern usernames.", "info")
                else:
                    self.log_message(f"Target of {self.target_available} available usernames reached!", "success")
            
            self.log_message("\nFinal Results:", "info")
            self.log_message(f"Checked: {self.checked} | Available: {self.available} | Unavailable: {self.unavailable} | Deleted: {self.deleted}", "info")
            
            if self.available > 0:
                self.log_message("Available usernames saved in available_snapchat.txt", "success")
        
        except Exception as e:
            self.log_message(f"Error in check thread: {str(e)}", "error")
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def stop_checking(self):
        self.run = False
        self.log_message("Stopping checker...", "warning")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def save_results(self):
        filename = filedialog.asksaveasfilename(title="Save Results", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            try:
                with open(filename, 'w', encoding="utf-8") as file:
                    file.write(self.results_text.get(1.0, tk.END))
                self.log_message(f"Results saved to {filename}", "success")
            except Exception as e:
                self.log_message(f"Error saving results: {str(e)}", "error")

if __name__ == "__main__":
    root = tk.Tk()
    app = SnapchatCheckerGUI(root)
    root.mainloop()