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
    get_cited_by() -> int
        Retrieves the is-referenced-by-count value.
    get_abstract() -> str
        Retrives the abstract. 
    get_url() -> str
        Retrieves the URL from the ["message]["resource"]["primary"]["URL"] location

    Usage notes
    -------
    You should use a time.sleep() function in your script between DOIs. 
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
            It includes the subtype as well returning a string that reads like a key:value pair
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

    def get_cited_by(self) -> int:
        """
        Retrieves the is-referenced-by-count value from the dictionary of JSON data

        Returns
        --------
        int
            An integer value that is the count of citations to this DOI from other DOIs in the Crossref database.

        """
        data = self.get_data()
        try:
            cited_by = str(data["message"]["is-referenced-by-count"]) #wrapped in str to change 0 to a string so that it does note equate as None in the next line
            if cited_by:
                return int(cited_by)
            else:
                return None
        except KeyError:
            return None

    def get_abstract(self) -> str:
        """
        This retrieves the abstract from the dictionary from the JSON data.

        Returns
        --------
        str
            Returns a string of the abstract contents from the REST API. 
            Note: You may want to compare this with the XML API call abstract element. The 
            REST API only returns the first abstract in the order it was received from the XML 
            submitted by the publisher to Crossref. The REST API only returns one abstract, but be aware
            that there are possibly other language versions available in the Crossref metadata. 
        """
        data = self.get_data()
        try:
            abstract = data["message"]["abstract"]
            if abstract:
                return abstract
            else:
                return None
        except KeyError:
            return None

    def get_url(self) -> str:
        """
        Retrives the resolution URL from the dictionary of JSON data. This is the URL as publisher provided it to Crossref. 
        Retrieved from the ['message']['resource']['primary']['URL] location. 
        Returns 
        -------
        str
            A string containing the resolution URL for the work. 
        """
        data = self.get_data()
        try:
            url:str = data["message"]["resource"]["primary"]["URL"]
            if url:
                return url
            else:
                return None
        except KeyError:
            return None

    def get_license(self) -> tuple:
        """
        Retrieves the license version and url for a work. 
        It specifically looks for 'vor' or 'unspecified', but does not get licenses for
        other types as these are typically for similarity checking or data mining which usually
        require privileges. 

        Returns
        -------
        A tuple of the version of record and the URL. 
        Example:
        ('vor','https://creativecommons.org/licenses/by/4.0/')
        """
        data = self.get_data()
        # retrieve the license if the content-version = "vor" or "unspecified", return the URL value
        if 'message' in data and 'license' in data['message']:
            licenses = data['message']['license']
            for license in licenses:
                if 'content-version' in license and (license['content-version'] == 'vor' or license['content-version'] == 'unspecified'):
                    version = license['content-version']
                    url = license['URL']
                    print(f"version:{version}")
                    print(f"url: {url}")
                    return (version, url)
        else:
            return (None,None)