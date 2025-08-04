import requests
import ipaddress
import time
import sys
import os

# --- ANSI Styles ---
RESET = "\033[0m"
REVERSE = "\033[7m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"

# --- HxTAYEFI Purple Theme Colors ---
DEEP_PURPLE = "\033[38;2;102;0;153m"
LIGHT_PURPLE = "\033[38;2;127;0;255m"
VIBRANT_PURPLE = "\033[38;2;178;102;255m"
MEDIUM_GRAY = "\033[38;2;180;180;180m"
BRIGHT_WHITE = "\033[38;2;255;255;255m"
PROMPT_MAGENTA = "\033[38;2;255;0;255m"
ORANGE = "\033[0;38;2;255;135;0;49m"

# --- Alert Color ----
ALERT_RED = "\033[31m"
WARNING_ORANGE = "\033[33m"
SUCCESS_GREEN = "\033[32m"

# --- ASCII Art Banner ---
def print_ipfinder_banner():
    """Prints the IPFinder banner with the professional purple theme."""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{BOLD}{DEEP_PURPLE}
██╗██████╗     ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██║██╔══██╗    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██║██████╔╝    █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██║██╔═══╝     ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║██║         ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝╚═╝         ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
{RESET}{DEEP_PURPLE}{BOLD}                 <═══{RESET}{BRIGHT_WHITE}{BOLD} IP Finder by Hamid Tayefi {RESET}{DEEP_PURPLE}{BOLD}═══>{RESET}
{BOLD}{MEDIUM_GRAY} About Me:{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {MEDIUM_GRAY}Website:   {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://hxtayefi.com{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {MEDIUM_GRAY}GitHub:    {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://github.com/hxtayefi{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {MEDIUM_GRAY}Instagram: {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://instagram.com/hxtayefi{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {MEDIUM_GRAY}Telegram:  {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://t.me/hxtayefi{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {MEDIUM_GRAY}X:         {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://x.com/hxtayefi{RESET}
"""
    print(banner)

# --- Loading Animation ---
def loading_animation(message, duration=1.5):
    """Displays a simple loading animation with the theme."""
    chars = ['|', '/', '-', '\\']
    start_time = time.time()
    sys.stdout.write(f"{VIBRANT_PURPLE}  {message} {RESET}")
    sys.stdout.flush()
    i = 0
    while time.time() - start_time < duration:
        sys.stdout.write(f"\b{chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\b{SUCCESS_GREEN}Done!{RESET}\n")
    sys.stdout.flush()

# --- Core Logic Functions ---
def fetch_announced_prefixes(asn):
    """Fetches announced IP prefixes for a given ASN from BGPView API."""
    url = f"https://api.bgpview.io/asn/{asn}/prefixes"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    sys.stdout.write(f"{WARNING_ORANGE}  [>] Fetching prefixes for ASN {asn}... {RESET}")
    sys.stdout.flush()
    
    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code != 200:
            sys.stdout.write(f"{ALERT_RED}FAIL ({res.status_code}){RESET}\n")
            return set()
        sys.stdout.write(f"{SUCCESS_GREEN}SUCCESS{RESET}\n")
    except requests.exceptions.RequestException as e:
        sys.stdout.write(f"{ALERT_RED}ERROR{RESET}\n")
        print(f"{ALERT_RED}  [!] An error occurred: {e}{RESET}")
        return set()

    data = res.json()
    prefixes = set()
    for item in data.get("data", {}).get("ipv4_prefixes", []):
        try:
            prefixes.add(ipaddress.IPv4Network(item["prefix"]))
        except (ipaddress.AddressValueError, ValueError):
            continue
    return prefixes

def remove_subnets(prefixes):
    """Removes subnets, keeping only the supernets."""
    if not prefixes: return []
    sorted_prefixes = sorted(list(prefixes), key=lambda x: x.prefixlen)
    cleaned = []
    for net in sorted_prefixes:
        if not any(net.subnet_of(bigger_net) for bigger_net in cleaned):
            cleaned.append(net)
    cleaned.sort(key=lambda x: (x.prefixlen, int(x.network_address)))
    return cleaned

def save_to_txt(prefixes, filename):
    """Saves a list of prefixes to a text file."""
    try:
        with open(filename, "w") as f:
            for p in prefixes:
                f.write(str(p) + "\n")
        print(f"\n{BOLD}{SUCCESS_GREEN} ┌───────────────────────────────────────────────────────────┐{RESET}")
        print(f"{BOLD}{SUCCESS_GREEN} │ [✓ SUCCESS] {len(prefixes)} unique ranges saved to {PROMPT_MAGENTA}'{filename}'{SUCCESS_GREEN}! │{RESET}")
        print(f"{BOLD}{SUCCESS_GREEN} └───────────────────────────────────────────────────────────┘{RESET}")
    except IOError as e:
        print(f"{ALERT_RED}  [✗ ERROR] Could not save file '{filename}': {e}{RESET}")

# --- Main Menu and Logic ---
def main():
    session_prefixes = set()

    while True:
        print_ipfinder_banner()
        print(f"\n{BOLD}{DEEP_PURPLE} ╔═════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║{RESET}{BOLD}{VIBRANT_PURPLE}                👾 {RESET}{BOLD}{BRIGHT_WHITE}MENU OPTION{RESET}{BOLD}{VIBRANT_PURPLE} 👾                {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ╠═════════════════════════════════════════════════╣{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║ {RESET}{BOLD}{ORANGE}[{RESET}{BOLD}{VIBRANT_PURPLE}1{RESET}{BOLD}{ORANGE}]{RESET} {VIBRANT_PURPLE}Single ASN Scan                             {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║                                                 ║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║ {RESET}{BOLD}{ORANGE}[{RESET}{BOLD}{VIBRANT_PURPLE}2{RESET}{BOLD}{ORANGE}]{RESET} {VIBRANT_PURPLE}Multi-line ASN Input                        {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║                                                 ║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║ {RESET}{BOLD}{ORANGE}[{RESET}{BOLD}{VIBRANT_PURPLE}3{RESET}{BOLD}{ORANGE}]{RESET} {VIBRANT_PURPLE}Scan ASNs From File                         {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║                                                 ║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║ {RESET}{BOLD}{ORANGE}[{RESET}{BOLD}{ALERT_RED}E{RESET}{BOLD}{ORANGE}]{RESET} {BOLD}{ALERT_RED}Exit                                        {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ╚═════════════════════════════════════════════════╝{RESET}")
        
        user_choice = input(f"{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{PROMPT_MAGENTA} Select an option: {RESET}").strip()

        if user_choice.lower() == 'e':
            loading_animation("Exiting and preparing to save ", 1)
            break # Exit the loop to proceed to the saving block

        asn_list = []
        if user_choice == '1':
            asn_input = input(f"{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{BOLD}{PROMPT_MAGENTA} Enter a single ASN: {RESET}").strip()
            if asn_input.isdigit(): asn_list.append(asn_input)
            else: print(f"{ALERT_RED}  [!] Invalid input: Please enter a valid number.{RESET}"); time.sleep(1.5); continue
        elif user_choice == '2':
            print(f"{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{BOLD}{PROMPT_MAGENTA} Enter ASNs, one per line (empty line to finish):{RESET}")
            lines = []
            while True:
                line = input(f"{PROMPT_MAGENTA}> {RESET}").strip()
                if not line: break
                lines.append(line)
            asn_list = [asn for asn in " ".join(lines).split() if asn.isdigit()]
        elif user_choice == '3':
            filepath = input(f"{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{BOLD}{PROMPT_MAGENTA} Enter the path to your text file: {RESET}").strip()
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f: content = f.read()
                    asn_list = [asn for asn in content.split() if asn.isdigit()]
                except Exception as e: print(f"{ALERT_RED}  [!] Error reading file: {e}{RESET}"); time.sleep(1.5); continue
            else: print(f"{ALERT_RED}  [!] File not found.{RESET}"); time.sleep(1.5); continue
        else:
            print(f"{ALERT_RED}  [!] Invalid selection.{RESET}"); time.sleep(1.5); continue

        if asn_list:
            print(f"\n{BOLD}{LIGHT_PURPLE}--- Initiating Prefix Collection ---{RESET}")
            old_count = len(session_prefixes)
            for asn in asn_list:
                session_prefixes.update(fetch_announced_prefixes(asn))
                time.sleep(0.1)
            
            newly_added_count = len(session_prefixes) - old_count
            print(f"\n{BOLD}{LIGHT_PURPLE}--- Collection Summary ---{RESET}")
            print(f"{SUCCESS_GREEN}  [+] This scan added {newly_added_count} new unique prefixes.{RESET}")
            print(f"{WARNING_ORANGE}  [>] Total unique prefixes in session: {len(session_prefixes)}{RESET}")
            
            loading_animation("Processing collected data ", 1)

            continue_choice = input(f"\n{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET} Press {BOLD}{PROMPT_MAGENTA}Enter{RESET} to return to menu or type {BOLD}{PROMPT_MAGENTA}S{RESET} to Save and Exit: {RESET}").strip().lower()
            if continue_choice == 's':
                break # Exit the loop to proceed to the saving block

    # --- FINAL PROCESSING & SAVING (runs after the loop breaks) ---
    if session_prefixes:
        print(f"\n{BOLD}{LIGHT_PURPLE}--- Finalizing Session ---{RESET}")
        loading_animation(f"Cleaning all {len(session_prefixes)} collected prefixes ", 2)
        final_prefixes = remove_subnets(session_prefixes)
        save_to_txt(final_prefixes, "IPFinder(Log).txt")
    else:
        print(f"\n{WARNING_ORANGE}[INFO] No prefixes were collected. Nothing to save.{RESET}")

    print(f"\n{BOLD}{DEEP_PURPLE}Thank you for using IP Finder!{RESET}")
    input(f"\n{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{BOLD}{BRIGHT_WHITE} Press {PROMPT_MAGENTA}Enter{BRIGHT_WHITE} to Exit...{RESET}")
    sys.exit(0)

# --- Script Entry Point ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{ALERT_RED}  [!] Operation interrupted by user (Ctrl+C) Exiting.{RESET}")
        sys.exit(0)
