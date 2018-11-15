# GenBank Polypodiales Summary Extraction Raw Data Synopsis
______________________________________________
## Purpose

This dataset was created as part of a study conducted by Daria Orlowska (iSchool, University of Illinois)
and Andrea Thomer, PhD (iSchool, University of Michigan) assessing the reproducability and representation of GenBank,
an NIH funded genetic sequence repository.
It was created as part of the Fall 2018 iSchool 590 Open Data Mashups class.

## System Requirements
The final dataset < name_here.csv > was created using Jupyter Notebook using python 3.7.1
Raw data files from GenBank < .xml > and the Catalogue of Life < .txt >
were imported into python and parsed to create an intermediate .csv file. The following
python libraries were used for this step:

- lxml
- bs4

This intermediate .csv file was then read back into python, where data was cleaned and
manipulated to create more columns. The following python libraries were used
for this step:

- pandas
- re

## File Attribution and Collection
**GenBank** summaries were mass-downloaded from Nucleotide as .xml files at Nucleotide at
https://www.ncbi.nlm.nih.gov/. Summaries are authored by individual researchers but
housed by NIH, so there is no restriction on access and reuse is encouraged.
Specifically, data was obtained from the following Orders within GenBank:

| Order         |Total Records   | Download Date    | Keywords Searched       |
| ------------- |:--------------:| ----------------:|------------------------:|
| Ferns         |  96993          | 2018-11-03       |polypodidales \[organism]|

**The Catalogue of Life** lists the distributions of all species within an Order, and can be
downloaded as a .txt file from a bulk downloader: http://www.catalogueoflife.org/DCA_Export/.
Downloads come in .zip file, with information separated by type in different .txt files.
This project only utilizes the .txt file titled “description”, which lists the species
ID and the areas where it occurs.
Specifically, data was obtained from the following source:

- Hassler M. (2018). World Ferns: Checklist of Ferns and Lycophytes of the World (version Apr 2018). In: Roskov Y., Ower G., Orrell T., Nicolson D., Bailly N., Kirk P.M., Bourgoin T., DeWalt R.E., Decock W., Nieukerken E. van, Zarucchi J., Penev L., eds. (2018). Species 2000 & ITIS Catalogue of Life, 30th October 2018. Digital resource at www.catalogueoflife.org/col. Species 2000: Naturalis, Leiden, the Netherlands. ISSN 2405-8858.

The **Standard Country or Area Codes for Statistical Use** (UN Geoscheme), originally published as
Series M, No. 49 and now commonly referred to as the M49 standard, provided geographic
region classifications:  https://unstats.un.org/unsd/methodology/m49/.
It is prepared by the repared by the Statistics Division of the United Nations
Secretariat, and in this project, served as a standard for cleaning locality information
from the previous two sources.

--------------------------------------------------------
## Data Cleaning Assessment
Data cleaning for the previously stated files consists primarily of the following:

1) extracting relevant information contained within summaries into variables,

2) standardizing locality information within the variables according to the standards
put out by the UN GeoScheme,

3) creating new variables based on information contained within the original
extracted variables.

--

Extracting variables was conducted programmatically, in order to replicate
results with multiple datasets. No data cleaning was conducted during this initial
stage. 

Standardizing locality information was done using a dictionary within
python. All special characters, spacing and capitalization were removed so that
small variances would not prevent matches. Locations not presented as countries would appended to the correct region
within the dictionary.

New variables were created based on the raw variables extracted from
GenBank summaries. For example, summaries were grouped into "linked", "unlinked",
and "omitted" based on presence or absence of PubMed IDs and article information.
New variables were also created by splitting original variables, such as splitting
"museum voucher" into "museum ID" and "collection number". Again, this
was done programmatically within python to allow replication on multiple datasets.


-------------------------------------------------------------------
## Variable Descriptions
The following are variable descriptions which function as column headers
in the final < file_name.csv > dataset.

###GenBank_ID
- Description: The GenBank identifier for each submission
- Values: A string consisting of a combination of 8 letters and numbers
- Missing values reason: This value should never be missing   
    - Number of missing values: 0
- Notes: This variable also serves as the primary key

####version
- Description: The version history of the GenBank submission
- Values: An integer, usually ranging from 1 to 3
- Missing values reason: This value should never be missing   
    - Number of missing values: 0 
- Unique values: 1 refers to no versioning (original submission), 2 refers to a new version and the presence of an original submission, ect
- Notes: Version is usually included as part of the GenBank ID, following the period, but for clarity, it has been isolated into its own variable 

####sci_name
- Description: The scientific name of the specimen represented in the GenBank summary
- Values: String
- Missing values reason: This should always be present   
    - Number of missing values: 0?
- Notes: This string usually consists of two phrases referring to the Family and Species. However, sometimes only the Family name is present if the specific Species is unknown (more general), or sometimes the subspecies is present (more specific)

####organism_name
- Description: The common name of the specimen represented in the GenBank summary
- Values: String
- Missing values reason: The common name is not always present in summaries because it is not a required field    
    - Number of missing values: xxx
- Notes: Commmon names can sometimes be linked from the Catalogue of Life, but not all entries contain common names, especially those while are found in non-English speaking countries

####authors
- Description: The authors that have published the article related to the GenBank summary OR who deposited the GenBank record
- Values: String
- Missing values reason: This field should not be blank. Even if an article was not published, this variable should feature the names of the authors who deposited the GenBank record
    - Number of missing values: 0?
- Notes: Author names are in the format last name, first initial, middle initial

####article_title
- Description: The article title that is related with the GenBank summary
- Values: String
- Missing values reason: Articles are not always linked with the GenBank summary or may not exist   
    - Number of missing values: xxx
- Notes: If there was no article associated with the summary, this could contain information found in "article_extra" 

####article_extra
- Description: An additional article title associated with the GenBank summary OR how the GenBank record was deposited
- Values: String
- Missing values reason: If no article was associated with the summary, deposit information might be contained within "article_title"    
    - Number of missing values: xxx
- Unique values: "Direct Submission" is the most common value
- Notes: Unique values only refer to information about how the GenBank record was deposited

####journal
- Description: The journal information where the associated article was published
- Values: String
- Missing values reason: Articles are not always linked with the GenBank summary   
    - Number of missing values: xxx
- Notes: If there was no article associated with the summary, this variable will indicate what author-affliated University or entity deposited the GenBank record

####journal_extra
- Description: The author-affiliated University or entity, in regards to the GenBank record deposit
- Values: String
- Missing values reason: If no article was associated with the summary, this information might be contained within "journal"    
    - Number of missing values: xxx

####doi
- Description: The unique identifier associated with the article
- Values: String (URI)
- Missing values reason: There is not always an article associatedd with the GenBank summary. Also, not all articles contain a persistent identifier    
    - Number of missing values: xxx
- Notes: A DOI is a "digital object identifier", and serves as a persistent identifier for articles, documents, and datasets online

####pubmed_ID
- Description: The unique identifier that links the GenBank summary with the associate article record in PubMed
- Values: Integer, 8 digit
- Missing values reason: There is not always an article associated with the GenBank summary. Even if there is, it isn't always found in PubMed, or it isn't always linked to its PubMed record    
    - Number of missing values: xxx

####linking
- Description: A variable derived from "pubmed_ID", "article_title", "article_extra", "journal", and "journal_extra"
- Values: String
- Missing values reason: This derived variable will never be missing    
    - Number of missing values: 0
- Unique values: linked, unlinked published, unlinked unpublished, unlinked missing 
- Notes: "Linked" refers to the presence of the actual hyperlink that allows visitors to easily access the associated article with the GenBank summary. "Unlinked published" refers to the fact that the associated article has been published (citation information has been included), but a hyperlink has not been provided. "Unlinked unpublished" means that an article title is given, but journal information does not exist (represented by the words "unpublished"). "Unlinked missing" means that no article information has been provided, which either means that it was published long after this deposit, the authors failed to provide it during deposit, or the GenBank record is not included in any publication by the authors that deposited it

####biosample
- Description: A unique identifier that ties the GenBank summary to the database BioSample
- Values: String, a mixture of letters and numbers
- Missing values reason: A GenBank summary is not always tied to a bioSample summary   
    - Number of missing values: xxx
- Notes: The BioSample database contains descriptions of biological source materials used in experimental assays

####bioproject
- Description: A unique identifiers that ties the GenBank summary to the database BioProject
- Values: String, a mixture of letters and numbers
- Missing values reason: A GenBank summary is not always tried to a BioProject
    - Number of missing values: xxx
- Notes: A BioProject is a collection of biological data related to a single initiative, originating from a single organization or from a consortium. A BioProject record provides users a single place to find links to the diverse data types generated for that project (congregates Biosamples)

####museum_ID
- Description: An acronym representing the museum where the specimen voucher associated with the GenBank record is located
- Values: String
- Missing values reason: The specimen used in the GenBank record is not always deposited in a public museum record, or catalogued in a private collection  
    - Number of missing values: xxx
- Notes: This variable is only for associate museums, if a specimen voucher is provided

####collection_ID
- Description: A unique identifier representing the collection containing the specimen associated with the GenBank record
- Values: String, usually a last name and a number
- Missing values reason: Not all specimens are part of a collection, or are deposited in a museum or other repository    
    - Number of missing values: xxx
- Notes: 

####specimen_location <unsure????>
- Description:
- Values:
- Missing values reason:    
    - Number of missing values:
- Unique values:
- Notes:

####location
- Description: Information about where the specimen originated from
- Values: Strings, sometimes geographic coordinates
- Missing values reason: This field is optional, so not all researchers include it    
    - Number of missing values: xxx
- Notes:

####note
- Description: A hodge-podge of values ranging from geographic coordinates to specimen location to species information or links to other records
- Values: Strings
- Missing values reason: This field is optional, so not all researchers include additional information about the specimen    
    - Number of missing values: xxx
- Notes: 


--------------------------------------------------
##License
This work is licensed under a
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)
(CC-BY), which requires attribution.