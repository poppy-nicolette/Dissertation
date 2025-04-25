# crossref_api.py
#!user/bin/env/ python3

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
        the Digital Object Identifier (DOI) of the work to be retrieved. This should only contain the prefix and suffix, not the resolver.
    url : str
        the URL of the Crossref API endpoint for the given DOI. 
    email : str
        email to be passed to the REST API for the polite pool (optional)

    Methods
    -------
    get_data() -> Dict[str, Any]
        retrieves data from the DOI sent to the Crossref API and returns it as a dictionary
    get_title() -> str
        Retrieves the title from the dictionary.
    get_type() -> str
        Retrieves the document type.
    """

    def __init__(self, doi: str) -> None:
        """
        Constructs all the necessary attributes for the CrossrefAPI object.
        Saves data so that subsequent API calls are not needed for each method

        Parameters
        ----------
        doi : str
            the Digital Object Identifier (DOI) of the work to be retrieved. This should only be the DOI, not the resolver.
        """
        self.doi = doi
        self.url = f"https://api.crossref.org/works/{self.doi}"
        self.data = None

    def get_data(self) -> Dict[str, Any]:
        """
        Retrieves data from the Crossref API and returns it as a dictionary.

        Returns
        -------
        Dict[str, Any]
            a dictionary containing data from the Crossref API
        """
        if self.data is None:
            response = requests.get(self.url)
            if response.status_code != 200:
                raise Exception(f"Response failed with status:{response.status_code}")
            self.data = json.loads(response.text)
        return self.data

    def get_title(self) -> str:
        """
        Retrieves the title from the JSON data retrieved from the Crossref API.

        Returns
        -------
        str
            the title of the work retrieved from the Crossref API
        """
        data = self.get_data()
        try:
            title = data["message"]["title"][0]
            if title:
                return title
            else:
                return "no title"
        except KeyError:
            return None

    def get_type(self) -> str:
        """
        Retrieves the document type from the JSON data. 

        Returns
        -------
        str
            The type of the work assigned to the DOI, such as journal-article, posted-content, etc.
        """
        data = self.get_data()
        try:
            doc_type = data["message"]["type"]
            sub_type = data["message"].get("subtype",None)
            if doc_type:
                return f"{doc_type}:{sub_type}"
            else:
                return "no doc type"
        except KeyError:
            return None
