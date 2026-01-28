# Research_proposal
repository for my research proposal for my dissertation. 
author: Poppy Riddle
Date: March 2025 -> December 2026

### venv
This uses a venv for running the Part3 notebook. 
source part_3_cohere/bin/activate
**You can find this on the local PHD drive, not here in Github as its silly to bring in a venv to a repository** 🤦🏽‍♀️

## Todo:
- [✅] set up requirements.txt file for each notebook
- [✅] update Github repository from local
- [ ] diagram file structure

## Purpose
This repository contains all notebooks from my dissertation. There are three parts. The purpose of this research was to document errors and noise in the title and abstract text of Crossref and OpenAlex metadata and to observe the effects of errors and noise on retrieval-augmented generation (RAG) retrieval and generation. 
### Part 1
Part 1 used a random selection of Crossref DOIs to observe errors and noise in title and abstract text. 
### Part 2 
In this part, I used the same DOIs, but compared OpenAlex metadata for any changes. 
### Part 3
For this part, I utilized two types of error and noise found in parts 1 and 2 to create two perturbed corpora. These were then used as the external knowledge for a golden set of questions with expected responses and context. 

## License
see license file

## Contents

|_ defense_presentation
|_ diagrams
|_ Part_1_data
|_ Part_2_data
|_ part_3_cohere
  |_ Dec_analysis_FINAL
    |_ Round1
    |_ Round2
    |_ Part_3_analysis.ipynb
  |_ reconstruct_abstract
    |_ reconstruct_abstract.py
  |_ corpus.pkl






