

---

# ppcurl.py Documentation

## Overview

This script fetches a URL, optionally resolves a hostname, and provides detailed information about the request and response, including headers, statistics, and an MD5 checksum of the response body. It also supports connection debugging and custom headers from a YAML file.

## Requirements

- Python 3.x
- `requests` library
- `PyYAML` library
- `tabulate` library

Install the required libraries using pip:

```bash
pip install requests pyyaml tabulate
```

## Usage

```bash
python script.py [options] URL [hostname]
```

### Positional Arguments

- `URL`: The URL to fetch.
- `hostname` (optional): The hostname to resolve.

### Optional Arguments

- `--connection_debug`: Enable connection debug mode.
- `--stdout`: Output the response body to stdout.
- `--header_file`: Path to the YAML file with header array.

## Example

```bash
python script.py --connection_debug --stdout --header_file headers.yaml https://example.com
```

## Functions

### `enhanced_tabulate(data, headers=None, width=80)`

Formats data into a table using the `tabulate` library.

- `data`: The data to be formatted.
- `headers`: Optional headers for the table.
- `width`: Maximum column width.

### `resolve_hostname(hostname)`

Resolves the IP address of a given hostname.

- `hostname`: The hostname to resolve.

### `load_headers(header_file)`

Loads headers from a YAML file.

- `header_file`: Path to the YAML file.

### `setup_logging()`

Sets up logging to capture debug information.

### `fetch_url(url, headers)`

Fetches the URL with the specified headers.

- `url`: The URL to fetch.
- `headers`: The headers to include in the request.

### `print_request_statistics(response, ip_address)`

Prints statistics about the HTTP request.

- `response`: The HTTP response object.
- `ip_address`: The resolved IP address of the hostname.

## Script Flow

1. **Argument Parsing**: Parses command-line arguments using `argparse`.
2. **Header Loading**: Loads headers from a YAML file if provided.
3. **Logging Setup**: Sets up logging if connection debugging is enabled.
4. **Hostname Resolution**: Resolves the hostname and optional proxy hostname.
5. **URL Fetching**: Fetches the URL with the specified headers.
6. **Output**: Prints the response body, request headers, response headers, and request statistics. If connection debugging is enabled, prints the connection log and MD5 checksum of the response body.

## Example YAML Header File (`headers.yaml`)

```yaml
headers:
  X-Unicorn-Magic: SparkleDust
  X-Random-Header: 42
  X-Meaningless-Value: FlibberFlabber
  X-Confusion-Level: Maximum
  X-Nonexistent-Feature: QuantumFlux
  X-Just-For-Fun: BananaBread
  X-Absurdity: Over9000
```

## Notes

- Ensure the YAML file is correctly formatted.
- The script disables SSL verification (`verify=False`). Use with caution in production environments.

---


