#bin/python3
#Developers: MexazoExecuted
#My Friend: LORDHOZOO
#Version: 5.0


import requests
import time
import random
import hashlib
import string
import asyncio
import aiohttp
import os
import sys
import json
from fake_useragent import UserAgent
from rich.console import Console
from rich.panel import Panel
from rich import box
from os import system

system("clear")
console = Console()

def animate_text(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_google_status():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return "AKTIF" if response.status_code == 200 else "TIDAK AKTIF"
    except:
        return "TIDAK AKTIF"

def get_weather():
    try:
        response = requests.get("http://wttr.in/?format=%C+%t", timeout=15)
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    return "-0°"

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return "735.2492.42.01"

# ==================== PASSWORD SYSTEM (DISABLED) ====================
def check_password():
    return True  # Password system dimatikan

# ==================== COOKIE MANAGEMENT SYSTEM ====================
class CookieManager:
    def __init__(self):
        self.cookies_file = "tiktok_cookies.json"
        self.active_cookies = []
        self.load_cookies()
    
    def load_cookies(self):
        """Load cookies dari file"""
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'r') as f:
                    self.active_cookies = json.load(f)
                console.print(f"[green]✅ Loaded {len(self.active_cookies)} cookies[/green]")
            else:
                console.print("[yellow]⚠️ No cookies file found[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ Error loading cookies: {e}[/red]")
    
    def save_cookies(self):
        """Save cookies ke file"""
        try:
            with open(self.cookies_file, 'w') as f:
                json.dump(self.active_cookies, f, indent=2)
            console.print(f"[green]✅ Saved {len(self.active_cookies)} cookies[/green]")
        except Exception as e:
            console.print(f"[red]❌ Error saving cookies: {e}[/red]")
    
    def add_cookie(self, cookie_string):
        """Add cookie baru"""
        try:
            cookie_dict = self.parse_cookie_string(cookie_string)
            if cookie_dict:
                self.active_cookies.append({
                    'cookie_string': cookie_string,
                    'cookie_dict': cookie_dict,
                    'added_time': time.time()
                })
                self.save_cookies()
                console.print("[green]✅ Cookie added successfully[/green]")
                return True
            else:
                console.print("[red]❌ Invalid cookie format[/red]")
                return False
        except Exception as e:
            console.print(f"[red]❌ Error adding cookie: {e}[/red]")
            return False
    
    def parse_cookie_string(self, cookie_string):
        """Parse cookie string menjadi dictionary"""
        cookie_dict = {}
        try:
            for part in cookie_string.split(';'):
                if '=' in part:
                    key, value = part.strip().split('=', 1)
                    cookie_dict[key] = value
            return cookie_dict
        except:
            return None
    
    def get_random_cookie(self):
        """Ambil cookie random dari pool"""
        if not self.active_cookies:
            return None
        return random.choice(self.active_cookies)
    
    def show_cookies(self):
        """Tampilkan semua cookies"""
        if not self.active_cookies:
            console.print("[yellow]⚠️ No cookies available[/yellow]")
            return
        
        for i, cookie in enumerate(self.active_cookies, 1):
            age = time.time() - cookie['added_time']
            console.print(f"[cyan]{i}. Added {age:.0f}s ago[/cyan]")
            # Tampilkan beberapa key penting
            important_keys = ['sessionid', 'msToken', 'tt_chain_token', 'sid_tt']
            for key in important_keys:
                if key in cookie['cookie_dict']:
                    console.print(f"   {key}: {cookie['cookie_dict'][key][:20]}...")

# ==================== VIDEO SCRAPER ====================
class TikTokVideoScraper:
    def __init__(self, cookie_manager):
        self.cookie_manager = cookie_manager
        self.session = requests.Session()
    
    def get_user_videos(self, username, max_videos=50):
        """Scrape video dari user target"""
        console.print(f"[yellow]🔍 Scraping videos from @{username}...[/yellow]")
        
        videos = []
        try:
            # Gunakan cookie aktif untuk scraping
            cookie_data = self.cookie_manager.get_random_cookie()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Referer': f'https://www.tiktok.com/@{username}',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # API endpoint untuk get user posts
            api_url = f"https://www.tiktok.com/api/post/item_list/"
            params = {
                'aid': '1988',
                'count': '30',
                'secUid': '',  # Will be filled if available
                'cursor': '0'
            }
            
            # Jika ada cookie, gunakan untuk request
            if cookie_data:
                headers['Cookie'] = cookie_data['cookie_string']
            
            response = self.session.get(api_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'itemList' in data:
                    for item in data['itemList'][:max_videos]:
                        video_data = {
                            'id': item.get('id', ''),
                            'desc': item.get('desc', '')[:100],
                            'createTime': item.get('createTime', ''),
                            'videoUrl': f"https://www.tiktok.com/@{username}/video/{item.get('id', '')}",
                            'stats': item.get('stats', {})
                        }
                        videos.append(video_data)
                    
                    console.print(f"[green]✅ Found {len(videos)} videos from @{username}[/green]")
                else:
                    console.print("[red]❌ No videos found in response[/red]")
            else:
                console.print(f"[red]❌ API request failed: {response.status_code}[/red]")
                
        except Exception as e:
            console.print(f"[red]❌ Error scraping videos: {e}[/red]")
        
        return videos

# ==================== TIKTOK GOD MODE (ENHANCED) ====================
class TikTokGodMode:
    def __init__(self):
        self.ua = UserAgent()
        self.request_count = 0
        self.success_count = 0
        self.session = requests.Session()
        self.cookie_manager = CookieManager()
        self.video_scraper = TikTokVideoScraper(self.cookie_manager)
        
        self.base_urls = {
            'copyright': "https://www.tiktok.com/api/report/copyright/v2/submit/",
            'privacy': "https://www.tiktok.com/api/report/privacy/v3/submit/", 
            'safety': "https://www.tiktok.com/api/report/safety/v2/submit/",
            'bullying': "https://www.tiktok.com/api/report/bullying/v2/submit/",
            'hate_speech': "https://www.tiktok.com/api/report/hate/speech/v2/submit/",
            'harassment': "https://www.tiktok.com/api/report/harassment/v2/submit/",
            'minor': "https://www.tiktok.com/api/report/minor/safety/v2/submit/",
            'impersonation': "https://www.tiktok.com/api/report/impersonation/v2/submit/",
            'spam': "https://www.tiktok.com/api/report/spam/v2/submit/",
            'fake_account': "https://www.tiktok.com/api/report/fake/account/v2/submit/",
            'violence': "https://www.tiktok.com/api/report/violence/v2/submit/",
            'suicide': "https://www.tiktok.com/api/report/suicide-selfharm/v2/submit/",
            'dangerous': "https://www.tiktok.com/api/report/dangerous-acts/v2/submit/",
            'animal': "https://www.tiktok.com/api/report/animal-cruelty/v2/submit/",
            'exploitation': "https://www.tiktok.com/api/report/human-exploitation/v2/submit/",
            'illegal_goods': "https://www.tiktok.com/api/report/illegal/goods/v2/submit/",
            'fraud': "https://www.tiktok.com/api/report/fraud/v2/submit/",
            'misinformation': "https://www.tiktok.com/api/report/misinformation/v2/submit/",
            'webform_privacy': "https://www.tiktok.com/legal/report/privacy/webform/id",
            'api_general': "https://www.tiktok.com/api/report/",
            'video_report': "https://www.tiktok.com/api/report/video/submit/"
        }

    def generate_temp_email(self):
        try:
            response = self.session.get(
                "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1",
                timeout=3
            )
            if response.status_code == 200:
                email_data = response.json()
                if email_data:
                    return email_data[0]
        except:
            pass
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com']
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        return f"{username}@{random.choice(domains)}"

    def generate_fingerprint(self):
        timestamp = int(time.time() * 1000)
        return {
            'device_id': f"7{random.randint(100000000000000000, 999999999999999999)}",
            'install_id': f"7{random.randint(100000000000000000, 999999999999999999)}",
            'session_id': hashlib.sha256(f"{timestamp}{random.random()}".encode()).hexdigest()[:32],
            'openudid': hashlib.sha256(f"openudid_{timestamp}".encode()).hexdigest()[:32],
            'clientudid': hashlib.sha256(f"clientudid_{timestamp}".encode()).hexdigest()[:32],
            'fp': hashlib.md5(f"fp_{timestamp}".encode()).hexdigest(),
            'ts': timestamp
        }

    def generate_advanced_headers(self, use_cookie=True):
        fingerprint = self.generate_fingerprint()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Sec-Fetch-Dest': 'empty',
            'X-Sec-Fetch-Mode': 'cors',
            'X-Sec-Fetch-Site': 'same-origin',
            'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Real-IP': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
            'X-Client-Device-Id': fingerprint['device_id'],
            'X-Client-Install-Id': fingerprint['install_id'],
            'X-Client-Session-Id': fingerprint['session_id'],
            'X-OpenUDID': fingerprint['openudid'],
            'X-ClientUDID': fingerprint['clientudid'],
            'X-Tt-Token': hashlib.sha256(f"token_{time.time()}".encode()).hexdigest()[:32],
            'X-Bogus': f"DFSzswVY{random.randint(1000,9999)}x{random.randint(1000,9999)}",
            'X-Tt-Env': 'boe_www',
            'X-Tt-Trace-Id': hashlib.md5(f"trace_{time.time()}".encode()).hexdigest(),
            'X-Tt-Stage': 'release',
            'X-Tt-Store-Region': 'us',
            'X-Tt-Store-Region-Src': 'uid',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Priority': 'u=1, i'
        }
        
        # Tambahkan cookie jika tersedia dan diminta
        if use_cookie:
            cookie_data = self.cookie_manager.get_random_cookie()
            if cookie_data:
                headers['Cookie'] = cookie_data['cookie_string']
                headers['X-Tt-Token'] = cookie_data['cookie_dict'].get('tt_chain_token', headers['X-Tt-Token'])
        
        return headers

    def generate_video_report_payload(self, target_username, video_data):
        """Generate payload khusus untuk report video"""
        email = self.generate_temp_email()
        timestamp = int(time.time() * 1000)
        
        return {
            "object_id": video_data['id'],
            "object_type": 1,  # 1 untuk video, 0 untuk user
            "owner_id": random.randint(100000000000000000, 999999999999999999),
            "report_type": random.choice([1001, 1002, 1003, 1004]),
            "reason": random.choice([2001, 2002, 2003, 2004, 2005]),
            "reporter_email": email,
            "reporter_country": "ID",
            "additional_info": f"Video '{video_data['desc']}' by @{target_username} violates community guidelines",
            "video_url": video_data['videoUrl'],
            "timestamp": timestamp,
            "platform": "web",
            "language": "id"
        }, email

    def generate_webform_payload(self, target_username):
        email = self.generate_temp_email()
        timestamp = int(time.time() * 1000)
        return {
            "username": target_username,
            "email": email,
            "country": "ID",
            "report_type": "privacy",
            "violation_category": random.choice(["data_collection", "personal_info", "location_tracking", "contact_harvesting"]),
            "description": f"User {target_username} is systematically collecting and misusing personal information from other users without consent. This includes harvesting email addresses, phone numbers, and location data through deceptive means.",
            "evidence_urls": f"https://www.tiktok.com/@{target_username}",
            "affected_users": random.randint(10, 1000),
            "severity": "high",
            "consent": "true",
            "language": "id",
            "platform": "web",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "timestamp": timestamp,
            "session_id": hashlib.sha256(f"session_{timestamp}".encode()).hexdigest()[:32],
            "csrf_token": hashlib.sha256(f"csrf_{timestamp}".encode()).hexdigest()[:32],
            "agreement": "true",
            "follow_up": "false",
            "urgent": random.choice(["true", "false"]),
            "additional_info": f"Automated privacy violation report for user {target_username}. Multiple instances of data harvesting detected.",
            "report_source": "web_form",
            "form_version": "2.0",
            "legal_basis": "gdpr_article_17"
        }

    def generate_api_general_payload(self, target_username):
        email = self.generate_temp_email()
        timestamp = int(time.time() * 1000)
        report_types = {
            'copyright': {
                'object_id': target_username,
                'object_type': 0,
                'owner_id': random.randint(100000000000000000, 999999999999999999),
                'report_type': 1001,
                'reason': 1001,
                'additional_info': {
                    'copyright_type': random.choice([1, 2, 3, 4, 5]),
                    'copyright_text': f'Original content ID: CP{random.randint(100000000,999999999)}',
                    'infringing_urls': [f'https://www.tiktok.com/@{target_username}'],
                    'description': f'Systematic copyright infringement by user {target_username}',
                    'evidence': f'Screenshots and timestamps proving infringement by {target_username}'
                }
            },
            'privacy': {
                'object_id': target_username,
                'object_type': 0,
                'owner_id': random.randint(100000000000000000, 999999999999999999),
                'report_type': 1002,
                'reason': 2001,
                'additional_info': {
                    'privacy_type': random.choice([1, 2, 3]),
                    'personal_info_type': random.choice([1, 2, 3, 4, 5]),
                    'description': f'Privacy violation - unauthorized data collection by {target_username}',
                    'evidence': 'User is harvesting personal information from comments and profiles'
                }
            }
        }
        report_type = random.choice(list(report_types.keys()))
        base_payload = {
            "report_id": f"RPT{timestamp}{random.randint(1000,9999)}",
            "reporter_id": random.randint(100000000000000000, 999999999999999999),
            "reporter_ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "reporter_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "reporter_email": email,
            "reporter_country": random.choice(['US', 'ID', 'GB', 'CA', 'AU']),
            "reporter_language": "en",
            "reporter_platform": "web",
            "reporter_app_version": "99.9.9",
            "reporter_os_version": "Windows 10",
            "reporter_device_model": "PC",
            "reporter_device_id": f"WEB_{random.randint(100000000000000000, 999999999999999999)}",
            "report_source": "web_report_form",
            "report_flow": "standard",
            "report_context": "profile_page",
            "violation_severity": random.choice(["low", "medium", "high", "critical"]),
            "violation_count": random.randint(1, 50),
            "first_observed": timestamp - random.randint(86400000, 2592000000),
            "last_observed": timestamp,
            "agreement": True,
            "additional_comments": f"Automated report for violations by user {target_username}",
            "evidence_attached": False,
            "witness_available": False,
            "legal_authority": False,
            "urgent": random.choice([True, False]),
            "anonymous": True,
            "csrf_token": hashlib.sha256(f"csrf_{timestamp}".encode()).hexdigest()[:32],
            "session_id": hashlib.sha256(f"session_{timestamp}".encode()).hexdigest()[:32],
            "request_id": f"REQ{timestamp}{random.randint(1000,9999)}",
            "timestamp": timestamp,
            "version": "2.0",
            "signature": hashlib.md5(f"sign_{timestamp}_{target_username}".encode()).hexdigest()
        }
        return {**base_payload, **report_types[report_type]}, email

    def generate_dynamic_params(self):
        timestamp = int(time.time() * 1000)
        return {
            'aid': '1988',
            'app_name': 'tiktok_web',
            'device_platform': 'web',
            'device_id': random.randint(700000000000000000, 799999999999999999),
            'region': random.choice(['US', 'ID', 'SG', 'MY', 'JP']),
            'priority_region': '',
            'os': 'windows',
            'referer': '',
            'root_referer': '',
            'cookie_enabled': 'true',
            'screen_width': '1920',
            'screen_height': '1080',
            'browser_language': 'en-US',
            'browser_platform': 'Win32',
            'browser_name': 'Mozilla',
            'browser_version': '5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/120.0.0.0+Safari/537.36',
            'browser_online': 'true',
            'timezone_name': 'America/New_York',
            'is_page_visible': 'true',
            'focus_state': 'true',
            'is_fullscreen': 'false',
            'history_len': random.randint(1, 50),
            'language': 'en',
            'ts': timestamp,
            '_rticket': timestamp
        }

    def build_url(self, endpoint):
        params = self.generate_dynamic_params()
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{self.base_urls[endpoint]}?{query_string}"

    def generate_proxy_display(self):
        return f"{random.randint(100,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

    async def execute_video_report(self, session, target_username, video_data, report_id):
        """Execute report untuk video spesifik"""
        url = self.build_url('video_report')
        payload, email = self.generate_video_report_payload(target_username, video_data)
        headers = self.generate_advanced_headers(use_cookie=True)  # Gunakan cookie untuk video report
        
        proxy_display = self.generate_proxy_display()
        start_time = time.time()
        current_time = time.strftime("%H:%M:%S")
        
        try:
            async with session.post(
                url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=3),
                ssl=False
            ) as response:
                status_code = response.status
                
            response_time = int((time.time() - start_time) * 1000)
            self.request_count += 1
            
            if status_code in [200, 201, 204, 302]:
                self.success_count += 1
                status_text = f"{status_code} SUCCESS"
                status_color = "bold green"
            else:
                status_text = f"{status_code} FAILED"
                status_color = "bold red"

            console.print(Panel(
                f"[#FFFFFF]Target : [bold underline]@{target_username}[/bold underline]\n"
                f"[#FFFFFF]Video ID : {video_data['id'][:15]}...\n"
                f"[#FFFFFF]Status : [{status_color}] {status_text}[/{status_color}]\n"
                f"[#FFFFFF]Gmail  : {email}\n"
                f"[#FFFFFF]Proxy  : {proxy_display}\n"
                f"[#FFFFFF]Time  : {current_time}\n"
                f"[#FFFFFF]Speed : {response_time}ms",
                title="[white on black][bold underline]VIDEO REPORT STATUS[/bold underline]",
                title_align="center",
                border_style="#B8B8B8"
            ))
            return True

        except Exception as e:
            console.print(Panel(
                f"[#FFFFFF]Target : [bold underline]@{target_username}[/bold underline]\n"
                f"[#FFFFFF]Video ID : {video_data['id'][:15]}...\n"
                f"[#FFFFFF]Status : [bold red]ERROR {str(e)[:30]}[/bold red]\n"
                f"[#FFFFFF]Gmail  : {email}\n"
                f"[#FFFFFF]Proxy  : {proxy_display}\n"
                f"[#FFFFFF]Time  : {current_time}\n"
                f"[#FFFFFF]Speed : TIMEOUT",
                title="[white on black][bold underline]VIDEO REPORT STATUS[/bold underline]",
                title_align="center",
                border_style="#B8B8B8"
            ))
            return False

    async def execute_single_report(self, session, target_username, report_id, use_cookie=True):
        endpoints = list(self.base_urls.keys())
        random.shuffle(endpoints)
        
        for endpoint in endpoints:
            if endpoint == 'webform_privacy':
                url = self.base_urls[endpoint]
                payload = self.generate_webform_payload(target_username)
                headers = self.generate_advanced_headers(use_cookie=False)  # No cookie for webform
                content_type = 'application/x-www-form-urlencoded'
            elif endpoint == 'api_general':
                url = self.build_url(endpoint)
                payload, email = self.generate_api_general_payload(target_username)
                headers = self.generate_advanced_headers(use_cookie=use_cookie)
                content_type = 'application/json'
            else:
                url = self.build_url(endpoint)
                payload, email = self.generate_api_general_payload(target_username)
                headers = self.generate_advanced_headers(use_cookie=use_cookie)
                content_type = 'application/json'
                
            proxy_display = self.generate_proxy_display()
            start_time = time.time()
            current_time = time.strftime("%H:%M:%S")
            
            try:
                if endpoint == 'webform_privacy':
                    async with session.post(
                        url,
                        data=payload,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=3),
                        ssl=False
                    ) as response:
                        status_code = response.status
                else:
                    async with session.post(
                        url,
                        json=payload,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=3),
                        ssl=False
                    ) as response:
                        status_code = response.status
                        
                response_time = int((time.time() - start_time) * 1000)
                self.request_count += 1
                
                status_colors = {
                    200: "bold green", 201: "bold green", 204: "bold green", 302: "bold green",
                    400: "bold yellow", 401: "bold yellow", 403: "bold yellow", 404: "bold yellow",
                    405: "bold red", 429: "bold red", 500: "bold red", 502: "bold red", 503: "bold red"
                }
                status_color = status_colors.get(status_code, "bold white")
                
                if status_code in [200, 201, 204, 302]:
                    self.success_count += 1
                    status_text = f"{status_code} SUCCESS"
                elif status_code in [400, 401, 403, 404]:
                    status_text = f"{status_code} FAILED"
                else:
                    status_text = f"{status_code} ERROR"

                cookie_status = "WITH COOKIE" if use_cookie and headers.get('Cookie') else "NO COOKIE"
                
                console.print(Panel(
                    f"[#FFFFFF]Target : [bold underline]@{target_username}[/bold underline]\n"
                    f"[#FFFFFF]Status : [{status_color}] {status_text}[/{status_color}]\n"
                    f"[#FFFFFF]Gmail  : {email if 'email' in locals() else 'N/A'}\n"
                    f"[#FFFFFF]Cookie : {cookie_status}\n"
                    f"[#FFFFFF]Proxy  : {proxy_display}\n"
                    f"[#FFFFFF]Time  : {current_time}\n"
                    f"[#FFFFFF]Speed : {response_time}ms",
                    title="[white on black][bold underline]INFO STATUS TARGET[/bold underline]",
                    title_align="center",
                    border_style="#B8B8B8"
                ))
                return True

            except Exception as e:
                proxy_display = self.generate_proxy_display()
                current_time = time.strftime("%H:%M:%S")
                cookie_status = "WITH COOKIE" if use_cookie else "NO COOKIE"
                
                console.print(Panel(
                    f"[#FFFFFF]Target : [bold underline]@{target_username}[/bold underline]\n"
                    f"[#FFFFFF]Status : [bold red]ERROR {str(e)[:30]}[/bold red]\n"
                    f"[#FFFFFF]Gmail  : {email if 'email' in locals() else 'N/A'}\n"
                    f"[#FFFFFF]Cookie : {cookie_status}\n"
                    f"[#FFFFFF]Proxy  : {proxy_display}\n"
                    f"[#FFFFFF]Time  : {current_time}\n"
                    f"[#FFFFFF]Speed : TIMEOUT",
                    title="[white on black][bold underline]INFO STATUS TARGET[/bold underline]",
                    title_align="center",
                    border_style="#B8B8B8"
                ))
                continue
        return False

    async def video_attack(self, target_username):
        """Attack khusus untuk report video"""
        console.print(f"[yellow]🎬 Starting video report attack for @{target_username}[/yellow]")
        
        # Scrape videos dulu
        videos = self.video_scraper.get_user_videos(target_username, max_videos=20)
        
        if not videos:
            console.print("[red]❌ No videos found, switching to profile attack[/red]")
            await self.smooth_attack(target_username)
            return
        
        connector = aiohttp.TCPConnector(limit=3, limit_per_host=3, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            report_id = 1
            while True:
                # Report random video
                video = random.choice(videos)
                await self.execute_video_report(session, target_username, video, report_id)
                
                # Kadang-kadang report profile juga
                if random.random() < 0.3:  # 30% chance untuk report profile
                    await self.execute_single_report(session, target_username, report_id, use_cookie=True)
                
                await asyncio.sleep(2)  # Delay lebih panjang untuk video report
                report_id += 1

    async def smooth_attack(self, target_username):
        connector = aiohttp.TCPConnector(limit=5, limit_per_host=5, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            report_id = 1
            while True:
                # Gunakan cookie secara bergantian
                use_cookie = random.random() < 0.7  # 70% pakai cookie
                await self.execute_single_report(session, target_username, report_id, use_cookie)
                await asyncio.sleep(1)
                report_id += 1

    def start_attack(self, target_username, attack_type="profile"):
        """Start attack dengan pilihan type"""
        if attack_type == "video":
            asyncio.run(self.video_attack(target_username))
        else:
            asyncio.run(self.smooth_attack(target_username))

# ==================== MAIN MENU ENHANCED ====================
def main():
    if not check_password():
        return

    google_status = get_google_status()
    weather = get_weather()
    public_ip = get_public_ip()
    current_time = time.strftime("%H:%M:%S")
    
    system("clear")
    console.print(f"""[bold red]
⠀⠀⠀⠀⠠⠤⠤⠤⠤⠤⣤⣤⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠛⠿⢶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣀⣀⣠⣤⣤⣴⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠿⠿⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠚⠛⠉⠉⠉⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⡴⠶⠶⠿⠿⠿⣧⡀⠀⠀⠀⠤⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠞⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⣶⣦⣤⣄⣈⡑⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⠔⠚⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡿⠟⠉⠉⠉⠉⠙⠛⠿⣿⣮⣷⣤⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣯⣧⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢷⡤⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠛⠻⠿⠿⣿⣶⣶⣦⣄⣀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣯⡛⠻⢦⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣆⠀⠙⢆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣆⠀⠈⢣
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡆⠀⠈
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⠀""")
    
    console.print(Panel(f"""[#FFFFFF][?]DEVELOPERS : [bold underline]MexazoExecuted[/bold underline]\n[#FFFFFF][?]MY FRIEND : [bold underline]LORDHOZOO[/bold underline]\n[#FFFFFF][?]VERSION : [bold underline]6.0 ENHANCED[/bold underline]\n[#FFFFFF][?]INFO : [bold underline]UNLIMITED REPORT TIKTOK[/bold underline]\n[#FFFFFF][?]GOOGLE : [bold underline]{google_status}[/bold underline]\n[#FFFFFF][?]IP YOUR : [bold underline]{public_ip}[/bold underline]\n[#FFFFFF][?]CUACA : [bold underline]{weather}[/bold underline]\n[#FFFFFF][?]TIME : [bold underline]{current_time}[/bold underline]""",border_style="#B8B8B8",title="[white on black][bold underline]INFORMASI[/bold underline]",title_align="center"))

    # Initialize reporter
    reporter = TikTokGodMode()
    
    while True:
        console.print("\n[bold cyan]🎯 SELECT ATTACK MODE:[/bold cyan]")
        console.print("[cyan]1. 🎪 PROFILE ATTACK (Report user profile)[/cyan]")
        console.print("[cyan]2. 🎬 VIDEO ATTACK (Scrape & report videos)[/cyan]")
        console.print("[cyan]3. 🔧 COOKIE MANAGEMENT[/cyan]")
        console.print("[cyan]4. ❌ EXIT[/cyan]")
        
        choice = console.input("[#FFFFFF][?] SELECT MODE (1-4): ").strip()
        
        if choice == "1":
            target = console.input("[#FFFFFF][?] USERNAME TARGET : ").strip().replace('@', '')
            if target:
                reporter.start_attack(target, "profile")
            else:
                console.print("[red]❌ No target specified[/red]")
                
        elif choice == "2":
            target = console.input("[#FFFFFF][?] USERNAME TARGET : ").strip().replace('@', '')
            if target:
                reporter.start_attack(target, "video")
            else:
                console.print("[red]❌ No target specified[/red]")
                
        elif choice == "3":
            console.print("\n[bold cyan]🍪 COOKIE MANAGEMENT[/bold cyan]")
            console.print("[cyan]1. ➕ ADD NEW COOKIE[/cyan]")
            console.print("[cyan]2. 📋 SHOW COOKIES[/cyan]")
            console.print("[cyan]3. 🗑️ CLEAR ALL COOKIES[/cyan]")
            console.print("[cyan]4. 🔙 BACK[/cyan]")
            
            cookie_choice = console.input("[#FFFFFF][?] SELECT (1-4): ").strip()
            
            if cookie_choice == "1":
                cookie_string = console.input("[#FFFFFF][?] PASTE COOKIE STRING: ").strip()
                if cookie_string:
                    reporter.cookie_manager.add_cookie(cookie_string)
                else:
                    console.print("[red]❌ No cookie provided[/red]")
                    
            elif cookie_choice == "2":
                reporter.cookie_manager.show_cookies()
                
            elif cookie_choice == "3":
                reporter.cookie_manager.active_cookies = []
                reporter.cookie_manager.save_cookies()
                console.print("[green]✅ All cookies cleared[/green]")
                
        elif choice == "4":
            console.print("[green]👋 Goodbye![/green]")
            break
            
        else:
            console.print("[red]❌ Invalid choice[/red]")

if __name__ == "__main__":
    main()
