import re
import socket
import whois
import requests
from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

def extract_features_from_url(url: str):
    features = {}

    try:
        # Normalize URL
        if not url.startswith("http"):
            url = "http://" + url

        parsed = urlparse(url)
        domain = parsed.netloc

        # 1. having_IP_Address
        features['having_IP_Address'] = 1 if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain) else 0

        # 2. URL_Length
        features['URL_Length'] = 1 if len(url) < 54 else (0 if len(url) <= 75 else -1)

        # 3. Shortining_Service
        shorteners = r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|shorte\.st|adf\.ly|bitly\.com"
        features['Shortining_Service'] = 1 if re.search(shorteners, url) else 0

        # 4. having_At_Symbol
        features['having_At_Symbol'] = 1 if "@" in url else 0

        # 5. double_slash_redirecting
        features['double_slash_redirecting'] = 1 if url.rfind('//') > 6 else 0

        # 6. Prefix_Suffix
        features['Prefix_Suffix'] = 1 if '-' in domain else 0

        # 7. having_Sub_Domain
        subdomain_count = domain.count('.')
        features['having_Sub_Domain'] = -1 if subdomain_count > 2 else (0 if subdomain_count == 2 else 1)

        # 8. SSLfinal_State
        features['SSLfinal_State'] = 1 if url.startswith('https') else 0

        # 9. Domain_registeration_length
        try:
            domain_info = whois.whois(domain)
            if domain_info.expiration_date and domain_info.creation_date:
                creation = domain_info.creation_date
                expiration = domain_info.expiration_date
                if isinstance(creation, list): creation = creation[0]
                if isinstance(expiration, list): expiration = expiration[0]
                domain_age = (expiration - creation).days
                features['Domain_registeration_length'] = 1 if domain_age > 365 else 0
            else:
                features['Domain_registeration_length'] = 0
        except:
            features['Domain_registeration_length'] = 0

        # 10. Favicon
        try:
            html = requests.get(url, timeout=5).text
            soup = BeautifulSoup(html, 'html.parser')
            features['Favicon'] = 0
            for link in soup.find_all('link', rel=lambda value: value and 'icon' in value.lower()):
                if domain in link.get('href', ''):
                    features['Favicon'] = 1
        except:
            features['Favicon'] = 0

        # 11. port
        try:
            socket.create_connection((domain, 80), timeout=3)
            features['port'] = 1
        except:
            features['port'] = 0

        # 12. HTTPS_token
        features['HTTPS_token'] = 1 if 'https' in domain else 0

        # 13. Request_URL
        try:
            total, internal = 0, 0
            soup = BeautifulSoup(html, 'html.parser')
            for img in soup.find_all('img', src=True):
                total += 1
                if domain in img['src']: internal += 1
            features['Request_URL'] = 1 if total == 0 or internal / total >= 0.6 else 0
        except:
            features['Request_URL'] = 0

        # 14. URL_of_Anchor
        try:
            anchors = soup.find_all('a', href=True)
            total_links = len(anchors)
            safe_links = sum(1 for a in anchors if domain in a['href'])
            features['URL_of_Anchor'] = 1 if total_links == 0 or safe_links / total_links > 0.7 else 0
        except:
            features['URL_of_Anchor'] = 0

        # 15. Links_in_tags
        try:
            tags = soup.find_all(['link', 'script'])
            total = len(tags)
            safe = sum(1 for t in tags if domain in (t.get('href') or '') or domain in (t.get('src') or ''))
            features['Links_in_tags'] = 1 if total == 0 or safe / total > 0.6 else 0
        except:
            features['Links_in_tags'] = 0

        # 16. SFH (Server Form Handler)
        try:
            forms = soup.find_all('form')
            features['SFH'] = 1
            for form in forms:
                if not form.get('action') or "about:blank" in form.get('action'):
                    features['SFH'] = 0
        except:
            features['SFH'] = 0

        # 17. Submitting_to_email
        features['Submitting_to_email'] = 1 if "mailto:" in html else 0

        # 18. Abnormal_URL
        features['Abnormal_URL'] = 1 if domain in requests.get(url).text else 0

        # 19. Redirect
        try:
            response = requests.get(url, timeout=5)
            features['Redirect'] = 1 if len(response.history) <= 1 else 0
        except:
            features['Redirect'] = 0

        # 20. on_mouseover
        features['on_mouseover'] = 1 if re.search(r"onmouseover", html, re.IGNORECASE) else 0

        # 21. RightClick
        features['RightClick'] = 1 if re.search(r"event.button ?== ?2", html) else 0

        # 22. popUpWidnow
        features['popUpWidnow'] = 1 if re.search(r"alert\(", html) else 0

        # 23. Iframe
        features['Iframe'] = 1 if "<iframe" in html else 0

        # 24. age_of_domain
        try:
            creation = domain_info.creation_date
            if isinstance(creation, list): creation = creation[0]
            if creation:
                age_days = (datetime.now() - creation).days
                features['age_of_domain'] = 1 if age_days > 180 else 0
            else:
                features['age_of_domain'] = 0
        except:
            features['age_of_domain'] = 0

        # 25. DNSRecord
        try:
            socket.gethostbyname(domain)
            features['DNSRecord'] = 1
        except:
            features['DNSRecord'] = 0

        # 26. web_traffic (simplified placeholder)
        features['web_traffic'] = 0

        # 27. Page_Rank (placeholder)
        features['Page_Rank'] = 0

        # 28. Google_Index (placeholder)
        features['Google_Index'] = 0

        # 29. Links_pointing_to_page
        try:
            links_count = html.count('<a href=')
            features['Links_pointing_to_page'] = 1 if links_count < 2 else 0
        except:
            features['Links_pointing_to_page'] = 0

        # 30. Statistical_report
        features['Statistical_report'] = 0

        return features

    except Exception as e:
        print("Feature extraction error:", e)
        return None
