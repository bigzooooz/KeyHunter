<a href="https://paypal.me/b4zb0z"><img src="https://shields.io/badge/paypal-Support_on_Paypal-blue?logo=paypal&style=for-the-badgePaypal" /></a> 
<a href="https://ko-fi.com/b4zb0z"><img src="https://shields.io/badge/KoFi-Buy_Me_a_coffee-blue?logo=ko-fi&style=for-the-badgeKofi" /></a> 
 <!-- [![GitHub All Releases](https://img.shields.io/github/downloads/bigzooooz/KeyHunter/total?color=blue&label=Downloads)](https://github.com/bigzooooz/KeyHunter/releases/latest) -->

---

# KeyHunter 🕵️‍♂️

**KeyHunter** is a powerful tool designed to discover API key leaks from subdomains and archived URLs. It automates the process of subdomain enumeration, URL collection, and API key detection, making it an essential tool for security researchers and bug bounty hunters.

---

## Features ✨

- **Subdomain Enumeration**: Utilizes `subfinder` to discover subdomains of a given domain.
- **URL Collection**: Uses `waybackurls` to gather URLs from the Wayback Machine.
- **URL Validation**: Filters out invalid URLs and checks for live endpoints.
- **API Key Detection**: Scans live URLs for potential API key leaks using customizable patterns.
- **Asynchronous Processing**: Efficiently handles multiple URLs concurrently for faster results.
- **Customizable Patterns**: Supports YAML-based patterns for detecting API keys from various providers.
- **Exclusion List**: Allows exclusion of specific file extensions to focus on relevant URLs.
- **Focused Reporting**: Saves results in a structured JSON format, focusing on the domain and detected API keys.
- **Multiple Domain Support**: Accepts a list of domains from an external file for batch scanning.
- **X-Request-For Header**: Supports custom headers for Bug Bounty programs that require a specific header.
- **Cookie Authentication**: Allows authenticated requests by providing a cookie for the target domain.
- **Random User-Agent**: Uses a random User-Agent for each request to avoid detection and blocking.

---

## Supported API Key Patterns 🗝️

| Cloudinary       | Firebase URL       | Firebase Bucket    | Firebase Database   | Slack Token         |
|------------------|--------------------|--------------------|---------------------|---------------------|
| PGP Private Key  | AWS Access Key     | Amazon MWS Token   | Facebook Token      | Facebook OAuth      |
| GitHub Token     | Generic API Key    | Generic Secret     | Google OAuth        | MailChimp           |
| Mailgun          | Stripe             | Square Token       | Square Secret       | Twilio              |
| Telegram         | GitLab PAT         | NPM Token          | Dropbox             | SendGrid            |
| Mapbox           | URL Password       | PayPal Braintree   | Picatic             | Slack Webhook       |
| Laravel ENV      | Alibaba Cloud      | Grafana API        | OpenAI              | Postman             |
| GitLab CI/CD     | OAuth2 Bearer      | Grafana SA Token   | Discord Webhook     | Heroku              |
| Instagram        | Microsoft Azure    | Vercel             | Shopify             | JWT                 |
| RSA Private Key  | React App ENV      |                    |                     |                     |

---

## Installation 🛠️

### Prerequisites

- Python 3.7+
- `subfinder` and `waybackurls` installed and available in your system's PATH.

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/bigzooooz/KeyHunter.git
   cd KeyHunter
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install External Tools**:
   - Install `subfinder` and `waybackurls` by following their respective installation guides.

4. **Configure API Key Patterns**:
   - Modify `api_patterns.yaml` to include patterns for detecting API keys from different providers.

5. **Run KeyHunter**:
   ```bash
   python Keyhunter.py -d example.com
   ```

---

## Usage 🚀

### Basic Usage

To scan a single domain for API key leaks:
```bash
python Keyhunter.py -d example.com
```

To scan multiple domains from a file:
```bash
python Keyhunter.py -f domains.txt
```

### Disable Subdomain Enumeration

To scan only the provided domain(s) without enumerating subdomains:
```bash
python Keyhunter.py -d example.com --no-subs
```

### Output

The tool will generate a JSON file in the `output` directory for each domain, containing the results of the scan, including:
- The target domain
- Detected API keys

---

## Command-Line Options 🛠️  

KeyHunter supports the following command-line options to customize and control the scanning process:  

- `-d, --domain` – Specify the target domain for scanning.  
- `-f, --file` – Provide a file containing a list of domains to scan.  
- `-ns, --no-subs` – Disable subdomain enumeration (default: enabled).  
- `--cookie` – Supply a cookie for authenticated requests.  
- `--x-request-for` – Set a custom `X-Request-For` header (e.g., `--x-request-for HackerOne`).  
- `--update` – Update KeyHunter to the latest version.  
- `--version` – Display the current version of KeyHunter.  
- `-v, --verbose` – Enable verbose output for detailed logs.  

These options provide flexibility to scan domains efficiently while allowing customization for different use cases. 🚀

---

## Configuration ⚙️

### `api_patterns.yaml`

This file contains regular expressions for detecting API keys from various providers. You can add or modify patterns as needed.

Example:
```yaml
aws:
  - "AKIA[0-9A-Z]{16}"
google:
  - "AIza[0-9A-Za-z\\-_]{35}"
```

### `excluded_extensions.yaml`

This file lists file extensions to exclude from the URL validation process.

Example:
```yaml
excluded_extensions:
  - .jpg
  - .png
  - .css
  - .js
```

---

## Example Output 📄

```json
{
  "domain": "example.com",
  "api_keys_found": {
    "http://example.com/page1": {
      "aws": ["AKIA1234567890ABCDEF"]
    }
  }
}
```

---

## Contributing 🤝

Contributions are welcome! Please feel free to submit issues or pull requests to improve the tool.

---

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support 💖

#### If you find this tool useful, consider:

1. Giving it a ⭐ on GitHub!
2. [Buying me a coffee](https://ko-fi.com/s/a6da3a9eec) ☕️ or [Supporting me on PayPal](https://paypal.me/b4zb0z) 💸
3. Sharing it with others who might benefit from it!
4. Providing feedback and suggestions for improvement.
5. Contributing to the project.


## Happy Hunting! 🎯

---

<qoute>
  Disclaimer: This tool is intended for educational and research purposes only. The author is not responsible for any misuse or damage caused by this tool. Use responsibly and do not violate any laws or policies.
</qoute>

---

![Visitor Count](https://profile-counter.glitch.me/{bigzooooz-KeyHunter}/count.svg)

