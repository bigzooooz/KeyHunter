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

---

## Installation 🛠️

### Prerequisites

- Python 3.7+
- `subfinder` and `waybackurls` installed and available in your system's PATH.

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/KeyHunter.git
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
   python keyhunter.py -d example.com
   ```

---

## Usage 🚀

### Basic Usage

To scan a single domain for API key leaks:
```bash
python keyhunter.py -d example.com
```

To scan multiple domains from a file:
```bash
python keyhunter.py -f domains.txt
```

### Disable Subdomain Enumeration

To scan only the provided domain(s) without enumerating subdomains:
```bash
python keyhunter.py -d example.com --no-subs
```

### Output

The tool will generate a JSON file in the `output` directory for each domain, containing the results of the scan, including:
- The target domain
- Detected API keys

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

## Acknowledgments 🙏

- **Subfinder**: For subdomain enumeration.
- **Waybackurls**: For collecting URLs from the Wayback Machine.
- **httpx**: For asynchronous HTTP requests.
- **tqdm**: For progress bars.
- **colorama**: For colored terminal output.

---

## Support 💖

If you find this tool useful, consider giving it a ⭐ on GitHub!

---

**Happy Hunting!** 🎯