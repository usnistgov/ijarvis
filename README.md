# Materials Data Curation System Django apps for https://jarvis.nist.gov/



JARVIS (Joint Automated Repository for Various Integrated Simulations) is a repository designed to automate materials discovery using classical force-field, density functional theory, machine learning calculations and experiments. 

Reference: https://www.nature.com/articles/s41524-020-00440-1

This repo contains necessary codes for several JARVIS apps:

JARVIS-DFT: Density functional theory calculations, http://127.0.0.1:8000/jarvisdft

JARVIS-FF: Force-field evaluations, http://127.0.0.1:8000/jarvisff

JARVIS-ML: Machine-learning predictions, http://127.0.0.1:8000/jarvisml

JARVIS-Hetero: 2D material heterostructure predictions, http://127.0.0.1:8000/jarvish

JARVIS-WTB: Wannier tight-binding predictions, http://127.0.0.1:8000/jarviswtb

JARVIS-BDFT: Beyond DFT calculations, http://127.0.0.1:8000/jarvisbdft  

& Many others ...

Note: The repo uses JARVIS-Tools code from https://github.com/usnistgov/jarvis



# Installation
 See `Installation.md` for WSL Linux

 For other systems: https://cdcs.nist.gov/cdcs-documentation/13.1.1-windows-deployment-via-pypi.html

# Disclaimer 

The NIST Materials Data Curation System (MDCS) provides a means for capturing, sharing, and transforming materials data
into a structured format that is XML based amenable to transformation to other formats. The data are organized using
user-selected templates encoded in XML Schema. These templates are used to create data entry forms. The documents are
saved in a non-relational (NoSQL) database, namely MongoDB. The data can be searched and retrieved by a template-driven
web-based form or by a RESTful API call. The system also enables the interconnection of MDCS repositories for federated
searches.

The software was developed by the National Institute of Standards and Technology (NIST)


The XML-based schemas provided with the Materials Data Curator are examples of schemas that may be written to represent
different aspects of materials data and to demonstrate some of the features that may be used within an XML schema (i.e.
including tabular data or composition selection using the periodic table). The schemas do not represent “standard”
metadata representations and are specifically release as “as is,” and as such NIST makes no warrant of any kind on the
correctness or accuracy of the content of the schemas, nor the fitness of the schemas for any purpose and accepts any
liability or responsibility for the consequences of the schemas use or misuse by anyone.


Also note that not all XML-schemas will load properly within the Materials Data Curator.

Now enabling mirror to GitHub.
