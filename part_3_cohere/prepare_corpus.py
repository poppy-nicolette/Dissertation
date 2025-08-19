#prepare_corpus.py
#!user/bin/env/python3
"""
This code prepares a corpus to be used in a RAG application. 
It takes a list of DOIs as input, uses an API call to OpenAlex to 
get the abstract, and then exports each document with the DOI, title, and abstract
as the content. 
The files are saved in a folder as plain text .txt. 
"""
import requests
import time
from reconstruct_abstract import reconstruct_abstract

class PrepareCorpus:
    """
    A class used to retrieve data from OpenAlex and structure a plain text file for each DOI

    Attributes
    ----------
    doi:str
        The Digital Object Identifier (DOI) of the work
    url:str
        the URL of the OpenAlex API endpoint

    Methods
    -------
    get_openalex_data()
        input a DOI of type str. 
        returns a dictionary of DOI, title, abstract
        The abstract is reconstructed using reconstruct_abstract()
    """

    def __init__(self, doi:str)->None:
        """
        Constructs all attributes for the OpenAlex API
        and makes them available to subsequent calls

        Parameters
        ----------
        doi : str
            the Digital Object Identifier
        
        """
        self.doi = doi
        self.url = f"https://api.openalex.org/works?filter=doi:{doi}&select=doi,title,abstract_inverted_index"
        self.data = None


    def get_openalex_data(self) -> dict:
        """
        Used to retrieve data from the OpenAlex API.
        Arg: takes a DOI as a string without the resolver.
        Return: A dictionary of values.

        Note: oa_abstract is reconstructed from the function reconstruct_abstract(). You will need to install
        https://github.com/poppy-nicolette/Bibliometric_tools/tree/7bcb724c95d9f6a571322076a730736097cf5886/reconstruct_abstract

        Example usage
            doi = "10.1234/example"
            data = get_openalex_data(doi)
            print(data)
        """
  
        try:
            result = requests.get(url)

            if result.status_code == 200:
                data = result.json()

                # Parse json data into each element:
                oa_doi = data['results'][0]['doi'].lstrip('https://doi.org/')
                oa_title = data['results'][0]['title']
                oa_abstract_inverted_index = data['results'][0]['abstract_inverted_index']
                # Reconstruct abstract
                oa_abstract = reconstruct_abstract(oa_abstract_inverted_index)

                return {
                    'oa_doi': oa_doi,
                    'oa_title': oa_title,
                    'oa_abstract': oa_abstract,
                    }
            else:
                print(f"Error: Received status code {result.status_code} for DOI {doi}")
                return {'oa_doi':oa_doi,
                        'oa_title':None,
                        'oa_abstract':None}
        except requests.exceptions.RequestException as e:
            print(f"Request failed for DOI {doi}: {e}")
            return {'oa_doi':oa_doi,
                    'oa_title':None,
                    'oa_abstract':None}
        finally:
            # Sleep so that you are below the 10 per second limit or 100k per day.
            time.sleep(0.11)

    #return document for each doi from dictionary 
    def prepare_document(self,x:dict):
        """
        Takes a dictionary of three values as input. 
        Outputs a plain text file
        Input
            dictionary containing oa_doi, oa_title, oa_abstract
        Output
            writes to a text tile
        Returns
            None
        """
        oa_doi = x.get('oa_doi', "None")
        oa_title = x.get('oa_title', "None")
        oa_abstract = x.get('oa_abstract', "None")

        #create file name
        file_name = f"{oa_doi}.txt"

        #write to file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"DOI: {oa_doi}\n")
            file.write(f"Title: {oa_title}\n")
            file.write(f"Abstract: {oa_abstract}\n")

    