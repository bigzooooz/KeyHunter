import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

import subprocess, argparse, json, httpx, re, asyncio, os, yaml, gc, time, random, requests
from colorama import Fore, Style, init
from tqdm import tqdm

with_subs = True
VERBOSE = False

BATCH_SIZE = 5000 
cookie = ""
VERSION = open("version.txt", "r").read().strip()
GITHUB_VERSION = requests.get("http://raw.githubusercontent.com/bigzooooz/KeyHunter/main/version.txt", verify=False).text.strip()
if GITHUB_VERSION == "404: Not Found":
    GITHUB_VERSION = VERSION

X_REQUEST_FOR = ""

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"
]


def run_subfinder(domain):
    try:
        result = subprocess.run(["subfinder", "-d", domain, "-all", "-recursive", "-silent"], capture_output=True, text=True)
        return (line.strip() for line in result.stdout.splitlines()) 
    except Exception as e:
        print(f"Error running subfinder: {e}")
        return iter([])

def run_waybackurls(domain):
    try:
        if with_subs:
            cmd = f'echo {domain} | waybackurls'
        else:
            cmd = f'echo {domain} | waybackurls -no-subs'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        filtered_urls = result.stdout.splitlines()
        filtered_urls = [url for url in filtered_urls if not any(url.lower().endswith(ext) for ext in excluded_extensions)]
        filtered_urls = [remove_version_param(url) for url in filtered_urls]
        filtered_urls = list(set(filtered_urls))


        return filtered_urls

    except Exception as e:
        print(f"Error running WaybackURLs: {e}")
        return []

def remove_version_param(url):
    return re.sub(r'(\?v=|ver=|version=|rev=|timestamp=|build=|_token=)[^&]+', '', url).rstrip('?')


def batched(iterable, size):
    """Yields chunks of the iterable in batches of the given size."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

def load_api_key_patterns(yaml_file):
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)

        api_key_patterns = {}

        def extract_patterns(d, parent_key=""):
            """ Recursively extract regex patterns from nested dictionaries. """
            for key, value in d.items():
                new_key = f"{parent_key} - {key}" if parent_key else key
                if isinstance(value, str):
                    api_key_patterns[new_key] = re.compile(r"{}".format(value))
                elif isinstance(value, dict):
                    extract_patterns(value, new_key)

        extract_patterns(data.get("api_keys", {}))
        return api_key_patterns

    except Exception as e:
        if VERBOSE:
            print(Fore.YELLOW + f"[-] Error loading API key patterns: {e}")
        return {}

def load_excluded_extensions(yaml_file):
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        
        excluded_extensions = data.get("excluded_extensions", [])
        return excluded_extensions

    except Exception as e:
        if VERBOSE:
            print(Fore.YELLOW + f"[-] Error loading excluded extensions: {e}")
        return []

api_key_patterns = load_api_key_patterns("api_patterns.yaml")

excluded_extensions = load_excluded_extensions("excluded_extensions.yaml")

def search_for_api_keys(content, url, domain, output_file):
    keys_found = {}
    for provider, pattern in api_key_patterns.items():
        matches = set(pattern.findall(content))
        if matches:
            keys_found[provider] = list(matches)
            print(Fore.GREEN + f"[+] Found {provider}.")
            print(Fore.GREEN + f"    - URL: {url}")
            print(Fore.GREEN + "-"*50)

            
            save_results(domain, {url: keys_found}, output_file, incremental=True)
    return keys_found

def fetch_url(url):
    global cookie
    global X_REQUEST_FOR

    if not url or not isinstance(url, str) or not url.strip():
        return None, None

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    if X_REQUEST_FOR:
        headers["X-Request-For"] = X_REQUEST_FOR

    try:
        response = requests.get(url, headers=headers, cookies=cookie, timeout=5, verify=False)

        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "").lower()

            if VERBOSE:
                print(Fore.WHITE + f"[+] Fetched {url}")

            if any(t in content_type for t in ["text/html", "application/javascript", "text/javascript", "application/json"]):
                return url, response.text
        else:
            if VERBOSE:
                print(Fore.YELLOW + f"[-] Non-200 status code {response.status_code} for {url}")

    except requests.exceptions.Timeout:
        if VERBOSE:
            print(Fore.YELLOW + f"[-] Timeout for {url}")
    except requests.exceptions.RequestException as e:
        if VERBOSE:
            print(Fore.YELLOW + f"[-] Request error for {url}: {e}")
    except Exception as e:
        if VERBOSE:
            print(Fore.YELLOW + f"[-] Unexpected error for {url}: {e}")

    return None, None

async def visit_and_check_for_keys(urls, domain, output_file):
    api_keys_found = 0
    async with httpx.AsyncClient(timeout=5, verify=False) as session:
        for batch in batched(urls, BATCH_SIZE):
            tasks = [asyncio.to_thread(fetch_url, url) for url in batch]
            results = await asyncio.gather(*tasks)
            for url, content in results:
                if VERBOSE:
                    print(Fore.WHITE + f"[+] Checking {url}")
                if content:
                    keys = search_for_api_keys(content, url, domain, output_file)
                    if keys:
                        api_keys_found += 1
            gc.collect()

    return api_keys_found

def save_results(domain, api_keys_found, output_file, incremental=False):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    if incremental:
        try:
            with open(output_file, "r") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {"domain": domain, "api_keys_found": {}}

        existing_data["api_keys_found"].update(api_keys_found)

        with open(output_file, "w") as f:
            json.dump(existing_data, f, indent=4)

    else:
        with open(output_file, "w") as f:
            json.dump({"domain": domain, "api_keys_found": api_keys_found}, f, indent=4)

        print(Fore.WHITE + f"[+] Results saved to ./{output_file}")

async def main():
    global with_subs
    global cookie
    global X_REQUEST_FOR
    global VERBOSE

    init(autoreset=True)

    print(Fore.CYAN + f"""

    ██╗  ██╗███████╗██╗   ██╗                           
    ██║ ██╔╝██╔════╝╚██╗ ██╔╝                           
    █████╔╝ █████╗   ╚████╔╝                            
    ██╔═██╗ ██╔══╝    ╚██╔╝                             
    ██║  ██╗███████╗   ██║                              
    ╚═╝  ╚═╝╚══════╝   ╚═╝                              
                                                        
    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
    ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   v{VERSION}      
                                    
    A tool to discover API key leaks from subdomains and archived URLs.  
                                
    """ + Style.RESET_ALL)

    time.sleep(1)
    if VERSION != GITHUB_VERSION:
        print(Fore.YELLOW + f"[!] A new version of KeyHunter is available. Please update to v{GITHUB_VERSION} using '--update' flag.") 
        print("")

    parser = argparse.ArgumentParser(description="KeyHunter - A tool to discover API key leaks from subdomains and archived URLs.")

    parser.usage = "Keyhunter.py -d TARGET_DOMAIN [--cookie COOKIE] [--no-subs]"

    parser.add_argument("-d", "--domain", help="Target domain for scanning.")
    parser.add_argument("-f", "--file", help="File containing a list of domains to scan.")
    parser.add_argument("-ns", "--no-subs", help="Disable subdomain enumeration.", action="store_true")
    parser.add_argument("--cookie", help="Cookie to use for requests.")
    parser.add_argument("--x-request-for", help="X-Request-For header to use for requests. (i.e. --x-request-for HackerOne)")
    parser.add_argument("--update", help="Update KeyHunter to the latest version.", action="store_true")
    parser.add_argument("--version", help="Show KeyHunter version.", action="store_true")
    parser.add_argument("-v","--verbose", help="Enable verbose output.", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        VERBOSE = True
    if args.update:
        if VERSION != GITHUB_VERSION:
            print(Fore.WHITE + "[+] Updating KeyHunter to the latest version...")
            subprocess.run(["git", "pull"])
            print(Fore.GREEN + "[+] KeyHunter updated successfully. Please re-run the tool.")
            print(Fore.YELLOW + "[!] Exiting...")
            exit(0)
            return
        else:
            print(Fore.GREEN + "[+] KeyHunter is already up-to-date.")
            print(Fore.YELLOW + "[!] Exiting...")
            exit(0)

    if args.x_request_for:
        X_REQUEST_FOR = args.x_request_for

    if args.version:
        print(Fore.WHITE + f"[+] KeyHunter version: {VERSION}")
        print(Fore.YELLOW + "[!] Exiting...")
        exit(0)
        return

    if args.cookie:
        cookie = args.cookie

    if args.no_subs:
        with_subs = False

    domains = []
    if args.domain:
        domains.append(args.domain)
    elif args.file:
        try:
            with open(args.file, 'r') as file:
                domains = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(Fore.RED + f"[-] Error reading domains from file: {e}")
            exit(1)
    else:
        print(Fore.RED + "[-] Please provide either a domain or a file containing domains.")
        exit(1)

    for domain in domains:
        urls = []

        print(Fore.WHITE + f"- Target: {domain}")
        print(Fore.WHITE + f"- Subdomains: {'✔️' if with_subs else '❌'}")
        print(Fore.WHITE + f"- Cookie: {'✔️'  if cookie else '❌'}")
        print(Fore.WHITE + f"- X-Request-For: {X_REQUEST_FOR if X_REQUEST_FOR else '❌'}")
        print("")
        print(Fore.WHITE + "-"*50)
        print("")

        if with_subs:
            print(Fore.WHITE + "[+] Looking for subdomains ...")
            subdomains = [domain] + list(run_subfinder(domain))
            print(Fore.GREEN + f"[+] Found {len(subdomains)} subdomains 🎯")
            print(Fore.WHITE + "[+] Looking for URLs ...")
            for subdomain in subdomains:
                urls.extend(run_waybackurls(subdomain))

            subdomains = None
            gc.collect()
        else:
            print(Fore.WHITE + "[+] Looking for URLs ...")
            urls.extend(run_waybackurls(domain))

        print(Fore.GREEN + f"[+] Found {len(urls)} URLs 🎯")
        print("")

        print(Fore.YELLOW + "-"*50)
        print(Fore.YELLOW + "While you're here, consider supporting the developer:")
        print(Fore.YELLOW + "PayPal: https://paypal.me/b4zb0z")
        print(Fore.YELLOW + "Ko-fi: https://ko-fi.com/b4zb0z")
        print(Fore.YELLOW + "Thank you, your support is greatly appreciated! ❤️")
        print(Fore.YELLOW + "-"*50)
        print("")

        print(Fore.WHITE + "[+] Scanning URLs for API key leaks... This may take a while.")

        output_file = f"output/{domain}_results.json"
        api_keys_found = await visit_and_check_for_keys(urls, domain, output_file)

        print(Fore.WHITE + f"[+] Scanned {len(urls)} URLs.")

        if api_keys_found:
            print(Fore.GREEN + f"[+] Found {api_keys_found} URLs with API keys.")
        else:
            print(Fore.YELLOW + "[-] No API keys found.")
        
        print(Fore.WHITE + "[+] Done! 🎉")
        print("")

if __name__ == "__main__":
    asyncio.run(main())