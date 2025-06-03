import socket
import requests
import os
import csv
from datetime import datetime

def get_ip_address():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        public_ip = requests.get("https://api64.ipify.org?format=json", timeout=3).json().get("ip", "Unknown")
        return hostname, local_ip, public_ip
    except Exception as e:
        print(f"Error getting IP: {e}")
        return "Unknown", "Unknown", "Unknown"

def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        data = response.json()
        return data.get("country", "Unknown")
    except Exception as e:
        print(f"Error getting location: {e}")
        return "Unknown"

def log_interaction(query, answer, log_file="query_logs.csv"):
    hostname, local_ip, public_ip = get_ip_address()
    country = get_location(public_ip)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_data = [timestamp, hostname, local_ip, public_ip, country, query, answer]
    header = ["Timestamp", "Hostname", "Local IP", "Public IP", "Country", "Query", "Answer"]

    if not os.path.exists(log_file):
        with open(log_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
    with open(log_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(log_data)
