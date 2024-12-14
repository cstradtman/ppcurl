import argparse
import hashlib
import requests
import socket
from tabulate import tabulate
from urllib.parse import urlparse
import io
import logging
import yaml

def enhanced_tabulate(data, headers=None, width=80):
    """
    Formats data into a table using the tabulate library.

    Parameters:
    - data: The data to be formatted.
    - headers: Optional headers for the table.
    - width: Maximum column width.

    Returns:
    - str: Formatted table as a string.
    """
    if headers is None:
        headers = []
    return tabulate(data, headers=headers, tablefmt='fancy_grid', maxcolwidths=width)

def resolve_hostname(hostname):
    """
    Resolves the IP address of a given hostname.

    Parameters:
    - hostname: The hostname to resolve.

    Returns:
    - str: The resolved IP address.

    Raises:
    - SystemExit: If the hostname cannot be resolved.
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        print(f"Could not resolve IP address for {hostname}. Exiting.")
        exit(1)

def load_headers(header_file):
    """
    Loads headers from a YAML file.

    Parameters:
    - header_file: Path to the YAML file.

    Returns:
    - dict: Dictionary of headers.
    """
    if header_file:
        with open(header_file, 'r') as file:
            header_vars = yaml.safe_load(file)
        return header_vars.get('headers', {})
    return {}

def setup_logging():
    """
    Sets up logging to capture debug information.

    Returns:
    - io.StringIO: String stream to capture logging output.
    """
    log_stream = io.StringIO()
    logging.basicConfig(level=logging.DEBUG, stream=log_stream, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    return log_stream

def fetch_url(url, headers):
    """
    Fetches the URL with the specified headers.

    Parameters:
    - url: The URL to fetch.
    - headers: The headers to include in the request.

    Returns:
    - requests.Response: The HTTP response object.
    """
    response = requests.get(url, headers=headers, verify=False)
    return response

def print_request_statistics(response, ip_address):
    """
    Prints statistics about the HTTP request.

    Parameters:
    - response: The HTTP response object.
    - ip_address: The resolved IP address of the hostname.
    """
    stat_info = [
        ["HTTP Code", response.status_code],
        ["Total Time", f"{response.elapsed.total_seconds()}s"],
        ["Size Download", f"{len(response.content)} bytes"],
        ["Content Type", response.headers.get('Content-Type')],
        ["Effective URL", response.url],
        ["Redirect Count", len(response.history)],
        ["Remote Address", ip_address]
    ]
    print("\nRequest Statistics")
    print("=" * 18)
    print(enhanced_tabulate(stat_info, headers=["Statistic", "Value"]))

def main():
    """
    Main function to parse arguments, fetch URL, and print request/response details.
    """
    parser = argparse.ArgumentParser(description="Fetch a URL and display detailed request/response information.")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("hostname", nargs='?', help="Hostname to resolve (optional)", default=None)
    parser.add_argument("--connection_debug", action="store_true", help="Enable connection debug mode")
    parser.add_argument("--stdout", action="store_true", help="Output response body to stdout")
    parser.add_argument('--header_file', type=str, help='Path to the YAML file with headers')

    args = parser.parse_args()

    url = args.url
    phostname = args.hostname
    conn_debug = args.connection_debug
    stdout = args.stdout
    headerfile = args.header_file

    headers = load_headers(headerfile)

    if conn_debug:
        log_stream = setup_logging()

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    ip_address = resolve_hostname(hostname)
    if phostname:
        headers["Host"] = hostname
        proxy_ip_address = resolve_hostname(phostname)
        url = url.replace(hostname, proxy_ip_address)

    response = fetch_url(url, headers)

    if stdout:
        print(enhanced_tabulate([[response.text]], width=132))

    print("\nRequest Headers")
    print("=" * 15)
    print(enhanced_tabulate(response.request.headers.items(), headers=["Header", "Value"]))

    print("\nResponse Headers")
    print("=" * 16)
    print(enhanced_tabulate(response.headers.items(), headers=["Header", "Value"]))

    print_request_statistics(response, ip_address)

    if conn_debug:
        log_contents = log_stream.getvalue()
        print("\nConnection Log")
        print("=" * 14)
        print(enhanced_tabulate([[log_contents]], width=132))

        md5sum = hashlib.md5(response.text.encode('utf-8')).hexdigest()
        print("\nMD5 Checksum of Response Body")
        print("=" * 29)
        print(enhanced_tabulate([[md5sum]], width=132))

if __name__ == "__main__":
    main()
