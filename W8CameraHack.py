import socket
import requests
import threading
from queue import Queue
import ipaddress
from colorama import Fore, Style
import pyfiglet
from datetime import datetime
import html
import time  # Add this line to import the time module
import os
from tqdm import tqdm

# Set a default timeout for socket connections
socket.setdefaulttimeout(0.25)

# Function to get the public IP address
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"

# Function to get the country based on IP address
def get_country(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        if response.status_code == 200:
            data = response.json()
            return data.get('country', 'Unknown')
        else:
            return "Unknown"
    except Exception as e:
        return "Unknown"

# Function to scan a specific IP and port
def scan(ip, port, results_file=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
            response = sock.recv(4096).decode(errors='ignore')
            if 'HTTP' in response and '<title>WEB SERVICE</title>' in response:
                # Banner grabbing and fingerprinting
                brand = None
                # Check Server header
                server_header = None
                for line in response.split('\r\n'):
                    if line.lower().startswith('server:'):
                        server_header = line.split(':', 1)[1].strip()
                        break
                # Check WWW-Authenticate header
                auth_header = None
                for line in response.split('\r\n'):
                    if line.lower().startswith('www-authenticate:'):
                        auth_header = line.split(':', 1)[1].strip()
                        break
                # Known patterns (expand as needed)
                patterns = [
                    ("Dahua", ["dahua", "DH-", "DVRDVS-Webs"], [server_header, auth_header, response]),
                    ("Hikvision", ["hikvision", "HIKVISION", "App-webs"], [server_header, auth_header, response]),
                    ("Axis", ["axis", "AXIS"], [server_header, auth_header, response]),
                    ("TP-Link", ["tp-link", "TP-LINK"], [server_header, auth_header, response]),
                    ("Foscam", ["foscam", "FOSCAM"], [server_header, auth_header, response]),
                    ("Provision", ["provision", "Provision"], [server_header, auth_header, response]),
                    ("Milesight", ["milesight", "Milesight"], [server_header, auth_header, response]),
                    ("UNV", ["uniview", "UNV"], [server_header, auth_header, response]),
                    ("Generic", ["webcam", "ip camera", "network camera"], [response]),
                ]
                for brand_name, keywords, sources in patterns:
                    for src in sources:
                        if src:
                            for kw in keywords:
                                if kw.lower() in src.lower():
                                    brand = brand_name
                                    break
                        if brand:
                            break
                    if brand:
                        break
                if port == 8080:
                    cam_url = f"http://{ip}:{port}"
                else:
                    cam_url = f"http://{ip}"
                if brand:
                    msg = f"Camera Found: {cam_url} | Brand: {brand}"
                else:
                    msg = f"Camera Found: {cam_url}"
                print(msg)
                # Live save to file, avoid duplicates
                try:
                    with open('cameras_found.txt', 'r') as f:
                        if cam_url in f.read():
                            return True
                except FileNotFoundError:
                    pass
                with open('cameras_found.txt', 'a') as f:
                    f.write(msg + "\n")
                return True
    except Exception as e:
        pass
    return False

# Function to execute the scan from the queue
def execute(queue, results_file=None, pbar=None, status=None):
    while True:
        ip, port = queue.get()
        # Update current IP/port in status dict
        if status is not None:
            status['current_ip'] = ip
            status['current_port'] = port
        found = scan(ip, port, results_file)
        if status is not None and found:
            status['success_count'] += 1
        if pbar:
            pbar.update(1)
        queue.task_done()

# Function to generate a range of IP addresses
def generate_ip_range(start_ip, end_ip):
    start = int(ipaddress.IPv4Address(start_ip))
    end = int(ipaddress.IPv4Address(end_ip))
    for ip_int in range(start, end + 1):
        yield str(ipaddress.IPv4Address(ip_int))

# Function to print the logo with public IP, country, and timestamp
def print_logo():
    green_code = "\033[32m"  # Green
    yellow_code = "\033[33m"  # Yellow
    reset_code = "\033[0m"   # Reset

    logo = pyfiglet.figlet_format("W8Team", font="slant")
    logo_lines = logo.split('\n')
    logo_width = len(logo_lines[0])
    bordered_logo = f"{green_code}+{'-' * (logo_width + 2)}+{reset_code}\n"
    for idx, line in enumerate(logo_lines):
        if idx == 0:
            bordered_logo += f"{green_code}| {line}{' ' * (logo_width - len(line))} {yellow_code}{get_public_ip()} - {get_country(get_public_ip())} - {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')} |{reset_code}\n"
        else:
            bordered_logo += f"{green_code}| {line}{' ' * (logo_width - len(line))}{' ' * (logo_width - len(line))} |{reset_code}\n"
    bordered_logo += f"{green_code}+{'-' * (logo_width + 2)}+{reset_code}\n"
    print(bordered_logo)

# Function to run the tool
def run_tool(start_ip=None, end_ip=None, ip_list=None, fast_mode=False, single_ip=None, results_file_path=None, max_threads=None, custom_targets=None):
    print_logo()
    if max_threads is not None:
        thread_count = max_threads
    elif fast_mode:
        thread_count = 300
        socket.setdefaulttimeout(0.1)
    else:
        thread_count = 100
        socket.setdefaulttimeout(0.25)
    if fast_mode:
        socket.setdefaulttimeout(0.1)
    else:
        socket.setdefaulttimeout(0.25)

    queue = Queue()
    start_time = time.time()

    results_file = open(results_file_path, 'a') if results_file_path else None

    # Prepare list of all (ip, port) pairs to scan
    if custom_targets is not None:
        targets = custom_targets
    else:
        targets = []
        if single_ip:
            targets.append((single_ip, 80))
            targets.append((single_ip, 8080))
        elif ip_list:
            for ip in ip_list:
                targets.append((ip, 80))
                targets.append((ip, 8080))
        elif start_ip and end_ip:
            for ip in generate_ip_range(start_ip, end_ip):
                targets.append((ip, 80))
                targets.append((ip, 8080))
        else:
            print("No valid IP input provided.")
            if results_file:
                results_file.close()
            return

    status = {'current_ip': '', 'current_port': '', 'success_count': 0}

    def pbar_format():
        elapsed = time.time() - start_time
        # tqdm will estimate remaining time
        return (
            f"IP: {status['current_ip']}  Port: {status['current_port']}  "
            f"Found: {status['success_count']}  "
            f"Elapsed: {int(elapsed)}s"
        )

    pbar = tqdm(
        total=len(targets),
        desc="Scanning",
        ncols=100,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt} {elapsed}<{remaining}] {postfix}",
        postfix=pbar_format()
    )

    # Create worker threads
    for _ in range(thread_count):
        thread = threading.Thread(target=execute, args=(queue, results_file, pbar, status))
        thread.daemon = True
        thread.start()

    # Enqueue all targets
    for t in targets:
        queue.put(t)

    # Update progress bar with current info
    while pbar.n < pbar.total:
        pbar.set_postfix_str(pbar_format())
        time.sleep(0.2)

    # Wait for all tasks to complete
    queue.join()
    pbar.set_postfix_str(pbar_format())
    pbar.close()

    elapsed_time = time.time() - start_time
    print(f'Time taken: {elapsed_time:.2f} seconds')
    if results_file:
        results_file.close()
        print(f"Results saved to {results_file_path}")

def main_menu():
    while True:
        # Ask for max threads at the start of each run
        try:
            max_threads = int(input("Enter max threads (default 300): ") or "300")
            if max_threads < 1:
                print("Max threads must be at least 1. Using default 300.")
                max_threads = 300
        except Exception:
            print("Invalid input. Using default 300.")
            max_threads = 300

        print("\nSelect scan mode:")
        print("1. Fast Scan (IP Range, more threads)")
        print("2. IPs from StartIP.txt to EndIP.txt")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            start_ip = input('Start IP Address: ')
            end_ip = input('End IP Address: ')
            run_tool(start_ip=start_ip, end_ip=end_ip, fast_mode=True, results_file_path='cameras_found.txt', max_threads=max_threads)
        elif choice == '2':
            start_ip_file = 'StartIP.txt'
            end_ip_file = 'EndIP.txt'
            created = False
            if not os.path.exists(start_ip_file):
                with open(start_ip_file, 'w') as f:
                    f.write('')
                print(f"Created {start_ip_file}. Please enter the start IP in this file and rerun the scan.")
                created = True
            if not os.path.exists(end_ip_file):
                with open(end_ip_file, 'w') as f:
                    f.write('')
                print(f"Created {end_ip_file}. Please enter the end IP in this file and rerun the scan.")
                created = True
            if created:
                return
            with open(start_ip_file, 'r') as f:
                start_ips = [line.strip() for line in f if line.strip()]
            with open(end_ip_file, 'r') as f:
                end_ips = [line.strip() for line in f if line.strip()]
            if not start_ips or not end_ips:
                print(f"Please make sure both {start_ip_file} and {end_ip_file} contain valid IP addresses.")
                return
            if len(start_ips) != len(end_ips):
                print(f"Error: {start_ip_file} and {end_ip_file} must have the same number of lines (ranges).")
                return
            # Collect all targets from all ranges
            all_targets = []
            for start_ip, end_ip in zip(start_ips, end_ips):
                for ip in generate_ip_range(start_ip, end_ip):
                    all_targets.append((ip, 80))
                    all_targets.append((ip, 8080))
            print(f"Scanning {len(all_targets)//2} IPs across {len(start_ips)} ranges...")
            run_tool(ip_list=None, fast_mode=True, results_file_path='cameras_found.txt', max_threads=max_threads, custom_targets=all_targets)
        elif choice == '0':
            print('Exiting.')
            print('Thank You For Using This Tool. Made By @W8SOJIB')
            break
        else:
            print('Invalid choice. Try again.')

if __name__ == "__main__":
    try:
        main_menu()
    except (KeyboardInterrupt, SystemExit):
        print('\nThank You For Using This Tool. Made By @W8SOJIB')
        exit(0)
