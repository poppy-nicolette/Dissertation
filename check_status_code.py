# counts for each type
# need to make function for https code

from urllib.parse import urlparse
import requests
import time

def check_status_code(url:str)-> str:
    """
    This function takes a URL as input and returns a string for 'Valid' or 'Invalid'.
    It checks if both the scheme ('https', etc) and the location (www.wikipedia.com) are present

    Returns
    str
        "Invalid URL scheme or netloc" - this means the URL is missing the scheme or netlocation.
        "Invalid URL" - this means that the response code was not received and the attempt failed.
        Status code - this is a status code that must be interpreted.

    Example:
    200 - This is a valid and functioning URL
    404 - Page not found.
    """
    result = urlparse(url)
    if not result.scheme and result.netloc:
        return "Invalid URL scheme or netloc"

    try:
        response = requests.get(url, timeout=5) # timeout in 5 seconds
        # rate limiting
        time.sleep(.5)
        return str(response.status_code)
    except requests.exceptions.RequestException:
        return f"Attempt failed"
