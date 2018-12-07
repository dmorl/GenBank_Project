# GenBank Polypodiales Summary Extraction Raw Data Synopsis
______________________________________________
## Purpose

This dataset was created as part of a study conducted by Daria Orlowska (iSchool, University of Illinois)
and Andrea Thomer, PhD (iSchool, University of Michigan) assessing the reproducability and representation of GenBank,
an NIH funded genetic sequence repository.
It was created as part of the Fall 2018 iSchool 590 Open Data Mashups class.

## System Requirements
The final dataset < name_here.csv > was created using Jupyter Notebook using python 3.7.1

The raw data files from GenBank polypodiales_download_2018-11-03 was imported in the python script GenBank_Root_fix
in order to add missing root elements. The following python libraries were used for this step:

- lxml (etree)
- lxml.html.soupparser (fromstring)
- bs4 (BeautifulSoup)

This file was then imported into python and the GenBank_ExtractionScript was used to parse through the file and
create an intermediate .csv file: polypodiales_GenBankextraction.csv. The following python libraries were used for
this step:

- lxml (etree)

This intermediate .csv file was then read back into python, and GenBank_toPandas was used to clean and manipulate data.
The following python libraries were used for this step:

- pandas
- re

The CatalogueLife_Distribution_CleanScript was used to import, clean and merge the following Catalogue of Life raw
data files: poly_locationdescription.txt, poly_taxa.txt, poly_vernacular.txt. 
The following python libraries were used for this step:

- pandas
- re

Finally, species names (from the sci_name column in both the Catalogue of Life dataframe and the GenBank dataframe) were
standardized and cleaned using OpenRefine. All the sci_name species names were copied and pasted into an Excel spreadsheet,
where names were de-deplicated within GenBank and across GenBank and the Catalogue of Life. The resulting spreadsheet,
species_openrefine_cluster.xlsx was then imported into OpenRefine where names were standardized. Due to OpenRefine
memory constraints, the dataset was filtered by starting letter to reduce the amount of fields being clustered.
The recipe for these manipulations can be found here <.txt>
The resulting file <.xlsx> was applied to the dataset and used to create more matches betweeen GenBank and the Catalogue
of Life.

## File Attribution and Collection
**GenBank** summaries were mass-downloaded from Nucleotide as INSDSeq_xml files at Nucleotide at
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
- Required
- Source: GenBank
- Description: The GenBank identifier for each submission
- Values: A string consisting of a combination of 8 letters and numbers
- Missing values reason: This value should never be missing   
    - Number of missing values: 0
- Notes: This variable also serves as the primary key; also contains the version

####sci_name
- Required
- Source: GenBank
- Description: The scientific name of the specimen represented in the GenBank summary
- Values: String
- Missing values reason: This should always be present   
    - Number of missing values: 0
- Notes: This string usually consists of two phrases referring to the Family and Species. However, sometimes only the Family name is present if the specific Species is unknown (more general), or sometimes the subspecies is present (more specific)

####common_name
- Optional
- Source: GenBank, Catalogue of Life
- Description: The common name of the specimen. Taken originally from GenBank, missing values supplemented by the Catalogue of Life, whenever applicable.
- Values: String
- Missing values reason: Not all specimens have a common name, or an English common name  
    - Number of missing values: 80362 (before Catalogue of Life merge)

####authors
- Required
- Source: GenBank
- Description: The authors that have published the article related to the GenBank summary OR who deposited the GenBank record
- Values: String
- Missing values reason: This field should not be blank. Even if an article was not published, this variable should feature the names of the authors who deposited the GenBank record
    - Number of missing values: 0
- Notes: Author names are in the format last name, first initial, middle initial

####article_title
- Required
- Source: GenBank
- Description: The article title that is related with the GenBank summary
- Values: String
- Missing values reason: This field should never be empty. Even if articles are not linked with the GenBank summary, this field will contain information about the record instead  
    - Number of missing values: 1 (**this is incorrect**)
- Notes: If there was no article associated with the summary, this field will contain information information about how the GenBank record was deposited (found in "article_extra") 

####article_extra
- Optional
- Source: GenBank
- Description: An additional article title associated with the GenBank summary OR how the GenBank record was deposited
- Values: String
- Missing values reason: If no article was associated with the summary, deposit information might be contained within "article_title"    
    - Number of missing values: 726
- Unique values: "Direct Submission" is the most common value
- Notes: Unique values only refer to information about how the GenBank record was deposited

####journal
- Required
- Source: GenBank
- Description: The journal information where the associated article was published
- Values: String
- Missing values reason: This field should never be empty. Even if article is not linked with the GenBank summary, this field will contain author-affiliated information
    - Number of missing values: 1 (**this is incorrect**)
- Notes: If there was no article associated with the summary, this variable will indicate what author-affliated University or entity deposited the GenBank record

####journal_extra
- Optional
- Source: GenBank
- Description: The author-affiliated University or entity, in regards to the GenBank record deposit
- Values: String
- Missing values reason: If no article was associated with the summary, this information might be contained within "journal"    
    - Number of missing values: 726

####doi
- Optional
- Source: GenBank
- Description: The unique identifier associated with the article
- Values: String (URI)
- Missing values reason: There is not always an article associatedd with the GenBank summary. Also, not all articles contain a persistent identifier    
    - Number of missing values: 16612
- Notes: A DOI is a "digital object identifier", and serves as a persistent identifier for articles, documents, and datasets online

####pubmed_ID
- Optional
- Source: GenBank
- Description: The unique identifier that links the GenBank summary with the associate article record in PubMed
- Values: Integer, 8 digit
- Missing values reason: There is not always an article associated with the GenBank summary. Even if there is, it isn't always found in PubMed, or it isn't always linked to its PubMed record    
    - Number of missing values: 16571

####linking
- Required
- Source: New categorixation
- Description: A variable derived from "pubmed_ID", "article_title", "article_extra", "journal", and "journal_extra"
- Values: Variable
- Missing values reason: This derived variable will never be missing    
    - Number of missing values: 0
- Unique values: linked, unlinked published, unlinked unpublished, unlinked missing 
- Notes: "Linked" refers to the presence of the actual hyperlink that allows visitors to easily access the associated article with the GenBank summary. "Unlinked published" refers to the fact that the associated article has been published (citation information has been included), but a hyperlink has not been provided. "Unlinked unpublished" means that an article title is given, but journal information does not exist (represented by the words "unpublished"). "Unlinked missing" means that no article information has been provided, which either means that it was published long after this deposit, the authors failed to provide it during deposit, or the GenBank record is not included in any publication by the authors that deposited it

####biosample
- Optional
- Source: GenBank
- Description: A unique identifier that ties the GenBank summary to the database BioSample
- Values: String, a mixture of letters and numbers
- Missing values reason: A GenBank summary is not always tied to a bioSample summary   
    - Number of missing values: 31517
- Notes: The BioSample database contains descriptions of biological source materials used in experimental assays

####bioproject
- Optional
- Source: GenBank
- Description: A unique identifiers that ties the GenBank summary to the database BioProject
- Values: String, a mixture of letters and numbers
- Missing values reason: A GenBank summary is not always tried to a BioProject
    - Number of missing values: 31158
- Notes: A BioProject is a collection of biological data related to a single initiative, originating from a single organization or from a consortium. A BioProject record provides users a single place to find links to the diverse data types generated for that project (congregates Biosamples)

####specimen_voucher
- Optional
- Source: GenBank
- Description: A unique identifier that links the specimen in the GenBank record with the physical specimen in a museum or private collection
- Values: String
- Missing values reason: The specimen used in the GenBank record is not always deposited in a public museum record, or catalogued in a private collection  
    - Number of missing values: 4015
- Notes: This variable usually contains the museum ID (usually an acronym representing the museum where the specimen voucher associated with the GenBank record is held) and the collection ID (consisting of the collector's last name and unique numbers representing the collection) 

####collection_date
- Optional
- Source: GenBank
- Description: The date when the specimen was originally collected on
- Values: Date
- Missing values reason: This information might not be available if the record is not linked to a museum voucher, or if the researcher neglected to include it  
    - Number of missing values: 78969
- Note: This information can be valuable in determining what standard was used to obtain specific coordinates

####collected_by
- Optional
- Source: GenBank
- Description: The names of the individuals responsible for finding the specimen
- Values: String
- Missing values reason: This information might not be available if the record is not linked to a museum voucher, or if the researcher neglected to include it  
    - Number of missing values: 78096
- Note: This information should match the specimen_voucher information

####location_country
- Optional
- Source: GenBank
- Description: The country from which the specimen originated from
- Values: String
- Missing values reason: This information might not be avaiable if the specimen was not linked to a specimen_voucher or if the authors neglected to include it    
    - Number of missing values: 63158
- Notes: This was originally the first half of the variable labeled "location". It was divided to better match up with geopolitical areas

####location_specific
- Optional
- Source: GenBank
- Description: The more specific textual information about where the specimen originated from
- Values: String
- Missing values reason: Strings of specific locations are not usually available unless the authors want to provide more detail about the location     
    - Number of missing values: 74006
- Notes: This was originally the second half of the variable labeled "location". It includes locations such as cities, counties, states, islands (that are not countries), and specific places

#####coordinates
- Optional
- Source: GenBank
- Description: Geographic coordinates in the form of latitute, longitude that point to where the specimen originated from
- Values: String
- Missing values reason: Specimen locations are not always provided in terms of specific geographic coordinates     
    - Number of missing values: 80178

####location_specificity
- Required
- Source: New categorixation
- Description: A variable derived from "location_country", "location_specific", and "coordinates"
- Values: Variable
- Missing values reason: This derived variable will never be missing    
    - Number of missing values: 0
- Unique values: broad textual (1), specific texual (2), coordinates (3), missing (999)  
- Notes: Classification of the granularity of locality information in the GenBank record. Includes four choices: coordinates (most granular, 3), specific textual (2), broad textual (1), missing (999). 

####geopolitical_match
- Optional
- Source: GenBank, UN Geoscheme
- Description: The matching geopolitical region to the country where the specimen originated from
- Values: Strings
- Missing values reason: This field will only be filled out if location_country is not blank    
    - Number of missing values: 63158

####record_overlap (may delete)
- Optional?
- Source: GenBank
- Description: This might be where overlap is listed between records --> unsure
- Values: Strings (GenBank ID)
- Missing values reason: Unsure how this is populated (automatically?)  
    - Number of missing values: 0

####note (may delete)
- Optional
- Source: GenBank
- Description: A hodge-podge of values ranging from geographic coordinates to specimen location to species information or links to other records
- Values: Strings
- Missing values reason: This field is optional, so not all researchers include additional information about the specimen    
    - Number of missing values: 60044


--------------------------------------------------
##License
This work is licensed under a
[Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)
(CC-BY), which requires attribution.
