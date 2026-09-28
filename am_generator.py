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

# ── Warna ────────────────────────────────────────────────────
C   = Fore.CYAN
Y   = Fore.YELLOW
G   = Fore.GREEN
R   = Fore.RED
M   = Fore.MAGENTA
W   = Fore.WHITE
B   = Fore.BLUE
LB  = Fore.LIGHTBLUE_EX
LG  = Fore.LIGHTGREEN_EX
LM  = Fore.LIGHTMAGENTA_EX
LW  = Fore.LIGHTWHITE_EX
DIM = Style.DIM
BRT = Style.BRIGHT
RST = Style.RESET_ALL

# ── Konstanta ────────────────────────────────────────────────
API_URL    = "https://anita-studio.netlify.app/.netlify/functions/amprem"
TOTAL_USER = 1247   # update manual atau ambil dari API kalau ada

# ── Banner ───────────────────────────────────────────────────
def print_banner():
    os.system("clear" if os.name == "posix" else "cls")

    # lebar card = 64 karakter dalam box
    W64 = 64

    top    = f"{BRT}{M}╔{'═'*W64}╗{RST}"
    bot    = f"{BRT}{M}╚{'═'*W64}╝{RST}"
    empty  = f"{BRT}{M}║{' '*W64}║{RST}"
    def row(txt_raw, txt_visible):
        # txt_raw  = string dengan escape code (untuk print)
        # txt_visible = string tanpa escape (untuk hitung panjang)
        pad = W64 - len(txt_visible)
        l   = pad // 2
        r   = pad - l
        return f"{BRT}{M}║{RST}{' '*l}{txt_raw}{' '*r}{BRT}{M}║{RST}"

    # ASCII art "TOOLS"
    art = [
        f"{BRT}{LM} _____  ___   ___  _      ___  {RST}",
        f"{BRT}{LM}|_   _|/ _ \ / _ \| |    / __| {RST}",
        f"{BRT}{C}  | | | (_) | (_) | |__   \__ \ {RST}",
        f"{BRT}{C}  | |  \___/ \___/|____| |___/ {RST}",
        f"{BRT}{LM}  |_|   AM PREMIUM GENERATOR   {RST}",
    ]
    art_vis = [
        " _____  ___   ___  _      ___  ",
        "|_   _|/ _ \ / _ \| |    / __| ",
        "  | | | (_) | (_) | |__   \__ \ ",
        "  | |  \___/ \___/|____| |___/ ",
        "  |_|   AM PREMIUM GENERATOR   ",
    ]

    sub1_r = f"{BRT}{Y}A L I G H T   M O T I O N   P R E M I U M{RST}"
    sub1_v =  "A L I G H T   M O T I O N   P R E M I U M"
    sub2_r = f"{BRT}{LW}G E N E R A T O R{RST}"
    sub2_v =  "G E N E R A T O R"

    info_r = f"{DIM}{LW}Creator : {BRT}{LG}dapjisync{RST}   {DIM}{LW}Version : {BRT}{LG}1.0{RST}   {DIM}{LW}Users : {BRT}{LG}{TOTAL_USER:,}{RST}"
    info_v = f"Creator : dapjisync   Version : 1.0   Users : {TOTAL_USER:,}"

    div_r  = f"{M}{'─'*W64}{RST}"

    print(top)
    print(empty)
    for a, av in zip(art, art_vis):
        print(row(a, av))
    print(empty)
    print(row(sub1_r, sub1_v))
    print(row(sub2_r, sub2_v))
    print(empty)
    # divider dalam box
    print(f"{BRT}{M}╠{'═'*W64}╣{RST}")
    print(row(info_r, info_v))
    print(bot)
    print()

# ── Helpers ──────────────────────────────────────────────────
def print_step(step, total, msg):
    bar_len = 30
    filled  = int(bar_len * step / total)
    bar     = f"{G}{'█'*filled}{RST}{DIM}{'░'*(bar_len-filled)}{RST}"
    print(f"\n{BRT}{C}[{step}/{total}]{RST} {BRT}{Y}{msg}{RST}")
    print(f"  [{bar}] {BRT}{G}{int(step/total*100)}%{RST}")

def print_success(msg):
    print(f"\n{BRT}{G}  ✔  {LW}{msg}{RST}")

def print_error(msg):
    print(f"\n{BRT}{R}  ✘  {LW}{msg}{RST}")

def print_info(msg):
    print(f"  {C}►  {DIM}{LW}{msg}{RST}")

def print_result(data: dict):
    w = 60
    print(f"\n{BRT}{M}╔{'═'*w}╗{RST}")
    print(f"{BRT}{M}║{RST}{BRT}{Y}{'  ✨  ALIGHT MOTION PREMIUM AKTIF  ✨':^{w}}{BRT}{M}║{RST}")
    print(f"{BRT}{M}╠{'═'*w}╣{RST}")
    for k, v in data.items():
        line = f"  {C}{k:<18}{RST}: {LG}{v}{RST}"
        vis  = f"  {k:<18}: {v}"
        pad  = w - len(vis)
        print(f"{BRT}{M}║{RST}{line}{' '*pad}{BRT}{M}║{RST}")
    print(f"{BRT}{M}╚{'═'*w}╝{RST}")

# ── HTTP ─────────────────────────────────────────────────────
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

def valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

# ── Main ─────────────────────────────────────────────────────
def main():
    print_banner()

    print(f"{BRT}{Y}  Masukkan email kamu untuk generate Alight Motion Premium:{RST}")
    print(f"  {DIM}(Email akan digunakan untuk magic link){RST}\n")
    while True:
        email = input(f"  {BRT}{C}Email{RST} : ").strip()
        if valid_email(email):
            break
        print_error("Format email tidak valid, coba lagi.")

    print()

    # Step 1
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

    print(f"\n{BRT}{Y}  Buka email kamu, klik magic link, lalu copy URL-nya.{RST}")
    print(f"  {DIM}(URL dimulai dengan https://...){RST}\n")
    raw_link = input(f"  {BRT}{C}Paste magic link{RST} : ").strip()
    if not raw_link.startswith("http"):
        print_error("Link tidak valid.")
        sys.exit(1)

    # Step 2
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

    # Step 3
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

    result_data = {k: v for k, v in r3.items() if k != "success"}
    result_data["email"] = email
    print_result(result_data)

    print(f"\n  {BRT}{G}Selesai! Buka Alight Motion dan nikmati fitur Premium-nya 🎉{RST}")
    print(f"  {DIM}Creator: dapjisync{RST}\n")


if __name__ == "__main__":
    main()
