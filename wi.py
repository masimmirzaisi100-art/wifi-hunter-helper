#!/usr/bin/env python3
# ═══════════════════════════════════════════════
#  🔐 SECURITY TOOLKIT v1.0
#  Termux & PC के लिए Complete Security Tools
# ═══════════════════════════════════════════════

import os
import sys
import json
import time
import string
import random
import hashlib
import getpass
import base64
from datetime import datetime

# ═══════════════════════════════════════════════
#  COLORS
# ═══════════════════════════════════════════════

class C:
    R = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

def title(text):
    print(f"\n{C.CYAN}{C.BOLD}{'─'*50}{C.R}")
    print(f"  {text}")
    print(f"{C.CYAN}{C.BOLD}{'─'*50}{C.R}\n")

def success(msg):
    print(f"  {C.GREEN}✅ {msg}{C.R}")

def error(msg):
    print(f"  {C.RED}❌ {msg}{C.R}")

def warn(msg):
    print(f"  {C.YELLOW}⚠️  {msg}{C.R}")

def info(msg):
    print(f"  {C.BLUE}ℹ️  {msg}{C.R}")


# ═══════════════════════════════════════════════
#  TOOL 1: WiFi PASSWORD STRENGTH CHECKER
# ═══════════════════════════════════════════════

def password_strength():
    title("🔐 PASSWORD STRENGTH CHECKER")

    pwd = getpass.getpass("  Password (hidden): ")
    if not pwd:
        error("Empty password!")
        return

    score = 0
    feedback = []
    length = len(pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in pwd)
    has_space = ' ' in pwd

    # Length score
    if length >= 8:  score += 20
    else: feedback.append("कम से कम 8 characters चाहिए")
    if length >= 12: score += 15
    if length >= 16: score += 10
    if length >= 20: score += 5

    # Character types
    if has_upper: score += 15
    else: feedback.append("Capital letters (A-Z) add करें")
    if has_lower: score += 10
    else: feedback.append("Small letters (a-z) add करें")
    if has_digit: score += 15
    else: feedback.append("Numbers (0-9) add करें")
    if has_special: score += 15
    else: feedback.append("Special chars (!@#$) add करें")

    # Common passwords check
    common = ['password', '123456', 'qwerty', 'abc123', 'letmein',
              'admin', 'welcome', 'monkey', 'master', 'dragon',
              'wifi', 'internet', 'login', 'iloveyou', 'sunshine']
    if pwd.lower() in common:
        score = min(score, 20)
        feedback.append("ये COMMON password है! बदलें!")

    # Sequential chars
    seq = '0123456789abcdefghijklmnopqrstuvwxyz'
    for i in range(len(seq) - 3):
        chunk = seq[i:i+4]
        if chunk.lower() in pwd.lower() or chunk[::-1].lower() in pwd.lower():
            score -= 10
            feedback.append("Sequential chars (abcd/1234) न use करें")
            break

    # Repeated chars
    for c in set(pwd):
        if pwd.count(c) > 3:
            score -= 5
            feedback.append(f"'{c}' बहुत बार repeat हुआ है")
            break

    score = max(0, min(100, score))

    # Brute force time estimate
    charset = 0
    if has_lower: charset += 26
    if has_upper: charset += 26
    if has_digit: charset += 10
    if has_special: charset += 32
    combinations = charset ** length
    seconds = combinations / 1e10  # 10 billion guesses/sec

    if seconds < 1:
        crack_time = "तुरंत hack होगा!"
    elif seconds < 3600:
        crack_time = f"{seconds/60:.0f} मिनट"
    elif seconds < 86400:
        crack_time = f"{seconds/3600:.1f} घंटे"
    elif seconds < 31536000:
        crack_time = f"{seconds/86400:.1f} दिन"
    elif seconds < 31536000 * 100:
        crack_time = f"{seconds/31536000:.1f} साल"
    elif seconds < 31536000 * 1e6:
        crack_time = f"{seconds/31536000/1000:.0f} हज़ार साल"
    elif seconds < 31536000 * 1e9:
        crack_time = f"{seconds/31536000/1e6:.0f} मिलियन साल"
    else:
        crack_time = "अरबों साल! 💪"

    # Result
    print(f"\n  {C.BOLD}Score: {score}/100{C.R}")

    # Progress bar
    bar_len = 30
    filled = int(bar_len * score / 100)
    if score >= 80:
        color, label = C.GREEN, "VERY STRONG 💪"
    elif score >= 60:
        color, label = C.CYAN, "STRONG ✅"
    elif score >= 40:
        color, label = C.YELLOW, "MODERATE ⚠️"
    else:
        color, label = C.RED, "WEAK ❌"

    bar = color + "█" * filled + C.DIM + "░" * (bar_len - filled) + C.R
    print(f"  [{bar}]")
    print(f"  {color}{C.BOLD}{label}{C.R}")

    print(f"\n  📏 Length: {length}")
    print(f"  💥 Crack time: {color}{crack_time}{C.R}")
    print(f"  🔢 Combinations: {combinations:.2e}")

    if has_upper: success("Capital letters ✓")
    if has_lower: success("Small letters ✓")
    if has_digit: success("Numbers ✓")
    if has_special: success("Special chars ✓")

    if feedback:
        print(f"\n  {C.YELLOW}💡 सुझाव:{C.R}")
        for f in feedback:
            print(f"     • {f}")

    input(f"\n  {C.DIM}Enter दबाएं...{C.R}")


# ═══════════════════════════════════════════════
#  TOOL 2: PASSWORD GENERATOR
# ═══════════════════════════════════════════════

def password_generator():
    title("🎲 PASSWORD GENERATOR")

    print(f"  {C.BOLD}1.{C.R} WiFi Password (easy to type)")
    print(f"  {C.BOLD}2.{C.R} Strong Password (all chars)")
    print(f"  {C.BOLD}3.{C.R} Memorable Password (words)")
    print(f"  {C.BOLD}4.{C.R} PIN (numbers only)")
    print(f"  {C.BOLD}5.{C.R} Bulk Generate (multiple)")

    choice = input(f"\n  👉 Choice: ").strip()

    if choice == '1':
        # WiFi friendly - no confusing chars
        chars = 'abcdefghjkmnpqrstuvwxyz23456789'
        length = int_input("Length", 16)
        pwd = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
        print(f"\n  🔑 WiFi Password: {C.GREEN}{C.BOLD}{pwd}{C.R}")

    elif choice == '2':
        chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        length = int_input("Length", 20)
        count = int_input("कितने?", 1)
        print()
        for i in range(count):
            pwd = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
            print(f"  🔑 #{i+1}: {C.GREEN}{C.BOLD}{pwd}{C.R}")

    elif choice == '3':
        words = ['tiger', 'moon', 'star', 'cloud', 'river', 'ocean', 'fire',
                 'eagle', 'storm', 'frost', 'shadow', 'thunder', 'dragon',
                 'phoenix', 'crystal', 'diamond', 'neon', 'cyber', 'pixel',
                 'rocket', 'cosmos', 'nova', 'pulse', 'vortex', 'blaze']
        count = int_input("कितने?", 3)
        print()
        for i in range(count):
            w1 = random.choice(words)
            w2 = random.choice(words)
            num = random.randint(10, 99)
            sym = random.choice('!@#$%')
            pwd = f"{w1.capitalize()}{w2.capitalize()}{num}{sym}"
            print(f"  🔑 #{i+1}: {C.GREEN}{C.BOLD}{pwd}{C.R}")

    elif choice == '4':
        length = int_input("PIN length", 6)
        pwd = ''.join(random.SystemRandom().choice(string.digits) for _ in range(length))
        print(f"\n  🔢 PIN: {C.GREEN}{C.BOLD}{pwd}{C.R}")

    elif choice == '5':
        count = int_input("कितने passwords?", 10)
        length = int_input("Length", 16)
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        filename = f"passwords_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            for i in range(count):
                pwd = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
                f.write(pwd + '\n')
                print(f"  🔑 #{i+1}: {pwd}")
        success(f"File saved: {filename}")

    input(f"\n  {C.DIM}Enter दबाएं...{C.R}")


def int_input(prompt, default):
    try:
        val = input(f"  {prompt} [{default}]: ").strip()
        return int(val) if val else default
    except:
        return default


# ═══════════════════════════════════════════════
#  TOOL 3: PASSWORD MANAGER (Encrypted)
# ═══════════════════════════════════════════════

class PasswordManager:
    def __init__(self):
        self.file = ".vault.dat"
        self.key = None
        self.data = {}

    def hash_key(self, master_pwd):
        return hashlib.sha256(master_pwd.encode()).hexdigest()

    def encrypt(self, text, key):
        # Simple XOR encryption (for demo - use real crypto in production)
        key_bytes = bytes.fromhex(key)[:32]
        text_bytes = text.encode()
        encrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_text, key):
        try:
            key_bytes = bytes.fromhex(key)[:32]
            encrypted_bytes = base64.b64decode(encrypted_text)
            decrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(encrypted_bytes)])
            return decrypted.decode()
        except:
            return None

    def load(self, master_pwd):
        self.key = self.hash_key(master_pwd)
        if not os.path.exists(self.file):
            self.save()
            return True
        try:
            with open(self.file, 'r') as f:
                encrypted_data = f.read()
            decrypted = self.decrypt(encrypted_data, self.key)
            if decrypted is None:
                return False
            self.data = json.loads(decrypted)
            return True
        except:
            return False

    def save(self):
        json_str = json.dumps(self.data, indent=2)
        encrypted = self.encrypt(json_str, self.key)
        with open(self.file, 'w') as f:
            f.write(encrypted)

    def add(self):
        title("➕ ADD PASSWORD")
        site = input("  Site/Name: ").strip()
        if not site:
            error("Empty!")
            return
        username = input("  Username: ").strip()
        pwd = getpass.getpass("  Password: ").strip()
        if not pwd:
            error("Empty password!")
            return

        self.data[site] = {
            'username': username,
            'password': pwd,
            'added': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        self.save()
        success(f"'{site}' saved!")

    def view(self):
        title("👁 VIEW PASSWORDS")
        if not self.data:
            info("कोई password नहीं है। पहले add करें।")
            input(f"\n  {C.DIM}Enter...{C.R}")
            return

        print(f"  {'#':<3} {'Site':<20} {'Username':<20} {'Added'}")
        print(f"  {'─'*55}")
        sites = list(self.data.keys())
        for i, site in enumerate(sites, 1):
            d = self.data[site]
            print(f"  {i:<3} {site:<20} {d['username']:<20} {d.get('added','?')}")

        print(f"\n  Total: {len(sites)}")

        choice = input(f"\n  Show password किसका? (number/Enter=skip): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(sites):
            site = sites[int(choice)-1]
            pwd = self.data[site]['password']
            print(f"\n  🔑 {site}: {C.GREEN}{C.BOLD}{pwd}{C.R}")

    def delete(self):
        title("🗑 DELETE PASSWORD")
        if not self.data:
            info("कोई password नहीं है")
            input(f"\n  {C.DIM}Enter...{C.R}")
            return

        for i, site in enumerate(self.data.keys(), 1):
            print(f"  {i}. {site}")
        choice = input("\n  Delete कौन सा? (number): ").strip()
        if choice.isdigit():
            sites = list(self.data.keys())
            if 0 < int(choice) <= len(sites):
                site = sites[int(choice)-1]
                confirm = input(f"  '{site}' delete? (y/n): ").lower()
                if confirm == 'y':
                    del self.data[site]
                    self.save()
                    success(f"'{site}' deleted!")
                    return
        error("Invalid!")

    def edit(self):
        title("✏️ EDIT PASSWORD")
        if not self.data:
            info("कोई password नहीं है")
            input(f"\n  {C.DIM}Enter...{C.R}")
            return

        for i, site in enumerate(self.data.keys(), 1):
            print(f"  {i}. {site}")
        choice = input("\n  Edit कौन सा? (number): ").strip()
        if choice.isdigit():
            sites = list(self.data.keys())
            if 0 < int(choice) <= len(sites):
                site = sites[int(choice)-1]
                print(f"\n  Site: {site}")
                new_user = input(f"  New Username [{self.data[site]['username']}]: ").strip()
                new_pwd = getpass.getpass("  New Password: ").strip()

                if new_user:
                    self.data[site]['username'] = new_user
                if new_pwd:
                    self.data[site]['password'] = new_pwd
                self.data[site]['modified'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                self.save()
                success("Updated!")
                return
        error("Invalid!")

    def search(self):
        title("🔍 SEARCH")
        query = input("  Search: ").strip().lower()
        if not query:
            return
        found = False
        for site, d in self.data.items():
            if query in site.lower() or query in d['username'].lower():
                print(f"\n  📄 {site}")
                print(f"     User: {d['username']}")
                print(f"     Added: {d.get('added','?')}")
                found = True
        if not found:
            warn("नहीं मिला!")

    def generate_and_save(self):
        title("🎲 GENERATE & SAVE")
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        length = int_input("Length", 16)
        site = input("  Site/Name: ").strip()
        if not site:
            error("Empty!")
            return
        pwd = ''.join(random.SystemRandom().choice(chars) for _ in range(length))
        self.data[site] = {
            'username': 'generated',
            'password': pwd,
            'added': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        self.save()
        print(f"\n  🔑 Password: {C.GREEN}{C.BOLD}{pwd}{C.R}")
        success(f"'{site}' में saved!")


def password_manager():
    clear()
    print(f"""
{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════╗
  ║   🗂 PASSWORD MANAGER            ║
  ╚══════════════════════════════════╝
{C.R}""")

    master = getpass.getpass("  🔑 Master Password: ")
    pm = PasswordManager()

    if not pm.load(master):
        error("गलत Master Password!")
        input(f"\n  {C.DIM}Enter...{C.R}")
        return

    success("Vault unlocked!")

    while True:
        print(f"""
  {C.BOLD}1.{C.R} ➕ Add password
  {C.BOLD}2.{C.R} 👁  View all
  {C.BOLD}3.{C.R} ✏️  Edit
  {C.BOLD}4.{C.R} 🗑  Delete
  {C.BOLD}5.{C.R} 🔍 Search
  {C.BOLD}6.{C.R} 🎲 Generate & save
  {C.BOLD}7.{C.R} ⬅️  Lock & Exit
""")
        choice = input("  👉 Choice: ").strip()
        clear()

        if choice == '1': pm.add()
        elif choice == '2': pm.view()
        elif choice == '3': pm.edit()
        elif choice == '4': pm.delete()
        elif choice == '5': pm.search()
        elif choice == '6': pm.generate_and_save()
        elif choice == '7':
            success("Vault locked!")
            time.sleep(1)
            return
        else:
            error("Invalid choice!")

        input(f"\n  {C.DIM}Enter दबाएं...{C.R}")
        clear()


# ═══════════════════════════════════════════════
#  TOOL 4: NETWORK INFO TOOL
# ═══════════════════════════════════════════════

def network_info():
    title("📶 NETWORK INFO")

    print(f"  {C.BOLD}1.{C.R} 📱 Device Info (local)")
    print(f"  {C.BOLD}2.{C.R} 🌐 Public IP & Location")
    print(f"  {C.BOLD}3.{C.R} 📋 Network Interfaces")
    print(f"  {C.BOLD}4.{C.R} 🏓 Ping Test")

    choice = input(f"\n  👉 Choice: ").strip()

    if choice == '1':
        print(f"\n  {C.BOLD}📱 Device Information:{C.R}")
        print(f"  {'─'*40}")
        print(f"  💻 OS: {sys.platform}")
        print(f"  🐍 Python: {sys.version.split()[0]}")
        print(f"  📂 CWD: {os.getcwd()}")
        print(f"  👤 User: {os.environ.get('USER', os.environ.get('USERNAME', 'unknown'))}")
        print(f"  🏠 Home: {os.environ.get('HOME', os.environ.get('USERPROFILE', 'unknown'))}")

        # MAC address (Termux/Linux)
        if os.path.exists('/sys/class/net'):
            try:
                interfaces = os.listdir('/sys/class/net')
                for iface in interfaces:
                    mac_file = f'/sys/class/net/{iface}/address'
                    if os.path.exists(mac_file):
                        with open(mac_file, 'r') as f:
                            mac = f.read().strip()
                        print(f"  🔌 {iface}: {mac}")
            except: pass

    elif choice == '2':
        info("Public IP fetch हो रहा है...")
        try:
            import urllib.request
            import urllib.error

            # Get public IP
            response = urllib.request.urlopen('https://api.ipify.org', timeout=5)
            public_ip = response.read().decode()
            print(f"\n  🌐 Public IP: {C.GREEN}{C.BOLD}{public_ip}{C.R}")

            # Get location info
            try:
                response = urllib.request.urlopen(f'http://ip-api.com/json/{public_ip}', timeout=5)
                data = json.loads(response.read().decode())
                if data.get('status') == 'success':
                    print(f"  🌍 Country: {data.get('country', '?')}")
                    print(f"  🏙️  City: {data.get('city', '?')}")
                    print(f"  🕐 Timezone: {data.get('timezone', '?')}")
                    print(f"  🏢 ISP: {data.get('isp', '?')}")
            except:
                warn("Location info नहीं मिली")

        except Exception as e:
            error(f"Internet नहीं चल रहा: {e}")

    elif choice == '3':
        print(f"\n  {C.BOLD}📋 Network Interfaces:{C.R}")
        if os.path.exists('/sys/class/net'):
            interfaces = os.listdir('/sys/class/net')
            for iface in sorted(interfaces):
                mac_file = f'/sys/class/net/{iface}/address'
                status_file = f'/sys/class/net/{iface}/operstate'
                mac = "?"
                status = "?"
                if os.path.exists(mac_file):
                    with open(mac_file) as f: mac = f.read().strip()
                if os.path.exists(status_file):
                    with open(status_file) as f: status = f.read().strip()
                status_icon = "🟢" if status == 'up' else "🔴"
                print(f"\n  {status_icon} {iface}")
                print(f"     Status: {status}")
                print(f"     MAC: {mac}")
        else:
            warn("सिर्फ Termux/Linux पर काम करता है")

    elif choice == '4':
        host = input("  Ping किसे? [google.com]: ").strip() or "google.com"
        count = int_input("कितनी बार?", 4)
        info(f"{host} को ping कर रहा हूं...")
        os.system(f'ping -c {count} {host}' if os.name != 'nt' else f'ping -n {count} {host}')

    input(f"\n  {C.DIM}Enter दबाएं...{C.R}")


# ═══════════════════════════════════════════════
#  TOOL 5: SECURITY EDUCATION
# ═══════════════════════════════════════════════

def security_education():
    title("📚 WiFi SECURITY EDUCATION")

    print(f"""  {C.BOLD}1.{C.R} 🔐 WiFi Security Types
  {C.BOLD}2.{C.R} 🛡️  अपना WiFi Secure कैसे करें
  {C.BOLD}3.{C.R} ⚔️  Common Attacks & Protection
  {C.BOLD}4.{C.R} 📱 Phone Security Tips
  {C.BOLD}5.{C.R} 🔑 Password Best Practices
""")

    choice = input("  👉 Choice: ").strip()
    clear()

    if choice == '1':
        title("🔐 WiFi Security Types")
        print(f"""  {C.CYAN}{C.BOLD}WEP (Wired Equivalent Privacy){C.R}
  📅 साल: 1997
  🔒 Security: {C.RED}बहुत कमजोर - DON'T USE!{C.R}
  ⚡ Crack time: कुछ मिनटों में
  📌 ये पुराना है, आज इस्तेमाल न करें

  {C.CYAN}{C.BOLD}WPA (WiFi Protected Access){C.R}
  📅 साल: 2003
  🔒 Security: {C.YELLOW}बेहतर, फिर भी पुराना{C.R}
  ⚡ Crack time: घंटों-दिनों में
  📌 WPA2 use करें इसकी जगह

  {C.CYAN}{C.BOLD}WPA2 (Most Common){C.R}
  📅 साल: 2004
  🔒 Security: {C.GREEN}अच्छा - अभी भी ठीक है{C.R}
  ⚡ Crack time: सालों लगेंगे (strong password हो तो)
  📌 ज़्यादातर routers में default है

  {C.CYAN}{C.BOLD}WPA3 (Latest){C.R}
  📅 साल: 2018
  🔒 Security: {C.GREEN}{C.BOLD}BEST! सबसे secure{C.R}
  ⚡ Crack लगभग impossible
  📌 नए routers में मिलता है

  {C.MAGENTA}💡 Recommendation: हमेशा WPA3 या WPA2 use करें{C.R}
""")

    elif choice == '2':
        title("🛡️ WiFi Secure कैसे करें")
        print(f"""  {C.BOLD}1. Strong Password रखें{C.R}
     • कम से कम 16 characters
     • Capital + small + numbers + symbols
     • अपना नाम/phone number न रखें

  {C.BOLD}2. WPA3 या WPA2 use करें{C.R}
     • Router settings में जाएं
     • WEP कभी न चुनें

  {C.BOLD}3. Default password बदलें{C.R}
     • Router का admin password भी बदलें
     • "admin/admin" न रखें

  {C.BOLD}4. WPS Disable करें{C.R}
     • WPS button से hack हो सकता है
     • Router settings में बंद करें

  {C.BOLD}5. Router Firmware Update{C.R}
     • Regular updates install करें

  {C.BOLD}6. Guest Network{C.R}
     • दूसरों को अलग guest network दें
     • Main network का password share न करें

  {C.BOLD}7. SSID Broadcasting{C.R}
     • SSID hide करना optional है
     • Security नहीं बढ़ाता, लेकिन discovery मुश्किल
""")

    elif choice == '3':
        title("⚔️ Common Attacks & Protection")
        print(f"""  {C.RED}{C.BOLD}1. Brute Force Attack{C.R}
     💥 हर possible password try करना
     🛡️  Protection: Long + complex password

  {C.RED}{C.BOLD}2. Dictionary Attack{C.R}
     💥 Common words list से try करना
     🛡️  Protection: Real words use न करें

  {C.RED}{C.BOLD}3. Man-in-the-Middle (MITM){C.R}
     💥 Network के बीच में आकर data चुराना
     🛡️  Protection: HTTPS use करें, VPN

  {C.RED}{C.BOLD}4. Evil Twin{C.R}
     💥 Fake WiFi hotspot बनाना
     🛡️  Protection: Unknown WiFi से connect न हों

  {C.RED}{C.BOLD}5. Packet Sniffing{C.R}
     💥 Network traffic capture करना
     🛡️  Protection: HTTPS, VPN use करें

  {C.RED}{C.BOLD}6. Deauth Attack{C.R}
     💥 WiFi से disconnect करना
     🛡️  Protection: WPA3, strong signal

  {C.GREEN}💡 सबसे बड़ा protection: STRONG PASSWORD{C.R}
""")

    elif choice == '4':
        title("📱 Phone Security Tips")
        print(f"""  {C.BOLD}🔒 Basic Security:{C.R}
  • Screen lock लगाएं (PIN/pattern/fingerprint)
  • अपने phone का IMEI number note करें
  • Find My Device ON रखें

  {C.BOLD}🌐 WiFi Safety:{C.R}
  • Public WiFi पर banking न करें
  • Unknown WiFi से connect न हों
  • VPN use करें (public WiFi पर)

  {C.BOLD}📱 Apps:{C.R}
  • सिर्फ Play Store/App Store से download करें
  • App permissions check करें
  • Unknown apps install न करें

  {C.BOLD}💬 Messages:{C.R}
  • Unknown links पर click न करें
  • OTP किसी को share न करें
  • "आप जीते हैं" वाले messages = FAKE

  {C.BOLD}🏦 Banking:{C.R}
  • Official banking apps ही use करें
  • Never share PIN/OTP
  • Transaction alerts ON रखें
""")

    elif choice == '5':
        title("🔑 Password Best Practices")
        print(f"""  {C.GREEN}{C.BOLD}✅ DO:{C.R}
  • हर site का अलग password
  • Password manager use करें
  • 2FA (Two-Factor Auth) ON करें
  • कम से कम 12-16 characters
  • Mix of capital/small/numbers/symbols
  • Passphrase use करें (e.g., "MyDog$Runs2024!")
  • Regular में password बदलें (हर 6 महीने)

  {C.RED}{C.BOLD}❌ DON'T:{C.R}
  • "password123", "12345678" use न करें
  • अपना नाम/birthdate use न करें
  • सब जगह same password न रखें
  • Password notes में save न करें
  • Chat में password share न करें
  • Easy patterns (qwerty, abc123) न use करें

  {C.CYAN}{C.BOLD}💡 Strong Password Formula:{C.R}
  Word + Symbol + Number + Word

  Example: Blue@Monkey42Rain
  • Blue = random word
  • @ = symbol
  • 42 = random number
  • Rain = another word

  याद रखने में easy, crack करने में मुश्किल! 💪
""")

    input(f"\n  {C.DIM}Enter दबाएं...{C.R}")


# ═══════════════════════════════════════════════
#  MAIN MENU
# ═══════════════════════════════════════════════

def main():
    while True:
        clear()
        print(f"""
{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════╗
  ║                                          ║
  ║        🔐 SECURITY TOOLKIT v1.0         ║
  ║                                          ║
  ║     Termux & PC के लिए Complete Kit      ║
  ║                                          ║
  ╠══════════════════════════════════════════╣
  ║                                          ║
  ║   1. 🔐 Password Strength Checker        ║
  ║   2. 🎲 Password Generator               ║
  ║   3. 🗂  Password Manager (Vault)        ║
  ║   4. 📶 Network Info Tool                ║
  ║   5. 📚 Security Education               ║
  ║   6. ℹ️  About                           ║
  ║   0. 🚪 Exit                             ║
  ║                                          ║
  ╚══════════════════════════════════════════╝
{C.R}""")

        choice = input(f"  👉 Choice: ").strip()
        clear()

        if choice == '1':
            password_strength()
        elif choice == '2':
            password_generator()
        elif choice == '3':
            password_manager()
        elif choice == '4':
            network_info()
        elif choice == '5':
            security_education()
        elif choice == '6':
            title("ℹ️ ABOUT")
            print(f"""  📦 Tool: Security Toolkit
  🏷 Version: 1.0
  🐍 Python: {sys.version.split()[0]}
  💻 Platform: {sys.platform}

  ⚠️  यह tool सिर्फ EDUCATIONAL purpose के लिए है।
  अपनी security improve करने के लिए use करें।

  📜 Legal: किसी के network/system को
  unauthorized access करना cyber crime है।
""")
            input(f"  {C.DIM}Enter...{C.R}")
        elif choice == '0':
            clear()
            print(f"\n  {C.GREEN}👋 Stay Safe! Stay Secure!{C.R}\n")
            time.sleep(1)
            break
        else:
            error("Invalid choice!")
            time.sleep(0.5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}👋 Interrupted! Bye!{C.R}\n")
        sys.exit(0)
