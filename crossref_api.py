# crossref_api.py

import requests
import json
from typing import Any, Dict

class CrossrefAPI:
    """
    A class used to retrieve data from the Crossref REST API
    ...

    Attributes
    ----------
    doi : str
        the Digital Object Identifier (DOI) of the work to be retrieved
    url : str
        the URL of the Crossref API endpoint for the given DOI
    filters: str
        filters to be passed to the class. These should be joined together with commas.
    email: str
        email to be passed to the REST API for the polite pool (optional)

    Methods
    -------
    get_data() -> Dict[str, Any]
        retrieves data from the Crossref API and returns it as a dictionary
    get_title() -> str
        retrieves the title from the JSON data retrieved from the Crossref API
    """

    def __init__(self, doi: str) -> None:
        """
        Constructs all the necessary attributes for the CrossrefAPI object.

        Parameters
        ----------
        doi : str
            the Digital Object Identifier (DOI) of the work to be retrieved
        """
        self.doi = doi
        self.title = title
        self.url = f"https://api.crossref.org/works/{self.doi}"

    def get_data(self) -> Dict[str, Any]:
        """
        Retrieves data from the Crossref API and returns it as a dictionary.

        Returns
        -------
        Dict[str, Any]
            a dictionary containing data from the Crossref API
        """
        response = requests.get(self.url)
        data = json.loads(response.text)
        return data

    def get_title(self) -> str:
        """
        Retrieves the DOI from the JSON data retrieved from the Crossref API.

        Returns
        -------
        str
            the title of the work retrieved from the Crossref API
        """
        data = self.get_data()
        title = data["message"]["title"][0]
        if title:
            return title
        else:
            return "no title"
