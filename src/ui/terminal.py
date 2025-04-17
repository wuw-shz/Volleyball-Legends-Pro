import os
import re
import time
import main
import logging
import requests
from typing import Optional
from unittest.mock import patch

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

IPINFO_API_URL = "https://ipinfo.io/"
IP_API_URL = "http://ip-api.com/json/"

last_ip: Optional[str] = None
cached_geo_info: Optional[str] = None
last_geo_info: Optional[str] = "Fetching geolocation info..."

def start() -> None:
    # threading.Thread(target=geo_updater, daemon=True).start()
    terminal_ui_loop()

def terminal_ui_loop() -> None:
    while True:
        os.system("cls")
        print("( Volleyball Legends Pro )\n")
        print(f"Ping value: {main.PING}ms")
        # print(last_geo_info)
        user_input = input("Enter new ping value in ms: ").strip()

        if user_input:
            try:
                main.PING = int(user_input)
            except ValueError:
                print("\nInvalid input. Please enter a valid number.")
                time.sleep(1)
        time.sleep(0.2)

def geo_updater() -> None:
    global last_ip, cached_geo_info, last_geo_info
    while True:
        new_geo_info = get_geolocation_info()
        if new_geo_info != last_geo_info:
            last_geo_info = new_geo_info
            patch("builtins.input", return_value="")
        time.sleep(1)

def get_geolocation_info() -> str:
    global last_ip, cached_geo_info
    try:
        local_appdata = os.getenv("LOCALAPPDATA")
        if not local_appdata:
            return "LOCALAPPDATA not found."
        log_dir = os.path.join(local_appdata, "Roblox", "logs")
        if not os.path.isdir(log_dir):
            return "Log directory not found."
        files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if "player" in f.lower()]
        if not files:
            return "No matching log files found."
        files.sort(key=lambda x: os.path.getctime(x), reverse=True)
        latest_log = files[0]
        with open(latest_log, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
        matches = re.findall(r"UDMUX Address = ([0-9\.]+)", content)
        if not matches:
            return "No IP address found in log."
        
        ip_address = matches[-1]
        if ip_address == last_ip and cached_geo_info is not None:
            return cached_geo_info

        response = requests.get(f"{IPINFO_API_URL}{ip_address}/json")
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                logging.info("ipinfo.io error encountered, falling back to ip-api.com")
                return fallback_to_ip_api(ip_address)
            else:
                city = data.get("city", "Unknown")
                region = data.get("region", "Unknown")
                country = data.get("country", "Unknown")
                geo_info = f"IP: {ip_address} | {city}, {region}, {country}"
                last_ip = ip_address
                cached_geo_info = geo_info
                return geo_info
        elif response.status_code == 429:
            logging.info("ipinfo.io rate limit reached, falling back to ip-api.com")
            return fallback_to_ip_api(ip_address)
        else:
            logging.info(f"ipinfo.io returned status code {response.status_code}, falling back to ip-api.com")
            return fallback_to_ip_api(ip_address)
    except Exception as e:
        logging.exception("Exception in get_geolocation_info:")
        return f"Error in get_geolocation_info: {e}"

def fallback_to_ip_api(ip_address: str) -> str:
    global last_ip, cached_geo_info
    try:
        response = requests.get(f"{IP_API_URL}{ip_address}")
        if response.status_code != 200:
            return f"Error querying ip-api.com: {response.status_code}"
        data = response.json()
        if data.get("status") != "success":
            return f"Error in ip-api response: {data.get('message', 'Unknown error')}"
        city = data.get("city", "Unknown")
        region = data.get("regionName", "Unknown")
        country = data.get("country", "Unknown")
        geo_info = f"IP: {ip_address} | {city}, {region}, {country}"
        last_ip = ip_address
        cached_geo_info = geo_info
        return geo_info
    except Exception as e:
        logging.exception("Exception in fallback_to_ip_api:")
        return f"Error in fallback_to_ip_api: {e}"
