import requests
from bs4 import BeautifulSoup
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
LIGHT_PURPLE = "\033[38;2;127;0;255m" 
DEEP_PURPLE = "\033[38;2;102;0;153m" 
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
def print_pro_banner():
    """Prints an advanced ASCII art banner with the new professional purple theme."""
    os.system('cls' if os.name == 'nt' else 'clear') # Clear console first
    banner = f"""
{BOLD}{DEEP_PURPLE}
 █████╗ ███████╗███╗   ██╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██╔════╝████╗  ██║    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
███████║███████╗██╔██╗ ██║    █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══██║╚════██║██║╚██╗██║    ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║  ██║███████║██║ ╚████║    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
{RESET}{DEEP_PURPLE}{BOLD}                 <═══{RESET}{BRIGHT_WHITE}{BOLD} ASN Finder Pro by Hamid Tayefi {RESET}{DEEP_PURPLE}{BOLD}═══>{RESET}
{BOLD}{MEDIUM_GRAY} About Me:{RESET}{DIM}{VIBRANT_PURPLE}{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {DIM}{MEDIUM_GRAY}Website:   {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://hxtayefi.com{RESET}{DIM}{VIBRANT_PURPLE}{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {DIM}{MEDIUM_GRAY}GitHub:    {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://github.com/hxtayefi{RESET}{DIM}{VIBRANT_PURPLE}{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {DIM}{MEDIUM_GRAY}Instagram: {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://instagram.com/hxtayefi{RESET}{DIM}{VIBRANT_PURPLE}{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {DIM}{MEDIUM_GRAY}Telegram:  {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://t.me/hxtayefi{RESET}{DIM}{VIBRANT_PURPLE}{RESET}
{BOLD}{BRIGHT_WHITE}─{RESET} {DIM}{MEDIUM_GRAY}X:         {RESET}{UNDERLINE}{VIBRANT_PURPLE}https://x.com/hxtayefi{RESET}{DIM}{VIBRANT_PURPLE}{RESET}
"""
    print(banner)

# --- Core Scraping Function (Themed Messages) ---
def get_asns_from_page(page_number):
    """
    This function extracts ASN numbers from a specific page on bgpview.io for Iran.
    Includes enhanced loading messages with the new theme.
    """
    url = f"https://bgpview.io/reports/countries/IR?page={page_number}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
    
    sys.stdout.write(f"{WARNING_ORANGE}  [>] Attempting to fetch data from page {page_number}... {RESET}")
    sys.stdout.flush() # Ensure the message is printed immediately

    try:
        res = requests.get(url, headers=headers, timeout=15) # Increased timeout slightly
        res.raise_for_status()
        sys.stdout.write(f"{SUCCESS_GREEN}SUCCESS{RESET}\n")
    except requests.exceptions.Timeout:
        sys.stdout.write(f"{ALERT_RED}TIMEOUT{RESET}\n")
        print(f"{ALERT_RED}  [!] Error: Request timed out for page {page_number}. Network might be slow.{RESET}")
        return []
    except requests.exceptions.ConnectionError:
        sys.stdout.write(f"{ALERT_RED}FAIL{RESET}\n")
        print(f"{ALERT_RED}  [!] Error: Connection failed for page {page_number}. Check your internet connection or URL.{RESET}")
        return []
    except requests.exceptions.HTTPError as e:
        sys.stdout.write(f"{ALERT_RED}HTTP ERROR {e.response.status_code}{RESET}\n")
        print(f"{ALERT_RED}  [!] HTTP Error {e.response.status_code} for page {page_number}: {e}. The page might not exist.{RESET}")
        return []
    except requests.exceptions.RequestException as e:
        sys.stdout.write(f"{ALERT_RED}ERROR{RESET}\n")
        print(f"{ALERT_RED}  [!] An unexpected request error occurred for page {page_number}: {e}{RESET}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    asn_numbers = []

    for row in soup.select("table#country-report tbody tr"):
        td = row.find("td")
        if td:
            asn_text = td.get_text(strip=True)
            if asn_text.upper().startswith("AS"):
                number = asn_text.upper().replace("AS", "").strip()
                if number.isdigit():
                    asn_numbers.append(number)
    
    if asn_numbers:
        print(f"{SUCCESS_GREEN}  [✓] Successfully extracted {len(asn_numbers)} ASNs from page {page_number}.{RESET}")
    else:
        print(f"{WARNING_ORANGE}  [i] No ASNs found on page {page_number}. This might be the last page with data.{RESET}")
    return asn_numbers

# --- Loading Animation (Themed) ---
def loading_animation(message, duration=2):
    """Displays a simple loading animation with the new theme."""
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

# --- Main Logic (Themed) ---
def main():
    # The initial print_pro_banner() is removed from here
    all_asn_numbers = []
    
    while True:
        print_pro_banner() # Moved here to run at the start of every loop iteration

        print(f"\n{BOLD}{DEEP_PURPLE} ╔═════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║{RESET}{BOLD}{VIBRANT_PURPLE}                👾 {RESET}{BOLD}{BRIGHT_WHITE}MENU OPTION{RESET}{BOLD}{VIBRANT_PURPLE} 👾                {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ╠═════════════════════════════════════════════════╣{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║ {RESET}{BOLD}{ORANGE}[{RESET}{BOLD}{VIBRANT_PURPLE}1{RESET}{BOLD}{ORANGE}]{RESET} {VIBRANT_PURPLE}​Single Page Scan                            {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║                                                 ║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║ {RESET}{BOLD}{ORANGE}[{RESET}{BOLD}{VIBRANT_PURPLE}2{RESET}{BOLD}{ORANGE}]{RESET} {VIBRANT_PURPLE}Page Range Scan                             {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║                                                 ║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ║ {RESET}{BOLD}{ORANGE}[{RESET}{BOLD}{ALERT_RED}E{RESET}{BOLD}{ORANGE}]{RESET} {BOLD}{ALERT_RED}Exit                                        {RESET}{BOLD}{DEEP_PURPLE}║{RESET}")
        print(f"{BOLD}{DEEP_PURPLE} ╚═════════════════════════════════════════════════╝{RESET}")
        
        user_choice = input(f"{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{PROMPT_MAGENTA} Select an option: {RESET}").strip()
        
        if user_choice.lower() == 'e':
            loading_animation(f"{VIBRANT_PURPLE}  Exiting ASN Finder Pro ", 1.5)
            break

        pages_to_process = []
        if user_choice == '1':
            try:
                page_num_str = input(f"{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{BOLD}{PROMPT_MAGENTA} Enter page number (e.g., 5): {RESET}").strip()
                page_num = int(page_num_str)
                if page_num < 1:
                    print(f"{ALERT_RED}  [!] Invalid input: Page number must be 1 or greater.{RESET}")
                    time.sleep(1.5)
                    continue
                pages_to_process.append(page_num)
            except ValueError:
                print(f"{ALERT_RED}  [!] Invalid input: Please enter a valid whole number for the page.{RESET}")
                time.sleep(1.5)
                continue
        elif user_choice == '2':
            try:
                page_range_str = input(f"{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{BOLD}{PROMPT_MAGENTA} Enter page range (e.g., 1-9): {RESET}").strip()
                start_page_str, end_page_str = page_range_str.split('-')
                start_page = int(start_page_str)
                end_page = int(end_page_str)

                if start_page < 1 or end_page < 1 or start_page > end_page:
                    print(f"{ALERT_RED}  [!] Invalid page range: Start and end must be positive, and start <= end.{RESET}")
                    time.sleep(1.5)
                    continue
                pages_to_process = range(start_page, end_page + 1)
            except (ValueError, IndexError):
                print(f"{ALERT_RED}  [!] Incorrect format: Please use 'start-end' (e.g., 1-9).{RESET}")
                time.sleep(1.5)
                continue
        else:
            print(f"{ALERT_RED}  [!] Invalid selection: Please choose 1, 2 or E.{RESET}")
            time.sleep(1.5) # Added sleep for consistent behavior
            continue
        
        if pages_to_process:
            print(f"\n{BOLD}{LIGHT_PURPLE}--- Initiating ASN Collection ---{RESET}")
            for page_num in pages_to_process:
                current_asns = get_asns_from_page(page_num)
                all_asn_numbers.extend(current_asns)
                time.sleep(0.1)
            
            print(f"\n{BOLD}{LIGHT_PURPLE}--- Collection Summary ---{RESET}")
            unique_count = len(set(all_asn_numbers))
            print(f"{SUCCESS_GREEN}  [+] This scan added {unique_count - (len(all_asn_numbers) - len(set(all_asn_numbers)))} new unique ASNs.{RESET}")
            print(f"{WARNING_ORANGE}  [>] Total unique ASNs gathered so far: {unique_count}{RESET}")
            loading_animation("  Processing collected data... ", 1.5)

            continue_choice = input(f"\n{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET} Press {BOLD}{PROMPT_MAGENTA}Enter{RESET} to return to menu or type {BOLD}{PROMPT_MAGENTA}S{RESET} to save and Exit: {RESET}").strip().lower()
            if continue_choice == 's':
                break
        
        # The print_pro_banner() call at the end of the loop is removed
            
    # --- Final Processing and Saving (Themed) ---
    if all_asn_numbers:
        print(f"\n{BOLD}{LIGHT_PURPLE}--- Finalizing Session ---{RESET}")
        unique_asn_numbers = sorted(list(set(all_asn_numbers)), key=int) 
        loading_animation(f"  Saving {len(unique_asn_numbers)} unique ASNs ", 2)
        
        filename = "ASNFinder(Log).txt"
        try:
            with open(filename, "w") as f:
                f.write("\n".join(unique_asn_numbers))
            print(f"\n{BOLD}{SUCCESS_GREEN} ┌──────────────────────────────────────────────────────────────────────┐{RESET}")
            print(f"{BOLD}{SUCCESS_GREEN} │ [✓ SUCCESS]{SUCCESS_GREEN} {len(unique_asn_numbers)} unique ASNs from Iran saved to {PROMPT_MAGENTA}'{filename}'{SUCCESS_GREEN}!  │{RESET}")
            print(f"{BOLD}{SUCCESS_GREEN} └──────────────────────────────────────────────────────────────────────┘{RESET}")
        except IOError as e:
            print(f"{ALERT_RED}  [✗ ERROR] Could not save file '{filename}': {e}{RESET}")
    else:
        print(f"\n{WARNING_ORANGE}[INFO] No ASNs were collected during this session, or the operation was cancelled before saving.{RESET}")

    print(f"\n{BOLD}{DEEP_PURPLE}Thank you for using ASN Finder Pro!{RESET}")
    input(f"\n{BRIGHT_WHITE}[{RESET}{PROMPT_MAGENTA}~{RESET}{BRIGHT_WHITE}]{RESET}{BOLD}{BRIGHT_WHITE} Press {PROMPT_MAGENTA}Enter{BRIGHT_WHITE} to Exit...{RESET}")
    sys.exit(0)

# --- Script Entry Point ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{ALERT_RED}  [!] Operation interrupted by user (Ctrl+C) Exiting.{RESET}")
        sys.exit(0)
