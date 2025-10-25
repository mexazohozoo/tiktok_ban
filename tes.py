
#Author : mexazoo
#support lordhozoo
import requests
import json
import time
import random
import re
from typing import Dict, List, Optional
import threading
from bs4 import BeautifulSoup
import hashlib

class TikTokReporter:
    def __init__(self):
        self.session = requests.Session()
        self.base_headers = {
            'authority': 'www.tiktok.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.tiktok.com',
            'referer': 'https://www.tiktok.com/legal/report/privacy/webform/id',
            'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.is_running = False
        self.report_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.current_temp_email = None
        self.current_mailbox = None
        self.form_data = None
        self.slardar_config = None
        self.region_data = None
        
    def get_1secmail_email(self):
        """Mendapatkan email temporary aktif dari 1secmail.com"""
        try:
            print("📧 Mendapatkan email temporary dari 1secmail.com...")
            
            # Generate random mailbox dari 1secmail
            api_url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
            
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                mailboxes = response.json()
                if mailboxes and len(mailboxes) > 0:
                    email = mailboxes[0]
                    mailbox_parts = email.split('@')
                    
                    self.current_temp_email = email
                    self.current_mailbox = {
                        'email': email,
                        'login': mailbox_parts[0],
                        'domain': mailbox_parts[1]
                    }
                    
                    print(f"📨 1secmail: {email}")
                    print(f"🔑 Mailbox: {mailbox_parts[0]}@{mailbox_parts[1]}")
                    return email
                else:
                    raise Exception("Tidak ada mailbox yang tersedia")
            else:
                raise Exception(f"API error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Gagal mendapatkan email dari 1secmail: {e}")
            # Fallback ke email random
            return self.get_fallback_email()
    
    def check_1secmail_inbox(self):
        """Memeriksa inbox email temporary"""
        if not self.current_mailbox:
            return None
            
        try:
            api_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={self.current_mailbox['login']}&domain={self.current_mailbox['domain']}"
            
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                messages = response.json()
                return messages
            else:
                return None
                
        except Exception as e:
            print(f"❌ Gagal memeriksa inbox: {e}")
            return None
    
    def get_1secmail_message(self, message_id):
        """Mendapatkan detail pesan dari inbox"""
        if not self.current_mailbox:
            return None
            
        try:
            api_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={self.current_mailbox['login']}&domain={self.current_mailbox['domain']}&id={message_id}"
            
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                message_data = response.json()
                return message_data
            else:
                return None
                
        except Exception as e:
            print(f"❌ Gagal mendapatkan pesan: {e}")
            return None
    
    def wait_for_tiktok_confirmation(self, timeout=60):
        """Menunggu konfirmasi email dari TikTok"""
        if not self.current_mailbox:
            return False
            
        print(f"📭 Menunggu konfirmasi email dari TikTok (timeout: {timeout} detik)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                messages = self.check_1secmail_inbox()
                
                if messages and len(messages) > 0:
                    print(f"📥 Ditemukan {len(messages)} pesan di inbox")
                    
                    for message in messages:
                        # Cek apakah pesan dari TikTok
                        if 'tiktok' in message['from'].lower() or 'bytedance' in message['from'].lower():
                            print(f"✅ Dapatkan konfirmasi dari TikTok!")
                            print(f"   From: {message['from']}")
                            print(f"   Subject: {message['subject']}")
                            
                            # Dapatkan detail pesan
                            message_detail = self.get_1secmail_message(message['id'])
                            if message_detail:
                                print(f"   Preview: {message_detail['textBody'][:100]}...")
                            
                            return True
                
                # Tunggu 5 detik sebelum cek lagi
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Error saat menunggu konfirmasi: {e}")
                time.sleep(10)
        
        print("⏰ Timeout menunggu konfirmasi email dari TikTok")
        return False

    def get_fallback_email(self):
        """Fallback email generator jika 1secmail down"""
        try:
            print("🔄 Menggunakan fallback email generator...")
            
            # Generate random email yang realistic
            domains = [
                'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com',
                'protonmail.com', 'icloud.com', 'aol.com', 'yandex.com'
            ]
            
            username_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
            username = ''.join(random.choices(username_chars, k=random.randint(8, 12)))
            domain = random.choice(domains)
            
            temp_email = f"{username}@{domain}"
            self.current_temp_email = temp_email
            
            print(f"📨 Fallback email: {temp_email}")
            return temp_email
            
        except Exception as e:
            print(f"❌ Gagal generate fallback email: {e}")
            fallback_email = f"user{random.randint(10000,99999)}@gmail.com"
            self.current_temp_email = fallback_email
            return fallback_email

    def get_temp_email(self):
        """Main function untuk mendapatkan email temporary"""
        # Coba 1secmail dulu, jika gagal pakai fallback
        try:
            return self.get_1secmail_email()
        except Exception as e:
            print(f"⚠️  1secmail tidak tersedia, menggunakan fallback: {e}")
            return self.get_fallback_email()

    def extract_slardar_config(self, soup):
        """Extract Slardar monitoring configuration"""
        try:
            slardar_script = soup.find('script', {'id': 'slardar-config'})
            if slardar_script:
                slardar_data = json.loads(slardar_script.string)
                self.slardar_config = slardar_data
                print("📊 Slardar config ditemukan")
                return slardar_data
        except Exception as e:
            print(f"❌ Gagal extract Slardar config: {e}")
        return None

    def extract_region_data(self, soup):
        """Extract region data dari script"""
        try:
            region_script = soup.find('script', {'id': '__REGION__DATA__INJECTED__'})
            if region_script:
                region_data = json.loads(region_script.string)
                self.region_data = region_data
                print("🌍 Region data ditemukan")
                return region_data
        except Exception as e:
            print(f"❌ Gagal extract region data: {e}")
        return None

    def extract_web_modules_config(self, soup):
        """Extract web modules configuration"""
        try:
            web_modules_script = soup.find('script', {'id': 'web-modules-config'})
            if web_modules_script:
                web_modules_data = json.loads(web_modules_script.string)
                print("⚙️ Web modules config ditemukan")
                return web_modules_data
        except Exception as e:
            print(f"❌ Gagal extract web modules config: {e}")
        return None

    def extract_headlessx_data(self, soup):
        """Extract HeadlessX data untuk API endpoints"""
        try:
            headlessx_script = soup.find('script', {'id': 'headlessx-data'})
            if headlessx_script:
                headlessx_data = json.loads(headlessx_script.string)
                print("🔗 HeadlessX config ditemukan")
                return headlessx_data
        except Exception as e:
            print(f"❌ Gagal extract HeadlessX data: {e}")
        return None

    def analyze_report_form(self):
        """Menganalisis form report asli dari TikTok dengan semua script"""
        try:
            print("🔍 Menganalisis form report TikTok secara mendalam...")
            form_url = "https://www.tiktok.com/legal/report/privacy/webform/id"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                'Referer': 'https://www.tiktok.com/'
            }
            
            response = self.session.get(form_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract semua configuration penting
                slardar_config = self.extract_slardar_config(soup)
                region_data = self.extract_region_data(soup)
                web_modules_config = self.extract_web_modules_config(soup)
                headlessx_data = self.extract_headlessx_data(soup)
                
                # Cari script yang mengandung data form dan API endpoints
                scripts = soup.find_all('script')
                form_info = {
                    'csrf_token': None,
                    'api_endpoint': None,
                    'form_fields': [],
                    'available_reasons': [],
                    'slardar_config': slardar_config,
                    'region_data': region_data,
                    'web_modules_config': web_modules_config,
                    'headlessx_data': headlessx_data,
                    'build_version': None,
                    'cdn_domain': None
                }
                
                for script in scripts:
                    script_content = script.string
                    if script_content:
                        # Cari CSRF token
                        csrf_match = re.search(r'csrfToken[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]', script_content)
                        if csrf_match:
                            form_info['csrf_token'] = csrf_match.group(1)
                        
                        # Cari API endpoint
                        api_match = re.search(r'report[\'"]?\s*:\s*{[\s\S]*?url[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]', script_content)
                        if api_match:
                            form_info['api_endpoint'] = api_match.group(1)
                        
                        # Cari build version dan CDN domain
                        build_match = re.search(r'BUILD_VERSION[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]', script_content)
                        if build_match:
                            form_info['build_version'] = build_match.group(1)
                        
                        cdn_match = re.search(r'CDN_DOMAIN[\'"]?\s*:\s*[\'"]([^\'"]+)[\'"]', script_content)
                        if cdn_match:
                            form_info['cdn_domain'] = cdn_match.group(1)
                
                # Default values jika tidak ditemukan
                if not form_info['api_endpoint']:
                    form_info['api_endpoint'] = "https://www.tiktok.com/api/report/submit/"
                
                if not form_info['build_version']:
                    form_info['build_version'] = "1.0.0.3552"
                
                # Reason options berdasarkan analisis TikTok
                form_info['available_reasons'] = [
                    "privacy", "harassment", "hate_speech", "illegal_activities",
                    "minor_safety", "intellectual_property", "spam", "impersonation",
                    "fake_account", "inappropriate_content", "bullying"
                ]
                
                self.form_data = form_info
                print("✅ Berhasil menganalisis form report secara mendalam")
                print(f"📡 API Endpoint: {form_info['api_endpoint']}")
                print(f"🛡️ CSRF Token: {'Ditemukan' if form_info['csrf_token'] else 'Default'}")
                print(f"🔧 Build Version: {form_info['build_version']}")
                print(f"🌐 CDN Domain: {form_info['cdn_domain']}")
                print(f"📊 Slardar: {'Aktif' if slardar_config else 'Tidak aktif'}")
                print(f"🌍 Region: {region_data.get('VRegion', 'Unknown') if region_data else 'Unknown'}")
                
                return form_info
            else:
                print(f"❌ Gagal mengakses form: Status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error analisis form: {e}")
            # Fallback ke default
            self.form_data = {
                'api_endpoint': "https://www.tiktok.com/api/report/submit/",
                'available_reasons': [
                    "privacy", "harassment", "hate_speech", "illegal_activities",
                    "minor_safety", "intellectual_property", "spam", "impersonation"
                ],
                'build_version': "1.0.0.3552",
                'cdn_domain': "https://sf16-website-login.neutral.ttwstatic.com"
            }
            return self.form_data

    def generate_slardar_headers(self):
        """Generate headers untuk Slardar monitoring"""
        if not self.slardar_config:
            return {}
        
        slardar_headers = {
            'X-Slardar-Session': self.generate_random_hex(32),
            'X-Slardar-Page': 'tiktok_privacy_request',
            'X-Slardar-Bid': self.slardar_config.get('bid', 'tiktok_article_legal'),
            'X-Slardar-Env': self.slardar_config.get('env', 'production')
        }
        
        return slardar_headers

    def generate_region_headers(self):
        """Generate headers berdasarkan region data"""
        if not self.region_data:
            return {}
        
        region_headers = {
            'X-Region': self.region_data.get('VRegion', 'sg'),
            'X-Geo': self.region_data.get('VGeo', 'VGEO-ROW'),
            'X-Locale': 'id-ID',
            'X-Build-Version': self.form_data.get('build_version', '1.0.0.3552') if self.form_data else '1.0.0.3552'
        }
        
        return region_headers

    def generate_advanced_payload(self, username: str, reason: str = "privacy", 
                                additional_info: str = None) -> Dict:
        """Generate payload advanced berdasarkan analisis mendalam"""
        
        # Mapping alasan yang lebih akurat berdasarkan TikTok
        reason_mapping = {
            "privacy": {
                "code": "privacy",
                "type": "user",
                "text": "Pelanggaran privasi - Data pribadi saya dibagikan tanpa izin"
            },
            "harassment": {
                "code": "harassment", 
                "type": "user",
                "text": "Pelecehan atau perundungan - Konten yang melecehkan atau mengintimidasi"
            },
            "hate_speech": {
                "code": "hate_speech",
                "type": "user", 
                "text": "Ujaran kebencian - Konten yang menyerang kelompok tertentu"
            },
            "illegal_activities": {
                "code": "illegal_activities",
                "type": "user",
                "text": "Aktivitas ilegal - Menampilkan atau mempromosikan aktivitas ilegal"
            },
            "minor_safety": {
                "code": "minor_safety", 
                "type": "user",
                "text": "Keamanan anak di bawah umur - Konten yang membahayakan anak"
            },
            "intellectual_property": {
                "code": "intellectual_property",
                "type": "user",
                "text": "Pelanggaran hak cipta - Menggunakan konten milik saya tanpa izin"
            },
            "spam": {
                "code": "spam",
                "type": "user",
                "text": "Spam atau akun fake - Akun tiruan atau aktivitas spam"
            },
            "impersonation": {
                "code": "impersonation",
                "type": "user",
                "text": "Peniruan identitas - Meniru identitas saya atau orang lain"
            }
        }
        
        selected_reason = reason_mapping.get(reason, reason_mapping["privacy"])
        
        if not additional_info:
            additional_info = f"""Saya ingin melaporkan akun TikTok @{username} karena melakukan {selected_reason['text']}.

Detail pelanggaran:
- Akun ini secara konsisten melanggar kebijakan komunitas TikTok
- {selected_reason['text']}
- Membahayakan pengguna lain dan lingkungan TikTok

Saya meminta TikTok untuk segera meninjau dan mengambil tindakan yang sesuai terhadap akun ini sesuai dengan kebijakan platform."""

        # Generate email dari 1secmail
        email = self.get_temp_email()
        
        # Timestamp dalam format TikTok
        current_timestamp = int(time.time() * 1000)
        
        # Payload berdasarkan analisis mendalam form TikTok
        payload = {
            "username": username,
            "object_id": "",
            "owner_id": "",
            "object_type": "user",
            "reason": selected_reason['code'],
            "report_type": selected_reason['type'],
            "additional_info": additional_info,
            "email": email,
            "country": "ID",
            "language": "id",
            "timestamp": current_timestamp,
            "platform": "web",
            "referer": "https://www.tiktok.com/legal/report/privacy/webform/id",
            "region": self.region_data.get('VRegion', 'sg') if self.region_data else 'sg',
            "locale": "id-ID",
            "build_version": self.form_data.get('build_version', '1.0.0.3552') if self.form_data else '1.0.0.3552'
        }
        
        return payload

    def send_advanced_report(self, username: str, reason: str = "privacy", 
                           additional_info: str = None, wait_for_confirmation: bool = False) -> Dict:
        """Mengirim report dengan payload dan headers yang sangat authentic"""
        
        # Analisis form terlebih dahulu
        if not self.form_data:
            self.analyze_report_form()
        
        endpoint = self.form_data['api_endpoint']
        
        # Generate parameter dynamic yang sangat realistic
        dynamic_params = {
            'aid': '1988',
            'app_name': 'tiktok_web',
            'device_platform': 'web',
            'region': 'ID',
            'priority_region': '',
            'os': 'windows',
            'referer': 'https://www.tiktok.com/legal/report/privacy/webform/id',
            'root_referer': 'https://www.tiktok.com/',
            'cookie_enabled': 'true',
            'screen_width': '1920',
            'screen_height': '1080',
            'browser_language': 'id-ID',
            'browser_platform': 'Win32',
            'browser_name': 'Mozilla',
            'browser_version': '5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/120.0.0.0+Safari/537.36',
            'browser_online': 'true',
            'timezone_name': 'Asia/Jakarta',
            'is_page_visible': 'true',
            'focus_state': 'true',
            'is_fullscreen': 'false',
            'history_len': random.randint(1, 10),
            'language': 'id',
            'build_version': self.form_data.get('build_version', '1.0.0.3552') if self.form_data else '1.0.0.3552'
        }
        
        # Build URL dengan parameters
        url_with_params = f"{endpoint}?{self.build_query_string(dynamic_params)}"
        
        # Headers yang sangat realistic berdasarkan analisis
        report_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/json',
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/legal/report/privacy/webform/id',
            'Sec-Ch-Ua': '"Chromium";v="120", "Google Chrome";v="120", "Not=A?Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Tt-Env': 'production',
            'X-Tt-Region': self.region_data.get('VRegion', 'sg') if self.region_data else 'sg'
        }
        
        # Add CSRF token jika ada
        if self.form_data and self.form_data.get('csrf_token'):
            report_headers['X-CSRFToken'] = self.form_data['csrf_token']
        
        # Add Slardar headers jika ada
        slardar_headers = self.generate_slardar_headers()
        report_headers.update(slardar_headers)
        
        # Add region headers
        region_headers = self.generate_region_headers()
        report_headers.update(region_headers)
        
        # Generate payload yang sangat realistic
        report_payload = self.generate_advanced_payload(username, reason, additional_info)
        
        try:
            # Random delay untuk simulasi user real
            time.sleep(random.uniform(2.0, 5.0))
            
            print(f"📤 Mengirim report ke: {endpoint}")
            print(f"🎯 Target: @{username}")
            print(f"📧 Email: {report_payload['email']}")
            print(f"🌍 Region: {report_headers.get('X-Tt-Region', 'Unknown')}")
            print(f"🔧 Build: {report_payload.get('build_version', 'Unknown')}")
            
            response = self.session.post(
                url_with_params,
                json=report_payload,
                headers=report_headers,
                timeout=25
            )
            
            # Cek konfirmasi email jika diminta
            confirmation_received = False
            if wait_for_confirmation and self.current_mailbox:
                confirmation_received = self.wait_for_tiktok_confirmation(timeout=45)
            
            # Analisis response yang mendalam
            result = {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_data': response.json() if response.status_code == 200 else response.text,
                'username': username,
                'reason': reason,
                'email_used': report_payload['email'],
                'endpoint_used': endpoint,
                'region': report_headers.get('X-Tt-Region'),
                'build_version': report_payload.get('build_version'),
                'email_confirmation': confirmation_received,
                'mailbox_type': '1secmail' if self.current_mailbox else 'fallback',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'username': username,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
            }

    def generate_random_hex(self, length: int) -> str:
        """Generate random hex string"""
        return ''.join(random.choices('0123456789abcdef', k=length))
    
    def build_query_string(self, params: Dict) -> str:
        """Build query string dari dictionary parameters"""
        return '&'.join([f"{k}={v}" for k, v in params.items()])
    
    def validate_username(self, username: str) -> bool:
        """Validasi format username TikTok"""
        if not username or len(username) < 2 or len(username) > 30:
            return False
        return bool(re.match(r'^[a-zA-Z0-9_.]+$', username))

    # ==================== ADVANCED UNLIMITED REPORTING ====================
    
    def start_advanced_unlimited_reports(self, username: str, reason: str = "privacy", 
                                       delay_range: tuple = (25, 45), max_reports: int = None,
                                       wait_for_confirmation: bool = False):
        """
        Memulai unlimited reports dengan analisis mendalam dan payload authentic
        """
        print("🚀 MEMULAI ADVANCED AUTO-REPORT SYSTEM...")
        print("🔍 Berdasarkan analisis mendalam form TikTok asli")
        print("📧 1SECMAIL INTEGRATION - Email temporary aktif")
        print("📊 Dilengkapi Slardar monitoring & region headers")
        print("🌍 Menggunakan konfigurasi region yang valid")
        print("🛡️  Payload sangat authentic untuk menghindari detection")
        print("⚠️  GUNAKAN DENGAN TANGGUNG JAWAB!")
        print(f"🎯 Target: @{username}")
        print(f"📋 Alasan: {reason}")
        print(f"⏰ Delay: {delay_range[0]}-{delay_range[1]} detik")
        print(f"🔢 Max Reports: {'Unlimited' if max_reports is None else max_reports}")
        print(f"📭 Email Confirmation: {'AKTIF' if wait_for_confirmation else 'NON-AKTIF'}")
        print("=" * 60)
        
        # Analisis form mendalam sebelum memulai
        self.analyze_report_form()
        
        self.is_running = True
        iteration = 0
        
        while self.is_running:
            try:
                iteration += 1
                print(f"\n🔄 Iterasi #{iteration} - {time.strftime('%H:%M:%S')}")
                
                # Rotasi email dengan pattern yang lebih natural
                if iteration % random.randint(3, 6) == 0:
                    self.get_temp_email()
                
                # Kirim report dengan payload sangat authentic
                result = self.send_advanced_report(username, reason, wait_for_confirmation=wait_for_confirmation)
                
                # Update counters dan tampilkan status detail
                self.report_count += 1
                if result['success']:
                    self.success_count += 1
                    print(f"✅ Report #{iteration} BERHASIL untuk @{username}")
                    print(f"📧 Email: {result.get('email_used', 'N/A')}")
                    print(f"🌍 Region: {result.get('region', 'Unknown')}")
                    print(f"🔧 Build: {result.get('build_version', 'Unknown')}")
                    print(f"📭 Mailbox: {result.get('mailbox_type', 'Unknown')}")
                    
                    if result.get('email_confirmation'):
                        print(f"📩 Email Confirmation: DITERIMA dari TikTok")
                    else:
                        print(f"📩 Email Confirmation: {'Tidak dicek' if not wait_for_confirmation else 'Tidak diterima'}")
                    
                    # Tampilkan response detail jika ada
                    if 'response_data' in result and isinstance(result['response_data'], dict):
                        if 'message' in result['response_data']:
                            print(f"📝 Response: {result['response_data']['message']}")
                        if 'code' in result['response_data']:
                            print(f"🔢 Code: {result['response_data']['code']}")
                else:
                    self.failed_count += 1
                    print(f"❌ Report #{iteration} GAGAL untuk @{username}")
                    if 'error' in result:
                        print(f"   Error: {result['error']}")
                    elif 'response_data' in result:
                        print(f"   Response: {result['response_data']}")
                
                # Tampilkan summary detail
                self.show_advanced_stats()
                
                # Cek batas maksimal
                if max_reports and iteration >= max_reports:
                    print(f"\n🎯 Mencapai batas maksimal {max_reports} reports")
                    break
                
                # Delay acak dengan variasi yang lebih natural
                base_delay = random.randint(delay_range[0], delay_range[1])
                jitter = random.uniform(-7, 7)  # Variasi lebih besar
                actual_delay = max(15, base_delay + jitter)  # Minimum 15 detik
                
                print(f"⏳ Menunggu {actual_delay:.1f} detik sebelum report berikutnya...")
                
                # Countdown dengan interrupt check
                for i in range(int(actual_delay), 0, -1):
                    if not self.is_running:
                        break
                    if i % 15 == 0 or i <= 5:
                        print(f"   ⏰ {i} detik...")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n🛑 Dihentikan oleh user")
                break
            except Exception as e:
                print(f"❌ Error dalam loop: {str(e)}")
                time.sleep(20)  # Delay lebih panjang jika error
        
        self.is_running = False
        print("\n🛑 ADVANCED AUTO-REPORT SYSTEM DIHENTIKAN")
        self.show_final_advanced_stats()
    
    def show_advanced_stats(self):
        """Tampilkan statistik advanced"""
        success_rate = (self.success_count / self.report_count * 100) if self.report_count > 0 else 0
        avg_success = self.success_count / max(1, self.report_count)
        
        print(f"\n📊 ADVANCED STATS:")
        print(f"📨 Total Reports: {self.report_count}")
        print(f"✅ Berhasil: {self.success_count}")
        print(f"❌ Gagal: {self.failed_count}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"🔥 Efficiency: {avg_success:.2f}")
        
        if self.form_data:
            print(f"🌍 Region: {self.region_data.get('VRegion', 'Unknown') if self.region_data else 'Unknown'}")
            print(f"🔧 Build: {self.form_data.get('build_version', 'Unknown')}")

    def show_final_advanced_stats(self):
        """Tampilkan statistik final advanced"""
        print("\n" + "="*70)
        print("📊 FINAL ADVANCED REPORT STATISTICS:")
        print(f"📨 Total Reports Dikirim: {self.report_count}")
        print(f"✅ Reports Berhasil: {self.success_count}")
        print(f"❌ Reports Gagal: {self.failed_count}")
        
        if self.report_count > 0:
            success_rate = (self.success_count / self.report_count) * 100
            efficiency = self.success_count / self.report_count
            print(f"📈 Success Rate: {success_rate:.2f}%")
            print(f"🔥 Efficiency Score: {efficiency:.3f}")
        
        if self.form_data:
            print(f"🔗 API Endpoint: {self.form_data['api_endpoint']}")
            print(f"🌍 Region: {self.region_data.get('VRegion', 'Unknown') if self.region_data else 'Unknown'}")
            print(f"🔧 Build Version: {self.form_data.get('build_version', 'Unknown')}")
            print(f"📊 Slardar: {'Aktif' if self.slardar_config else 'Tidak aktif'}")
            print(f"📧 Mailbox Provider: {'1secmail.com' if self.current_mailbox else 'Fallback'}")
        
        print("="*70)

# ==================== ENHANCED INTERFACE DENGAN 1SECMAIL ====================

def advanced_quick_start():
    """Interface advanced dengan 1secmail integration"""
    print("⚡ ADVANCED TIKTOK AUTO-REPORT SYSTEM")
    print("📧 DILENGKAPI 1SECMAIL.COM - Email Temporary Aktif")
    print("🔍 Dilengkapi analisis mendalam form TikTok asli")
    print("📊 Slardar Monitoring | Region Headers | Build Version")
    print("=" * 60)
    
    # Input username
    username = input("Masukkan username TikTok target: ").strip().replace('@', '')
    
    if not username:
        print("❌ Username tidak boleh kosong!")
        return
    
    reporter = TikTokReporter()
    
    # Validasi username
    if not reporter.validate_username(username):
        print("❌ Format username tidak valid!")
        return
    
    # Test 1secmail terlebih dahulu
    print("\n🧪 Testing 1secmail.com integration...")
    try:
        test_email = reporter.get_1secmail_email()
        if test_email:
            print("✅ 1secmail.com: BERHASIL")
        else:
            print("⚠️  1secmail.com: GAGAL, menggunakan fallback")
    except Exception as e:
        print(f"⚠️  1secmail.com: ERROR - {e}")
    
    # Analisis form mendalam sebelum memulai
    print("\n🔍 Menganalisis form report TikTok secara mendalam...")
    form_info = reporter.analyze_report_form()
    
    if form_info:
        print("✅ Advanced form analysis completed!")
        if form_info.get('slardar_config'):
            print("📊 Slardar monitoring: AKTIF")
        if form_info.get('region_data'):
            print(f"🌍 Region: {form_info['region_data'].get('VRegion', 'Unknown')}")
    else:
        print("⚠️  Using advanced default configuration")
    
    # Pilihan mode advanced
    print("\n🎯 PILIH MODE REPORT:")
    print("1. ⚡ QUICK ATTACK (25 reports, fast rotation)")
    print("2. 🚀 STANDARD ATTACK (Unlimited, balanced)") 
    print("3. 🐢 STEALTH MODE (Unlimited, slow & safe)")
    print("4. 🔥 AGGRESSIVE MODE (75 reports, maximum speed)")
    print("5. 🎯 PRECISION MODE (Custom configuration)")
    print("6. 📧 EMAIL CONFIRMATION MODE (Tunggu balasan TikTok)")
    
    mode = input("Pilih mode (1-6): ").strip()
    
    wait_for_confirmation = False
    
    # Konfigurasi berdasarkan mode
    if mode == "1":
        delay_range = (20, 35)
        max_reports = 25
        print("⚡ Mode: QUICK ATTACK (25 reports)")
    elif mode == "2":
        delay_range = (30, 50)
        max_reports = None
        print("🚀 Mode: STANDARD ATTACK (Unlimited)")
    elif mode == "3":
        delay_range = (45, 75)
        max_reports = None
        print("🐢 Mode: STEALTH MODE (Unlimited)")
    elif mode == "4":
        delay_range = (15, 25)
        max_reports = 75
        print("🔥 Mode: AGGRESSIVE MODE (75 reports)")
    elif mode == "5":
        # Custom configuration
        min_delay = int(input("Delay minimum (detik): ") or "30")
        max_delay = int(input("Delay maksimum (detik): ") or "50")
        max_reports_input = input("Max reports (kosong untuk unlimited): ").strip()
        max_reports = int(max_reports_input) if max_reports_input else None
        confirm_choice = input("Tunggu konfirmasi email? (y/n): ").strip().lower()
        wait_for_confirmation = confirm_choice == 'y'
        delay_range = (min_delay, max_delay)
        print("🎯 Mode: PRECISION MODE (Custom)")
    elif mode == "6":
        delay_range = (40, 60)
        max_reports = 20
        wait_for_confirmation = True
        print("📧 Mode: EMAIL CONFIRMATION MODE (20 reports)")
    else:
        delay_range = (30, 50)
        max_reports = None
        print("🚀 Mode: STANDARD ATTACK (Default)")
    
    # Pilihan alasan advanced
    print("\n📋 PILIH ALASAN REPORT:")
    reasons = {
        "1": "privacy",
        "2": "harassment", 
        "3": "hate_speech",
        "4": "illegal_activities",
        "5": "minor_safety",
        "6": "intellectual_property",
        "7": "spam",
        "8": "impersonation",
        "9": "bullying"
    }
    
    reason_texts = {
        "privacy": "Pelanggaran Privasi",
        "harassment": "Pelecehan",
        "hate_speech": "Ujaran Kebencian", 
        "illegal_activities": "Aktivitas Illegal",
        "minor_safety": "Keamanan Anak",
        "intellectual_property": "Hak Cipta",
        "spam": "Spam",
        "impersonation": "Peniruan Identitas",
        "bullying": "Perundungan"
    }
    
    for key, value in reasons.items():
        print(f"{key}. {reason_texts[value]}")
    
    choice = input("Pilih alasan (1-9): ").strip()
    reason = reasons.get(choice, "privacy")
    
    # Konfirmasi final advanced
    print(f"\n⚙️  KONFIGURASI FINAL ADVANCED:")
    print(f"🎯 Target: @{username}")
    print(f"📋 Alasan: {reason_texts[reason]} ({reason})")
    print(f"⏰ Delay: {delay_range[0]}-{delay_range[1]} detik")
    print(f"🔢 Max Reports: {'Unlimited' if max_reports is None else max_reports}")
    print(f"📧 Email: 1secmail.com (aktif & bisa terima balasan)")
    print(f"📭 Email Confirmation: {'AKTIF' if wait_for_confirmation else 'NON-AKTIF'}")
    if form_info:
        print(f"🔗 Endpoint: {form_info['api_endpoint']}")
        print(f"🌍 Region: {form_info.get('region_data', {}).get('VRegion', 'Unknown')}")
        print(f"🔧 Build: {form_info.get('build_version', 'Unknown')}")
        print(f"📊 Slardar: {'AKTIF' if form_info.get('slardar_config') else 'NON-AKTIF'}")
    
    confirm = input("\n🚀 Jalankan advanced attack? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            reporter.start_advanced_unlimited_reports(
                username=username,
                reason=reason,
                delay_range=delay_range,
                max_reports=max_reports,
                wait_for_confirmation=wait_for_confirmation
            )
        except KeyboardInterrupt:
            print("\n🛑 Program dihentikan oleh user")
    else:
        print("❌ Dibatalkan")

def test_1secmail_function():
    """Function untuk testing 1secmail"""
    print("🧪 TESTING 1SECMAIL FUNCTIONALITY")
    print("=" * 40)
    
    reporter = TikTokReporter()
    
    try:
        # Test email generation
        print("1. Testing email generation...")
        email = reporter.get_1secmail_email()
        if email:
            print(f"   ✅ Email: {email}")
        else:
            print("   ❌ Failed to generate email")
            return
        
        # Test inbox checking
        print("2. Testing inbox check...")
        messages = reporter.check_1secmail_inbox()
        if messages is not None:
            print(f"   ✅ Inbox checked: {len(messages)} messages")
        else:
            print("   ❌ Failed to check inbox")
            return
            
        # Test waiting for confirmation (short timeout)
        print("3. Testing email confirmation wait (10 seconds)...")
        confirmation = reporter.wait_for_tiktok_confirmation(timeout=10)
        if confirmation:
            print("   ✅ Confirmation received!")
        else:
            print("   ⏰ No confirmation (expected in test)")
            
        print("\n🎉 1secmail testing completed successfully!")
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")

def main():
    """Menu utama advanced dengan 1secmail"""
    print("🚫 ADVANCED TIKTOK AUTO-REPORT SYSTEM")
    print("📧 DILENGKAPI 1SECMAIL.COM - Email Temporary Aktif")
    print("🔍 Berdasarkan analisis mendalam form TikTok asli")
    print("📊 Dilengkapi Slardar Monitoring & Region Configuration")
    print("🌍 Menggunakan data dari: https://www.tiktok.com/legal/report/privacy/webform/id")
    print("⚡ Payload sangat authentic & realistic")
    print("⚠️  GUNAKAN HANYA UNTUK PELAPORAN LEGITIMATE!")
    print("❌ JANGAN GUNAKAN UNTUK SPAM ATAU ABUSE!")
    print("=" * 70)
    
    while True:
        print("\n🎯 PILIH MENU:")
        print("1. ⚡ ADVANCED SINGLE USER ATTACK (Recommended)")
        print("2. 📧 TEST 1SECMAIL FUNCTIONALITY")
        print("3. 📊 DETAILED FORM ANALYSIS")
        print("4. 🔧 SYSTEM INFORMATION")
        print("5. ❌ KELUAR")
        
        choice = input("\nPilih menu (1-5): ").strip()
        
        if choice == "1":
            advanced_quick_start()
        elif choice == "2":
            test_1secmail_function()
        elif choice == "3":
            reporter = TikTokReporter()
            form_info = reporter.analyze_report_form()
            if form_info:
                print("\n📋 DETAILED FORM ANALYSIS:")
                print(json.dumps(form_info, indent=2, ensure_ascii=False))
        elif choice == "4":
            reporter = TikTokReporter()
            reporter.analyze_report_form()
            if reporter.form_data:
                print("\n🔧 SYSTEM INFORMATION:")
                print(f"Build Version: {reporter.form_data.get('build_version')}")
                print(f"CDN Domain: {reporter.form_data.get('cdn_domain')}")
                print(f"Region: {reporter.region_data.get('VRegion') if reporter.region_data else 'Unknown'}")
                print(f"Slardar Active: {bool(reporter.slardar_config)}")
                # Test 1secmail status
                try:
                    test_email = reporter.get_1secmail_email()
                    print(f"1secmail Status: ✅ AKTIF ({test_email})")
                except:
                    print("1secmail Status: ❌ TIDAK AKTIF")
        elif choice == "5":
            print("👋 Terima kasih, gunakan dengan bijak!")
            break
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    main()
