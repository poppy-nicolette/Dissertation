import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_status_code(url: str) -> str:
    """
    This function takes a URL as input and returns the HTTP status code.
    It checks the status code of the URL and returns it as a string.

    Returns
    str
        Status code - this is a status code that must be interpreted.

    Example:
    200 - This is a valid and functioning URL
    404 - Page not found.
    """
    try:
        response = requests.get(url, timeout=5)  # timeout in 5 seconds
        return str(response.status_code)
    except requests.exceptions.RequestException as e:
        return f"Attempt failed: {str(e)}"

def check_urls(urls: list, max_workers: int = 5) -> dict:
    """
    This function takes a list of URLs and checks their status codes using multithreading.

    Args:
    urls (list): List of URLs to check.
    max_workers (int): Maximum number of threads to use.

    Returns:
    dict: A dictionary with URLs as keys and their status codes as values.
    """
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks to the executor
        future_to_url = {executor.submit(check_status_code, url): url for url in urls}

        # Collect results as they complete
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                status_code = future.result()
                results[url] = status_code
            except Exception as e:
                results[url] = f"Error: {str(e)}"

    return results

# Example usage
# urls = ["https://www.example.com", "https://www.google.com", "https://www.github.com"]
# status_codes = check_urls(urls)
# print(status_codes)
