import os
import time
import requests
import zipfile
import tarfile
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from stem.control import Controller
from stem import Signal
import colorama

# Initialize colorama
colorama.init()

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TOR_DIR = os.path.join(BASE_DIR, "tor")
GECKO_DIR = os.path.join(BASE_DIR, "geckodriver")
GECKO_BINARY = os.path.join(GECKO_DIR, "geckodriver.exe")

# Tor settings
TOR_SOCKS_PROXY = "127.0.0.1:9050"
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = ""

# Direct Download URLs for Windows
TOR_WINDOWS_URL = "https://archive.torproject.org/tor-package-archive/torbrowser/14.0.6/tor-expert-bundle-windows-x86_64-14.0.6.tar.gz"
GECKO_WINDOWS_URL = "https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.35.0-win64.zip"

# UI Styles
RESET = colorama.Fore.RESET
INFO = colorama.Fore.CYAN + "[INFO]" + RESET
SUCCESS = colorama.Fore.GREEN + "[SUCCESS]" + RESET
ERROR = colorama.Fore.RED + "[ERROR]" + RESET
ACTION = colorama.Fore.YELLOW + "[ACTION]" + RESET

# User settings
print(f"\n{INFO} Welcome to the Tor IP Changer\n" + "=" * 50)
CHANGE_INTERVAL = int(input(f"{ACTION} Enter seconds between IP changes: "))
CHANGE_LIMIT = int(input(f"{ACTION} Enter how many times to change IP (0 for unlimited): "))
print("=" * 50 + "\n")

def is_tor_running():
    """Check if Tor is running by trying to connect to the SOCKS proxy."""
    try:
        response = requests.get("http://check.torproject.org", proxies={"http": f"socks5h://{TOR_SOCKS_PROXY}", "https": f"socks5h://{TOR_SOCKS_PROXY}"}, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def start_tor():
    """Ensure Tor is running before launching Firefox."""
    tor_executable = os.path.join(TOR_DIR, "tor.exe")

    if not os.path.exists(tor_executable):
        print(f"{ERROR} Tor binary not found! Please check the installation.")
        exit(1)

    print(f"{INFO} Starting Tor... ", end="", flush=True)
    tor_process = subprocess.Popen(
        [tor_executable, "--SocksPort", "9050", "--ControlPort", "9051"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for Tor to start with an animated loading effect
    for _ in range(15):
        if is_tor_running():
            print(f"\r{SUCCESS} Tor is running!            ")
            return tor_process
        print(".", end="", flush=True)
        time.sleep(2)

    print(f"\n{ERROR} Tor failed to start!")
    exit(1)

def set_firefox_tor():
    """Configure Firefox to use Tor's SOCKS5 proxy."""
    options = Options()
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", "127.0.0.1")
    options.set_preference("network.proxy.socks_port", 9050)
    options.set_preference("network.proxy.socks_version", 5)
    options.set_preference("network.proxy.socks_remote_dns", True)
    return options

def get_current_ip():
    """Get the current IP using Tor without opening a browser."""
    try:
        response = requests.get("http://check.torproject.org/api/ip", proxies={"http": f"socks5h://{TOR_SOCKS_PROXY}", "https": f"socks5h://{TOR_SOCKS_PROXY}"}, timeout=5)
        return response.text.strip()
    except requests.RequestException:
        return "Unable to retrieve IP"

def browse_tor():
    """Open Firefox through Tor only once to verify the first connection."""
    print(f"{INFO} Opening Firefox for initial verification...")
    options = set_firefox_tor()
    service = FirefoxService(GECKO_BINARY)

    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        driver.get("https://check.torproject.org/")  # Verify Tor usage
        time.sleep(5)
    finally:
        driver.quit()
    print(f"{SUCCESS} Verified Tor connection in Firefox!\n")

def change_tor_identity():
    """Request a new Tor identity and display new IP."""
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)
            time.sleep(3)  # Wait for a new identity to be assigned
            new_ip = get_current_ip()
            print(f"{SUCCESS} New Tor IP: {colorama.Fore.MAGENTA}{new_ip}{RESET}")
    except Exception as e:
        print(f"{ERROR} Error changing Tor identity: {e}")

def ip_changer():
    """Continuously change IP based on user settings."""
    count = 0
    browse_tor()  # Open Firefox only once on the first check
    print(f"{SUCCESS} Initial Tor IP: {colorama.Fore.MAGENTA}{get_current_ip()}{RESET}\n")

    while CHANGE_LIMIT == 0 or count < CHANGE_LIMIT:
        change_tor_identity()
        count += 1
        print(f"{INFO} IP changed {count} times. Waiting {CHANGE_INTERVAL} seconds...\n")
        time.sleep(CHANGE_INTERVAL)  # Wait for the user-defined interval

# **Main Execution**
if __name__ == "__main__":
    tor_process = start_tor()
    ip_changer()
    tor_process.terminate()
    print(f"{SUCCESS} Tor process terminated. Exiting...")
