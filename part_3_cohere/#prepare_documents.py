#prepare_documents.py
from prepare_corpus import PrepareCorpus
import os


def main():
    # if folder does not exist, create folder
    folder_to_be_saved = 'data'
    if not os.path.exists(folder_to_be_saved):
        os.makedirs(folder_to_be_saved)

    PrepareCorpus("10.1080/10382046.2011.588505")
    print("all done")

if __name__ == '__main__':
    main()

