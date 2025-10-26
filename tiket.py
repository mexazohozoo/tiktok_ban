import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import hashlib
import uuid
import os
import sys
from typing import Dict, Any

# ASCII Art Banner
BANNER = """
████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗
╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝  AUTHOR: LORDHOZOOO
   ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝      SUPPORT MEXAZO EXECUTE
   ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗      YT : LORDHOZOOO 
   ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗    TIKTOK: LORDHOZOO
   ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   OPEN JASA BAN HARGA 250K EMAIL hozoonetwork@gmail.com   
"""

LINE_SEPARATOR = "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"

class WeatherInfo:
    """Kelas untuk mendapatkan informasi cuaca simbolis"""
    
    @staticmethod
    def get_weather_icon():
        """Mendapatkan ikon cuaca berdasarkan waktu"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "☀️  Pagi Cerah"
        elif 12 <= hour < 15:
            return "🌤️  Siang Berawan"
        elif 15 <= hour < 18:
            return "⛅ Sore Hari"
        elif 18 <= hour < 24:
            return "🌙 Malam Tenang"
        else:
            return "🌜 Larut Malam"
    
    @staticmethod
    def get_season():
        """Mendapatkan musim simbolis"""
        month = datetime.now().month
        
        if 3 <= month <= 5:
            return "🌸 Musim Semi"
        elif 6 <= month <= 8:
            return "☀️  Musim Panas"
        elif 9 <= month <= 11:
            return "🍂 Musim Gugur"
        else:
            return "❄️  Musim Dingin"

class SystemInfo:
    """Kelas untuk informasi sistem"""
    
    @staticmethod
    def get_system_status():
        """Status sistem simbolis"""
        return {
            "status": "🟢 ONLINE",
            "cpu": "⚡ Optimal",
            "memory": "💾 Stabil",
            "network": "📡 Terhubung"
        }
    
    @staticmethod
    def clear_screen():
        """Membersihkan layar terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')

class TikTokMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.setup_headers()
        
    def setup_headers(self):
        """Setup headers untuk meniru browser"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Origin': 'https://www.tiktok.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.tiktok.com/',
            'Sec-Ch-Ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site'
        })
    
    def generate_telemetry_data(self):
        """Generate data telemetri seperti TikTok"""
        timestamp = int(time.time() * 1000)
        return {
            "header": {
                "app_id": 1233,
                "app_lan": "id-ID",
                "app_name": "tiktok_web",
                "app_ver": "1.0.0.65",
                "carrier_region": "ID",
                "device_id": str(uuid.uuid4()),
                "device_platform": "web",
                "domain": "www.tiktok.com",
                "os": "linux",
                "region": "SG",
                "report_time": timestamp,
                "req_id": f"{timestamp}{hashlib.md5(str(timestamp).encode()).hexdigest()[:16]}",
                "tz_offset": 7
            },
            "batch": [
                {
                    "type": "performance",
                    "name": "page_view",
                    "timestamp": timestamp,
                    "data": {
                        "url": "https://www.tiktok.com/feedback/session?entrance=support_home",
                        "page_id": "feedback_session",
                        "duration": 1234,
                        "load_time": 567
                    }
                }
            ]
        }
    
    def send_telemetry_request(self):
        """Kirim request monitoring seperti TikTok"""
        url = "https://mon.tiktokv.com/monitor_browser/collect/batch/?biz_id=webmssdk"
        
        telemetry_data = self.generate_telemetry_data()
        
        try:
            print("🛰️  Mengirim telemetri ke TikTok...")
            response = self.session.post(
                url,
                json=telemetry_data,
                timeout=10,
                verify=False
            )
            
            # Analisis response headers
            telemetry_info = {
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'request_size': len(json.dumps(telemetry_data)),
                'response_time': response.elapsed.total_seconds()
            }
            
            print("✅ Telemetri berhasil dikirim!")
            return telemetry_info
            
        except Exception as e:
            print(f"❌ Gagal mengirim telemetri: {str(e)}")
            return {'error': str(e), 'url': url}

def display_header():
    """Menampilkan header dengan informasi lengkap"""
    SystemInfo.clear_screen()
    
    print(BANNER)
    print(LINE_SEPARATOR)
    
    # Informasi waktu dan tanggal
    now = datetime.now()
    print(f"📅 Tanggal: {now.strftime('%A, %d %B %Y')}")
    print(f"🕐 Jam: {now.strftime('%H:%M:%S')}")
    print(f"🌡️  Cuaca: {WeatherInfo.get_weather_icon()}")
    print(f"🎯 Musim: {WeatherInfo.get_season()}")
    
    # Status sistem
    system_status = SystemInfo.get_system_status()
    print(f"🔧 Status Sistem: {system_status['status']}")
    
    print(LINE_SEPARATOR)

def check_tiktok_ticket_status():
    """Cek status tiket TikTok"""
    
    url = "https://www.tiktok.com/feedback/session?entrance=support_home"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    try:
        print("🌐 Memeriksa status tiket TikTok...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Cari elemen status tiket
            status_elements = soup.find_all(class_=['text-LOjvWm', 'no-support-ticket'])
            
            if status_elements:
                status = "❌ Tidak ada tiket dukungan"
                description = "Tiket yang Anda kirim akan muncul di sini sehingga Anda dapat memeriksa pembaruannya."
            else:
                status = "✅ Tiket ditemukan"
                description = "Ada tiket aktif yang perlu diperiksa"
            
            # Analisis response headers
            response_info = {
                'tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': status,
                'deskripsi': description,
                'url': url,
                'status_code': response.status_code,
                'response_headers': dict(response.headers),
                'content_length': len(response.content),
                'response_time': response.elapsed.total_seconds()
            }
            
            print("✅ Pemeriksaan website berhasil!")
            return response_info
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return {'error': f'HTTP {response.status_code}', 'url': url}
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {'error': str(e), 'url': url}

def buat_laporan_tikTok(akun_dilaporkan, bukti_screenshot=None):
    """Buat template laporan untuk TikTok Safety Team"""
    
    template_laporan = f"""Dear TikTok Safety Team,

I am reporting the account @{akun_dilaporkan} for repeatedly uploading and sharing hardcore pornographic content. The videos contain explicit sexual acts that clearly violate TikTok's Community Guidelines against sexual exploitation and explicit material.

This account is a severe threat to the community, especially minors.{" I have attached screenshots as evidence." if bukti_screenshot else ""} I urgently request you to review this account and PERMANENTLY BAN it immediately.

Thank you for your immediate attention.

---
Report Details:
- Reported Account: @{akun_dilaporkan}
- Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Violation Type: Sexual Content, Explicit Material
- Severity: High
- Platform: TikTok
"""

    return template_laporan

def analisis_telemetri_tiktok(telemetry_data):
    """Analisis data telemetri TikTok"""
    
    analysis = {
        'request_timestamp': telemetry_data.get('timestamp'),
        'status_code': telemetry_data.get('status_code'),
        'server': telemetry_data.get('headers', {}).get('server', 'Unknown'),
        'response_time': telemetry_data.get('response_time'),
        'request_size': telemetry_data.get('request_size'),
        'cache_status': telemetry_data.get('headers', {}).get('x-cache', 'Unknown'),
        'trace_id': telemetry_data.get('headers', {}).get('x-tt-trace-id', 'N/A'),
        'log_id': telemetry_data.get('headers', {}).get('x-tt-logid', 'N/A')
    }
    
    # Deteksi CDN dan infrastructure
    if 'akamai' in telemetry_data.get('headers', {}).get('server', '').lower():
        analysis['cdn_provider'] = 'Akamai'
    elif 'cloudflare' in telemetry_data.get('headers', {}).get('server', '').lower():
        analysis['cdn_provider'] = 'Cloudflare'
    else:
        analysis['cdn_provider'] = 'Unknown'
    
    # Analisis performance
    response_time = analysis.get('response_time', 0)
    if response_time < 0.5:
        analysis['performance'] = '⚡ Excellent'
    elif response_time < 1.0:
        analysis['performance'] = '✅ Good'
    else:
        analysis['performance'] = '🐌 Slow'
    
    return analysis

def simpan_laporan_lengkap(akun_dilaporkan, status_tiket, telemetry_data, bukti_screenshot=None):
    """Simpan laporan lengkap dengan analisis telemetri"""
    
    # Buat template laporan
    laporan_tikTok = buat_laporan_tikTok(akun_dilaporkan, bukti_screenshot)
    
    # Analisis telemetri
    telemetry_analysis = analisis_telemetri_tiktok(telemetry_data)
    
    # Status tiket dan telemetri
    monitoring_info = f"""
{LINE_SEPARATOR}
🎯 TIKET STATUS & MONITORING
{LINE_SEPARATOR}
Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 WEBSITE STATUS
{LINE_SEPARATOR}
Ticket Status: {status_tiket.get('status', 'Unknown')}
Description: {status_tiket.get('deskripsi', 'No description')}
URL: {status_tiket.get('url', 'No URL')}
Status Code: {status_tiket.get('status_code', 'N/A')}
Response Time: {status_tiket.get('response_time', 'N/A'):.3f}s
Content Length: {status_tiket.get('content_length', 'N/A')} bytes

🛰️ TELEMETRY ANALYSIS
{LINE_SEPARATOR}
Telemetry Status: {telemetry_data.get('status_code', 'N/A')}
Server: {telemetry_analysis.get('server', 'Unknown')}
CDN Provider: {telemetry_analysis.get('cdn_provider', 'Unknown')}
Performance: {telemetry_analysis.get('performance', 'Unknown')}
Response Time: {telemetry_analysis.get('response_time', 'N/A'):.3f}s
Request Size: {telemetry_analysis.get('request_size', 'N/A')} bytes
Cache Status: {telemetry_analysis.get('cache_status', 'Unknown')}
Trace ID: {telemetry_analysis.get('trace_id', 'N/A')}
Log ID: {telemetry_analysis.get('log_id', 'N/A')}

⚠️ ERRORS & WARNINGS
{LINE_SEPARATOR}
{'❌ ERROR: ' + status_tiket['error'] if 'error' in status_tiket else '✅ Website Check Successful'}
{'❌ ERROR: ' + telemetry_data['error'] if 'error' in telemetry_data else '✅ Telemetry Check Successful'}
"""
    
    # Gabungkan semua informasi
    laporan_lengkap = laporan_tikTok + monitoring_info
    
    # Buat filename
    filename = f"tiktok_report_{akun_dilaporkan}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Simpan file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(laporan_lengkap)
    
    print(f"✅ Laporan disimpan sebagai: {filename}")
    return filename, laporan_lengkap

def buat_laporan_json(akun_dilaporkan, status_tiket, telemetry_data):
    """Simpan laporan dalam format JSON untuk tracking"""
    
    laporan_data = {
        'report_id': f"TT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'timestamp': datetime.now().isoformat(),
        'reported_account': f"@{akun_dilaporkan}",
        'violation_type': ['sexual_content', 'explicit_material'],
        'severity': 'high',
        'report_content': {
            'title': 'Report for Pornographic Content',
            'body': f"Reporting account @{akun_dilaporkan} for explicit sexual content violation"
        },
        'website_status': status_tiket,
        'telemetry_data': telemetry_data,
        'platform': 'TikTok',
        'monitoring': {
            'telemetry_url': 'https://mon.tiktokv.com/monitor_browser/collect/batch/?biz_id=webmssdk',
            'feedback_url': 'https://www.tiktok.com/feedback/session?entrance=support_home'
        }
    }
    
    json_filename = f"telemetry_report_{akun_dilaporkan}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(laporan_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Data JSON disimpan sebagai: {json_filename}")
    return json_filename

def tampilkan_analisis_detil(telemetry_analysis):
    """Tampilkan analisis detil telemetri"""
    
    print("\n" + LINE_SEPARATOR)
    print("📊 TELEMETRY ANALYSIS DETAIL")
    print(LINE_SEPARATOR)
    
    print(f"📡 Status Code: {telemetry_analysis.get('status_code')}")
    print(f"🖥️  Server: {telemetry_analysis.get('server')}")
    print(f"🌐 CDN Provider: {telemetry_analysis.get('cdn_provider')}")
    print(f"⚡ Performance: {telemetry_analysis.get('performance')}")
    print(f"⏱️  Response Time: {telemetry_analysis.get('response_time', 0):.3f} seconds")
    print(f"📦 Request Size: {telemetry_analysis.get('request_size')} bytes")
    print(f"💾 Cache Status: {telemetry_analysis.get('cache_status')}")
    print(f"🔍 Trace ID: {telemetry_analysis.get('trace_id')}")
    print(f"📝 Log ID: {telemetry_analysis.get('log_id')}")

def install_dependencies():
    """Install dependencies yang diperlukan"""
    print(LINE_SEPARATOR)
    print("📦 CHECKING DEPENDENCIES...")
    print(LINE_SEPARATOR)
    
    required_packages = ['requests', 'beautifulsoup4']
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} sudah terinstall")
        except ImportError:
            print(f"📥 Menginstall {package}...")
            os.system(f"pip install {package}")
            print(f"✅ {package} berhasil diinstall")

def animated_loading(text, duration=3):
    """Animasi loading"""
    print(f"\n{text}", end="", flush=True)
    for i in range(duration):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print()

# Program Utama
def main():
    display_header()
    
    # Install dependencies jika diperlukan
    install_dependencies()
    
    print(LINE_SEPARATOR)
    print("🚀 MEMULAI TIKTOK REPORT GENERATOR")
    print(LINE_SEPARATOR)
    
    # Inisialisasi monitor
    monitor = TikTokMonitor()
    
    # Input akun yang dilaporkan
    akun_dilaporkan = input("🎯 Masukkan username akun yang dilaporkan (tanpa @): ").strip()
    
    if not akun_dilaporkan:
        print("❌ Username tidak boleh kosong!")
        return
    
    # Tampilkan preview
    print(f"\n🔍 Memeriksa status untuk akun: @{akun_dilaporkan}")
    
    preview = buat_laporan_tikTok(akun_dilaporkan)
    print("\n" + LINE_SEPARATOR)
    print("📄 PREVIEW LAPORAN:")
    print(LINE_SEPARATOR)
    print(preview)
    print(LINE_SEPARATOR)
    
    if input("\n🎯 Lanjutkan dengan monitoring? (y/n): ").lower().strip() != 'y':
        print("❌ Proses dibatalkan.")
        return
    
    # Tanya apakah ada screenshot
    ada_bukti = input("📸 Apakah ada screenshot bukti? (y/n): ").lower().strip() == 'y'
    
    # Eksekusi monitoring
    print("\n" + LINE_SEPARATOR)
    print("🔍 MEMULAI MONITORING TIKTOK")
    print(LINE_SEPARATOR)
    
    animated_loading("1 Memeriksa status tiket website")
    status_tiket = check_tiktok_ticket_status()
    
    animated_loading("2 Mengirim request telemetri")
    telemetry_data = monitor.send_telemetry_request()
    
    # Analisis telemetri
    telemetry_analysis = analisis_telemetri_tiktok(telemetry_data)
    
    # Tampilkan analisis
    tampilkan_analisis_detil(telemetry_analysis)
    
    # Buat laporan lengkap
    print("\n" + LINE_SEPARATOR)
    print("📝 MEMBUAT LAPORAN LENGKAP")
    print(LINE_SEPARATOR)
    
    filename, laporan_lengkap = simpan_laporan_lengkap(akun_dilaporkan, status_tiket, telemetry_data, ada_bukti)
    
    # Buat backup JSON
    json_file = buat_laporan_json(akun_dilaporkan, status_tiket, telemetry_data)
    
    # Tampilkan summary
    print("\n" + LINE_SEPARATOR)
    print("✅ MONITORING & REPORTING COMPLETE")
    print(LINE_SEPARATOR)
    print(f"👤 Akun yang dilaporkan: @{akun_dilaporkan}")
    print(f"📁 File laporan: {filename}")
    print(f"📊 File data: {json_file}")
    print(f"🌐 Status website: {status_tiket.get('status', 'Unknown')}")
    print(f"🛰️  Status telemetri: {telemetry_data.get('status_code', 'Unknown')}")
    
    if 'error' in status_tiket:
        print(f"⚠️  Website Error: {status_tiket['error']}")
    if 'error' in telemetry_data:
        print(f"⚠️  Telemetry Error: {telemetry_data['error']}")
    
    print(LINE_SEPARATOR)
    print("🎉 PROSES SELESAI! Laporan telah dibuat dan siap dikirim.")
    print(LINE_SEPARATOR)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Program dihentikan oleh pengguna")
    except Exception as e:
        print(f"\n\n💥 Error tidak terduga: {str(e)}")
