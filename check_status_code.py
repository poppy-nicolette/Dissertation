#check_status_code.py

"""
Usage: pass list of URLs to check_urls() to take advantage of multithreading.
Otherwise, you can just use check_status_code(url).

"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import pandas as pd


def check_status_code(url: str) -> str:
    """
    This function takes a URL as input and returns the HTTP status code.
    It checks the status code of the URL and returns it as a string.

    Returns
    str
        Status code - this is a status code that must be interpreted.
        "Attempt Failed" - if the request fails.

    Example:
    200 - This is a valid and functioning URL
    404 - Page not found.
    """

    #add headers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url,
                                headers=headers,
                                timeout=10,#increase timeout to 10 seconds
                                allow_redirects=True) #allows redirects
        return str(response.status_code)
    except requests.exceptions.RequestException:
        return "Attempt Failed"

def check_urls(urls: list, max_workers: int = 5) -> list:
    """
    This function takes a list of URLs and checks their status codes using multithreading.

    Args:
    urls (list): List of URLs to check.
    max_workers (int): Maximum number of threads to use.

    Returns:
    list: A list of status codes or "Access Failed" for each URL.

    References:
        https://realpython.com/python-concurrency/
        https://docs.python.org/3/library/concurrent.futures.html
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # submit all tasks to the executor - must be a list otherwise doesn't take advantage of multithreading
        future_to_url = {executor.submit(check_status_code, url): url for url in urls}

        # collect results as they complete
        for future in as_completed(future_to_url):
            try:
                status_code = future.result()
                results.append(status_code)
            except Exception:
                results.append("Attempt Failed")

    return results
