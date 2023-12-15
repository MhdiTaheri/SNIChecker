import socket
import subprocess
from tabulate import tabulate
import os
from colorama import init, Fore, Style
import time

init()

HEADER_STYLE = f"{Fore.YELLOW}"
ERROR_STYLE = f"{Fore.RED}"
INFO_STYLE = f"{Fore.GREEN}"

def create_default_snis_file():
    default_snis = ["github.com", "google.com"]
    with open("snis.txt", "w") as file:
        file.write('\n'.join(default_snis) + '\n')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_sni_ping(sni):
    try:
        ip = socket.gethostbyname(sni)
        if ip:
            ping_process = subprocess.Popen(["ping", "-c", "4", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            ping_output, _ = ping_process.communicate()
            ping_output_lines = ping_output.splitlines()
            if ping_output_lines:
                avg_ping_line = [line for line in ping_output_lines if "rtt" in line]
                if avg_ping_line:
                    avg_ping = avg_ping_line[0].split('=')[1].split('/')[1]
                    return [sni, f"{avg_ping} ms"]

    except (socket.gaierror, subprocess.CalledProcessError) as e:
        return [sni, f"{ERROR_STYLE}Unable to resolve or ping: {e}" + Style.RESET_ALL]

    return [sni, f"{ERROR_STYLE}Unable to resolve or ping" + Style.RESET_ALL]

def find_sni(sni_list):
    clear_screen()
    print(HEADER_STYLE + r"""
 __  __ _         _ _   _____     _               _   ____  _   _ ___    ____ _               _             
|  \/  | |__   __| (_) |_   _|_ _| |__   ___ _ __(_) / ___|| \ | |_ _|  / ___| |__   ___  ___| | _____ _ __ 
| |\/| | '_ \ / _` | |   | |/ _` | '_ \ / _ \ '__| | \___ \|  \| || |  | |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |  | | | | | (_| | |   | | (_| | | | |  __/ |  | |  ___) | |\  || |  | |___| | | |  __/ (__|   <  __/ |   
|_|  |_|_| |_|\__,_|_|   |_|\__,_|_| |_|\___|_|  |_| |____/|_| \_|___|  \____|_| |_|\___|\___|_|\_\___|_|            
""" + Style.RESET_ALL)

    animation = "|/-\\"
    for i in range(20):
        time.sleep(0.1)
        print(INFO_STYLE + f"Testing, please wait... {animation[i % len(animation)]}" + Style.RESET_ALL, end="\r")

    results = []
    for sni in sni_list:
        ping_result = check_sni_ping(sni)
        results.append(ping_result)

    print("\n")
    print(tabulate(results, headers=["SNI", "Average Ping"], tablefmt="pretty"))

def add_sni(existing_sni_list):
    try:
        snis = input("Enter SNIs separated by commas: ")
        new_snis = [sni.strip() for sni in snis.split(',')]
        existing_sni_list.extend(new_snis)
        with open("snis.txt", "a") as file:
            file.write('\n'.join(new_snis) + '\n')
        return existing_sni_list
    except Exception as e:
        print(ERROR_STYLE + f"Error occurred: {e}" + Style.RESET_ALL)
        return existing_sni_list

def load_sni_list():
    if not os.path.exists("snis.txt"):
        create_default_snis_file()

    with open("snis.txt", "r") as file:
        sni_list = file.read().splitlines()
    return sni_list

def show_menu():
    while True:
        clear_screen()
        print(HEADER_STYLE + r"""
  ____            _             _   ____                  _ 
 / ___|___  _ __ | |_ _ __ ___ | | |  _ \ __ _ _ __   ___| |
| |   / _ \| '_ \| __| '__/ _ \| | | |_) / _` | '_ \ / _ \ |
| |__| (_) | | | | |_| | | (_) | | |  __/ (_| | | | |  __/ |
 \____\___/|_| |_|\__|_|  \___/|_| |_|   \__,_|_| |_|\___|_|
""" + Style.RESET_ALL)
        print(f"{INFO_STYLE}[ 1 ]{Style.RESET_ALL} : Check SNI")
        print(f"{INFO_STYLE}[ 2 ]{Style.RESET_ALL} : Add SNI")
        print(f"{INFO_STYLE}[ q ]{Style.RESET_ALL} : Quit")
        choice = input("Enter your choice (1, 2, or q): ")

        if choice in ['1', '2', 'q']:
            return choice
        else:
            print(ERROR_STYLE + "Invalid choice. Please choose 1, 2, or q." + Style.RESET_ALL)
            input("Press Enter to continue...")

if __name__ == "__main__":
    sni_list = load_sni_list()
    try:
        while True:
            choice = show_menu()
            if choice == '1':
                find_sni(sni_list)
            elif choice == '2':
                sni_list = add_sni(sni_list)
                print("Added SNIs successfully!")
            elif choice.lower() == 'q':
                break
            else:
                print(ERROR_STYLE + "Invalid choice. Please choose 1, 2, or q." + Style.RESET_ALL)

            input("Press Enter to continue...")
    except KeyboardInterrupt:
        clear_screen()
        print(ERROR_STYLE + "Have a good day! Bye." + Style.RESET_ALL)
