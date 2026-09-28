#!/usr/bin/env python3
# ============================================================
#   Alight Motion Premium Generator
#   Creator  : dapjisync
#   Language : Python 3
#   Usage    : python3 generator.py
# ============================================================

import requests
import json
import sys
import os
import re
import time

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class _Dummy:
        def __getattr__(self, _): return ""
    Fore = Back = Style = _Dummy()

# ── Warna shorthand ─────────────────────────────────────────
C  = Fore.CYAN
Y  = Fore.YELLOW
G  = Fore.GREEN
R  = Fore.RED
M  = Fore.MAGENTA
W  = Fore.WHITE
B  = Fore.BLUE
DIM = Style.DIM
RST = Style.RESET_ALL

# ── Konstanta ───────────────────────────────────────────────
API_URL = "https://anita-studio.netlify.app/.netlify/functions/amprem"

# ── ASCII Banner ────────────────────────────────────────────
def print_banner():
    os.system("clear" if os.name == "posix" else "cls")
    banner = f"""
{M}╔══════════════════════════════════════════════════════════════╗
{M}║                                                              ║
{M}║  {C} ██████╗ ███████╗███╗   ██╗{W}███████╗██████╗  █████╗ ████████╗{M} ║
{M}║  {C}██╔════╝ ██╔════╝████╗  ██║{W}██╔════╝██╔══██╗██╔══██╗╚══██╔══╝{M} ║
{M}║  {C}██║  ███╗█████╗  ██╔██╗ ██║{W}█████╗  ██████╔╝███████║   ██║   {M} ║
{M}║  {C}██║   ██║██╔══╝  ██║╚██╗██║{W}██╔══╝  ██╔══██╗██╔══██║   ██║   {M} ║
{M}║  {C}╚██████╔╝███████╗██║ ╚████║{W}███████╗██║  ██║██║  ██║   ██║   {M} ║
{M}║  {C} ╚═════╝ ╚══════╝╚═╝  ╚═══╝{W}╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  {M} ║
{M}║                                                              ║
{M}║       {Y}A L I G H T   M O T I O N   P R E M I U M{M}              ║
{M}║                  {C}G E N E R A T O R{M}                            ║
{M}║                                                              ║
{M}║  {DIM}Creator : {G}dapjisync{M}   {DIM}Version : {G}1.0{M}                          ║
{M}╚══════════════════════════════════════════════════════════════╝{RST}
"""
    print(banner)

def print_step(step, total, msg):
    bar_len = 30
    filled  = int(bar_len * step / total)
    bar     = "█" * filled + "░" * (bar_len - filled)
    print(f"\n{C}[{step}/{total}]{RST} {Y}{msg}{RST}")
    print(f"  {G}[{bar}]{RST} {int(step/total*100)}%")

def print_success(msg):
    print(f"\n{G}  ✔  {W}{msg}{RST}")

def print_error(msg):
    print(f"\n{R}  ✘  {W}{msg}{RST}")

def print_info(msg):
    print(f"  {C}►  {DIM}{msg}{RST}")

def print_result(data: dict):
    print(f"\n{M}{'─'*62}")
    print(f"{Y}  HASIL PREMIUM:{RST}")
    print(f"{M}{'─'*62}{RST}")
    for k, v in data.items():
        print(f"  {C}{k:<20}{RST}: {G}{v}{RST}")
    print(f"{M}{'─'*62}{RST}")

# ── HTTP helper ──────────────────────────────────────────────
def api_post(action: str, payload: dict) -> dict:
    body = {"action": action, **payload}
    resp = requests.post(
        API_URL,
        json=body,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()

# ── Validasi email sederhana ─────────────────────────────────
def valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

# ── Main flow ────────────────────────────────────────────────
def main():
    print_banner()

    # ── Input email ─────────────────────────────────────────
    print(f"{Y}  Masukkan email kamu untuk generate Alight Motion Premium:{RST}")
    print(f"  {DIM}(Email akan digunakan untuk magic link){RST}\n")
    while True:
        email = input(f"  {C}Email{RST} : ").strip()
        if valid_email(email):
            break
        print_error("Format email tidak valid, coba lagi.")

    print()

    # ── Step 1: Kirim magic link ──────────────────────────────
    print_step(1, 3, "Mengirim magic link ke email kamu...")
    try:
        r1 = api_post("send-magiclink", {"email": email})
        print_info(f"Response: {json.dumps(r1)}")
        if not r1.get("success"):
            print_error(r1.get("message") or "Gagal mengirim magic link")
            sys.exit(1)
        print_success("Magic link berhasil dikirim ke email kamu!")
    except requests.RequestException as e:
        print_error(f"Koneksi error: {e}")
        sys.exit(1)

    # ── Input raw magic link ──────────────────────────────────
    print(f"\n{Y}  Buka email kamu, klik magic link, lalu copy URL-nya.{RST}")
    print(f"  {DIM}(URL biasanya dimulai dengan https://...){RST}\n")
    raw_link = input(f"  {C}Paste magic link{RST} : ").strip()
    if not raw_link.startswith("http"):
        print_error("Link tidak valid.")
        sys.exit(1)

    # ── Step 2: Verifikasi akun ───────────────────────────────
    print_step(2, 3, "Memverifikasi akun...")
    try:
        r2 = api_post("verify-account", {"email": email, "rawLink": raw_link})
        print_info(f"Response: {json.dumps(r2)}")
        if not r2.get("success"):
            print_error(r2.get("message") or "Verifikasi gagal")
            sys.exit(1)
        id_token = r2.get("idToken") or (r2.get("profile") or {}).get("idToken")
        if not id_token:
            print_error("idToken tidak ditemukan di response")
            sys.exit(1)
        print_success("Verifikasi berhasil!")
        print_info(f"idToken: {id_token[:40]}...")
    except requests.RequestException as e:
        print_error(f"Koneksi error: {e}")
        sys.exit(1)

    # ── Step 3: Apply premium ─────────────────────────────────
    print_step(3, 3, "Mengaktifkan Alight Motion Premium...")
    time.sleep(1)
    try:
        r3 = api_post("apply-premium", {"email": email, "idToken": id_token})
        print_info(f"Response: {json.dumps(r3)}")
        if not r3.get("success"):
            print_error(r3.get("message") or "Proses premium gagal")
            sys.exit(1)
        print_success("Alight Motion Premium berhasil diaktifkan!")
    except requests.RequestException as e:
        print_error(f"Koneksi error: {e}")
        sys.exit(1)

    # ── Tampilkan hasil ───────────────────────────────────────
    result_data = {k: v for k, v in r3.items() if k != "success"}
    result_data["email"] = email
    print_result(result_data)

    print(f"\n{G}  Selesai! Buka Alight Motion dan nikmati fitur Premium-nya 🎉{RST}")
    print(f"  {DIM}Creator: dapjisync{RST}\n")


if __name__ == "__main__":
    main()
