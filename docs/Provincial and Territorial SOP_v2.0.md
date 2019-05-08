![](media/image1.png){width="8.559453193350832in" height="11.4375in"}

**Version Control**

+-------------+-------------+-------------+-------------+-------------+
| **Revision  | **Date of   | **Author(s) | **Brief     | **Baseline  |
| Number**    | Issue**     | **          | Description | Affected?** |
|             |             |             | of Change** |             |
|             |             |             |             | **(Y/N)**   |
+=============+=============+=============+=============+=============+
| 1.1         | January 10, | Kevin       |             | Y           |
|             | 2018        | Ballantyne  |             |             |
+-------------+-------------+-------------+-------------+-------------+
|             |             |             |             |             |
+-------------+-------------+-------------+-------------+-------------+
|             |             |             |             |             |
+-------------+-------------+-------------+-------------+-------------+

Table of Contents {#table-of-contents .ListParagraph .TOCHeading}
=================

[1 Purpose 7](#purpose)

[2 Web Scraping Basics 7](#web-scraping-basics)

[2.1 View Web Page Source HTML 7](#view-web-page-source-html)

[2.2 Page Elements for Extraction 9](#page-elements-for-extraction)

[3 Data Extraction 10](#data-extraction)

[3.1 All Extractions 10](#all-extractions)

[3.1.1 Create CSV File 10](#create-csv-file)

[3.1.2 Retrieve the Page Group's URL(s)
11](#retrieve-the-page-groups-urls)

[3.2 Geoportals 11](#geoportals)

[3.2.1 Description 11](#description)

[3.2.2 Extraction Process 12](#extraction-process)

[3.3 Catalogues 15](#catalogues)

[3.3.1 Description 15](#description-1)

[3.3.2 Extraction Process 16](#extraction-process-1)

[3.4 Web Pages 18](#web-pages)

[3.4.1 Description 18](#description-2)

[3.4.2 Extraction Process 18](#extraction-process-2)

[3.5 Interactive Maps 20](#interactive-maps)

[3.5.1 Description 20](#description-3)

[3.5.2 Extraction Process 20](#extraction-process-3)

[3.6 Map Services 21](#map-services)

[3.6.1 Description 21](#description-4)

[3.6.2 Extraction Process 22](#extraction-process-4)

[3.7 FTP 23](#ftp)

[3.7.1 Description 23](#description-5)

[3.7.2 Extraction Process 23](#extraction-process-5)

[A FGP P/T Web Extractor 25](#fgp-pt-web-extractor)

[A.1 Description 25](#_Toc534968591)

[A.2 Folder Structure 26](#folder-structure)

[A.3 Setup 27](#setup)

[A.3.1 Python Installation 27](#python-installation)

[A.3.2 Installing Python Packages 27](#installing-python-packages)

[A.4 Run Batch File 27](#run-batch-file)

[A.5 Enter Parameters 28](#enter-parameters)

[A.5.1 Province/Territory 28](#provinceterritory)

[A.5.2 Page Group Option 28](#page-group-selection)

[A.5.3 Page Group Arguments 29](#page-group-options)

[A.5.4 Results 30](#results)

[A.5.5 Exiting and Resetting 30](#exiting-and-resetting)

[B Scripts 31](#scripts)

[B.1 Python Packages 31](#python-packages)

[B.1.1 pip 31](#pip)

[B.1.2 Check\_packages.bat 31](#check_packages.bat)

[B.1.3 Install\_packages.bat 31](#install_packages.bat)

[B.1.4 BeautifulSoup 31](#beautifulsoup)

[B.1.5 Selenium 32](#selenium)

[B.1.6 Browsermob-proxy 33](#browsermob-proxy)

[B.1.7 Requests 33](#requests)

[B.1.8 PyPDF 33](#pypdf)

[B.1.9 OpenPyXL 34](#openpyxl)

[B.1.10 XMLtoDict 34](#xmltodict)

[B.2 Functionality 35](#functionality)

[B.3 PT\_WebExtractor 36](#pt_webextractor)

[B.3.1 Cmd Class 36](#cmd-class)

[B.4 Main Extractor Class 36](#_Toc534968618)

[B.4.1 Main Extractor Methods 36](#extractor-methods)

[B.5 PT Extractor Class 39](#pt-extractor-class)

[B.6 Shared.py 39](#shared.py)

[B.6.1 Shared.py Methods 39](#shared.py-functions)

[B.6.2 MyCSV Class 50](#pt_csv-class)

[B.7 Services.py 52](#_Toc534968624)

[B.7.1 MyGeocortex Class 52](#mygeocortex-class)

[B.7.2 MyREST Class 53](#myrest-class)

[B.8 PageGroup Class 53](#_Toc534968627)

[B.8.1 PageGroup Methods 54](#pagegroup-methods)

[B.9 Recurse\_FTP.py 56](#recurse_ftp.py)

[B.9.1 Recurse\_FTP Methods 56](#recurse_ftp-methods)

[C Provincial/Territorial Extractions
57](#provincialterritorial-extractions)

[C.1 Alberta 57](#alberta)

[C.1.1 GeoDiscover Alberta 57](#geodiscover-alberta)

[C.1.2 Open Data Catalogue 59](#open-data-catalogue)

[C.1.3 Interactive Maps 65](#interactive-maps-1)

[C.1.4 Map Services 67](#map-services-1)

[C.2 British Columbia 68](#british-columbia)

[C.2.1 Data Catalogue 68](#data-catalogue)

[C.2.2 Web Pages 69](#web-pages-1)

[C.2.3 Interactive Maps 70](#interactive-maps-2)

[C.2.4 Map Services 78](#map-services-2)

[C.2.5 FTP 79](#ftp-1)

[C.3 Manitoba 79](#manitoba)

[C.3.1 Web Pages 79](#web-pages-2)

[C.3.2 Interactive Maps 106](#interactive-maps-3)

[C.3.3 Map Services 113](#map-services-3)

[C.3.4 Municipal Web Pages 113](#municipal-web-pages)

[C.4 New Brunswick 121](#new-brunswick)

[C.4.1 Web Pages 121](#web-pages-3)

[C.4.2 Interactive Maps 124](#interactive-maps-6)

[C.4.3 Map Services 125](#map-services-4)

[C.5 Newfoundland & Labrador 126](#newfoundland-labrador)

[C.5.1 Open Data Catalogue 126](#open-data-catalogue-2)

[C.5.2 Web Pages 128](#web-pages-4)

[C.5.3 Interactive Maps 130](#interactive-maps-7)

[C.5.4 Web Map Services 132](#web-map-services)

[C.5.5 Municipal Pages 133](#municipal-pages)

[C.5.6 Other Pages 134](#other-pages)

[C.6 Northwest Territories 134](#northwest-territories)

[C.6.1 NWT Discovery Portal 134](#nwt-discovery-portal)

[C.6.2 Web Pages 136](#web-pages-5)

[C.6.3 Interactive Maps 137](#interactive-maps-8)

[C.6.4 Map Services 138](#map-services-5)

[C.7 Nova Scotia 139](#nova-scotia)

[C.7.1 Catalogues 139](#catalogues-1)

[C.7.2 Web Pages 139](#web-pages-6)

[C.7.3 Interactive Maps 144](#interactive-maps-9)

[C.7.4 Geoscience & Mines Branch Interactive Maps
146](#geoscience-mines-branch-interactive-maps)

[C.7.5 Map Services 148](#map-services-6)

[C.8 Nunavut 149](#nunavut)

[C.8.1 Government of Nunavut Community & Government Services Planning &
Lands Division
149](#government-of-nunavut-community-government-services-planning-lands-division)

[C.8.2 Maps & Data - Department of Lands and Resources
150](#maps-data---department-of-lands-and-resources)

[C.8.3 Nunaliit Atlas Framework 152](#nunaliit-atlas-framework)

[C.9 Ontario 153](#ontario)

[C.9.1 Data Catalogue 153](#data-catalogue-1)

[C.9.2 Land Information Ontario 158](#land-information-ontario)

[C.10 Prince Edward Island 161](#prince-edward-island)

[C.10.1 Web Pages 161](#web-pages-7)

[C.10.2 Interactive Maps 163](#interactive-maps-10)

[C.10.3 Map Services 167](#map-services-7)

[C.11 Québec 167](#québec)

[C.11.1 Catalogue d\'Information Géographique Gouvernementale (CIGG)
167](#catalogue-dinformation-géographique-gouvernementale-cigg)

[C.11.2 Géoboutique Québec 169](#géoboutique-québec)

[C.11.3 Données Québec 170](#données-québec)

[C.11.4 Géoinfo Québec 178](#géoinfo-québec)

[C.12 Saskatchewan 179](#saskatchewan)

[C.12.1 Interactive Maps 179](#interactive-maps-11)

[C.12.2 Web Pages/Catalogues 182](#web-pagescatalogues)

[C.12.3 Map Services 188](#map-services-8)

[C.13 Yukon 190](#yukon)

[C.13.1 Geoportal 190](#geoportal)

[C.13.2 Yukon Geological Survey Web Pages
191](#yukon-geological-survey-web-pages)

[C.13.3 Yukon Energy, Mines & Resources Web Pages
193](#yukon-energy-mines-resources-web-pages)

[C.13.4 Other Web Pages 195](#other-web-pages)

[C.13.5 Interactive Maps 195](#interactive-maps-12)

[C.13.6 ArcGIS Hub 197](#arcgis-hub-1)

[C.13.7 Yukon Government Corporate Spatial Warehouse Gallery
198](#yukon-government-corporate-spatial-warehouse-gallery)

[C.13.8 Map Services 199](#map-services-9)

[C.13.9 FTP 199](#ftp-2)

Purpose
=======

> This Standard Operating Procedure (SOP) has been developed to assist
> anyone working on the Federal Geospatial Platform (FGP) project for
> the purpose of extracting the geospatial datasets, web services and
> mapping applications from the provincial and territorial web pages.
> This document provides both generic and specific instructions on how
> to scrape these pages and how to use the FGP P/T Web Extractor tool.

Web Scraping Basics
===================

> All web scraping is done in Python using the BeautifulSoup package (in
> some cases the pages are loaded with Selenium but BeautifulSoup is
> still used for scraping the pages; see Section B.1 for more
> information on the packages used for the extraction process).

View Web Page Source HTML
-------------------------

> Extracting web pages requires looking at the source HTML code of the
> page. In a browser, there are two ways of getting the HTML code:
> viewing the source code or inspecting the page using Development
> Tools.

![H:\\GIS\_Data\\Work\\NRCan\\FGP\\TA001\\view\_source.jpg](media/image2.jpeg){width="6.489583333333333in"
height="5.645833333333333in"}

Figure 2‑1 An example of how to view the page source and inspect in
Chrome by right-clicking on the page.

![](media/image3.png){width="6.5in" height="5.655555555555556in"}

Figure 2‑2 After click Inspect, the Development Tools appear with the
Elements tab.

Page Elements for Extraction
----------------------------

> Web pages are divided into different elements and each element has its
> own attributes. To extract the elements, BeautifulSoup requires the
> element name (tag) and can include the attribute name and its value.
>
> The image below (Figure 2‑3) contains an example of a page's HTML
> source:

1.  The \<body\> element contains an attribute called class which is set
    to "environment-prod". The class attribute can be used for
    extracting a specific element. However, the class value is not
    unique and it can be used for several elements.

2.  On the other hand, the first \<div\> element in the \<body\> has an
    attribute called id and has a value of "header". The id attribute is
    unique to a specific element and is a better option for extraction
    purposes.

3.  Links are contained in the \<a\> (anchor) element. Anchors often
    have an attribute called href which include the URL.

![](media/image4.png){width="6.5in" height="6.044444444444444in"}

Figure 2‑3 Example of a page\'s HTML source code.

Data Extraction
===============

All Extractions
---------------

### Create CSV File

> For all site extractions, the first step is to create and open the CSV
> inventory file. Below is an example of the CSV creation in the Alberta
> extractor script. The CSV file is created using the MyCSV class in the
> shared.py script (for more information on the MyCSV and the shared.py
> script, see Section B.5.2).

  ---------------------------------------------------
  *\# Create the CSV file\
  *csv\_fn = **\"GeoDiscover\_results\"\
  **my\_csv = shared.MyCSV(csv\_fn, self.province)\
  my\_csv.open\_csv()

  ---------------------------------------------------

### Retrieve the Page Group's URL(s)

> The next step is to retrieve the URL, or URLs, for the page group that
> is being extracted. The URLs are stored in the PageGroup object on the
> Extractor (for more information on the PageGroup object, see Section
> B.5.2). In the following example, the script grabs the main\_url URL
> from the current PageGroup.

  -------------------------------------------------------
  *\# Get the service url\
  *main\_url = self.pg\_grp.get\_url(**\'main\_url\'**)

  -------------------------------------------------------

Geoportals
----------

### Description

> The geoportals of the provinces and territories provide access to the
> various geospatial resources in their catalogues. For automatic
> extraction, geoportals offer the ability to query these resources
> using HTML query string. The results are returned either in JSON or
> XML format for easy extraction. Alberta, Northwest Territories,
> Ontario and Yukon are the only jurisdictions which have geoportals as
> of July 30, 2018.

![](media/image5.png){width="6.5in" height="5.655555555555556in"}

Figure 3‑1 Alberta\'s GeoDiscover: An example of a Geoportal

### Extraction Process

#### Querying

> As mentioned above, all geoportals provide the user with the ability
> to query datasets using a URL query string. The query results can be
> returned in either JSON or XML format. For this extraction example,
> the JSON format will be used (only Discovering Ontario's site returns
> XML; see Section C.9.2).
>
> The best way to obtain the URL query for a geoportal is to review the
> Network results of the geoportal for any JSON formatted documents that
> the portal loaded.

-   If necessary, start a search as the portal will query its engine
    using the search parameter.

-   In a browser (in all cases, instructions are given for Chrome),
    click F12 to open the Development Tools window.

-   Once the window appears in the browser, click the Network tab to
    show a table containing all documents which were loaded by the
    geoportal.

    ![](media/image6.png){width="6.971527777777778in" height="3.3125in"}

    Here's an example of a GeoDiscover Alberta URL query:

<https://geodiscover.alberta.ca/geoportal/rest/find/document?contentType=downloadableData,offlineData&f=pjson&start=1&max=10>

> The parameters for this query are:

-   **contentType:** The content types of the datasets to be included in
    the results.

-   **f:** The format for the results (pjson returns a readable JSON
    format).

-   **start:** The starting dataset for the results.

-   **max:** The number of datasets which will be returned in the
    results.

    ![](media/image7.png){width="6.8902777777777775in"
    height="5.510416666666667in"}

Figure 3‑3 An example of a readable JSON (pjson) with the results listed
in \"records\".

> In a Python script, query the geoportal using a URL query string and
> store the JSON results. Construct the query using a set of parameters
> applicable to the required search.
>
> The following code creates a dictionary of the parameters for the
> query URL string. It then uses the build\_query\_html method in the
> shared.py script. It retrieves the JSON formatted results by calling
> the get\_json method in shared.

+------------------------------------------------------------------------+
| *\# Set the parameters for the URL query\                              |
| *params = collections.OrderedDict()\                                   |
| **if** word **is not** None:\                                          |
| params\[**\'searchText\'**\] = word\                                   |
| params\[**\'max\'**\] = **\'5000\'\                                    |
| **params\[**\'f\'**\] = **\'pjson\'\                                   |
| **params\[**\'contentType\'**\] = **\'downloadableData,offlineData\'** |
|                                                                        |
| *\# Build the URL query\                                               |
| *query\_url = shared.build\_query\_html(portal\_url, params)           |
|                                                                        |
| *\# Get the JSON results\                                              |
| *json\_results = shared.get\_json(query\_url)                          |
+------------------------------------------------------------------------+

#### Extract Results

> The next step is to extract the information from the JSON results
> using Python (see 3.7.2.1 for more in depth information about the
> various available methods).

1.  Using the JSON results, grab the "records" listed (see Figure 2‑3).

  ---------------------------------------------
  *\# Get a list of the results\
  *records = json\_results\[**\'records\'**\]

  ---------------------------------------------

2.  Cycle through the results in the list and extract all necessary and
    available values (ex: **Title**, **Description**, **Spatial
    Reference**, etc.). The values are stored as different keys in each
    JSON record.

+------------------------------------------+
| **for** rec **in** records:**\           |
| \                                        |
| ***\# Get the title if it is in records\ |
| ***if \'title\' in** rec:\               |
| title\_str = rec\[**\'title\'**\]\       |
| **else**:\                               |
| title\_str = **\'\'**                    |
|                                          |
| **... ...**                              |
+------------------------------------------+

3.  Write the results for each record to a CSV file (my\_csv).

  ----------------------------------------------
  *\# Add all values to the CSV file object\
  *my\_csv.add(**\'Title\'**, title\_str)\
  my\_csv.add(**\'Description\'**, desc\_str)\
  my\_csv.add(**\'Date\'**, date\_str)\
  ...\
  *\# Write the dataset to the CSV file\
  *my\_csv.write\_dataset()

  ----------------------------------------------

Catalogues
----------

### Description

> The provincial and territorial data catalogues are search engines
> which allow the user to search through their public datasets. The
> searching can be done using the web page's textbox search or using an
> HTML query string. The results are returned as a [Search Engine
> Results
> Pages](https://en.wikipedia.org/wiki/Search_engine_results_page)
> (SERP).

### Extraction Process

#### Build Query String

> The only way to perform a search of any catalogue in Python is using
> an HTML query string. Each catalogue uses different parameter names of
> the query string. In the Alberta example, the following parameters are
> used in Python script:

-   **q:** Filter the results by key word search.

-   **dataset\_type**: Filter the results by the information type (see
    the Information Type list under Refine Results on the page for a
    list of values).

-   **res\_format:** Filter results by format type of the files (see the
    Formats list under Refine Results on the page for a list of values).

  -------------------------------------------------------------------------------------------------------------------
  *\# Set the parameters for the URL query\
  *params = collections.OrderedDict()\
  params\[**\'q\'**\] = word *\# word is the search word\
  *params\[**\'dataset\_type\'**\] = **\"opendata\"\
  **params\[**\'res\_format\'**\] = format *\# format is set to one of the formats in the format list on the page*\
  \
  *\# Build the URL query\
  *query\_url = shared.build\_query\_html(opendata\_url, params)

  -------------------------------------------------------------------------------------------------------------------

> For example, on Alberta's data catalogue web page, the following query
> URL returns open data results with shapefiles:

<https://open.alberta.ca/dataset?dataset_type=opendata&res_format=SHP>

#### Determine Page Count

> Unfortunately, not all the results are displayed on a single page. In
> order to determine the total number of results, the page count must be
> determined first. The page count is usually found at the bottom of the
> page of results. **NOTE**: The result count is often at the top of the
> page, however the HTML element for that result count may not have any
> id or class that can be used for extraction (for example, the result
> count \<div\> on Alberta's data catalogue page only contains a class
> "col-xs-12" which cannot be located easily).
>
> The shared Python script includes a method, called get\_page\_count,
> which will get the page count from the page based on parameters
> provided by the calling script. In the following code, the script
> calls get\_page\_count and passes in:

-   **soup**: The BeautifulSoup object of the page containing the page
    count (first page of results)

-   **element\_type**: The element name to find.

-   **attrb**: The attribute name and value as tuple (or list), ex:
    (\<attr\_name\>, \<attr\_value\>)

-   **sub\_element**: The element type of the buttons.

-   **subtract (optional)**: Number of buttons to subtract to get the
    highest value.

  --------------------------------------------------------------------------------------------------------------
  *\# Get the soup for the query page results\
  *soup = shared.get\_soup(query\_url)\
  \
  *\# Get the page count\
  *page\_count = shared.get\_page\_count(soup, **\'div\'**, \[**\'class\'**, **\'pagination\'**\], **\'li\'**)

  --------------------------------------------------------------------------------------------------------------

#### Retrieve and Extract Each Page

> For each page, here are the steps for extracting its results:

1.  Create the URL query string and get the soup using the current page
    number

  -------------------------------------------------------------------------
  **for** page **in** range(0, page\_count):\
  *\# Open each iteration of pages:\
  ***if** special\_chr == **\"\"**:\
  *\# Some of the search entries can include \"&\" character\
  \# but if an error is returned, use the \"?\" character instead\
  ***try**:\
  page\_url = **\"%s&page=%s\"** % (query\_url, page + 1)\
  special\_chr = **\"&\"\
  except**:\
  page\_url = **\"%s?page=%s\"** % (query\_url, page + 1)\
  special\_chr = **\"?\"\
  else**:\
  page\_url = **\"%s%spage=%s\"** % (query\_url, special\_chr, page + 1)\
  \
  *\# Create the soup object of the current page\
  *page\_soup = shared.get\_soup(page\_url, silent=True)

  -------------------------------------------------------------------------

2.  Gather all the elements which contain each result (in this case all
    the \<div\> tags with class 'dataset-item').

  -----------------------------------------------------------------------------------------------------------
  *\# Get all the datasets on the current page (all datasets are in a \'div\' with class \'dataset-item\')\
  *results = page\_soup.find\_all(**\'div\'**, attrs={**\'class\'**: **\'dataset-item\'**})

  -----------------------------------------------------------------------------------------------------------

3.  If there are no results, let the user know, otherwise go through
    each result element and gather all the information for the CSV file.

+-----------------------------------------------------------------------+
| *\# Let the user know if there are no records\                        |
| ***if** len(results) == 0 **and** record\_count == 0:\                |
| **print \"No records exist with the given search parameters.\"\       |
| print \"URL query sample: %s\"** % query\_url\                        |
| **return** None\                                                      |
| \                                                                     |
| *\# Cycle through each result\                                        |
| ***for** res **in** results:\                                         |
| *\# Start time used to estimate the total length of time\             |
| ***if** time\_count == 0.0:\                                          |
| start\_time = datetime.datetime.now()\                                |
| \                                                                     |
| *\# Used to determine if the result is geospatial or not\             |
| *geo\_data = False\                                                   |
| \                                                                     |
| *\# Get the title of the dataset\                                     |
| *title\_res = res.find(**\'h3\'**, attrs={**\'class\'**:              |
| **\'package-header\'**})\                                             |
| title\_str = title\_res.a.string\                                     |
| **if** title\_str **is** None:\                                       |
| title\_str = **\'\'**                                                 |
|                                                                       |
| ...                                                                   |
|                                                                       |
| *\# Add all values to the CSV file object\                            |
| *my\_csv.add(**\'Title\'**, title\_str)\                              |
| my\_csv.add(**\'Description\'**, desc\_str)\                          |
| my\_csv.add(**\'Date\'**, date\_str)\                                 |
| ...\                                                                  |
| *\# Write the dataset to the CSV file\                                |
| *my\_csv.write\_dataset()                                             |
+-----------------------------------------------------------------------+

Web Pages
---------

### Description

> For extraction purposes, web pages contain links to one or more
> geospatial datasets but have no search capabilities.

### Extraction Process

#### Page Header

> In some cases, the information for the CSV inventory can be found in
> the page's header. All pages contain a \<title\> tag which can be
> extracted if the title references the specific dataset being placed in
> the CSV inventory file (ex: an interactive map's page title). Other
> information, such as the **Description**, **Publisher**, etc. can be
> extracted from the page's \<meta\> tags. The following example (Figure
> 3‑4) shows the header for one of BC's interactive maps
> (<https://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-data-tools/real-time-water-data-reporting>).

![](media/image8.png){width="6.5in" height="6.6in"}

Figure 3‑4 The header section of one of BC\'s web page for an
interactive map

> Use the following code to extract the **Description** from the
> \<meta\> tag:

  ---------------------------------------------------------------------------
  desc = soup.find(**\'meta\'**, attrs={**\'name\'**: **\'description\'**})
  ---------------------------------------------------------------------------

> There is also a method called get\_page\_metadata in the shared.py
> script which will extract all the \<meta\> tags into a dictionary with
> the name as keys and the content as values.

#### Page Contents

> The extraction process of a web page's contents is often unique to
> each site. When extracting a web page, it is important to look at its
> HTML source code to determine which elements contain the information
> for the inventory CSV file (see Section 2 for details on how to scrape
> elements in a page). For specific examples of provincial/territorial
> web pages, see Appendix C.

Interactive Maps
----------------

### Description

> Although there are several types of interactive maps, there are two
> methods for extracting them. Since ArcGIS Online Maps provide more
> details, there is a separate method for extracting them. All other
> interactive maps are extracted in a similar way to the web page
> extraction process.

### Extraction Process

#### ArcGIS Online Maps

> Extracting the data of an ArcGIS Online map requires extracting the ID
> of the map from the URL and using it to access the JSON data of the
> map.
>
> For example, the map URL for **Alberta Interactive Minerals Map** is:
>
> [**http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=cfb4ed4a8d7d43a9a5ff766fb8d0aee5**](http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=cfb4ed4a8d7d43a9a5ff766fb8d0aee5)
>
> The data for this map can be retrieved in JSON format using the ID
> from the map URL. The generic URL for ArcGIS map data is:
>
> **http://\<arcgis\_map\_domain\>/sharing/rest/content/items/\<map\_id\>?f=pjson**
>
> So the data URL for the Alberta Interactive Minerals Map would be:
>
> [**http://ags-aer.maps.arcgis.com/sharing/rest/content/items/cfb4ed4a8d7d43a9a5ff766fb8d0aee5?f=pjson**](http://ags-aer.maps.arcgis.com/sharing/rest/content/items/cfb4ed4a8d7d43a9a5ff766fb8d0aee5?f=pjson)

![](media/image9.png){width="6.489583333333333in"
height="5.197916666666667in"}

Figure 3‑5 The JSON results for the Alberta Interactive Minerals Map
data

> As with the geoportal, the JSON results can be used to extract the
> necessary results in Python. Unlike the geoportal, all information is
> provided by the JSON document. The data includes the **Title**,
> **Type**, **Description**, **Date** and **Licensing** of the map.
> Extraction in Python uses the JSON request call.

#### Other Interactive Maps

> The extraction of other interactive maps is similar to extracting web
> pages. The inventory information can sometimes be found in the
> \<head\> tag of the map page or the contents of the page as well.
> However, in some cases, the information is only available from the
> parent page which contains the link to the map.

Map Services
------------

### Description

> For the provincial/territorial extractions, there are 3 types of map
> services: ArcGIS REST, Geocortex and Web Map Services (WMS).

### Extraction Process

#### ESRI REST Services

##### Query to Get JSON Data

> ESRI REST services can be returned in multiple formats. Again, for
> Python scripting, the best option is JSON format.
>
> The JSON results can be accessed by adding "?f=pjson**" to the service
> URL and subsequent Mapserver URLs.**
>
> **The access\_rest.py script contains a set of methods which will take
> the home page of the service, cycle through each folder and collect
> all the mapservices found under any folders and subfolders.**

##### Extract Results

> As with other JSON results, all necessary information is contained in
> its keys and values.
>
> The following items can be found in the Mapserver JSON data:

-   **Title** (or "mapName" as it appears in the JSON results)

-   **Description** (or "serviceDescription")

-   **Available Formats**

    -   Determined by the type of service:

        -   Mapserver: **KMZ**, **LYR**, **NMF**, **AMF**

        -   Imagerserver: KMZ, LYR

        -   Geometryserver or Featureserver: None

-   **Publisher** (or in this case "Author")

#### Geocortex Services

> The querying and extraction process for Geocortex Services is the same
> as ArcGIS REST Service except that the services are called sites and
> some of the keys in the JSON format have different names.
>
> The following items can be found in the Geocortex JSON data:

-   **Title** (or "displayName" as it appears in the JSON results)

-   **Description** (or "description")

-   **Available Formats** and **Publisher** doesn't apply for Geocortex
    services

#### WMS

> The extraction of a Web Map Service requires using BeautifulSoup's XML
> parser. The XML data of the WMS is obtained by querying the WMS URL.
> To get the XML info, use the "getcapabilities" option in the "request"
> parameter of the query string (ex:
> [https://openmaps.gov.bc.ca/lzt/ows?service=wms&version=1.1.1&**request=getcapabilities**](https://openmaps.gov.bc.ca/lzt/ows?service=wms&version=1.1.1&request=getcapabilities)).
> With the XML data, the inventory information can be found at (although
> these can change depending on the WMS):

-   **Service Type** under \<name\> element

-   **Title** under \<title\> element

-   **Description** under \<abstract\>

-   **Publisher** under \<contactorganization\> element

> If layers exist for the WMS, they will be listed under elements
> \<layer\>.

FTP
---

### Description

> Some provinces have geospatial data on FTP servers which needs to be
> search and extracted for the provincial inventories.

### Extraction Process

> The FTP extraction process requires walking through each folder in the
> FTP server looking for any file extensions that are connected to
> geospatial data (i.e. ".shp", ".tif", etc). The Recurse\_FTP.py script
> has several methods for walking through the FTP site.
>
> Here are the steps for extracting FTP files:

1.  Create a list of valid FTP folders in the root location of the
    server. For British Columbia's FTP site, the list of folders would
    be \[\'/pub/\', \'/sections/\'\] (see Figure 3‑6).

2.  Create a header list for columns in the FTP site for easier
    extraction of the folder information.

> For example, the image below shows the root results for British
> Columbia's FTP <ftp://ftp.geobc.gov.bc.ca/>. The results are listed in
> columns but no header is provided for the columns. Therefore, the
> header list for the folders on this site would be \['date', 'time',
> 'type', 'filename'\] (the header list is not used for files so
> although the file listed below has an extra column for file sizes,
> it's not included in the header list).

![](media/image10.png){width="6.5in" height="2.2159722222222222in"}

Figure 3‑6 The results of BC\'s FTP site showing how the folders and
files are listed

3.  For each folder in the folder list:

    a.  Create a RecFTP object (from the recurse\_ftp.py script) using
        the root domain (without "ftp://"), the current folder and the
        header list.

    b.  Get a list of all files in the current folder and sub-folders
        and add it to a file list.

4.  For each file in the file list, add it to the CSV inventory, parsing
    the filename for the **Title**, **Download**, **Data URL**, etc.

FGP P/T Web Extractor {#fgp-pt-web-extractor .ListParagraph}
=====================

Overview {#overview .ListParagraph}
--------

> The FGP P/T Web Extractor is designed to allow access to all the
> provincial/territorial inventory extractor scripts using a single
> batch file. The Extractor was designed using Python and is accessed
> through the command-prompt.
>
> Before processing, the user is asked to enter the province/territory
> (P/T), a page group and various arguments related to the page group.
> Once the information is entered, the Extractor uses this information
> to extract geospatial data from the various provincial/territorial web
> pages and services.

### Page Groups {#page-groups .ListParagraph}

> The provinces/territories have a large quantity of online resources
> such as web pages, catalogues, FTP sites, portals and services which
> offer geospatial datasets. For the Extractor, these pages are grouped
> into categories depending on their type. For example, British Columbia
> has 6 page groups: Open Data Catalogue, ArcGIS Maps, Interactive Maps,
> FTP Datasets, Map Services, and Web Pages.
>
> In the Extractor, the user is asked to enter a Page Group for
> processing (running all the page groups is an option). Once the
> process is complete, the Page Group creates a CSV file with the
> extracted geospatial datasets. For command-prompt information, see
> Appendix A.5.2)
>
> In Python, each Page Group has its own method which is in the P/T's
> Extractor Class (see Appendix B.4.2.1 for more information).

### Available Arguments {#available-arguments .ListParagraph}

> A Page Group can sometimes contain a set of arguments which the user
> is asked to enter. For example, a catalogue Page Group will often have
> the option to enter a search word argument. Some catalogue Page Groups
> might also have the option to enter a category based on a list of
> available categories. For more information on its use in Python, see
> Appendix B.4.3.

Folder Structure {#folder-structure .ListParagraph}
----------------

> ![](media/image11.jpeg)

  **Folder Name**               **Description**
  ----------------------------- ----------------------------------------------------------------------------------------------------------
  PT\_WebExtractor              Contains the main batch file to run the FGP P/T Web Extractor script.
  batch                         Contains the batch files for all the provinces and for setting up the FGP P/T Web Extractor.
  extras                        Contains extra applications such as merging lists, counting inventories and running the analysis filter.
  files                         Contains files used by the Web Extractor scripts.
  epsg                          Contains CSV files with EPSG codes.
  errors                        Contains error JSON files from the BC Extractor.
  results                       Contains a folder for every province/territory with the CSV inventory results.
  scripts                       Contains the provincial/territorial scripts used by the Web Extractor.
  common                        Contains the Python scripts shared by the provincial/territorial extractor scripts.
  webdrivers                    Contains the webdrivers for Selenium to use.
  browsermob-proxy-2.1.4        Contains the files for the browsermob-proxy package.
  chromedriver\_win32           Contains the driver for Chrome.
  geckodriver-v0.20.0-win64     Contains the driver for Firefox.
  IEDriverServer\_x64\_2.42.0   Contains the driver for Internet Explorer.

Setup {#setup .ListParagraph}
-----

### Python Installation {#python-installation .ListParagraph}

> Before using the FGP P/T Web Extractor, make sure Python 2.7 is
> installed. To verify, in a command-prompt type **ftype Python.File**
> and if a path to the Python executable is return (ex:
> **Python.File=\"C:\\Python27\\ArcGIS10.4\\python.exe\" \"%1\" %\***)
> then the FGP P/T Web Extractor will be able to locate the correct
> install location for Python. If an error is returned, Python probably
> needs to be installed or reinstalled. Contact IT for help on
> installing Python.

### Installing Python Packages {#installing-python-packages .ListParagraph}

> Some extra Python packages need to be installed for the extraction
> process. For the installation steps of these packages, see Section
> B.1.

#### Check Packages {#check-packages .ListParagraph}

> Before installing the Python packages, run the "check\_packages.bat"
> batch file located in the PT\_WebExtractor root folder. This batch
> file will help determine which Python packages need to be installed
> before using FGP P/T Web Extractor.

Run Batch File {#run-batch-file .ListParagraph}
--------------

> The batch file can be run with or without parameters. If no parameters
> are provided, the user will be prompted to enter them before the
> extraction process.

Table A‑1 List of parameters for the FGP P/T Web Extractor

  **Parameter**        **Variable Name**   **Shortcuts**   **Description**
  -------------------- ------------------- --------------- ---------------------------------------------------------------------------------------------------------------------------------------
  Province/Territory   jurisdiction        -j              The name or postal abbreviation (ex: 'ab' for Alberta) of a province or territory.
  Page Group Name      page                -p              The method name of the page group in which to extract (ex: 'maps' will extract all the interactive maps for a province or territory).
  Help                 n/a                 -h              Displays the help for the FGP P/T Web Extractor.

![](media/image12.png){width="6.4375in" height="1.09375in"}

Figure A‑1 The help screen of the FGP P/T Web Extractor

Enter Parameters {#enter-parameters .ListParagraph}
----------------

### Province/Territory {#provinceterritory .ListParagraph}

> The user is first asked to enter the province or territory. Either the
> full name of the province/territory or its postal abbreviation can be
> entered (ex: 'ab' for Alberta).
>
> **NOTE:** This parameter is not case sensitive.

![](media/image13.png){width="6.5in" height="2.6215277777777777in"}

Figure A‑2 Entering the province/territory in the command prompt

### Page Group Selection {#page-group-selection .ListParagraph}

> The second parameter to enter is the page group name of the extraction
> method. In the command prompt, the user is provided with the available
> entries for this parameter in the round brackets. The user can enter
> the entire word or just the capital letter specified in each value. If
> the user wishes to run more than one page group, each value can be
> entered separated by a comma. If the user leaves it blank, the default
> will be used (the value in the square brackets).
>
> **NOTE:** Like the province/territory, this parameter is not case
> sensitive.
>
> Figure A‑3 shows an example of the 5 options of page group names for
> British Columbia.

![](media/image14.png){width="6.125in" height="1.71875in"}

Figure A‑3 Entering the page group name in the command prompt

> Table shows a list of the different scenarios for entering the page
> group name(s) for the Province of British Columbia.

  **Scenario**                                                     **Entry Description**                                                                                                                                             **Entry Example**
  ---------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------
  Extract BC's Open Data Catalogue                                 The user can enter the full name of the page group or just the capital letter of the page group name.                                                             Enter: **catalogue**
                                                                                                                                                                                                                                     Enter: **c**
  Extract BC's Open Data Catalogue, ArcGIS Maps and Map Services   The user can enter the full name or just the capital letter of each page, separating each page group name with a comma. The order of the entry does not matter.   Enter: **catalogue,arcgismaps,services**
                                                                                                                                                                                                                                     Enter: **c,r,s**
  Extract all of BC's pages                                        The user can enter the word 'all' or hit enter, as 'all' is the default value (the value in square brackets).                                                     Enter: **all** or leave it blank

### Page Group Options {#page-group-options .ListParagraph}

> There are several other parameters the user might be prompted to enter
> depending on which page is chosen. The user will not be asked to enter
> all of these parameters every time. For example, the catalogue options
> will only be asked if the user specified a catalogue or open data
> option as the page name.

#### Catalogue Parameters {#catalogue-parameters .ListParagraph}

> When the user selects a geoportal or catalogue page, they will be
> prompted to enter the following depending on which province/territory
> is selected:

-   **Search word**: The results will only include datasets with a given
    search word. This parameter is not case-sensitive.

-   **Format**: The results will only include datasets with a specified
    format such shp, kml, zip, etc. Depending on the site, this option
    is case-sensitive.

-   **Status**: This parameter is for Ontario's catalogues and filters
    the search results by the status of the datasets ('open', 'to be
    opened', etc.).

-   **Data type**: Applies only to BC's catalogue and filters the
    results by the dataset type ('Geographic', 'Dataset', 'Application',
    'WebService')

-   **Downloadable**: Determines whether to filters the results for
    downloadable datasets only.

    ![](media/image15.png){width="6.5in" height="2.9472222222222224in"}

Figure A‑5 An example of the Ontario Open Data Catalogue prompts

### Results {#results .ListParagraph}

> The CSV inventory file will be saved in the respective province folder
> in the "results" folder of the "PT\_WebExtractor" folder.
>
> Ex: For Alberta, the CSV file will be save in
> "PT\_WebExtractor\\results\\Alberta".

### Exiting and Resetting {#exiting-and-resetting .ListParagraph}

> Once processing is finished, the Extractor will go back to prompting
> the user for another province/territory. However, at any point during
> the prompting of parameters, the user can exit the Extractor by typing
> either "quit" or "exit". The prompt process can also be restarted by
> typing "reset".

Scripts {#scripts .ListParagraph}
=======

Python Packages {#python-packages .ListParagraph}
---------------

### pip {#pip .ListParagraph}

> All the packages need pip for installation. Pip does not need to be
> installed as it comes with Python.

#### Verify pip {#verify-pip .ListParagraph}

> In command-prompt, enter **pip**. If an error occurs, it means the
> PATH environment variable is not set to Python's Scripts folder. The
> "Scripts" folder is found under the Python installation (ex:
> C:\\Python27\\Scripts).

### Check\_packages.bat {#check_packages.bat .ListParagraph}

> This batch file will help determine which Python packages need to be
> installed before using the FGP P/T Web Extractor.

### Install\_packages.bat {#install_packages.bat .ListParagraph}

> There is a batch file which can be used to install all the packages
> mentioned below. The install\_packages.bat is found in the root folder
> of the PT\_WebExtractor. This batch file will ask which package to
> install or give the user the option of installing all of the packages.

### BeautifulSoup {#beautifulsoup .ListParagraph}

#### Description {#description-6 .ListParagraph}

> The BeautifulSoup package is required for the extraction of all
> province/territory web pages. BeautifulSoup grabs the source contents
> of a web page and works on all pages that do not have long loading
> times or require Javascript to completely load the page.

#### Installation and Use {#installation-and-use .ListParagraph}

> There is no Windows installer for BeautifulSoup. However,
> BeautifulSoup can be installed using pip.

1.  In a command prompt, enter **pip install beautifulsoup4**.

2.  Once the installation is complete, open Python by typing **python**
    into the command prompt.

3.  Once open, enter **import bs4**.

4.  If no error is returned, Beautifulsoup is ready for use.

> In Python scripts, import Beautifulsoup and its other objects by
> entering:

  ----------------------------------------------------------------------
  **from** bs4 **import** BeautifulSoup, Tag, NavigableString, Comment
  ----------------------------------------------------------------------

#### Documentation {#documentation .ListParagraph}

> The documentation for BeautifulSoup can be found at
> <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>.

#### XML Parser {#xml-parser .ListParagraph}

> For some pages, the XML parser for BeautifulSoup is needed. To install
> the XML parser, enter **pip install lxml** in command-prompt.

### Selenium {#selenium .ListParagraph}

#### Description {#description-7 .ListParagraph}

> Selenium is used to load any web pages that have a long loading time
> or require Javascript to complete the loading process. Selenium opens
> up a browser, Firefox for the extraction processes, and uses the
> browser to fully load the page before obtaining the contents of the
> page. Selenium can also be used to manipulate the page before getting
> the contents, such as clicking on a Javascript button to load more
> contents on the page. However, due to the time it takes to load the
> browser and the page, Selenium should only be used if BeautifulSoup
> cannot obtain the full contents of a page.

#### Installation and Use {#installation-and-use-1 .ListParagraph}

> As with BeautifulSoup, pip can be used to install Selenium. To install
> this package:

1.  In a command prompt, enter **pip install selenium**.

2.  In order to use the different browsers in Selenium, the following
    web drivers are provided under the "webdrivers" folder in the
    PT\_WebExtractor folder:

    -   browsermob-proxy-2.1.4: Folder containing files for a proxy
        which allows access to network information of a web page.

    -   chromedriver\_win32: Folder containing Chrome's web driver
        executable.

    -   geckodriver-v0.20.0-win64: Folder containing Firefox's web
        driver executable.

    -   IEDriverServer\_x64\_2.42.0: Folder containing Internet
        Explorer's files for its web driver.

3.  In order to use these web drivers, their paths must be added to the
    PATH environment variable in Windows. The page
    <https://warwick.ac.uk/fac/sci/dcs/people/research/csrcbc/teaching/howto/javapath/>
    shows how to add a Java path to the PATH environment variable.

    To import and use Selenium in Python, enter the following into a
    script:

  --------------------------------------------------------------------------------
  **from** selenium **import** webdriver\
  **from** selenium.webdriver.common.keys **import** Keys\
  **from** selenium.webdriver.support.ui **import** WebDriverWait\
  **from** selenium.webdriver.support **import** expected\_conditions **as** EC\
  **from** selenium.webdriver.common.by **import** By\
  **from** selenium.common.exceptions **import** TimeoutException\
  **from** selenium.webdriver.firefox.options **import** Options\
  **from** selenium.webdriver.firefox.firefox\_binary **import** FirefoxBinary

  --------------------------------------------------------------------------------

#### Documentation {#documentation-1 .ListParagraph}

> The documentation for Selenium can be found at
> <https://selenium-python.readthedocs.io/>.

### Browsermob-proxy {#browsermob-proxy .ListParagraph}

#### Description {#description-8 .ListParagraph}

> The browsermob-proxy is used to grab the network information of the
> web page.

#### Installation and Use {#installation-and-use-2 .ListParagraph}

> Like the other packages, the browsermob-proxy can be installed using
> pip. In command-prompt, enter **pip install browsermob-proxy**.
>
> Importing this package into Python requires entering the following:

  --------------------------------------------
  **from** browsermobproxy **import** Server
  --------------------------------------------

#### Documentation {#documentation-2 .ListParagraph}

> The documentation for the browsermob-proxy is found at
> <https://browsermob-proxy-py.readthedocs.io/en/stable>.

### Requests {#requests .ListParagraph}

#### Description {#description-9 .ListParagraph}

> Requests provides the ability to send HTTP requests through Python. It
> works in place of the urllib2 package when the urllib2 fails to open a
> page. The Requests package is also used to get JSON requests.

#### Installation and Use {#installation-and-use-3 .ListParagraph}

> Use the pip program to install the Requests package. In a
> command-prompt, enter **pip install requests**.
>
> To import the Requests package into Python, enter the following into
> the script:

  ---------------------
  **import** requests
  ---------------------

#### Documentation {#documentation-3 .ListParagraph}

> The documentation for the Requests can be found at
> <http://docs.python-requests.org/en/master>.

### PyPDF {#pypdf .ListParagraph}

#### Description {#description-10 .ListParagraph}

> The PyPDF gives read and write access to a PDF file. The Province of
> Nova Scotia contains one page with datasets which use PDF files for
> their metadata. This package is used to open the metadata PDF link and
> extract all the necessary information of the inventory.

#### Installation and Use {#installation-and-use-4 .ListParagraph}

> Again, installing PyPDF is done using pip. To install PyPDF:

1.  In a command prompt, enter **pip install pypdf**.

2.  To verify if the installation worked, open Python in the command
    prompt and enter **import pyPdf**.

3.  If no error is returned, the installation was successful.

    In order to import and use pyPdf and its reader and writer objects,
    enter into a script:

  --------------------------------------------------------
  **from** pyPdf **import** PdfFileWriter, PdfFileReader
  --------------------------------------------------------

### OpenPyXL {#openpyxl .ListParagraph}

#### Description {#description-11 .ListParagraph}

> The OpenPyXL package is used to access Excel files in Python. For the
> inventories, this package is used to access the Excel file with the
> updated datasets of the Discovering Ontario portal. The updated file
> is at
> <https://www.sse.gov.on.ca/sites/MNR-PublicDocs/EN/CMID/DataDistributionCatalogue.xlsx>.
>
> OpenPyXL also requires xlsxwriter package.

#### Installation and Use {#installation-and-use-5 .ListParagraph}

> Installing OpenPyXL requires pip. To install OpenPyXL:

1.  In a command prompt, enter **pip install openpyxl**.

2.  Also, to install the xlsxwriter package, enter **pip install
    xlsxwriter**.

3.  To verify if the installations worked, open Python in the command
    prompt and enter **import openpyxl** and then enter **import
    xlsxwriter** on another line.

4.  If no error is returned, the installation was successful.

    In order to import and use OpenPyXL and its reader and writer
    objects, enter into a script:

  ---------------------
  **import openpyxl**
  ---------------------

#### Documentation {#documentation-4 .ListParagraph}

> The documentation for OpenPyXL can be found at
> <https://openpyxl.readthedocs.io/en/stable/>.

### XMLtoDict {#xmltodict .ListParagraph}

#### Description {#description-12 .ListParagraph}

#### Installation and Use {#installation-and-use-6 .ListParagraph}

#### Documentation {#documentation-5 .ListParagraph}

> The documentation for OpenPyXL can be found at

Functionality {#functionality .ListParagraph}
-------------

![](media/image16.jpeg)

Figure B‑1 The flow of the FGP P/T Extractor with the classes

PT\_WebExtractor {#pt_webextractor .ListParagraph}
----------------

> The PT\_WebExtractor script provides access to all the individual
> provincial/territorial extractor scripts. The script uses Python's
> argparse package to facilitate command prompt use (see A.3 for more
> information on how to enter the command-line parameters).

### Cmd Class {#cmd-class .ListParagraph}

> The PT\_WebExtractor contains a class called 'Cmd'. This class
> contains several methods used to hold page group information and also
> help facilitate command prompt entry.

#### Cmd Methods {#cmd-methods .ListParagraph}

> These are the methods for Cmd class as of January 14, 2019.

  []{#_Toc534968618 .anchor}**determine\_pg\_grp**   
  -------------------------------------------------- ---------------------------------------------------------------
  **Description:**                                   Determines which page to extract based on the user\'s answer.
  **Parameters:**                                    **answer:** (Required) The answer given by the user
  **Return:**                                        A list of the proper page objects.

  **get\_arg\_names**   
  --------------------- ----------------------------------------------
  **Description:**      Gets a list of argument names from the pages
  **Parameters:**       None
  **Return:**           A list of argument names

  **get\_pg\_grp\_question**   
  ---------------------------- ---------------------------------------------------------------------------------------
  **Description:**             Gets the question for asking the user which page to extract with the proper shortcuts
  **Parameters:**              None
  **Return:**                  The question with the proper shortcuts (capital letters in the options list).

  **set\_shortcuts**   
  -------------------- ------------------------------------------------------
  **Description:**     Sets the shortcut keys for easier command-line entry
  **Parameters:**      None
  **Return:**          None

Main\_Extractor.py {#main_extractor.py .ListParagraph}
------------------

> The Main\_Extractor.py script contains a set of classes which is used
> by the PT\_WebExtractor, such as the Extractor Class, PageGroup Class,
> Ext\_Arg Class and Ext\_Org Class.

### Extractor Class {#extractor-class .ListParagraph}

> The Main Extractor class contains the methods used by each PT
> Extractor class.

#### Extractor Methods {#extractor-methods .ListParagraph}

> These are the methods that all extractor classes share as of January
> 14, 2019.

  **\_\_init\_\_**   
  ------------------ --------------------------------------
  **Description:**   Initializer for the Extractor class.
  **Parameters:**    None
  **Return:**        None

  **call\_method**   
  ------------------ -----------------------------------------------------------------
  **Description:**   Calls the proper extract method based on the current page group
  **Parameters:**    None
  **Return:**        None

  --------------------------------------------------------------------------------------------------------------
  **check\_result**   
  ------------------- ------------------------------------------------------------------------------------------
  **Description:**    Verifies if the soup is None or contains an error.

  **Parameters:**     **in\_res:** (Required) The input result (soup or other) to check.\
                      **url:** (Optional) The URL of the result object. (default = \'\')\
                      **title:** (Optional) The title for the dataset for the err\_log file. (default = \'\')\
                      **txt:** (Optional) The error text. (default = \'\')\
                      **output:** (Optional) (default = True)

  **Return:**         True if the input is valid and has no errors; False if not.
  --------------------------------------------------------------------------------------------------------------

  **close\_log**     
  ------------------ ----------------------
  **Description:**   Closes the log file.
  **Parameters:**    None
  **Return:**        None

  **get\_arg**       
  ------------------ ----------------------------------------------------------------
  **Description:**   Gets the specified Ext\_Arg object from the list of arguments.
  **Parameters:**    **arg\_name:** (Required)
  **Return:**        None

  **get\_arg\_opts**   
  -------------------- --------------------------------------------------
  **Description:**     Gets a list of options for a specified argument.
  **Parameters:**      **arg\_name:** (Required)
  **Return:**          None

  **get\_arg\_val**   
  ------------------- ------------------------------------------
  **Description:**    Gets the value of a given argument name.
  **Parameters:**     **arg\_name:** (Required)
  **Return:**         None

  **get\_args**      
  ------------------ ------------------------------------------------------
  **Description:**   Gets a list of arguments for the current page group.
  **Parameters:**    None
  **Return:**        None

  **get\_param**     
  ------------------ -----------------------------------------------------
  **Description:**   Gets a parameter from the current page group.
  **Parameters:**    **param:** (Required) The parameter name to extract
  **Return:**        The parameter value

  **get\_pg\_grp**   
  ------------------ -----------------------------------------------
  **Description:**   Gets the current page group of the Extractor.
  **Parameters:**    **pg\_name:** (Optional) (default = None)
  **Return:**        None

  **get\_pg\_grps**   
  ------------------- -------------------------------------------------------------------
  **Description:**    Gets a list of available page group types (ex: cigg, maps, etc.).
  **Parameters:**     None
  **Return:**         A list of page group types.

  **get\_pggrp\_ids**   
  --------------------- -----------------------------------
  **Description:**      Gets a list of the page group IDs
  **Parameters:**       None
  **Return:**           None

  **get\_province**   
  ------------------- ------------------------------------------
  **Description:**    Gets the province name of the extractor.
  **Parameters:**     None
  **Return:**         The province name of the extractor.

  **print\_log**     
  ------------------ -----------------------------------------------------------------------
  **Description:**   Writes a text to the log file.
  **Parameters:**    **txt:** (Required) The string which will be written to the log file.
  **Return:**        None

  **print\_title**   
  ------------------ -----------------------------------------------------------------
  **Description:**   Prints the specified title to the command-prompt with a border.
  **Parameters:**    **title:** (Required) The text with the title.
  **Return:**        None

  **run**            
  ------------------ --------------------------------------------------------
  **Description:**   Runs the extraction methods based on the user\'s input
  **Parameters:**    None
  **Return:**        None

  **set\_args**      
  ------------------ --------------------------------------------------------
  **Description:**   Sets the arguments for the specified page group.
  **Parameters:**    **pg\_grp:** (Required) The current page group object.
  **Return:**        None

  **set\_debug**     
  ------------------ -------------------------------------------------------------------------------------
  **Description:**   Sets the debug value, True if in debug mode.
  **Parameters:**    **debug:** (Required) A boolean determining whether the extractor is in debug mode.
  **Return:**        None

  **set\_notes**     
  ------------------ ------------------------------------------------
  **Description:**   Sets the notes variable to a specified string.
  **Parameters:**    **notes:** (Required) A string for the notes.
  **Return:**        None

  **set\_params**    
  ------------------ -------------------------------------------------------------------------------------------
  **Description:**   Sets the parameters for the extract\_opendata method
  **Parameters:**    **params:** (Required) A dictionary of parameters (keys are the method\'s argument names)
  **Return:**        None

  **set\_pg\_grp**   
  ------------------ -------------------------------------------------------------------
  **Description:**   Sets the ID for the Extractor based on the given page group type.
  **Parameters:**    **pg\_grp\_name:** (Required) The page group type to set the ID.
  **Return:**        None

  **set\_run\_pg\_grps**   
  ------------------------ ----------------------------------------------------------------------------------
  **Description:**         Sets the list of page group IDs for the Extractor based on the list of pg\_grps.
  **Parameters:**          **pg\_grps:** (Required) A list of page groups which will be run.
  **Return:**              None

  **set\_xl**        
  ------------------ -------------------------------------
  **Description:**   Sets the self.xl with boolean value
  **Parameters:**    **xl:** (Required)
  **Return:**        None

  ----------------------------------------------------------------------------------------------------------------------
  **write\_err\_xl**   
  -------------------- -------------------------------------------------------------------------------------------------
  **Description:**     Writes the errors to the Excel spreadsheet.

  **Parameters:**      **pt\_xl:** (Required) The PT\_XL object.\
                       **ws\_name:** (Optional) The worksheet name in which the errors will be added. (default = None)

  **Return:**          None
  ----------------------------------------------------------------------------------------------------------------------

  --------------------------------------------------------------------------------------------
  **write\_error**   
  ------------------ -------------------------------------------------------------------------
  **Description:**   Writes an error line to the error log file.

  **Parameters:**    **url:** (Required) The URL causing the error.\
                     **title:** (Optional) The title of the page. (default = \'\')\
                     **txt:** (Optional) The text to place in the CSV file. (default = \'\')

  **Return:**        None
  --------------------------------------------------------------------------------------------

### PageGroup Class {#pagegroup-class .ListParagraph}

> The PageGroup Class contains the methods and variables for the Page
> Groups containing the web pages of the P/T. For information on Page
> Groups, see Appendix A.1.1.

#### PageGroup Methods {#pagegroup-methods .ListParagraph}

> These are the methods for the PageGroup class as of January 14, 2019.

  -----------------------------------------------------------------------------
  **\_\_init\_\_**   
  ------------------ ----------------------------------------------------------
  **Description:**   The initializer for the PageGroup object.

  **Parameters:**    **title:** (Required) The name/title of the page group.\
                     **id:** (Required) The unique ID for the page group.

  **Return:**        None
  -----------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------------------
  **add\_arg**       
  ------------------ --------------------------------------------------------------------------------------------
  **Description:**   Adds a new argument to the list of arguments for the page group. the page group.

  **Parameters:**    **arg\_name:** (Required) The unique name of the argument being added to\
                     **default:** (Optional) The default value for the argument. (default = None)\
                     **value:** (Optional) The value of the argument. (default = None)\
                     **debug:** (Optional) Determines if the argument is only for debugging. (default = False)\
                     **in\_opts:** (Optional) The available options for the argument. (default = None)\
                     **title:** (Optional) The title of the argument. (default = None)\
                     **required:** (Optional) Determines if the argument is required or not. (default = False)

  **Return:**        None
  ---------------------------------------------------------------------------------------------------------------

  ------------------------------------------------------------------------------
  **add\_url**       
  ------------------ -----------------------------------------------------------
  **Description:**   Adds a web page to the list of URLs.

  **Parameters:**    **url:** (Required) The URL of the web page.\
                     **title:** (Required) The variable title of the web page.

  **Return:**        None
  ------------------------------------------------------------------------------

  **get\_arcgis\_urls**   
  ----------------------- -----------------------------------------------------------------------------
  **Description:**        Gets all the ArcGIS Online URLs besides \"arcgis\".
  **Parameters:**         **other\_word:** (Optional) Provides another search option (default = None)
  **Return:**             A list of ArcGIS URLs.

  **get\_arg**       
  ------------------ -----------------------------------------------
  **Description:**   Gets the argument object with specified name.
  **Parameters:**    **arg\_name:** (Required)
  **Return:**        None

  **get\_args**      
  ------------------ ------------------------------------
  **Description:**   Gets the list of argument objects.
  **Parameters:**    None
  **Return:**        None

  **get\_id**        
  ------------------ ----------------------------------------
  **Description:**   Gets the ID of the current page group.
  **Parameters:**    None
  **Return:**        The ID of the current page group.

  **get\_page\_count**   
  ---------------------- ----------------------------------------------
  **Description:**       Gets the number of pages in this page group.
  **Parameters:**        None
  **Return:**            None

  **get\_title**     
  ------------------ -----------------------------------
  **Description:**   Gets the title of the page group.
  **Parameters:**    None
  **Return:**        The title of the page group.

  **get\_url**       
  ------------------ -------------------------------------
  **Description:**   Gets a URL from the list of URLs.
  **Parameters:**    **param:** (Required) The URL name.
  **Return:**        The URL containing param.

  **get\_url\_list**   
  -------------------- --------------------
  **Description:**     Gets the URL list.
  **Parameters:**      None
  **Return:**          The URL list.

  **get\_urls**      
  ------------------ --------------------------------------------
  **Description:**   Gets a list of the URLs of the page group.
  **Parameters:**    None
  **Return:**        A list of URLs.

  **set\_title**     
  ------------------ ------------------------------------------------------------
  **Description:**   Sets the title of the page group.
  **Parameters:**    **title:** (Required) The title string for the page group.
  **Return:**        None

### Ext\_Arg Class {#ext_arg-class .ListParagraph}

> The Ext\_Arg Class represents one of the arguments within a Page
> Group. It contains all the methods, options and variables for the
> argument. For more information, see Appendix A.1.2.

#### Ext\_Arg Methods {#ext_arg-methods .ListParagraph}

> These are the methods for Ext\_Arg class as of January 14, 2019.

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **\_\_init\_\_**   
  ------------------ -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**   The initializer for the Ext\_Arg class (The default can be a string or a dictionary with the page groups as keys). (It can be a string or a dictionary with page groups as keys).

  **Parameters:**    **arg\_name:** (Required) The argument unique ID.\
                     **pg\_grp:** (Required) The page\_group object of the argument.\
                     **def\_val:** (Optional) The default value(s) of the argument. (default = None)\
                     **val:** (Optional) The specified value(s) of the argument. (default = None)\
                     **debug:** (Optional) The value used for debug mode. (default = False)\
                     **in\_opts:** (Optional) A list of options. (default = None)\
                     **title:** (Optional) The title of the argument. (default = None)\
                     **required:** (Optional) Determines whether the argument is required. (default = False)\
                     **unique:** (Optional) Determines whether the argument is unique. (default = False)

  **Return:**        None
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  -----------------------------------------------------------------------------------------------------------
  **add\_opt**       
  ------------------ ----------------------------------------------------------------------------------------
  **Description:**   Adds an option to the list of options. prompting options.

  **Parameters:**    **name:** (Required) The name of the option being added.\
                     **entry\_opts:** (Optional) The list of options containing the valid (default = \[\])\
                     **url\_tags:** (Optional) The list URL tags. (default = \[\])\
                     **arg\_obj:** (Optional) The argument object. (default = None)\
                     **method:** (Optional) The method/page\_group name. (default = None)

  **Return:**        None
  -----------------------------------------------------------------------------------------------------------

  **get\_default**   
  ------------------ -----------------------------------------
  **Description:**   Gets the default value of the argument.
  **Parameters:**    None
  **Return:**        None

  **get\_name**      
  ------------------ --------------------------------
  **Description:**   Gets the name of the argument.
  **Parameters:**    None
  **Return:**        None

  **get\_opt**       
  ------------------ --------------------------
  **Description:**   Gets the current option.
  **Parameters:**    None
  **Return:**        None

  **get\_opts**      
  ------------------ -----------------------------
  **Description:**   Gets a list of the options.
  **Parameters:**    None
  **Return:**        None

  **get\_pg\_grp**   
  ------------------ ---------------------------------------
  **Description:**   Gets the page\_group of the argument.
  **Parameters:**    None
  **Return:**        None

  **get\_question**   
  ------------------- ------------------------------------------------------------------
  **Description:**    Gets the question for the argument.
  **Parameters:**     **pg\_grp:** (Optional) The page\_group object. (default = None)
  **Return:**         None

  **get\_urltags**   
  ------------------ ------------------------------------
  **Description:**   Gets the URL tags of the argument.
  **Parameters:**    None
  **Return:**        None

  **get\_value**     
  ------------------ ---------------------------------
  **Description:**   Gets the value of the argument.
  **Parameters:**    None
  **Return:**        None

  **is\_debug**      
  ------------------ --------------------------------------------------------
  **Description:**   Determines if the argument is used only for debugging.
  **Parameters:**    None
  **Return:**        None

  **is\_unique**     
  ------------------ -------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**   Determines whether the argument should be asked more than once (if the argument is unique, it will be asked even if it has already been asked).
  **Parameters:**    None
  **Return:**        None

  **set\_default**   
  ------------------ -----------------------------------------
  **Description:**   Sets the default value of the argument.
  **Parameters:**    **def\_val:** (Required)
  **Return:**        None

  **set\_name**      
  ------------------ --------------------------------
  **Description:**   Sets the name of the argument.
  **Parameters:**    **arg\_name:** (Required)
  **Return:**        None

  **set\_opt**       
  ------------------ --------------------------
  **Description:**   Sets the current option.
  **Parameters:**    None
  **Return:**        None

  **set\_opts**      
  ------------------ ---------------------------------------
  **Description:**   Sets a list options for the argument.
  **Parameters:**    **opts:** (Required)
  **Return:**        None

  **set\_pg\_grp**   
  ------------------ ---------------------------------------
  **Description:**   Sets the page\_group of the argument.
  **Parameters:**    **pg\_grp:** (Required)
  **Return:**        None

  **set\_value**     
  ------------------ ----------------------------------------------------------------------
  **Description:**   Determines if the input value is valid and then sets the self.value.
  **Parameters:**    **val:** (Required) The value for the argument.
  **Return:**        None

### Ext\_Opt Class {#ext_opt-class .ListParagraph}

> The Ext\_Opt represents one of the available entry options for an
> argument (Ext\_Arg). If applicable, each Ext\_Arg object has a list of
> Ext\_Opt options.

#### Ext\_Opt Methods {#ext_opt-methods .ListParagraph}

> These are the methods for the Ext\_Opt class as of January 14, 2019.

  -------------------------------------------------------------------------------------------------------------------------------------
  **\_\_init\_\_**   
  ------------------ ------------------------------------------------------------------------------------------------------------------
  **Description:**   The initializer for the Ext\_Opt class. to enter in the command-prompt (will also include the name as a option).

  **Parameters:**    **name:** (Required) The unique option name.\
                     **entry\_opts:** (Optional) The available options for the user (default = \[\])\
                     **url\_tags:** (Optional) The tags used in the URL query. (default = \[\])\
                     **arg\_obj:** (Optional) The parent Ext\_Arg object for the option. (default = None)\
                     **method:** (Optional) The method/page\_group of the argument. (default = None)

  **Return:**        None
  -------------------------------------------------------------------------------------------------------------------------------------

  **get\_arg**       
  ------------------ -----------------------------------------
  **Description:**   Gets the argument of the option object.
  **Parameters:**    None
  **Return:**        None

  **get\_entryopts**   
  -------------------- -----------------------------------
  **Description:**     Gets a list of prompting options.
  **Parameters:**      None
  **Return:**          None

  **get\_method**    
  ------------------ -----------------------------------
  **Description:**   Gets the method/page\_group name.
  **Parameters:**    None
  **Return:**        None

  **get\_name**      
  ------------------ -------------------------------------
  **Description:**   Gets the name of the option object.
  **Parameters:**    None
  **Return:**        None

  **get\_urltags**   
  ------------------ ------------------------------
  **Description:**   Gets a list of the URL tags.
  **Parameters:**    None
  **Return:**        None

  **set\_arg**       
  ------------------ -----------------------------------------
  **Description:**   Sets the argument of the option object.
  **Parameters:**    **arg:** (Required)
  **Return:**        None

  **set\_entryopts**   
  -------------------- -----------------------------------
  **Description:**     Sets a list of prompting options.
  **Parameters:**      **opts:** (Required)
  **Return:**          None

  **set\_method**    
  ------------------ -----------------------------------
  **Description:**   Sets the method/page\_group name.
  **Parameters:**    **method:** (Required)
  **Return:**        None

  **set\_name**      
  ------------------ -------------------------------------
  **Description:**   Sets the name of the option object.
  **Parameters:**    **name:** (Required)
  **Return:**        None

  **set\_urltags**   
  ------------------ --------------------------------
  **Description:**   Sets the list of the URL tags.
  **Parameters:**    **tags:** (Required)
  **Return:**        None

PT Extractor Class {#pt-extractor-class .ListParagraph}
------------------

> Each province/territory contains an Extractor class with its unique
> extraction methods.

BSoup.py {#bsoup.py .ListParagraph}
--------

> The bsoup.py script contains the common functions used when accessing
> BeautifulSoup for the P/T Web Extractor.

### BSoup.py Functions {#bsoup.py-functions .ListParagraph}

> These are the functions for the bsoup.py script as of January 14,
> 2019.

  **clean\_soup**    
  ------------------ ---------------------------------------------------
  **Description:**   Prettifies a soup object.
  **Parameters:**    **soup:** (Required) The unformatted soup object.
  **Return:**        The prettified soup.

  ----------------------------------------------------------------------------
  **find\_parent\_tag**   
  ----------------------- ----------------------------------------------------
  **Description:**        Finds the previous parent tag with the tag\_name.

  **Parameters:**         **tag\_name:** (Required) The tag name to locate.\
                          **init\_element:** (Required)

  **Return:**             The tag with tag\_name.
  ----------------------------------------------------------------------------

  --------------------------------------------------------------------------------------------------------
  **find\_prev\_tag\_containing**   
  --------------------------------- ----------------------------------------------------------------------
  **Description:**                  Finds the previous sibling tag with tag\_name with part of contains.

  **Parameters:**                   **txt:** (Required) Part of the tag name to locate.\
                                    **init\_element:** (Required)

  **Return:**                       The tag with tag\_name.
  --------------------------------------------------------------------------------------------------------

  ---------------------------------------------------------------------
  **find\_tag**      
  ------------------ --------------------------------------------------
  **Description:**   Finds an element with tag\_name, ignoring cases.

  **Parameters:**    **soup:** (Required)\
                     **tag\_name:** (Required)\
                     **attrs:** (Optional) (default = {})

  **Return:**        None
  ---------------------------------------------------------------------

  --------------------------------------------------------------------------------------------------------------------------------
  **find\_tag\_by\_text**   
  ------------------------- ------------------------------------------------------------------------------------------------------
  **Description:**          Finds a tag with exact text in a tag

  **Parameters:**           **soup:** (Required) The soup to search in.\
                            **text:** (Required) The text to find.\
                            **tag\_name:** (Optional) The tag to locate. Default is to search all tags in soup. (default = None)

  **Return:**               The tag containing the text.
  --------------------------------------------------------------------------------------------------------------------------------

  -------------------------------------------------------------------------------------------------------------------------------
  **find\_tags\_by\_id**   
  ------------------------ ------------------------------------------------------------------------------------------------------
  **Description:**         Find tags with id containing the input string.

  **Parameters:**          **soup:** (Required) The soup to search in.\
                           **contains:** (Required) An id string used to located the tag.\
                           **tag\_name:** (Optional) The tag to locate. Default is to search all tags in soup. (default = None)

  **Return:**              None
  -------------------------------------------------------------------------------------------------------------------------------

  ------------------------------------------------------------------------------------------------------------------------------------
  **find\_tags\_containing**   
  ---------------------------- -------------------------------------------------------------------------------------------------------
  **Description:**             Finds a tag with text containing a certain string

  **Parameters:**              **soup:** (Required) The soup to search in.\
                               **contains:** (Required) A string or list of the text to find.\
                               **tag\_name:** (Optional) The tag to locate. Default is to search all tags in soup. (default = None)\
                               **output:** (Optional) Returns a list if output = \'list\'. (default = None)

  **Return:**                  The tag containing the text.
  ------------------------------------------------------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------------
  **find\_xml\_tags**   
  --------------------- -----------------------------------------------------------
  **Description:**      Searches for a tag in an XML soup, ignoring cases.

  **Parameters:**       **xml\_soup:** (Required) The XML soup.\
                        **tag\_names:** (Required)\
                        **attrs:** (Optional) (default = \[\])\
                        **find\_all:** (Optional) (default = False)

  **Return:**           The tag containing the text (or None is no tag is found).
  ---------------------------------------------------------------------------------

  --------------------------------------------------------------
  **find\_xml\_text**   
  --------------------- ----------------------------------------
  **Description:**      Gets the text of a specified XML tag

  **Parameters:**       **xml\_soup:** (Required)\
                        **tag\_name:** (Required)\
                        **attrs:** (Optional) (default = None)

  **Return:**           None
  --------------------------------------------------------------

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **get\_adj\_tags\_by\_text**   
  ------------------------------ -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**               Retrieves the adjacent tags of a tag with a given text (label). This is used for any text in a table with the label proceeding the value. Ex: If a page has an entry like \"Created On: 2018-07-12\", the label will be \"Created On\" and the return value will be \"2018-07-12\".

  **Parameters:**                **soup:** (Required) The soup containing the tag with a specific label.\
                                 **tag:** (Required) The tag name of the label element.\
                                 **label:** (Required) The label text.\
                                 **contains:** (Optional) If true, the method will search for any tag containing the label (default = False)\
                                 **url:** (Optional) (default = None)

  **Return:**                    A list of tags adjacent to any tags with label.
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **get\_adj\_text\_by\_label**   
  ------------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**                Retrieves the adjacent text of a tag with a given text (label). This is used for any text in a table with the label proceeding the value. Ex: If a page has an entry like \"Created On: 2018-07-12\", the label will be \"Created On\" and the return value will be \"2018-07-12\".

  **Parameters:**                 **soup:** (Required) The soup containing the tag with a specific label.\
                                  **tag:** (Required) The tag name of the label element.\
                                  **label:** (Required) The label text.\
                                  **contains:** (Optional) If true, the method will search for any tag containing the label (default = False)\
                                  **url:** (Optional) (default = None)

  **Return:**                     The adjacent text of a tag with label (the first instance found).
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  --------------------------------------------------------------------------------------------
  **get\_adjacent\_cell**   
  ------------------------- ------------------------------------------------------------------
  **Description:**          Gets the adjacent cell (column \<td\>) of a given tag and value.

  **Parameters:**           **value:** (Required) The input text of the element.\
                            **tag:** (Required) The input tag name of the element.\
                            **soup:** (Required) The page\'s soup object.

  **Return:**               The sibling \<td\> of the input tag.
  --------------------------------------------------------------------------------------------

  ----------------------------------------------------------------------------------------------------------
  **get\_dl\_text**   
  ------------------- --------------------------------------------------------------------------------------
  **Description:**    Finds the \<dt\> tage with specified text and returns its corresponding \<dd\> text.

  **Parameters:**     **text:** (Required) The text so search for.\
                      **soup:** (Required) The soup containing the \<dt\> tag.

  **Return:**         The text of the corresponding \<dd\> of the \<dt\> tag.
  ----------------------------------------------------------------------------------------------------------

  **get\_first\_text**   
  ---------------------- --------------------------------------------
  **Description:**       Gets the first text on a page.
  **Parameters:**        **soup:** (Required) The soup of the page.
  **Return:**            The first text on a page.

  -----------------------------------------------------------------------------------------------------------
  **get\_link\_datasets**   
  ------------------------- ---------------------------------------------------------------------------------
  **Description:**          Gets the download links from a page with text in the txt\_vals list. link tags.

  **Parameters:**           **soup:** (Required) The soup contents containing the links.\
                            **txt\_vals:** (Required) A list of strings that are contained in the\
                            **in\_url:** (Required)\
                            **tag\_name:** (Optional) (default = None)

  **Return:**               A list of dictionaries containing the resulting records.
  -----------------------------------------------------------------------------------------------------------

  -----------------------------------------------------------------------------------------------------------------------
  **get\_page\_count**   
  ---------------------- ------------------------------------------------------------------------------------------------
  **Description:**       Gets the number of pages from a specified element on the page

  **Parameters:**        **soup:** (Required) The soup containing the element.\
                         **element\_type:** (Required) The element name to find.\
                         **attrb:** (Required) The attribute name and value as tuple (or list), ex\
                         **sub\_element:** (Required) The element type of the buttons.\
                         **subtract:** (Optional) Number of buttons to subtract to get the highest value. (default = 2)

  **Return:**            The total number of pages.
  -----------------------------------------------------------------------------------------------------------------------

  **get\_page\_metadata**   
  ------------------------- ---------------------------------------------------------------------------------------
  **Description:**          Gets the metadata from the web page and puts them in a dictionary.
  **Parameters:**           **soup:** (Required) The soup of the page.
  **Return:**               A dictionary containing the names of the metadata as keys and the contents as values.

  --------------------------------------------------------------------------------------------------------------------------
  **get\_parent**    
  ------------------ -------------------------------------------------------------------------------------------------------
  **Description:**   Gets the parent element with the given tag and attributes, if applicable.

  **Parameters:**    **soup:** (Required) The soup of the page.\
                     **tag:** (Required) The tag of the parent element.\
                     **attr:** (Optional) A specific attribute name that the parent element will have (ex (default = None)

  **Return:**        The parent element with the given tag.
  --------------------------------------------------------------------------------------------------------------------------

  --------------------------------------------------------------------------------------------------------------------------------------------------
  **get\_soup**      
  ------------------ -------------------------------------------------------------------------------------------------------------------------------
  **Description:**   Retrieves the BeautifulSoup object for a specified web page. ex: (\'class\', \'esriAttribution\')

  **Parameters:**    **url:** (Required) The URL of the web page.\
                     **selenium:** (Optional) Determines whether the page should be open using Selenium or urllib2. (default = False)\
                     **attrb:** (Optional) A tuple containing (\<element attribute name\>, \<element attribute value\>) (default = None)\
                     **delay:** (Optional) For Selenium, the amount of delay in seconds before retrieving the BeautifulSoup object. (default = 2)\
                     **silent:** (Optional) Determines whether statements should be printed. (default = True)\
                     **browser:** (Optional) (default = firefox)

  **Return:**        The BeautifulSoup object containing the web page HTML content.
  --------------------------------------------------------------------------------------------------------------------------------------------------

  **get\_text**      
  ------------------ ----------------------------------------------------
  **Description:**   Gets the text for a given soup and cleans it.
  **Parameters:**    **soup:** (Required) The soup containing the text.
  **Return:**        The clean text from the soup.

  ---------------------------------------------------------------
  **get\_xml**       
  ------------------ --------------------------------------------
  **Description:**   Gets the XML from the URL

  **Parameters:**    **url:** (Required)\
                     **silent:** (Optional) (default = True)\
                     **selenium:** (Optional) (default = False)

  **Return:**        None
  ---------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------------------------------
  **get\_xml\_soup**   
  -------------------- ------------------------------------------------------------------------------------------------------
  **Description:**     Gets the XML BeautifulSoup object of the URL page.

  **Parameters:**      **url:** (Required) The URL of the page containing XML data.\
                       **silent:** (Optional) If true, statements will not be printed to the output. (default = True)\
                       **selenium:** (Optional) Determines whether to use Selenium when opening the page. (default = False)

  **Return:**          A BeautifulSoup object of the page.
  ---------------------------------------------------------------------------------------------------------------------------

  ----------------------------------------------------------------------------------------
  **parse\_dl**      
  ------------------ ---------------------------------------------------------------------
  **Description:**   Parses a \<dl\> list

  **Parameters:**    **dl:** (Required) The \<dl\> soup contents.\
                     **parsed\_dl:** (Optional) The parsed DL contents. (default = None)

  **Return:**        The parsed DL contents.
  ----------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------------------------
  **walk\_dl**       
  ------------------ --------------------------------------------------------------------------------------------------
  **Description:**   Walks through a \<dl\> list.

  **Parameters:**    **dl:** (Required) A soup \<dl\> element.\
                     **results:** (Optional) The results of the previous recursive method. (default = OrderedDict())\
                     **level:** (Optional) The current level in the list. (default = 0)

  **Return:**        :return:
  ---------------------------------------------------------------------------------------------------------------------

  -----------------------------------------------------------------
  **xml\_to\_dict**   
  ------------------- ---------------------------------------------
  **Description:**    Convert an XML page to JSON format

  **Parameters:**     **xml\_url:** (Required)\
                      **selenium:** (Optional) (default = False)\
                      **silent:** (Optional) (default = True)

  **Return:**         None
  -----------------------------------------------------------------

Shared.py {#shared.py .ListParagraph}
---------

> The shared.py script contains all the general functions which are
> shared between all the provincial/territorial extractors

### Shared.py Functions {#shared.py-functions .ListParagraph}

> These are the functions for shared.py script as of January 14, 2019.

  **check\_page**    
  ------------------ --------------------------------------------------
  **Description:**   Checks to see if a page can open with no errors.
  **Parameters:**    **url:** (Required) The URL of the page to load.
  **Return:**        True if the page loads with no errors.

  **clean\_table**   
  ------------------ ---------------------------------------------------------------------------
  **Description:**   Fixes any issues in a table such as completing at \<tr\> tag with \</tr\>
  **Parameters:**    **table:** (Required) The input table element.
  **Return:**        A fixed table element.

  **clean\_text**    
  ------------------ --------------------------------------------------------------------
  **Description:**   Removes all whitespaces from txt.
  **Parameters:**    **txt:** (Required) The string in which to remove all whitespaces.
  **Return:**        The string with no whitespaces.

  -------------------------------------------------------------------------------------------------
  **create\_wkt\_extents**   
  -------------------------- ----------------------------------------------------------------------
  **Description:**           Creates the WKT extents from two points

  **Parameters:**            **ext:** (Required) A tuple or list with (north, south, east, west)\
                             **in\_epsg:** (Optional) (default = None)\
                             **in\_wkt:** (Optional) (default = None)

  **Return:**                None
  -------------------------------------------------------------------------------------------------

  **epsg\_to\_spatref**   
  ----------------------- ----------------------------------------------------
  **Description:**        Converts a EPSG code to its coordinate system name
  **Parameters:**         **epsg\_code:** (Required) The EPSG code
  **Return:**             The name of the coordinate system

  -------------------------------------------------------------------------------------------------------------------
  **estimate\_time**   
  -------------------- ----------------------------------------------------------------------------------------------
  **Description:**     Estimates the amount of time for an extraction process.

  **Parameters:**      **start\_time:** (Required) The start time of the process.\
                       **rec\_count:** (Required) The total number of records.\
                       **rec\_idx:** (Optional) The number of records up to the call of this method. (default = 10)

  **Return:**          The estimated time as a datetime object.
  -------------------------------------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------
  **filter\_unicode**   
  --------------------- -----------------------------------------------------------------
  **Description:**      Replaces unicode characters with corresponding ascii characters

  **Parameters:**       **in\_str:** (Required) The input unicode string.\
                        **out\_type:** (Optional) (default = None)\
                        **french:** (Optional) (default = False)\
                        **all:** (Optional) (default = False)

  **Return:**           None
  ---------------------------------------------------------------------------------------

  **find\_duplicates**   
  ---------------------- ------------------------------------------------
  **Description:**       Finds the indices of all the duplicate entries
  **Parameters:**        **in\_rows:** (Required)
  **Return:**            None

  -------------------------------------------------------------------------------
  **format\_date**   
  ------------------ ------------------------------------------------------------
  **Description:**   Formats a date string to a specified format or yyyy-mm-dd.

  **Parameters:**    **in\_date:** (Required)\
                     **out\_format:** (Optional) (default = %Y-%m-%d)

  **Return:**        None
  -------------------------------------------------------------------------------

  -------------------------------------------------------------------------------
  **ftp\_files**     
  ------------------ ------------------------------------------------------------
  **Description:**   Gets a list of files from an FTP URL.

  **Parameters:**    **url:** (Required) The FTP URL which contains the files.\
                     **ftp:** (Required) An FTP object.

  **Return:**        A list of files.
  -------------------------------------------------------------------------------

  --------------------------------------------------------------------------------------
  **get\_anchor\_url**   
  ---------------------- ---------------------------------------------------------------
  **Description:**       Joins the link text from an anchor with its page\'s root URL.

  **Parameters:**        **root\_url:** (Required) The root URL of the page.\
                         **anchor:** (Required) The anchor tag.

  **Return:**            The full URL link.
  --------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------
  **get\_arcgis\_data**   
  ----------------------- ---------------------------------------------------
  **Description:**        Extracts the information from ArcGIS Online data.

  **Parameters:**         **map\_url:** (Required) The ArcGIS Map URL\
                          **title\_prefix:** (Optional) (default = None)\
                          **pre\_info:** (Optional) (default = None)

  **Return:**             A dictionary containing the ArcGIS data.
  ---------------------------------------------------------------------------

  **get\_arcgis\_gallery**   
  -------------------------- ------------------------------------------------------
  **Description:**           Gets all the maps on a ArcGIS Gallery page.
  **Parameters:**            **gallery\_url:** (Required) The ArcGIS Gallery URL.
  **Return:**                A list of dictionaries of ArcGIS map data.

  -----------------------------------------------------------------------------------------------------------------------------------------
  **get\_arcgis\_url**   
  ---------------------- ------------------------------------------------------------------------------------------------------------------
  **Description:**       Gets the specified ArcGIS URL from the given ArcGIS URL (values: \'data\', \'overview\', \'webmap\', \'viewer\')

  **Parameters:**        **url:** (Required) The initial ArcGIS URL.\
                         **link\_type:** (Optional) Determines the type of ArcGIS to return. (default = data)

  **Return:**            The specified ArcGIS URL.
  -----------------------------------------------------------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------
  **get\_bracket\_text**   
  ------------------------ --------------------------------------------------------------
  **Description:**         Gets the text between two round brackets.

  **Parameters:**          **txt:** (Required) The input text containing the brackets.\
                           **bracket:** (Optional) (default = ()\
                           **beg:** (Optional) (default = 0)

  **Return:**              The text between the brackets.
  ---------------------------------------------------------------------------------------

  **get\_data\_type**   
  --------------------- ----------------------------------------------------------
  **Description:**      Gets the data type based on the file extension of a URL.
  **Parameters:**       **url:** (Required) The data URL.
  **Return:**           The data type of the URL.

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **get\_download\_text**   
  ------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**          Sets the download string and access string based on the formats. Ex: If no formats exist, then the download string is \'No\' and the access string is \'Contact the Province\'. If only one format exists, then the download string is the download URL and access is \'Download/Web Accessible\'. If more than one format exists, then the download string is \'Multiple Downloads\' and the access string is \'Download/Web Accessible\'. It can either be a list or a string.

  **Parameters:**           **formats:** (Optional) A list of the formats for the dataset. (default = \[\])\
                            **download\_url:** (Optional) The download URL, if applicable. (default = \'\')\
                            **date:** (Optional) The date, if applicable. It can either be a list or a string. (default = \'\')

  **Return:**               The download sting and access string (see above).
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ----------------------------------------------------------------------------------------------------------------
  **get\_driver**    
  ------------------ ---------------------------------------------------------------------------------------------
  **Description:**   Gets the Selenium driver based on the specified browser name.

  **Parameters:**    **browser:** (Optional) The name of the browser (firefox, chrome, ie). (default = firefox)\
                     **headless:** (Optional) (default = True)

  **Return:**        The Selenium driver.
  ----------------------------------------------------------------------------------------------------------------

  **get\_ftp**       
  ------------------ ----------------------------------
  **Description:**   Sets up an FTP object using URL.
  **Parameters:**    **url:** (Required) The FTP URL.
  **Return:**        An FTP object.

  **get\_header**    
  ------------------ ---------------------------------
  **Description:**   Gets the header from a CSV file
  **Parameters:**    **csv\_lines:** (Required)
  **Return:**        None

  **get\_home\_folder**   
  ----------------------- --------------------------------------------------------
  **Description:**        Gets the top folder location of the FGP\_WebExtractor.
  **Parameters:**         None
  **Return:**             The folder location of the Web Extractor.

  -------------------------------------------------------------------
  **get\_json**      
  ------------------ ------------------------------------------------
  **Description:**   Gets the JSON of a specified URL.

  **Parameters:**    **url:** (Required) The URL of the JSON data.\
                     **silent:** (Optional) (default = True)\
                     **timeout:** (Optional) (default = 10)\
                     **attempts:** (Optional) (default = 1)

  **Return:**        JSON formatted string.
  -------------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------
  **get\_key**       
  ------------------ --------------------------------------------------------------------------------
  **Description:**   A recursive algorithm that returns the item in a JSON text with a certain key.

  **Parameters:**    **key:** (Required) The key to search for.\
                     **json\_dict:** (Required) A JSON dictionary.

  **Return:**        Returns the item with the specified key
  ---------------------------------------------------------------------------------------------------

  -----------------------------------------------------------------------------
  **get\_link**      
  ------------------ ----------------------------------------------------------
  **Description:**   Gets the link from the anchor in the HTML code

  **Parameters:**    **html:** (Required) The HTML code containing the link.\
                     **url:** (Optional) (default = None)

  **Return:**        The full URL of the link
  -----------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **get\_network\_traffic**   
  --------------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**            Gets a list of the files loaded for a web page. ex: (\'class\', \'esriAttribution\') JSON Ex: { log: { entries: \[ { request: { url: http://www.arcgis.com/ } }, { }, \... \] } }

  **Parameters:**             **url:** (Required) The web page URL to load.\
                              **attrb:** (Required) A tuple containing (\<element attribute name\>, \<element attribute value\>)\
                              **delay:** (Optional) The delay, in seconds, to wait until scraping the page. (default = 2)\
                              **silent:** (Optional) (default = True)

  **Return:**                 A list of files loaded by the web page.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  ------------------------------------------------------------------------------------------------------------------------------
  **get\_network\_urls**   
  ------------------------ -----------------------------------------------------------------------------------------------------
  **Description:**         Gets a list of the files loaded for a web page. ex: (\'class\', \'esriAttribution\')

  **Parameters:**          **url:** (Required) The web page URL to load.\
                           **attrb:** (Required) A tuple containing (\<element attribute name\>, \<element attribute value\>)\
                           **delay:** (Optional) The delay, in seconds, to wait until scraping the page. (default = 2)

  **Return:**              A list of the entries in the page\'s network information.
  ------------------------------------------------------------------------------------------------------------------------------

  ------------------------------------------------------------------------------------------------------------------------
  **get\_post\_query**   
  ---------------------- -------------------------------------------------------------------------------------------------
  **Description:**       Builds a URL query string using a dictionary of parameters and values

  **Parameters:**        **form\_data:** (Required) A dictionary containing parameters and values for the query string.\
                         **url:** (Required) The base URL which the query string will be added to.

  **Return:**            A string of the query URL.
  ------------------------------------------------------------------------------------------------------------------------

  **get\_pt\_abbreviation**   
  --------------------------- -------------------------------------------------------
  **Description:**            Gets the provincial/territorial 2-letter abbreviation
  **Parameters:**             **pt:** (Required)
  **Return:**                 None

  **get\_pt\_folders**   
  ---------------------- ----------------------------------------------
  **Description:**       Gets a list of the paths for the P/T results
  **Parameters:**        **juris:** (Optional) (default = None)
  **Return:**            None

  **get\_pt\_name**   
  ------------------- ------------------------------------------------------------
  **Description:**    Gets the province name based on the 2-letter abbreviation.
  **Parameters:**     **pt\_abbrev:** (Required)
  **Return:**         None

  --------------------------------------------------------------------------------------------------
  **get\_request**   
  ------------------ -------------------------------------------------------------------------------
  **Description:**   Gets a URL request with specified form\_data.

  **Parameters:**    **url:** (Required) The URL for the request\
                     **form\_data:** (Required) A dictionary of form data for the request.\
                     **headers:** (Optional) A list of headers for the request. (default = None)\
                     **silent:** (Optional) (default = True)

  **Return:**        A tuple containing the text of the request results and the request query URL.
  --------------------------------------------------------------------------------------------------

  **get\_results\_folder**   
  -------------------------- --------------------------------------
  **Description:**           Gets the path of the results folder.
  **Parameters:**            **pt:** (Optional) (default = None)
  **Return:**                None

  **get\_service\_url**   
  ----------------------- --------------------------
  **Description:**        Gets the base server URL
  **Parameters:**         **url:** (Required)
  **Return:**             None

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **get\_spatialref**   
  --------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**      Locates the spatialReference item in a JSON formatted text. If the spatial reference contains \'wkid\', then the text is formatted with \"(WKID: \<wkid\>) \<spatial reference\>\".

  **Parameters:**       **json\_dict:** (Required) The JSON dictionary.\
                        **sp\_key:** (Optional) The spatial reference key to locate. (default = None)

  **Return:**           A formatted string of the spatial reference.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **info\_to\_dict**   
  -------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**     Converts a table with a list of information to a dictionary: Ex Table: Citation Information: \<- the heading Title: DP ME 002, Version 11, 2016, Nova Scotia Mineral Occurrence Database Originator: G. A. O\'Reilly , G. J. Demont , J. C. Poole , B. E. Fisher Date: March 2016 \... for the column \<td\>. ex: (\'class\', \'esriAttribution\')

  **Parameters:**      **table:** (Required) The \<table\> element.\
                       **text\_only:** (Optional) Return only text. (default = False)

  **Return:**          Returns a dictionary of the items in the table.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  -------------------------------------------------------------------------------------------------------------------------------------------------------
  **open\_selenium\_page**   
  -------------------------- ----------------------------------------------------------------------------------------------------------------------------
  **Description:**           Opens a page using Selenium and waits until a specific element is loaded on the page. ex: (\'class\', \'esriAttribution\')

  **Parameters:**            **url:** (Required) The URL of the page to load.\
                             **attrb:** (Required) A tuple containing (\<element attribute name\>, \<element attribute value\>)\
                             **delay:** (Optional) The delay, in seconds, to wait until the contents is grabbed from the page. (default = 2)\
                             **silent:** (Optional) If True, nothing will be printed. (default = True)\
                             **browser:** (Optional) The browser name used to open the page. (default = firefox)

  **Return:**                The contents of the page after the element (attrb) has been loaded.
  -------------------------------------------------------------------------------------------------------------------------------------------------------

  ---------------------------------------------------------------------------------------------------------------------------------------------
  **open\_selenium\_wait**   
  -------------------------- ------------------------------------------------------------------------------------------------------------------
  **Description:**           Opens a page using Selenium and waits explicitly for the number of seconds of delay.

  **Parameters:**            **url:** (Required) The URL of the page to load.\
                             **delay:** (Optional) The delay, in seconds, to wait until the contents is grabbed from the page. (default = 2)\
                             **silent:** (Optional) If True, nothing will be printed. (default = True)\
                             **browser:** (Optional) The browser name used to open the page. (default = firefox)

  **Return:**                The contents of the page after waiting to load.
  ---------------------------------------------------------------------------------------------------------------------------------------------

  **open\_webpage**   
  ------------------- ------------------------------------------------------------------------------
  **Description:**    Opens a web page using urllib2
  **Parameters:**     **url:** (Required) The URL of the page to open.
  **Return:**         If an error occurs, return None, otherwise return the page\'s HTML contents.

  -------------------------------------------------
  **output\_json**   
  ------------------ ------------------------------
  **Description:**   Outputs JSON data to a file.

  **Parameters:**    **out\_fn:** (Required)\
                     **in\_json:** (Required)

  **Return:**        None
  -------------------------------------------------

  **parse\_csv\_row**   
  --------------------- ----------------------------------------
  **Description:**      Divides at quotes CSV line into a list
  **Parameters:**       **in\_row:** (Required)
  **Return:**           None

  **parse\_query\_url**   
  ----------------------- -------------------------------------------
  **Description:**        Retrieves the base URL of a query string.
  **Parameters:**         **url:** (Required) The URL query string.
  **Return:**             The base URL.

  ------------------------------------------------------------------------
  **print\_oneliner**   
  --------------------- --------------------------------------------------
  **Description:**      Prints the msg to the command-prompt in one line

  **Parameters:**       **msg:** (Required) The message to print.\
                        **leading:** (Optional) (default = \*\*\*\*)

  **Return:**           None
  ------------------------------------------------------------------------

  **process\_duplicates**   
  ------------------------- -----------------------------------
  **Description:**          Finds duplicates and merges them.
  **Parameters:**           **in\_rows:** (Required)
  **Return:**               None

  **query\_to\_dict**   
  --------------------- ----------------------------------------------------------------------------
  **Description:**      Converts a query URL string into a dictionary of its parameters and values
  **Parameters:**       **url:** (Required) The URL with the query string.
  **Return:**           A dictionary with the parameters of the query string as keys.

  -------------------------------------------------------------------------------------------------------------------------------
  **reduce\_text**   
  ------------------ ------------------------------------------------------------------------------------------------------------
  **Description:**   Reduces the description text to 100 characters.

  **Parameters:**    **in\_text:** (Required)\
                     **tag\_names:** (Optional) The tag name in an HTML description with the description text. (default = None)

  **Return:**        The edited description.
  -------------------------------------------------------------------------------------------------------------------------------

  **remove\_duplicates**   
  ------------------------ -------------------------------------
  **Description:**         Removes duplicates by merging them.
  **Parameters:**          **in\_lst:** (Required)
  **Return:**              None

  **sort\_fields**   
  ------------------ -------------------------------------------------------
  **Description:**   Sorts a list of header fields in a specified order.
  **Parameters:**    **in\_flds:** (Required) A list of headers for fields
  **Return:**        A list of the sorted headers.

  **soup\_php**      
  ------------------ ----------------------------------
  **Description:**   Soups up a PHP URL.
  **Parameters:**    **url:** (Required) The PHP URL.
  **Return:**        A soup object.

  **split\_upper**   
  ------------------ --------------------------------------------------------
  **Description:**   Splits a string at its capital letters
  **Parameters:**    **word:** (Required) A string with capital letters.
  **Return:**        A string with spaces in front of every capital letter.

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **table\_to\_dict**   
  --------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Description:**      Converts a spreadsheet table to a dictionary. Example Table: Title Orginator Date \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-- DP ME 002 G. A. O\... March 2016 DP ME 154 B. E. Fisher 2006 \...

  **Parameters:**       **table:** (Required) A soup object containing the table.\
                        **header\_row:** (Optional) The row number which contains the header info. (default = None)\
                        **header:** (Optional) A list of header values in case none exist in the table. (default = None)\
                        **text\_only:** (Optional) Determines whether only to return the text of the table and not the HTML code. (default = False)\
                        **start\_row:** (Optional) The row number in which to start collecting the data. (default = 0)

  **Return:**           A list of rows, each containing a dictionary with the header as keys.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  **translate\_date**   
  --------------------- -------------------------------------------------
  **Description:**      Converts a timestamp value to a formatted date.
  **Parameters:**       **tmestmp:** (Required) The input timestamp.
  **Return:**           A formatted date based on the timestamp.

  ------------------------------------------------------------------------------------------------------------------
  **wait\_page\_load**   
  ---------------------- -------------------------------------------------------------------------------------------
  **Description:**       Implements a wait command for a selenium driver

  **Parameters:**        **driver:** (Required) The selenium drive object.\
                         **attr\_type:** (Required) The attribute type to wait to load (By.ID or By.CLASS\_NAME).\
                         **attr\_name:** (Required) The attribute value that must be loaded before proceeding.\
                         **delay:** (Optional) The number of seconds the driver should wait. (default = 10)\
                         **silent:** (Optional) (default = True)

  **Return:**            None
  ------------------------------------------------------------------------------------------------------------------

  **wkid\_to\_spatref**   
  ----------------------- -------------------------------------------------------------------------
  **Description:**        Converts a WKID value to a spatial reference text using two JSON files.
  **Parameters:**         **wkid:** (Required) The WKID spatial reference value.
  **Return:**             A string of the spatial reference with the WKID in brackets.

Spreadsheet.py {#spreadsheet.py .ListParagraph}
--------------

> The spreadsheet.py script contains the functions and classes used in
> the creation of both CSV files and Excel Spreadsheets.

### Spreadsheet Function {#spreadsheet-function .ListParagraph}

This is the function for the spreadsheet.py script as of January 14,
2019.

  **get\_header\_info**   
  ----------------------- --------------------------------------------------------
  **Description:**        This method contains the different header information.
  **Parameters:**         **out\_type:** (Optional) (default = pt)
  **Return:**             None

### PT\_CSV Class {#pt_csv-class .ListParagraph}

> The PT\_CSV class contains methods for creating and editing the CSV
> inventory file for the provinces/territories.

#### PT\_CSV Methods {#pt_csv-methods .ListParagraph}

> These are the methods for the PT\_CSV class as of January 14, 2019.

  --------------------------------------------------------------------------------------------
  []{#_Toc534968624 .anchor}**add**   
  ----------------------------------- --------------------------------------------------------
  **Description:**                    Add a dataset to the data dictionary.

  **Parameters:**                     **value:** (Required) The value of the parameter.\
                                      **param:** (Required) The name of the parameter (key).

  **Return:**                         None
  --------------------------------------------------------------------------------------------

  **add\_header\_item**   
  ----------------------- ---------------------------------------------------
  **Description:**        Adds header (columns) to the top of the CSV file
  **Parameters:**         **hd\_item:** (Required) A list of header values.
  **Return:**             None

  **check\_exists**   
  ------------------- ------------------------------------------
  **Description:**    Checks to see if the CSV file exists.
  **Parameters:**     None
  **Return:**         True is it exists, False if it does not.

  **close\_csv**     
  ------------------ ---------------------
  **Description:**   Close the CSV file.
  **Parameters:**    None
  **Return:**        None

  **create\_csv\_fn**   
  --------------------- ---------------------------
  **Description:**      Creates the CSV file name
  **Parameters:**       None
  **Return:**           None

  **get\_dictrows**   
  ------------------- --------------------------------------
  **Description:**    Gets a list of rows as dictionaries.
  **Parameters:**     None
  **Return:**         None

  **get\_header**    
  ------------------ -------------------------------------------
  **Description:**   Get the header (columns) of the CSV file.
  **Parameters:**    None
  **Return:**        A list of header names.

  **open\_csv**      
  ------------------ ----------------------------------------------------------------------------
  **Description:**   Opens the CSV file based on the specified mode.
  **Parameters:**    **f\_mode:** (Optional) The mode used when opening the file. (default = w)
  **Return:**        None

  --------------------------------------------------------------------------------------------------------------
  **remove\_duplicates**   
  ------------------------ -------------------------------------------------------------------------------------
  **Description:**         Removes duplicate entries in the CSV file based on the unique\_field as the column.

  **Parameters:**          **unique\_field:** (Required)\
                           **url:** (Optional) (default = False)

  **Return:**              None
  --------------------------------------------------------------------------------------------------------------

  **write\_dataset**   
  -------------------- ----------------------------------------------------------------------------
  **Description:**     Writes the specified or current dataset to the CSV file.
  **Parameters:**      **dataset:** (Optional) A dataset to add to the CSV file. (default = None)
  **Return:**          None

  **write\_datasets**   
  --------------------- ---------------------------------------------------------
  **Description:**      Adds a list of datasets to the CSV file
  **Parameters:**       **ds\_list:** (Required) A list of dataset information.
  **Return:**           None

  **write\_header**   
  ------------------- ------------------------------------------------------------------
  **Description:**    Write the header to the top of the CSV file.
  **Parameters:**     **fieldnames:** (Optional) A list of fieldnames (default = None)
  **Return:**         None

  **write\_line**    
  ------------------ ---------------------------------------------------------------------
  **Description:**   Write a line to the CSV file.
  **Parameters:**    **line:** (Required) A string of the line to put into the CSV file.
  **Return:**        None

  **write\_list**    
  ------------------ ---------------------------------------------------------
  **Description:**   Write a list of items to a single line in the CSV file.
  **Parameters:**    **item\_list:** (Required) A list of items.
  **Return:**        None

  -------------------------------------------------------------------------------------
  **write\_url**     
  ------------------ ------------------------------------------------------------------
  **Description:**   Writes a URL to the top of the CSV file.

  **Parameters:**    **url:** (Optional) The URL of the page. (default = None)\
                     **url\_name:** (Optional) The name of the page. (default = None)

  **Return:**        None
  -------------------------------------------------------------------------------------

### PT\_XL Class {#pt_xl-class .ListParagraph}

> The PT\_XL class contains the methods used in the creation of an Excel
> Spreadsheet.

#### PT\_XL Methods {#pt_xl-methods .ListParagraph}

These are the methods for the PT\_XL class as of January 14, 2019.

  -----------------------------------------------------------------------
  **add\_cell**      
  ------------------ ----------------------------------------------------
  **Description:**   Adds a cell to the current row list (self.row).

  **Parameters:**    **cell\_val:** (Required) The value for the cell.\
                     **column:** (Optional) (default = None)\
                     **ws\_name:** (Optional) (default = None)

  **Return:**        None
  -----------------------------------------------------------------------

  ------------------------------------------------------------------------------------------------------
  **add\_header**    
  ------------------ -----------------------------------------------------------------------------------
  **Description:**   Add the given header (either in\_header or self.header) to the current Worksheet.

  **Parameters:**    **in\_header:** (Optional) (default = None)\
                     **ws\_name:** (Optional) (default = None)

  **Return:**        None
  ------------------------------------------------------------------------------------------------------

  --------------------------------------------------------------
  **add\_item**      
  ------------------ -------------------------------------------
  **Description:**   Adds an item to the Excel spreadsheet

  **Parameters:**    **column:** (Required)\
                     **item:** (Required)\
                     **ws\_name:** (Optional) (default = None)

  **Return:**        None
  --------------------------------------------------------------

  ---------------------------------------------------------------------------
  **add\_title**     
  ------------------ --------------------------------------------------------
  **Description:**   Adds a title to the next row in the current worksheet.

  **Parameters:**    **title:** (Required)\
                     **merge:** (Optional) (default = (1, 2))

  **Return:**        None
  ---------------------------------------------------------------------------

  -------------------------------------------------------------------------
  **add\_worksheet**   
  -------------------- ----------------------------------------------------
  **Description:**     Add a worksheet to the current Workbook (self.wb).

  **Parameters:**      **ws\_name:** (Optional) (default = \'\')\
                       **header:** (Optional) (default = None)\
                       **title:** (Optional) (default = None)\
                       **replace:** (Optional) (default = None)

  **Return:**          None
  -------------------------------------------------------------------------

  **close\_workbook**   
  --------------------- ------------------------------
  **Description:**      Closes the current workbook.
  **Parameters:**       None
  **Return:**           None

  **create\_workbook**   
  ---------------------- -------------------------
  **Description:**       Creates a new Workbook.
  **Parameters:**        None
  **Return:**            None

  **delete\_sheet**   
  ------------------- ----------------------------------
  **Description:**    Deletes the specified worksheet.
  **Parameters:**     **ws\_name:** (Required)
  **Return:**         None

  **get\_abbreviation**   
  ----------------------- ------------------------------------------------------------------
  **Description:**        Conver the province/territory name to its 2-letter abbreviation.
  **Parameters:**         **pt:** (Required)
  **Return:**             None

  **get\_dictrows**   
  ------------------- ------------------------------------------
  **Description:**    Gets a list of rows as dictionaries.
  **Parameters:**     **output:** (Optional) (default = cells)
  **Return:**         None

  **get\_header**    
  ------------------ -------------------------------------------------------
  **Description:**   Gets the header (top row) from the Excel spreadsheet.
  **Parameters:**    None
  **Return:**        None

  **get\_rows**      
  ------------------ ----------------------------------------------
  **Description:**   Gets all the rows for the current Worksheet.
  **Parameters:**    None
  **Return:**        None

  **get\_worksheet**   
  -------------------- ---------------------------------------------
  **Description:**     Gets the current worksheet of the Workbook.
  **Parameters:**      None
  **Return:**          None

  **get\_ws\_list**   
  ------------------- ---------------------------------
  **Description:**    Gets a list of worksheet names.
  **Parameters:**     None
  **Return:**         None

  **get\_ws\_name**   
  ------------------- -----------------------------------------
  **Description:**    Gets the name of the current worksheet.
  **Parameters:**     None
  **Return:**         None

  -------------------------------------------------------------------
  **merge\_cells**   
  ------------------ ------------------------------------------------
  **Description:**   Merges cells in the row after the current row.

  **Parameters:**    **end\_col:** (Required)\
                     **start\_col:** (Required)

  **Return:**        None
  -------------------------------------------------------------------

  ----------------------------------------------------------------------------------------------------
  **move\_sheet**    
  ------------------ ---------------------------------------------------------------------------------
  **Description:**   Moves the position of a sheet\'s tab (if None, the sheet is placed at the end).

  **Parameters:**    **ws\_name:** (Required) The name of the sheet to move.\
                     **pos:** (Optional) The final position of the sheet (default = None)

  **Return:**        None
  ----------------------------------------------------------------------------------------------------

  **save\_file**     
  ------------------ ---------------------------------------
  **Description:**   Saves the current Workbook (self.wb).
  **Parameters:**    None
  **Return:**        None

  **set\_column\_widths**   
  ------------------------- ----------------------------------------------
  **Description:**          Sets the columns widths of the current sheet
  **Parameters:**           **widths:** (Required)
  **Return:**               None

  -----------------------------------------------------------------
  **set\_workbook**   
  ------------------- ---------------------------------------------
  **Description:**    Loads an existing Workbook (Excel file)

  **Parameters:**     **fn:** (Optional) (default = \'\')\
                      **read\_only:** (Optional) (default = True)

  **Return:**         None
  -----------------------------------------------------------------

  ------------------------------------------------------------------------------------------------------------------------------------------------------
  **set\_worksheet**   
  -------------------- ---------------------------------------------------------------------------------------------------------------------------------
  **Description:**     Set the current Worksheet (self.ws) to a specified existing worksheet. NOTE: To create a new worksheet, use \'add\_worksheet\'.

  **Parameters:**      **ws\_name:** (Optional) (default = None)\
                       **ws:** (Optional) (default = None)

  **Return:**          None
  ------------------------------------------------------------------------------------------------------------------------------------------------------

  --------------------------------------------------------------------------------------------------------------------------------------------
  **style\_range**   
  ------------------ -------------------------------------------------------------------------------------------------------------------------
  **Description:**   Apply styles to a range of cells as if they were a single cell.

  **Parameters:**    **cell\_range:** (Required)\
                     **border:** (Optional) An openpyxl Border (default = \<openpyxl.styles.borders.Border object\>\
                     Parameters:\
                     outline=True, diagonalUp=False, diagonalDown=False, start=None, end=None, left=\<openpyxl.styles.borders.Side object\>\
                     Parameters:\
                     style=None, color=None, right=\<openpyxl.styles.borders.Side object\>\
                     Parameters:\
                     style=None, color=None, top=\<openpyxl.styles.borders.Side object\>\
                     Parameters:\
                     style=None, color=None, bottom=\<openpyxl.styles.borders.Side object\>\
                     Parameters:\
                     style=None, color=None, diagonal=\<openpyxl.styles.borders.Side object\>\
                     Parameters:\
                     style=None, color=None, vertical=None, horizontal=None)\
                     **fill:** (Optional) An openpyxl PatternFill or GradientFill (default = None)\
                     **font:** (Optional) An openpyxl Font object (default = None)\
                     **alignment:** (Optional) (default = None)

  **Return:**        None
  --------------------------------------------------------------------------------------------------------------------------------------------

  ------------------------------------------------------------------------------
  **write\_cell**    
  ------------------ -----------------------------------------------------------
  **Description:**   Writes a single sell to a specific location in the sheet.

  **Parameters:**    **value:** (Required)\
                     **row:** (Required)\
                     **col:** (Required)

  **Return:**        None
  ------------------------------------------------------------------------------

  ----------------------------------------------------------------
  **write\_list**    
  ------------------ ---------------------------------------------
  **Description:**   Writes a list as a row.

  **Parameters:**    **row\_list:** (Optional) (default = \[\])\
                     **ws\_name:** (Optional) (default = None)

  **Return:**        None
  ----------------------------------------------------------------

  **write\_row**     
  ------------------ -------------------------------------------------
  **Description:**   Write the current row to the current Worksheet.
  **Parameters:**    **ws\_name:** (Optional) (default = None)
  **Return:**        None

  **ws\_exists**     
  ------------------ --------------------------------------
  **Description:**   Checks to see if a worksheet exists.
  **Parameters:**    **ws\_name:** (Required)
  **Return:**        None

Services.py {#services.py .ListParagraph}
-----------

### MyGeocortex Class {#mygeocortex-class .ListParagraph}

> The MyGeocortex class contains the methods for the Geocortex
> interactive maps.

#### MyGeocortex Methods {#mygeocortex-methods .ListParagraph}

> These are the methods for the MyGeocortex class as of August 13, 2018.
>
> get\_data(self)
>
> **Description**: Gets the data for the GeoCortex Services.
>
> **Parameter(s)**: None
>
> **Return**: A list of data as dictionaries.
>
> get\_site\_json(self, site\_json)
>
> **Description**: Gets the JSON for a site from a list of sites in an
> initial JSON page.
>
> **Parameter(s)**:

-   **site\_json**: The initial JSON page containing a list of sites.

> **Return**: The JSON of the site.
>
> get\_sites(self, url=None, json=None)
>
> **Description**: Gets all the JSON text for all the sites under a
> Geocortex Service page.
>
> **Parameter(s)**:

-   **url**: The root URL.

-   **json**: The root JSON format.

> **Return**: A list of JSON formatted sites.

### MyREST Class {#myrest-class .ListParagraph}

> The MyREST class' methods are used for extracting information from
> ESRI REST Services.

#### MyREST Methods {#myrest-methods .ListParagraph}

> These are the methods for the MyREST class as of August 13, 2018.
>
> get\_data(self)
>
> **Description**: Gets the data for the ESRI REST Services.
>
> **Parameter(s)**: None
>
> **Return**: A list of data as dictionaries.
>
> get\_metadata(self, mdata\_url)
>
> **Description**: Gets the metadata for a specific service.
>
> **Parameter(s)**:

-   **service**: The service to extract the metadata from.

> **Return**: A dictionary of the metadata.
>
> get\_root\_json(self)
>
> **Description**: Gets the home JSON dictionary of the REST service.
>
> **Parameter(s)**: None
>
> **Return**: The JSON dictionary of the home page of the REST service.
>
> get\_service\_json(self, url, serv\_json=None)
>
> **Description**: Gets the map service in JSON format.
>
> **Parameter(s)**:

-   **url**: The home URL of the ESRI REST Service.

-   **serv\_json**: The JSON of the ESRI REST Service.

> **Return**: The service in JSON format.
>
> get\_services(self, url=None, json=None)
>
> **Description**: Gets all the services in a mapservice.
>
> **Parameter(s)**:

-   **url**: The mapservice URL.

-   **json**: The JSON text.

> **Return**: A list of JSON services.

Recurse\_FTP.py {#recurse_ftp.py .ListParagraph}
---------------

> The Recurse\_FTP.py contains methods to walk through folders and
> subfolders of an FTP site.

### Recurse\_FTP Methods {#recurse_ftp-methods .ListParagraph}

> These are the methods for the Recurse\_FTP class as of August 13,
> 2018.
>
> check\_dir(self, adir)
>
> **Description:** Checks for a list of folders in a FTP folder.
>
> **Parameter(s):**

-   **adir**: An FTP folder.

> **Return**: None
>
> get\_dirs(self, ln)
>
> **Description:** Gets a list of directories under a given line from
> the FTP page.
>
> **Parameter(s):**

-   **ln**: FTP line text.

> **Return**: None
>
> get\_file\_list(self)
>
> **Description:** Gets a list of all the files at an FTP location.
>
> **Parameter(s):** None
>
> **Return**: A list of the FTP files.

Provincial/Territorial Extractions {#provincialterritorial-extractions .ListParagraph}
==================================

Alberta {#alberta .ListParagraph}
-------

### GeoDiscover Alberta {#geodiscover-alberta .ListParagraph}

#### Description {#description-13 .ListParagraph}

> The provincial geoportal for Alberta is GeoDiscover Alberta. The
> portal includes a catalogue with the ability to search and locate all
> of Alberta's geospatial data. The main web page includes a search
> option and a "browse by topic" option. Using the "browse by topic"
> page, the query URL can be extracted (see the querying instructions in
> the Provincial and Territorial Data and Web Service Inventories SOP
> document).

#### URLs {#urls .ListParagraph}

##### Catalogue Browser URL {#catalogue-browser-url .ListParagraph}

> <https://geodiscover.alberta.ca/geoportal/catalog/search/browse/browse.page>

##### Query URL {#query-url .ListParagraph}

> [**https://geodiscover.alberta.ca/geoportal/rest/find/document**](https://geodiscover.alberta.ca/geoportal/rest/find/document)

#### Extraction Process {#extraction-process-6 .ListParagraph}

##### Query to Get JSON Data {#query-to-get-json-data-1 .ListParagraph}

> The query URL for GeoDiscover Alberta is similar to other provincial
> geoportals. The URL path for the geoportal is
> **<https://geodiscover.alberta.ca/geoportal/rest/find/document>. The
> query string can include the following parameters:**

-   **f**: The output format of the results

-   **id**: The unique ID of a record (only used if one record should be
    returned)

-   **start**: The record number on which to start the results

-   **max**: The number of records to return in the results

-   **showRelativeUrl**: Determines whether relative paths should be
    used in the results

-   **searchText**: The search text used to filter the results

> Here's an example of a query URL for the GeoDiscover geoportal:

-   Query URL:
    <https://geodiscover.alberta.ca/geoportal/rest/find/document?f=pjson&start=1&max=10&showRelativeUrl=True&contentType=downloadableData,offlineData>

<!-- -->

-   Results:

> The results are provided in a JSON format containing information on
> the query (title, description, source, number of results, etc.) and
> the records are in a list under the "records" field (Figure 1 shows an
> example of the results of the above query).

![](media/image17.png){width="6.489583333333333in"
height="5.197916666666667in"}

Figure C‑1 Results of a query on the GeoDiscover Alberta geoportal.

##### Extract Results {#extract-results-2 .ListParagraph}

> The next step is to extract the information from the JSON results
> using Python.

1.  Using the JSON results in a Python script, grab the "records" list
    mentioned above.

2.  The JSON results for the GeoDiscover portal includes the title,
    summary, date and metadata link.

3.  The metadata link provides the metadata as an XML.

4.  Scrape the XML metadata using BeautifulSoup and use it to retrieve
    the rest of the information, such as the metadata type, spatial
    reference, download link, available formats, date type, licensing
    and publisher

### Open Data Catalogue {#open-data-catalogue .ListParagraph}

#### Description {#description-14 .ListParagraph}

> The open data catalogue for Alberta is a search engine that allows
> users to locate Alberta's open data collection. The results are
> displayed as web pages with 10 items per page (or 25 or 50 depending
> on what the user selects).

#### URLs {#urls-1 .ListParagraph}

##### Main URL {#main-url .ListParagraph}

> <https://open.alberta.ca/dataset>

#### Extraction Process {#extraction-process-7 .ListParagraph}

##### Query {#query .ListParagraph}

> The URL for querying Alberta's open data is
> <https://open.alberta.ca/dataset>. The query string can have the
> following parameters:

-   **q**: Filter the results by key word search.

-   **dataset\_type**: Filter the results by the information type (see
    the Information Type list under Refine Results on the page for a
    list of values).

-   **topic**: The topic used to filter the results (see the Information
    Type list under Refine Results on the page for a list of values).

-   **res\_format**: Filter results by format type of the files (see the
    Formats list under Refine Results on the page for a list of values).

-   **audience**: Filter results by the audience type (see the Audience
    list under Refine Results on the page).

-   **tags**: Filter the results by tag.

-   **pubtype**: Filter results by the publication type (see the
    Publication Type list under Refine Results on the page).

-   **organization**: Filter results by the publisher (see the Publisher
    list under Refine Results on the page).

-   **page**: Specifies the page number of the results to be displayed.

-   **items\_per\_page**: Specifies the number of items per page.

-   **sort**: Specifies how to sort the results.

> For example, the following query URL returns open data results with
> shapefiles:
>
> <https://open.alberta.ca/dataset?dataset_type=opendata&res_format=SHP>

![](media/image18.png){width="6.5in" height="5.875694444444444in"}

Figure C‑2 The results of the above query filtering results with
shapefiles and are open data.

> As shown, the results can only be returned as a web page. In order to
> extract the information from these datasets, each result page will
> have to be scraped using BeautifulSoup and Python
>
> **NOTE**: The rest of the instructions assumes understanding of
> browser Development Tools, HTML code and its elements.

##### Determine Page Count {#determine-page-count-1 .ListParagraph}

> For the Alberta Open Data site, the total number of pages is listed at
> the bottom of the page. The area highlighted in Figure 4 is a \<div\>
> with class name "pagination". Each link in the pagination is in a
> \<li\> element so the total number of pages can be found in the second
> last li element.

![](media/image19.png){width="6.5in" height="5.875694444444444in"}

Figure C‑3 Bottom of the results page containing the links to the
different pages.

##### Extract Results {#extract-results-3 .ListParagraph}

> To get the information within each result, the different elements in
> the web page have to be scraped.
>
> Here are the scraping procedures for the results page (numbers
> correspond to the numbers in Figure 5):

1)  Each result is contained in a \<div\> with class name
    "dataset-item".

2)  The **Title** is found under the element \<h3\> with class
    \"package-header\".

3)  For the **Available Formats**, find all the \<a\> elements with
    class "btn" and has the attribute data-format.

4)  For the **Date**, locate the \<h5\> with text "Last Modified", get
    its parent and then locate the \<p\> in the parent.

![](media/image21.png){width="6.5in" height="5.875694444444444in"}

Figure C‑4 The result page showing the different elements on the page.

> The rest of the information can be extracted from the metadata page of
> the result (the link is found under the title \<h3\> element mentioned
> above). There are 2 tabs on the metadata page which contain the rest
> of the information for the inventory, "Summary" (Figure 6) and
> "Detailed Information" (Figure 7 and Figure 8).
>
> Here are the scraping procedures for the Summary tab (numbers
> correspond to the numbers in Figure 6):

1)  For the **Description**, find the \<h5\> element containing text
    "Description" and then locate its \<p\> sibling.

2)  For the **Downloads**, find the \<section\> element with id
    "dataset-resources**".**

3)  **Next, find all** \<li\> **elements and get the second** \<a\> **to
    retrieve the download link.**

![](media/image22.png){width="6.660838801399825in"
height="5.291666666666667in"}

Figure C‑5 The summary tab of the metadata page.

> Here are the scraping procedures for the Detailed Information tab
> (numbers correspond to the numbers in Figure 7 and Figure 8):

1)  For the **Publisher**, find the \<h5\> element containing text
    "Publisher" and then locate its \<p\> sibling.

2)  For the **Licence**, find the \<h5\> element containing text
    "Licence" and then locate its \<p\> sibling.

![](media/image23.png){width="6.5in" height="5.163888888888889in"}

Figure C‑6 The top part of the "Detailed Information" tab of the
metadata page.

![](media/image24.png){width="6.5in" height="5.163888888888889in"}

Figure C‑7 The bottom part of the "Detailed Information" tab of the
metadata page.

> Repeat the extraction for all records on the page. To get to the next
> page, add "&page=2" to the query URL and continue with each page until
> all pages have been extracted.

### Interactive Maps {#interactive-maps-1 .ListParagraph}

#### Description {#description-15 .ListParagraph}

> The Province of Alberta includes a few ArcGIS Online maps. The maps
> are provided by the Alberta Geological Survey (AGS)
> (<http://ags-aer.maps.arcgis.com>).

#### URLs {#urls-2 .ListParagraph}

##### Alberta Interactive Minerals Map {#alberta-interactive-minerals-map .ListParagraph}

> <http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=cfb4ed4a8d7d43a9a5ff766fb8d0aee5>

##### Alberta Sand & Gravel Deposits {#alberta-sand-gravel-deposits .ListParagraph}

> <http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=d85fd3dd5daa424488bd82dfd9033846>

##### Northern Alberta RADARSAT-1 Imagery {#northern-alberta-radarsat-1-imagery .ListParagraph}

> <http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=30e3bc42140f4979a9b2d7963e49c101>

##### Alberta Seismic Events {#alberta-seismic-events .ListParagraph}

> <http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=1b1efd0717c441f595dbfdba66d95217>

#### Extraction Process {#extraction-process-8 .ListParagraph}

##### Query to Get JSON Data {#query-to-get-json-data-2 .ListParagraph}

> Extracting the data of an ArcGIS Online map requires extracting the ID
> of the map from the URL and using it to access the JSON data of the
> map.
>
> For example, the map URL for **Alberta Interactive Minerals Map** is:
>
> [**http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=cfb4ed4a8d7d43a9a5ff766fb8d0aee5**](http://ags-aer.maps.arcgis.com/apps/webappviewer/index.html?id=cfb4ed4a8d7d43a9a5ff766fb8d0aee5)
>
> The data for this map can be retrieved in JSON format using the ID
> from the map URL. The generic URL for ArcGIS map data is:
>
> **http://\<arcgis\_map\_domain\>/sharing/rest/content/items/\<map\_id\>?f=pjson**
>
> So the data URL for the Alberta Interactive Minerals Map would be:
>
> [**http://ags-aer.maps.arcgis.com/sharing/rest/content/items/cfb4ed4a8d7d43a9a5ff766fb8d0aee5?f=pjson**](http://ags-aer.maps.arcgis.com/sharing/rest/content/items/cfb4ed4a8d7d43a9a5ff766fb8d0aee5?f=pjson)

![](media/image9.png){width="6.489583333333333in"
height="5.197916666666667in"}

Figure C‑8 The JSON results for the Alberta Interactive Minerals Map
data.

##### Extract Results {#extract-results-4 .ListParagraph}

> As with the geoportal, the JSON results can be used to extract the
> necessary results in Python. Unlike the geoportal, all information is
> provided by the JSON document. The data includes the title, type,
> description, date and licensing of the map. Extraction in Python uses
> the JSON request call.

### Map Services {#map-services-1 .ListParagraph}

#### Description {#description-16 .ListParagraph}

> Alberta has 3 map services, all of which are ESRI REST services.

#### URLs {#urls-3 .ListParagraph}

##### ESRI REST Service Home URL {#esri-rest-service-home-url .ListParagraph}

> <https://maps.alberta.ca/genesis/rest/services>

##### Services2 Home URL {#services2-home-url .ListParagraph}

> <https://services2.arcgis.com/jQV6VMr2Loovu7GU/arcgis/rest/services>

##### Tiles Services Home URL {#tiles-services-home-url .ListParagraph}

> <https://tiles.arcgis.com/tiles/jQV6VMr2Loovu7GU/arcgis/rest/services>

#### Extraction Process {#extraction-process-9 .ListParagraph}

##### Query to Get JSON Data {#query-to-get-json-data-3 .ListParagraph}

> ESRI REST services can be returned in multiple formats. Again, for
> Python scripting, the best option is JSON format.
>
> The JSON results can be accessed by adding "**?f=pjson" to the service
> URL and subsequent Mapserver URLs.**
>
> **The access\_rest.py script contains a set of methods which will take
> the home page of the service, cycle through each folder and collect
> all the mapservices found under any folders and subfolders.**

##### Extract Results {#extract-results-5 .ListParagraph}

> As with other JSON results, all necessary information is contained in
> its keys and values. However, Alberta's services are unique in that
> they have a "Latest" mapserver which is identical to the latest dated
> service (ex: /Air-Layers/Latest/MapServer is identical to
> /Air-Layers/20180323/MapServer). As part of the extraction process,
> the "Latest" mapserver must be omitted.
>
> The following items can be found in the Mapserver JSON data:

-   Title (or "mapName" as it appears in the JSON results)

-   Description (or "serviceDescription")

-   Available formats

    -   Determined by the type of service:

        -   Mapserver: **KMZ**, **LYR**, **NMF**, **AMF**

        -   Imagerserver: KMZ, LYR

        -   Geometryserver or Featureserver: None

-   Publisher (or in this case "Author")

British Columbia {#british-columbia .ListParagraph}
----------------

### Data Catalogue {#data-catalogue .ListParagraph}

#### Description {#description-17 .ListParagraph}

> The BC Data Catalogue is a search engine which allows users to locate
> datasets in DataBC. The Data Catalogue also includes an API for easy
> automatic searches.

#### URLs {#urls-4 .ListParagraph}

##### Main URL {#main-url-1 .ListParagraph}

> <https://catalogue.data.gov.bc.ca/dataset>

##### API URL {#api-url .ListParagraph}

> <https://catalogue.data.gov.bc.ca/api/3>

#### Extraction Process {#extraction-process-10 .ListParagraph}

##### Create Query String URL {#create-query-string-url .ListParagraph}

> The following parameters are available for the query string URL:

-   **q:** Filter the results by key word search.

-   **type**: Filter the results by the dataset type.

-   **license\_id:** Filter results by the license.

-   **sector:** Filter results by sector.

-   **res\_format**: Filter the results by format.

-   **organization**: Filter results by organization.

-   **download\_audience**: Filter results by download permission.

> For the inventory, the only parameters that are used are **q** and
> **type**.

##### Extract Results {#extract-results-6 .ListParagraph}

> Here are the steps for extracting the results:

1.  Determine the page count (see Section 3.3.2.2).

2.  Go through each result on each page and get the dataset link found
    in the \<a\> under the \<h3\> with class "dataset-heading".

3.  Get the base name of the link to get the name of the dataset.

4.  Using the API URL and the dataset name, create the API query string
    URL. For example, the dataset link
    <https://catalogue.data.gov.bc.ca/dataset/fire-burn-severity-historical>
    becomes
    <https://catalogue.data.gov.bc.ca/api/3/action/package_show?id=fire-burn-severity-historical>
    for the API query URL.

5.  Use the JSON formatted information returned from the API query URL
    to get the **Title**, **Description** ("purpose" or "notes" in
    JSON), **Date** ("record\_last\_modified" in JSON),
    **Organization**, **Publisher** ("full\_title" in JSON),
    **Licensing** ("license\_title" in JSON), and **Spatial Reference**
    ("projection\_name" in JSON).

### Web Pages {#web-pages-1 .ListParagraph}

#### Description {#description-18 .ListParagraph}

> The Province of British Columbia has several interactive maps as
> downloadable KML files.

#### URLs {#urls-5 .ListParagraph}

##### FrontCounter BC Discovery Tool URL {#frontcounter-bc-discovery-tool-url .ListParagraph}

> <http://www.frontcounterbc.gov.bc.ca/mapping/>

##### Orthophoto Viewer URL {#orthophoto-viewer-url .ListParagraph}

> <https://www2.gov.bc.ca/gov/content/data/geographic-data-services/digital-imagery/orthophotos/orthophoto-viewer>

##### Air Photo Viewer URL {#air-photo-viewer-url .ListParagraph}

> <https://www2.gov.bc.ca/gov/content/data/geographic-data-services/digital-imagery/air-photos/air-photo-viewer>

##### Management of Survey Control Operations & Tasks Map Viewer {#management-of-survey-control-operations-tasks-map-viewer .ListParagraph}

> <https://www2.gov.bc.ca/gov/content/data/geographic-data-services/georeferencing/survey-control-operations>

##### B.C. Address Geocoder URL {#b.c.-address-geocoder-url .ListParagraph}

> <https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder>

#### Extraction Process {#extraction-process-11 .ListParagraph}

> The extraction process is the same for each page:

1.  The information for the inventory CSV file is located in the
    \<meta\> of the page (see Section 3.4.2.1).

2.  The download link is located in the first \<a\> with href containing
    ".kml" or ".kmz".

### Interactive Maps {#interactive-maps-2 .ListParagraph}

> British Columbia has over 2 dozen interactive maps not listed in their
> "Applications" section of the Data Catalogue. For extraction purposes,
> the interactive maps have been divided into 4 categories,
> Environmental Maps, Industry Maps, Transportation Maps, and all other
> interactive maps.

#### Environmental Maps {#environmental-maps .ListParagraph}

##### Description {#description-19 .ListParagraph}

> The environmental maps are any maps that deal with the environment of
> British Columbia, such as parks, groundwater, waterbodies, wild-life
> and climate.

##### URLs {#urls-6 .ListParagraph}

> See the extraction process section for each interactive map URL.

##### Extraction Process {#extraction-process-12 .ListParagraph}

###### BC Parks {#bc-parks .ListParagraph}

> Map URL: <http://www.env.gov.bc.ca/bcparks/explore/map.html>
>
> Large Map URL:
> <http://apps.gov.bc.ca/pub/dmf-viewer/?siteid=5859423305973444492>
>
> The BC Parks map contains the locations of provincial parks, protected
> areas, conservancies, recreation areas, ecological reserves, wildlife
> management areas (WMAs), and conservation study areas. The parks map
> is a Google Map.
>
> The information for the CSV inventory is located in the \<meta\> of
> the page with the smaller map. The metadata contains the **Title**,
> **Description** and **Publisher**.

###### Groundwater Levels {#groundwater-levels .ListParagraph}

> URL:
> <http://www.env.gov.bc.ca/soe/indicators/water/groundwater-levels.html>
>
> The Groundwater Levels map contains the location of observation wells
> throughout the province. Each well contains the groundwater level
> throughout a certain time period. The map is a Google Map and is
> embedded on the page.
>
> Again, the information for the CSV inventory is located in the
> \<meta\> of the page. The metadata contains the **Title**,
> **Description, Date** and **Publisher**.

###### Real-time Water Data {#real-time-water-data .ListParagraph}

> URL:
> <http://www2.gov.bc.ca/gov/content/environment/air-land-water/water/water-science-data/water-data-tools/real-time-water-data-reporting>
>
> The map contains continuous surface, groundwater and snow data from
> various monitoring stations across the province.
>
> The information for the inventory can be found in the \<meta\> of the
> page. The metadata contains the **Title**, **Description, Date** and
> **Publisher**. The link to the interactive map is found in an \<a\>
> with class "alert-link".

###### CDC iMap {#cdc-imap .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/environment/plants-animals-ecosystems/conservation-data-centre/explore-cdc-data/known-locations-of-species-and-ecosystems-at-risk/cdc-imap-theme>
>
> The B.C. Conservation Data Centre (CDC) map allows the viewing and
> printing of occurrences of species and ecosystems at risk in the
> province. The CDC iMap is a Geocortex interactive map.
>
> The information for the inventory is contained in the metadata of the
> page. The metadata contains the **Title**, **Description**, **Date**
> and **Publisher**. The map link is found in an \<a\> with text "Launch
> CDC iMap".

###### Frogwatching {#frogwatching .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/environment/plants-animals-ecosystems/wildlife/wildlife-conservation/amphibians-reptiles/frogwatching>
>
> The BC Frogwatch Atlas contains data collected by the BC Frogwatch
> program on where amphibians, reptiles and turtles have been observed
> throughout the province. The map is a Silverlight map which can only
> be opened in Internet Explorer.
>
> The contents for the inventory are contained in the metadata of the
> page. The metadata contains the **Title**, **Description**, **Date**
> and **Publisher**. The map link is found in an \<a\> with text "BC
> Frogwatch Atlas".

###### EcoCat:The Ecological Reports Catalogue {#ecocatthe-ecological-reports-catalogue .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/environment/research-monitoring-reporting/libraries-publication-catalogues/ecocat>
>
> The EcoCat can search for a broad range of environmental and natural
> resource information, including publications on British Columbia\'s
> species and the habitats they live in. The map is a Silverlight map
> which can only be opened in Internet Explorer.
>
> The contents for the inventory are contained in the metadata of page.
> The metadata contains the **Title**, **Description**, **Date** and
> **Publisher**. The map link is located on the search page of the
> catalogue. The search page URL is in an \<a\> with text "Search for
> Reports using a map". The URL must have "/public/welcome.do" appended
> to the end of it. With this search URL, the map link is contained in
> an \<a\> with text "Search for Reports using a map".

###### ClimateBC/WNA/NA {#climatebcwnana .ListParagraph}

> URL: <http://cfcg.forestry.ubc.ca/projects/climate-data/climatebcwna>
>
> This page contains 3 maps containing climate data for climate change
> studies. The page includes links to interactive maps and downloads for
> desktop applications.
>
> The information for the CSV inventory is contained in the metadata of
> each map page. The metadata contains the **Description** and the
> **Title** is taken from the title of the map page.

###### BC Water Tools {#bc-water-tools .ListParagraph}

> URL: <http://www.bcwatertool.ca>
>
> The BC Water tool page contains a list of interactive maps providing
> access information about natural water availability, existing water
> users and monitoring data.
>
> Each map link is contained in a \<div\> with class "project
> primary-text". Next, go through each map and grab the **Title** from
> the \<div\> with class "project-title headline", the **Description**
> from the \<div\> with class "project-description" and the **Web Map
> URL** from the \<div\> with class "project-actions".

###### Pacific Climate Impacts Consortium Data Portal {#pacific-climate-impacts-consortium-data-portal .ListParagraph}

> URL: <http://www.pacificclimate.org/data>
>
> This page provides access to the consortium's products which is
> available to the public.
>
> All items (subsections) on the page are contained in \<div\> elements
> with class "subsection". The **Title** is in \<h2\>, and the
> **Description** is in \<h2\>'s next sibling \<p\>.
>
> To get the **Web Map URL**, get the subsection URL from the \<a\>
> under the \<h2\>, open the page and look for an \<a\> with text
> "Access and download".

###### BC Environmental Assessment Office {#bc-environmental-assessment-office .ListParagraph}

> URL: <https://www.projects.eao.gov.bc.ca/>
>
> This page provides information on the many projects using the
> provincial environmental assessment process. The page contains an
> interactive map showing the locations of all the projects with
> environmental assessments.
>
> The **Title** of the map is found in \<h1\> on the page while the
> **Description** is found in the next sibling of the \<h1\> which is a
> \<p\> element.
>
> The map link is found in the \<a\> under the \<span\> with text "View
> Map".

#### Industry Maps {#industry-maps .ListParagraph}

##### Description {#description-20 .ListParagraph}

> The Industry Maps include maps relating to the forestry, food
> production and mining.

##### URLs {#urls-7 .ListParagraph}

> See the extraction process section for each interactive map URL.

##### Extraction Process {#extraction-process-13 .ListParagraph}

###### Meat Inspection & Licensing {#meat-inspection-licensing .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/industry/agriculture-seafood/food-safety/meat-inspection-licensing>
>
> This site contains a link to a map of provincially licensed slaughter
> establishments throughout British Columbia.
>
> The information for the inventory can be found in the page's metadata.
> The **Title** and **Description** are contained in their respective
> metadata elements while the **Date** is in "DCTERMS.modified" and
> **Publisher** is in "DCTERMS.publisher". The **Web Map URL** is found
> in an \<a\> containing text "Find a provincially licensed" (use the
> find\_tags\_containing method in shared.py) under a \<div\> with class
> "contentPageRightColumn".

###### Provincial Site Productivity Layer {#provincial-site-productivity-layer .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/forest-inventory/site-productivity/provincial-site-productivity-layer>
>
> The site productivity layer contains the timber-growing potential of
> forested sites across British Columbia.
>
> The page contains 2 maps, the Site Productivity Layer application and
> the Hectares BC map. For the first map, the information for the
> inventory can be extracted from the page's metadata. The items are the
> same as the Meat Inspection & Licensing page.
>
> The following steps are used to get the URL for the Site Productivity
> Layer application:

1.  Locate the \<div\> with id "main-content".

2.  Under the main content \<div\>, locate a \<div\> with id "body".

3.  Locate the \<h2\> containing text "Access to the Database & PDF Maps
    Catalogue" under the body \<div\> using the find\_tags\_containing
    method in shared.py.

4.  Locate the \<ul\> element under the \<h2\>.

5.  Get the **Web Map URL** from the \<a\> under the \<ul\>.

> The information for the Hectares BC is in the page's content. The
> steps for extracting this information is:

1.  Under the body \<div\> mentioned above, locate an \<h2\> containing
    text "Hectares BC Website & Data Catalogue".

2.  Under the \<h2\>, extract the text of a \<p\> to get the
    **Description**.

3.  To get the **Web Map URL**, locate a \<span\> containing text
    "Access Hectare BC" and then get the link of its parent \<a\>.

###### Seedlot Area of Use {#seedlot-area-of-use .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/tree-seed/seed-planning-use/seedlot-aou>
>
> The Seedlot Area of Use Spatial Data Locator Map contains
> approximately 4000 Seedlots throughout British Columbia.
>
> Much like the other sites on the www2.gov.bc.ca domain, the
> information can be extracted from the metadata on the page. The names
> of the metadata are also the same for the **Title**, **Description**,
> **Date** and **Publisher** (see 3.3.11). The **Web Map URL** is found
> in an \<a\> in the second \<p\> under the \<div\> with id
> "introduction".

###### SeedMap {#seedmap .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/industry/forestry/managing-our-forest-resources/tree-seed/seed-planning-use/seedmap>
>
> The SeedMap provides access for clients to information for genetic
> resource management planning.
>
> The information for the page is taken from the metadata and contains
> the same names as other www2.gov.bc.ca sites. The **Web Map URL** is
> found in the sidebar in \<a\> with text "Launch the SeedMap
> Application" under \<div\> with class "contentPageRightColumn".

###### The Invasive Alien Plant Program (IAPP) Application {#the-invasive-alien-plant-program-iapp-application .ListParagraph}

> URL: <https://www.for.gov.bc.ca/hra/plants/application.htm>
>
> The IAPP Application contains invasive plant surveys, treatments, and
> activity plans for the entire province of British Columbia.
>
> The **Title**, **Description**, **Date** and **Publisher** can all be
> taken from the metadata. The **Date** and **Publisher** are under
> "DC.date" and "DC.publisher", respectively. The **Web Map URL** is
> found under \<a\> containing text "IAPP Map Display".

###### Mineral Titles Online {#mineral-titles-online .ListParagraph}

> URL: <http://www.mtonline.gov.bc.ca/mtov/home.do>
>
> The Mineral Titles Online site contains three categories of maps that
> show current mineral, placer and coal tenures throughout the entire
> province.
>
> There are 3 types of maps: Mineral Map, Placer Map and Coal Map. Each
> map contains links to the CWM Viewer and the IMF2 Viewer for a total
> of 6 maps on the page. All maps are found under \<strong\> elements
> with text "Map Viewer".
>
> For each \<strong\> element:

1.  Find the parent \<p\> of the \<strong\> to get part of the Title of
    the map.

2.  Get the next siblings \<a\> elements of the \<p\>.

3.  For each \<a\> element:

    a.  Get the link of \<a\> removing any text outside of the brackets.
        The link is a Javascript method that opens the map (ex:
        javascript:openMap(\'/showTenure.do?tenureTypeParam=M\'))

    b.  To determine what type of map is contained in the link, find in
        the link "=M" or "min" if the map is a Mineral Map, "=P" or
        "pla" if the map is a Placer Map or "=C" or "coal" if the map is
        a Coal Map. Append the type of map to the **Title** text.

#### Transportation Maps {#transportation-maps .ListParagraph}

##### Description {#description-21 .ListParagraph}

> The Transportation Maps deal with traffic data and travel information,
> such as stops of interests throughout the province.

##### URLs {#urls-8 .ListParagraph}

> See the extraction process section for each interactive map URL.

##### Extraction Process {#extraction-process-14 .ListParagraph}

###### Stop of Interest Signs {#stop-of-interest-signs .ListParagraph}

> URL:
> <http://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/traveller-information/stop-of-interest>
>
> The Stop of Interest Signs map contains locations of the signs
> throughout the province. Each point on the map has a brief history
> about the location and a small image of the sign.
>
> The information for the inventory can be found in the metadata of the
> page in the same elements as all other www2.gov.bc.ca sites. The **Web
> Map URL** is found by first locating the \<img\> with attribute alt
> "Stop of Interest Signs Map" and then getting the link of its parent
> element which is an \<a\>.

###### Traffic Data Program {#traffic-data-program .ListParagraph}

> URL: <http://www.th.gov.bc.ca/trafficData>

The Traffic Data Program application contains traffic count sites
throughout British Columbia.

The inventory items can be found at:

-   **Description**: locate the next sibling of \<h3\> which is a \<p\>.

-   **Web Map URL**: locate the \<h1\> with class "heading sizable", get
    its parent \<div\> and then find the next \<a\>.

-   **Title** is hard-coded as "Traffic Data Map".

#### Other Maps {#other-maps .ListParagraph}

##### Description {#description-22 .ListParagraph}

> This category includes any other maps found throughout British
> Columbia's web pages.

##### URLs {#urls-9 .ListParagraph}

> See the extraction process section for each interactive map URL.

##### Extraction Process {#extraction-process-15 .ListParagraph}

###### Elections BC {#elections-bc .ListParagraph}

> URL: <http://elections.bc.ca/resources/maps>
>
> The Elections map contains the electoral districts for the province.
>
> The Web Map URL can be found in an \<a\> with text containing
> "Electoral District Explorer". The rest of the information for the map
> is found on the map page. The **Title** is in the page's title and the
> **Description** is in a \<p\> in a \<div\> with class "content".

###### Francophone Affairs Program {#francophone-affairs-program .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/governments/organizational-structure/office-of-the-premier/intergovernmental-relations-secretariat/francophone>
>
> This map provides the ability to locate francophone resources and
> services throughout the province.
>
> The **Title**, **Description**, **Date** and **Publisher** are all in
> the metadata elements of the page in the same locations as Section
> 3.2.3.1. The **Web Map URL** is located in an \<a\> with text
> containing "interactive map".

###### BC Community Health Atlas {#bc-community-health-atlas .ListParagraph}

> URL: <http://communityhealth.phsa.ca/Home/HealthAtlas>
>
> The BC Community Health Atlas contains data related to population
> health and demographics.
>
> The **Title** is found in the \<h1\> containing text "BC Community
> Health Atlas". The **Description** is found under the \<h1\> in a
> \<p\> element. The **Web Map URL** is in an \<a\> containing text "BC
> Community Health Atlas" under the \<p\> element.

###### Processing Plants {#processing-plants .ListParagraph}

> URL:
> <http://www.bccdc.ca/health-info/food-your-health/fish-shellfish/processing-plants>
>
> This map shows the location of BC fish processing plants.
>
> The **Title** is found in the \<h1\> with class "page-title". The
> **Description** is found in a \<p\> element under \<main\> with class
> "content-body". The **Web Map URL** is found in an \<a\> with title
> "Map of BC Fish Processing Plants".

###### Child Development & Family Support Services {#child-development-family-support-services .ListParagraph}

> URL:
> <http://www2.gov.bc.ca/gov/content/family-social-supports/data-monitoring-quality-assurance/find-services-for-children-teens-families>
>
> This map shows the locations and contact information for a variety of
> early years programs and services in BC.
>
> The **Web Map URL** is found under an \<a\> containing text "Family
> Support Services". Both the **Title** and **Description** are
> hard-coded.

###### Geographical Names {#geographical-names .ListParagraph}

> URL:
> <http://www2.gov.bc.ca/gov/content/governments/celebrating-british-columbia/historic-places/geographical-names>
>
> This map contains the geographic names of the entire province.
>
> The **Web Map URL** is found in the \<a\> with text containing "Launch
> Application:". The information for the Geographic Names map is found
> on the map page. The **Title** is the page's title. The
> **Description** is found in a \<p\> under the \<div\> with class
> "welcome".

###### Recreation Sites & Trails {#recreation-sites-trails .ListParagraph}

> URL:
> <http://www2.gov.bc.ca/gov/content/sports-culture/recreation/camping-hiking/sites-trails>
>
> Map URL: <http://www.sitesandtrailsbc.ca>
>
> This map is used to assist in identifying and navigating recreation
> sites and trails throughout the province.
>
> The inventory information is taken from the metadata on the map page.
> The **Title** is page's title and the **Description** is in the
> \<meta\> element with name "description".

###### The MapPlace Table of Maps {#the-mapplace-table-of-maps .ListParagraph}

> URL: <http://webmap.em.gov.bc.ca/mapplace/minpot/ex_maps.asp>
>
> This site contains a table of MapPlace interactive maps for the
> Ministry of Energy, Mines and Petroleum Resources.
>
> For extraction, find all the tables on the page. Using the 5^th^ table
> on the page, go through each row and:

1.  Get the **Title** from the "Available Maps" column.

2.  Get the **Description** from the "General Description" column.

3.  Get the **Web Map URL** from \<a\> in the "Available Maps" column.

###### Safe Harbour Map {#safe-harbour-map .ListParagraph}

> URL: http://apps.gov.bc.ca/pub/dmf-viewer/?siteid=4758954260021402554
>
> Since the Safe Harbour Map page takes a while to load, Selenium is
> used to access the page while waiting for an element with id
> 'about-text' is loaded for about 20 seconds.
>
> If the \<title\> element is not empty, its text is used for the
> **Title**, otherwise the **Title** is hard-coded as "Safe Harbour
> Map". The **Description** is found in the \<div\> with id
> 'about-text'.

###### B.C. Address Geocoder {#b.c.-address-geocoder .ListParagraph}

> URL:
> <https://www2.gov.bc.ca/gov/content/data/geographic-data-services/location-services/geocoder>
>
> The BC Address Geocoder is used to resolve the physical locations of
> addresses in British Columbia.
>
> The items for extraction are on the map page. The **Web Map URL** is
> found in \<a\> with text containing "Launch Location Services". The
> **Title** is the title of the map page.

### Map Services {#map-services-2 .ListParagraph}

#### Description {#description-23 .ListParagraph}

> British Columbia has 2 ArcGIS REST Services and 3 Web Map Services
> (WMS).

#### URLs {#urls-10 .ListParagraph}

##### ArcGIS REST Service URLs {#arcgis-rest-service-urls .ListParagraph}

> <https://services6.arcgis.com/ubm4tcTYICKBpist/ArcGIS/rest/services>
>
> <http://maps.gov.bc.ca/arcserver/rest/services>

##### WMS URLs {#wms-urls .ListParagraph}

###### BC Imagery WMS {#bc-imagery-wms .ListParagraph}

> <http://openmaps.gov.bc.ca/imagex/ecw_wms.dll?service=wms&request=getcapabilities&version=1.3.0>

###### BC Imagery WMS -- DataBC Imagery WMS - Landsat {#bc-imagery-wms-databc-imagery-wms---landsat .ListParagraph}

> <http://openmaps.gov.bc.ca/imagex/ecw_wms.dll?wms_landsat?service=wms&request=getcapabilities&version=1.3.0>

###### DataBC Express Server WMS {#databc-express-server-wms .ListParagraph}

> <https://openmaps.gov.bc.ca/lzt/ows?service=wms&version=1.1.1&request=getcapabilities>

#### Extraction Process {#extraction-process-16 .ListParagraph}

##### ArcGIS REST Services {#arcgis-rest-services .ListParagraph}

> The extraction process of the ArcGIS REST Services for British
> Columbia is the same as other provinces, using the get\_data method in
> the MyREST class (see Section 3.6.2.1).

##### WMS {#wms-1 .ListParagraph}

> The extraction of the WMS for British Columbia is similar to the
> regular extraction of WMS (see Section 3.6.2.3)
>
> The information for the inventory is found in the following elements
> in the XML:

-   Service Type: \<name\> or \<Name\>

-   Service Name: \<title\> or \<Title\>

-   Description: \<abstract\> or \<Abstract\>

-   Publisher: \<contactorganization\> or \<ContractOrganization\>

> The layers are located under 2 different elements depending on the
> WMS. For the imagery WMS, the layers are located in \<layer\> elements
> with attribute queryable set to 1 and the **Title** of the layer is
> under \<name\>. For the DataBC Express Server WMS, the layers are
> located in \<layer\> elements with attribute opaque set to 1 and the
> **Title** of the layer is under \<Title\>.

### FTP {#ftp-1 .ListParagraph}

#### Description {#description-24 .ListParagraph}

> A great deal of British Columbia's geospatial datasets are found on
> their FTP site.

#### URLs {#urls-11 .ListParagraph}

> <ftp://ftp.geobc.gov.bc.ca>

#### Extraction Process {#extraction-process-17 .ListParagraph}

> The FTP site of BC has two folders containing geospatial datasets:
> "pub" and "sections". The steps for extracting these folders are:

1.  Create a folder list containing "pub" and "sections".

2.  Create a header list containing "date", "time", "type" and
    "filename".

3.  For each folder in the folder list:

    a.  Create the RecFTP object using the root domain (without
        "ftp://"), the current folder and the header list.

    b.  Get a list of files from the folder and its sub-folders and add
        them to a file list

4.  Add each file in the file list to the inventory.

Manitoba {#manitoba .ListParagraph}
--------

### Web Pages {#web-pages-2 .ListParagraph}

#### Fire Mapping {#fire-mapping .ListParagraph}

##### Description {#description-25 .ListParagraph}

> This section contains the downloadable datasets for fire monitoring.
> The fire monitoring site has downloads of the fire conditions since
> 2010.

##### URLs {#urls-12 .ListParagraph}

> <http://www.gov.mb.ca/sd/fire/Fire-Maps/index.html>

##### Extraction Process {#extraction-process-18 .ListParagraph}

###### Scraping Webpage {#scraping-webpage .ListParagraph}

> The scraping of the fire monitoring page is very similar to some of
> the interactive maps mentioned above.
>
> Below is a list of the steps taken to extract the fire monitoring page
> (see Figure 2‑1 for location of steps on the page):

1.  Locate the \<div\> with id "main-content".

2.  Get a list of all the \<a\> in the \<div\>.

3.  Go through each link, determine its year and link as each year will
    be a separate entry in the CSV file and the links for that year will
    determine the **Available Formats**. For example, there are two
    links for 2018: "2018 Fires KMZ" and "2018 Fire ZIP" so the
    **Title** for the entry in the CSV file will be "Fire Locations --
    2018", the **Date** will be 2018 and the **Available Formats** will
    be "SHP\|KMZ".

    ![](media/image25.png){width="6.5in" height="6.977083333333334in"}

Figure C‑9 Fire Monitoring page

#### DEMSM Downloads and Ordering {#demsm-downloads-and-ordering .ListParagraph}

##### Description {#description-26 .ListParagraph}

> This web site contains four Digital Elevation Models (DEM) of Manitoba
> (version DEMSM-1.0, DEMSM-2.0, and Manitoba-1.0, and MB\_SRTM), as
> well as various image files of, or derived from, the DEM.

##### URLs {#urls-13 .ListParagraph}

###### Main URL {#main-url-2 .ListParagraph}

> <http://www.gov.mb.ca/iem/geo/demsm/downloads.html>

###### Metadata URL {#metadata-url .ListParagraph}

> <http://www.gov.mb.ca/iem/geo/demsm/metadata.html>

##### Extraction Process {#extraction-process-19 .ListParagraph}

###### Extract Metadata {#extract-metadata .ListParagraph}

> Before extracting from the DEMSM downloads, the **Description**,
> **Date** and **Publisher** can be extracted from the metadata page.
> The metadata page contains different sections for each version of DEM:
> Version 1, Version 2 and Manitoba Version.
>
> Here are the steps for extraction in Python (see Figure 2‑2):

1.  Each version starts with a title contained in an \<h2\> tag.
    Therefore, the page is split at these \<h2\> tags.

2.  The **Description**, **Date** and **Publisher** are extracted for
    each version and stored in a dictionary containing keys with the
    version title.

    ![](media/image26.png){width="6.5in" height="6.977083333333334in"}

Figure C‑10 Metadata page for the DEMs

###### Extract the Downloads {#extract-the-downloads .ListParagraph}

> Once the metadata has been collected, the next step is to scrape the
> page containing the DEM downloads. The scraping process for the
> downloads is different than other web pages so far.
>
> Here are the steps for extracting the downloads from the DEMSM page:

1.  Locate the \<h2\> tag containing the text "Ordering".

2.  Find the \<ol\> sibling tag of the \<h2\> tag and then get a list of
    all the \<li\> tags to get the links to the bookmarks on the page.

3.  Go through each \<li\> and, using its text, get the title, format
    and bookmark link. Store the format and link in a dictionary
    containing the titles as keys.

4.  For each item in the dictionary:

    a.  get the **Title** from the key

    b.  get **Available Formats** from the item

    c.  using the bookmark link, locate the download link anchor if
        there is only one available format

    d.  get the metadata using the key that corresponds with the
        metadata dictionary from the previous section. Petroleum:
        Interactive GIS Map Gallery.

#### Petroleum Page {#petroleum-page .ListParagraph}

##### Description {#description-27 .ListParagraph}

> This site contains an interactive map and a set of shapefiles for
> various petroleum datasets. For the interactive map on this page, go
> to Section 1.2.1.

##### URLs {#urls-14 .ListParagraph}

###### Main URL {#main-url-3 .ListParagraph}

> <http://www.manitoba.ca/iem/petroleum/gis/index.html>

##### Extraction Process {#extraction-process-20 .ListParagraph}

###### Scraping {#scraping .ListParagraph}

> This page contains links to various shapefiles. The links are located
> in the right box called "Technical Files & Maps" and under the heading
> "**GIS Shapefiles to Download**".
>
> Here are the instructions for extracting the downloads (numbers
> correspond with Figure 2‑3):

1.  First, locate the \<h2\> tag with text "GIS Shapefiles to Download".

2.  Next, locate the sibling \<div\>.

3.  Get all the \<a\> in the \<div\> and get their href to get the
    downloads for the shapefiles.

![](media/image27.png){width="6.5in" height="5.875694444444444in"}

Figure C‑11 The Petroleum page with the elements mentioned above.

#### Manitoba Land Initiative {#manitoba-land-initiative .ListParagraph}

##### Description {#description-28 .ListParagraph}

> The Manitoba Land Initiative site provides access to various land
> related geospatial datasets from across different government
> departments.

##### URLs {#urls-15 .ListParagraph}

###### Main URL {#main-url-4 .ListParagraph}

> <http://mli2.gov.mb.ca/mli_data/index.html>

##### Extraction Process -- Scraping Pages {#extraction-process-scraping-pages .ListParagraph}

> The Manitoba Land Initiative includes websites to the different
> categories of geospatial data. The categories are listed in the
> sidebar of the index, or about, page (and all category pages).
>
> Here are the instructions to extract the links to each category (see
> Figure 2‑4):

1.  Locate the \<div\> with class "section".

2.  Next, locate all the \<li\> tags in the \<div\>.

3.  Go through each \<li\> and extract its \<a\>, ignoring any \<a\>
    with text "About" and "Comment".

4.  Open the links of each anchor and start scraping.

![](media/image28.png){width="6.5in" height="5.875694444444444in"}

Figure C‑12 The About page of the Manitoba Land Initiative

###### All Pages {#all-pages .ListParagraph}

> All categories under the Manitoba Land Initiative (MLI) website
> contain tables with the downloadable datasets. The tables are either
> on the category's main page or buried somewhere is its sub pages. The
> Manitoba\_extractor script includes methods which will help in the
> extraction of these tables.
>
> Here are the methods used in the extraction of the MLI pages:

  **Method**       **Description**
  ---------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  process\_table   Takes in a \<table\> element, goes through each row (\<tr\>) and stores its columns (\<td\>) into a dictionary. Each key in the dictionary are the same as the fields in the final CSV file. The Title is always column 1, the metadata, date and description columns are specified by the user, some columns are ignored (also specified by the user) and the remaining columns are used to determine the available formats.
  get\_metadata    Extracts the MLI metadata for a given URL. (see Section 2.4.3.6 for more details on the types of MLI metadata and how to extract them). The method will determine which the type of metadata and extract the information accordingly.

###### Administrative Boundaries {#administrative-boundaries .ListParagraph}

> <http://mli2.gov.mb.ca/adminbnd/index.html>
>
> The Administrative Boundaries' page contains a table with different
> datasets, links to their metadata and downloads for the different
> available formats. Locate the proper \<table\> element and use the
> process\_table method (mentioned in Section 2.4.3.1) to get a list of
> rows containing a dictionary of the different fields in the table (the
> field names in the dictionaries should be the same as the final CSV
> file).
>
> The "Boundary Layer" is the dataset title, the ".DOC" column is the
> metadata column, the ".GIF" and "Version" columns are ignored and the
> rest of the columns are used to list the available formats.
>
> ![](media/image29.png){width="6.5in" height="5.875694444444444in"}
>
> Figure C‑13 The Administrative Boundaries page

###### Base Maps {#base-maps .ListParagraph}

> <http://mli2.gov.mb.ca/base_maps/index.html>
>
> The Base Maps page also contains a single table with links to base
> layers for the entire province. Extracting the table works in the same
> way as the Administrative Boundaries page.
>
> The "Dataset" is the dataset title, the ".DOC" column is the metadata
> column, the ".GIF" column is ignored and the rest of the columns are
> used to list the available formats.
>
> ![](media/image30.png){width="6.5in" height="5.875694444444444in"}
>
> Figure C‑14 The Base Maps page

###### Cadastral {#cadastral .ListParagraph}

> <http://mli2.gov.mb.ca/cadastral/index.html>
>
> The Cadastral page is setup differently than the previous two
> categories. The Cadastral page contains a map, a table with a single
> dataset and links to various other datasets at the right of the page.
>
> Here are the instructions for extracting this page (numbers correspond
> to Figure 2‑7 and Figure 2‑8 and the order corresponds to the order in
> the script):

1.  To extract the table, the same method is used as the previous pages.
    The metadata column is "Metadata", the date column is "Date" and the
    "Update Info" and "Version columns are ignored. The remaining column
    ".GDB" is used as the format.

2.  The map contains links to the different cadastral maps throughout
    the province. However, this map can be ignored since all these
    datasets are listed in the "Tabular selection page".

3.  The Tabular selection contains several tables which can be extracted
    using the process\_table method. The first column of every table is
    used for the **Title** of the dataset, the ".DOC" column is the
    metadata link, the "Date" column is the date, the "Adjust" column is
    used for the spatial reference and the ".GIF", ".PDF", "Ver" columns
    are ignored. The rest of the columns are used for the **Available
    Formats**.

4.  Within the table, there are two locations that contain subpages to
    more datasets: St. Nobert and Winnipeg. The Winnipeg page (Figure
    2‑8) contains a map with different areas throughout the city. The
    outlined areas are stored as \<area\> tags with href links. These
    pages contain a map with the cadastral datasets for the specified
    area in Winnipeg. The St. Nobert page has map with links to 2
    datasets contained in \<area\> tags.

5.  The Township Diagrams link can be ignored since it leads to the same
    site as the Spatial Referencing category.

6.  The rest of the dataset links can be extracted by grabbing their
    \<a\> tags and getting their href.

> ![](media/image31.png){width="6.5in" height="5.875694444444444in"}
>
> Figure C‑15 The Cadastral page
>
> ![](media/image32.png){width="6.5in" height="5.875694444444444in"}
>
> Figure C‑16 The Winnipeg subpage containing a map with links to
> cadastral maps.

###### Digital Elevation Models {#digital-elevation-models .ListParagraph}

> <http://mli2.gov.mb.ca/dems/index.html>
>
> The Digital Elevation Models (DEMs) page contains two tables with
> links to the available DEMs of Manitoba. The tables can be extracted
> using the process\_table method. The first column is the **Title**,
> the ".DOC Metadata" column is the metadata and the ".GIF Overview" and
> ".TIF Download" columns are ignored. The rest of the columns are used
> to determine the **Available Formats** and download links.
>
> At the bottom of the page is a link to the province's LiDAR datasets.
> The same columns as above can be used when extracting the 2 tables on
> the LiDAR page. In the results, the word "Contour" should be replaced
> with "SHP".

###### Digital Imagery {#digital-imagery .ListParagraph}

> <http://mli2.gov.mb.ca/ortho/index.html>
>
> The Digital Imagery page contains a table with links to maps
> containing image datasets. The table has no column names but it
> appears to have a column for metadata and a description column (see
> Figure 2‑9).

![](media/image33.png){width="6.5in" height="5.6875in"}

Figure C‑17 The Digital Imagery page of the MLI site

> The first step in the extraction of the Digital Imagery table is to
> get the metadata pages. The metadata contains the **Description** (a
> more in depth description than the table's description),
> **Licensing**, **Date**, **Spatial Reference** and **Publisher**.
>
> There are 3 formats of metadata for the MLI pages: TXT, XML and HTML
> (or webpage). There are also 3 types of webpage metadata (see Figure
> 2‑10). The get\_metadata method determines which type of metadata by:

1.  Checking the \<html\> tag for the "xmlns:res" attribute (ArcGIS
    metadata)

2.  Checking to see if there are \<meta\> tags on the page which contain
    names such as dc.description, dc.publisher, etc. (FGDC metadata)

3.  Checking for neither 1 or 2 (FGDC & ESRI metadata

4.  Checking for the file extension of the link (for TXT and XML
    metadata).

![H:\\GIS\_Data\\Work\\NRCan\\FGP\\TA001\\\_Manitoba\\\_working\\MLI\_mdata\_types.jpg](media/image34.jpeg){width="6.489583333333333in"
height="4.9375in"}

Figure C‑18 The 3 types of webpage MLI metadata

> Although the layouts can differ for the Digital Imagery sub pages,
> most of the pages contain a map that can be extracted using the
> following method:

1.  Collect all the \<area\> tags on the map into a list

2.  For each area:

    a.  Grab its link from the href

    b.  Grab its alt attribute for the **Title** of the dataset

3.  Add each area to the CSV file

> For these images, a world file is required to open them. Each page
> usually has a link to these world files (see Figure 2‑11). The links
> for the world files are located in the CSV under the "Data URL"
> column.

![](media/image35.png){width="6.5in" height="5.6875in"}

Figure C‑19 An example of one of the MLI sub pages

> Some of the sites (such as the Nickel Belt -- MrSid, IRS -- Capital
> Region, Refresh - (2007-2014) Color) do not have maps but just a
> single table. These tables can be extracted using the process\_table
> method mentioned on the other pages.

###### Environment {#environment .ListParagraph}

> <http://mli2.gov.mb.ca/environment/index.html>
>
> The Environment page contains a table with various environmental
> datasets. The script uses the same code to run the Environment page as
> the Administrative Boundaries page.

###### Forest Inventory {#forest-inventory .ListParagraph}

> <http://mli2.gov.mb.ca/forestry/index.html>
>
> The Forest Inventory page contains 2 tables with links in the forest
> inventory. The map on the page is for reference only and does not
> include any links.
>
> Here are the steps for extracting the forest inventory page (see
> Figure 2‑12):

1.  For the first table, the title is the "Fires" column, the metadata
    column is ".DOC" and the ".GIF" column is ignored.

2.  For the second table, each row contains 2 datasets so the table has
    to be divided in some way by the middle blank column. The
    table\_to\_dict method in the shared.py script adds a number to any
    duplicate columns in a table. So the resulting dictionary will have
    keys with fmu1, date1, .gif1, .doc1, .shp1, .geo1 and fmu2, date2,
    .gif2, .doc2, .shp2, .geo2. Using these numbers, each row can be
    divided into separate dictionaries.

3.  At the bottom of the page, there are two links to shapefiles for RFQ
    and Forest Resource Inventory lines. To locate these links, use
    BeautifulSoup to locate the \<a\> with text "RFQ\_shp" and "FRI
    Lines".

![](media/image36.png){width="5.8125in" height="8.083333333333334in"}

Figure C‑20 The Forest Inventory page

###### Geographical Names {#geographical-names-1 .ListParagraph}

> <http://mli2.gov.mb.ca/geognames/index.html>
>
> The Geographical Names page contains a table with a single
> Geographical Names dataset. The script uses the same code to run the
> Geographic Names page as the Administrative Boundaries page.

###### Geology Mapping {#geology-mapping .ListParagraph}

> <http://mli2.gov.mb.ca/geology/index.html>
>
> The Geology Mapping page contains no tables but only a link to a
> 1:1,000,000 Geology page (see Figure 2‑13).
>
> The 1:1,000,000 Geology page contains a table of various geological
> datasets (see Figure 2‑14). The tables can be extracted using the
> process\_table method. The "Dataset" column is the **Title**, the
> ".DOC Metadata" column is the metadata and the ".GIF Overview" and
> ".TIF Download" columns are ignored. The rest of the columns are used
> to determine the **Available Formats** and download links.

![](media/image37.png){width="6.5in" height="6.652777777777778in"}

Figure C‑21 The Geology Mapping page

![](media/image38.png){width="6.5in" height="6.128472222222222in"}

Figure C‑22 The 1:1,000,000 Geology page

###### Hydrography {#hydrography .ListParagraph}

> <http://mli2.gov.mb.ca/water_resources/index.html>
>
> The Hydrography page contains 2 maps with links to pages with drainage
> and basin datasets. The page also contains 2 links to more hydrography
> datasets. All the sub pages contain tables.
>
> Here are the instructions for extracting the Hydrography page (see
> Figure 2‑15):

1.  Get the \<a\> in the Designated Drain Watercourses map and get the
    soup for it. There are 2 tables on the watercourses page. The
    **Title** of the dataset is the "Dataset" column in the tables, the
    ".DOC column is the metadata link, the ".GIF" column is ignored
    while the rest of the columns is used to determine the **Available
    Formats**.

2.  Next, get the \<a\> of the Basins & Watersheds of Manitoba map and
    get the soup for it. The page contains a single table with the same
    columns as the previous step.

3.  Get the \<a\> of the Floods link and open the page. This page
    contains 2 tables with the same columns as the previous steps. Each
    table is contained in a \<table\> with ids "table1" and "table2".

4.  The 1:20,000 Digital Topographic Mapping -- Seamless Water page has
    1 table with the same columns as before.

![](media/image39.png){width="6.5in" height="5.6875in"}

Figure C‑23 The Hydrography page

###### Land Use/Cover Maps {#land-usecover-maps .ListParagraph}

> <http://mli2.gov.mb.ca/landuse/index.html>
>
> The Land Use/Cover Maps page contains a map with no links and 3
> tables. The first 2 tables have the **Title** as the "Dataset" column,
> ".DOC" as the metadata column and ".GIF" is ignored. The rest of the
> columns are used to determine the **Available Formats**. For the final
> table, the **Title** is still the "Dataset" column, the metadata
> column is "Metadata", the ".GIF" column is ignored and the rest are
> used to determine the **Available Formats**.

###### Municipal Maps {#municipal-maps .ListParagraph}

> <http://mli2.gov.mb.ca/municipalities/index.html>
>
> The Municipal Maps page has one table with links to various municipal
> maps. The "Municipality" column is the Title and the ".PDF" column is
> ignored. The rest of the columns are used to determine the **Available
> Formats**. There is no metadata column in the table.

###### Quarter Section Grids {#quarter-section-grids .ListParagraph}

> <http://mli2.gov.mb.ca/quarter_sec/index.html>
>
> The Quarter Section Grids page contains a table with links to sub
> pages and a description for each dataset.
>
> The table contains the following pages:

1.  The Manitoba Cadastral Polygons which links back to the Cadastral
    page mentioned in Section 2.4.3.4.

2.  The Original Southern Grid which contains a table of municipalities
    that can be extracted using the process\_table method. The metadata
    column is ".DOC Metadata" and the ".GIF Overview" can be ignored.

3.  The Manitoba Reference Grid page contains a map which can be
    extracted using the process\_map method. (NOTE: This page is under
    construction as of 2018-07-04).

4.  The Northern Grid Master tiles page contains a map which can be
    extracted using the process\_map method.

5.  The Northern Grid Sub-tiles page contains a map with the Province of
    Manitoba divided into 5 areas. Each area contains a page with a map
    with the area divided into smaller areas.

6.  The Northern Grid Quarter Sections is a shapefile of the northern
    grid.

7.  The DLS corner points is a zip file which contains CSV files of the
    quarter-sections and sections points.

![](media/image40.png){width="6.5in" height="5.967361111111111in"}

Figure C‑24 The Quarter Section Grids page

###### Soil Classification {#soil-classification .ListParagraph}

> <http://mli2.gov.mb.ca/soils/index.html>
>
> The Soil Classification page contains a table with 3 links to soil
> maps for municipalities in Manitoba. All 3 links load sub pages with
> tables which can be processed using the process\_table method.
> However, the Agricultural Interpretation Database (SoilAID) page
> includes KMZ files for soils and drains. The soils KMZ can be included
> in each municipality dataset in the CSV file but the drains have to be
> a separate entry in the CSV file.

###### Spatial Referencing {#spatial-referencing .ListParagraph}

> <http://mli2.gov.mb.ca/spatial_ref/index.html>
>
> The Spatial Referencing page contains a table with datasets of the
> Manitoba Spatial Referencing network. The table contains a **Title**
> column called "Product", a metadata column named ".DOC", a format
> column and a description column.

![](media/image41.png){width="6.5in" height="5.6875in"}

Figure C‑25 The Spatial Referencing page

###### Topographic Maps {#topographic-maps .ListParagraph}

> <http://mli2.gov.mb.ca/topo_mapping/index.html>
>
> The Topographic Maps page contains a table with links to the indices
> for 1:20,000 scale maps and 1:50,000 scale maps. The links include
> (see Figure 2‑18):

1.  The first 3 1:20,000 links lead to pages with maps that can be
    extracted using the process\_map method.

2.  The 1:20,000 Seamless page contains a table with datasets containing
    different topographic categories such as hydrography, buildings,
    transportation, etc.

3.  The 1:50,000 page contains a map with the Province of Manitoba
    divided into the National Topographic System grid.

4.  For the 1:50,000 and 1:250,000 scale, there are 2 links to the
    GeoGratis FTP site which are not included in the CSV inventory file.

    ![](media/image42.png){width="6.5in" height="5.625694444444444in"}

Figure C‑26 The Topographic Maps page

###### Town & Village Plans {#town-village-plans .ListParagraph}

> <http://mli2.gov.mb.ca/towns/index.html>
>
> The Town & Village Plans page is not required for extraction since all
> the dataset formats are either in .gif or .pdf and they don't include
> geospatial information.

###### Transportation {#transportation .ListParagraph}

> <http://mli2.gov.mb.ca/roads_hwys/index.html>
>
> The Transportation page contains a table with various datasets. The
> script uses the same code to run the Transportation page as the
> Administrative Boundaries page.

### Interactive Maps {#interactive-maps-3 .ListParagraph}

#### Description {#description-29 .ListParagraph}

> Manitoba has several interactive maps throughout its provincial
> website. The types of maps include ArcGIS Online, Adobe Flash, Leaflet
> and Google Maps.

#### URLs {#urls-16 .ListParagraph}

##### Petroleum Map Gallery {#petroleum-map-gallery .ListParagraph}

> Parent URL: <http://www.manitoba.ca/iem/petroleum/gis/index.html>
>
> Map URL: <https://web33.gov.mb.ca/mapgallery/mgp.html>

##### Manitoba Drought Management Map {#manitoba-drought-management-map .ListParagraph}

> <http://www.gov.mb.ca/sd/waterstewardship/water_info/drought/index.html>

##### Drinking Water Advisories Map {#drinking-water-advisories-map .ListParagraph}

> <http://www.gov.mb.ca/sd/waterstewardship/odw/public-info/boil-water/water_advisories_in_mb.html>

##### WeatherView Map {#weatherview-map .ListParagraph}

> <http://www.gov.mb.ca/sd/fire/Wx-Display/weatherview/weatherview.html>

##### FireView Map {#fireview-map .ListParagraph}

> Parent URL: <http://www.gov.mb.ca/sd/fire/Fire-Maps/>
>
> Map URL:
> <http://www.gov.mb.ca/sd/fire/Fire-Maps/fireview/fireview.html>

##### Fire Restrictions Map {#fire-restrictions-map .ListParagraph}

> <http://www.gov.mb.ca/sd/fire/Restrictions/index.html>

##### Wildlife Management Areas {#wildlife-management-areas .ListParagraph}

> Parent URL: <http://www.gov.mb.ca/sd/wildlife/habcons/wmas/index.html>
>
> Map URL:
> <http://www.gov.mb.ca/sd/wildlife/habcons/wmas/gMap/index.html>

##### Beach Monitoring Map {#beach-monitoring-map .ListParagraph}

> Parent URL:
> <http://www.gov.mb.ca/sd/waterstewardship/quality/beaches.html>
>
> Map URL:
> <http://www.gov.mb.ca/sd/waterstewardship/quality/beach_table.html>

#### Extraction Process {#extraction-process-21 .ListParagraph}

##### ArcGIS Online Interactive Maps {#arcgis-online-interactive-maps .ListParagraph}

> The Manitoba Drought Management and the Drinking Water Advisories maps
> are ArcGIS Online maps.

###### Query to Get JSON Data {#query-to-get-json-data-4 .ListParagraph}

> The ArcGIS Online maps are embedded on the pages for the Drought
> Management and Drinking Water Advisories maps. The map ID has to be
> extracted from the \<iframe\> tag which contains the ArcGIS Online
> MapSeries link in its src attribute (see Figure 1‑1).

![](media/image43.png){width="6.5in" height="4.932638888888889in"}

Figure C‑27 The source code of the Drought Management map page.

> Using the URL from the \<iframe\> src attribute, the ID can be
> extracted and converted to the proper URL in order to retrieve the
> data in JSON format for the ArcGIS map. The generic URL for ArcGIS map
> data is:
>
> So the data URL for the Drought Management Map would be:

###### Extract Results {#extract-results-7 .ListParagraph}

> The JSON results can be used to extract the necessary results in
> Python. The data includes the title, type, description, date and
> licensing of the map. Extraction in Python uses the JSON request call.

##### Other Interactive Maps {#other-interactive-maps-1 .ListParagraph}

> For the other interactive maps, the information needs to be extracted
> from the parent page containing the link to the map.
>
> For example, the Petroleum Map Gallery map has the title, description
> and date on its parent page
> (<http://www.manitoba.ca/iem/petroleum/gis/index.html>) so it needs to
> be extracted using BeautifulSoup in Python.

###### Extract Parent Page {#extract-parent-page .ListParagraph}

####### Petroleum Map Gallery {#petroleum-map-gallery-1 .ListParagraph}

> The parent page for the Petroleum Map Gallery contains no class or IDs
> for the different elements on the page (except for a \<div\> with id
> "main-content") so the information has to be extracted based on a
> certain text found in the element.
>
> Here are the different elements for the specific information (numbers
> correspond to Figure 1‑2):

1.  For the **Title**, locate the \<h1\> tag in the \<div\> with id
    "main-content" on the page and extract its text.

2.  For the **Description**, locate a \<strong\> element containing
    "this Interactive Map" and extract its text.

3.  To get the **Date**, locate a \<strong\> element containing
    "Updated:" and extract its text.

![](media/image44.png){width="6.5in" height="5.875694444444444in"}

Figure C‑28 The Petroleum Map Gallery parent page.

####### WeatherView Map {#weatherview-map-1 .ListParagraph}

> Like the Petroleum map, the page for the WeatherView map (which
> contains the title, description, etc.) contains no class or IDs for
> the different elements except for a \<div\> with id "main-content".
> Again, the information has to be extracted based on a certain text
> found in the element.
>
> Here are the different elements for the specific information (numbers
> correspond to Figure 1‑3):

1.  For the **Title**, locate the \<h1\> tag in the \<div\> with id
    "main-content" on the page and extract its text.

2.  For the **Description**, locate the first \<p\> element in the
    \<div\>.

![](media/image45.png){width="6.5in" height="5.875694444444444in"}

Figure C‑29 The WeatherView Map page

####### FireView Map {#fireview-map-1 .ListParagraph}

> Again, extracting the FireView map is the same as the previous maps.
>
> Here are the different elements for the specific information (numbers
> correspond to Figure 1‑4):

1.  For the **Title**, locate the \<h1\> tag in the \<div\> with id
    "main-content" on the page and extract its text.

2.  For the **Description**, locate the first \<p\> element in the
    \<div\>.

![](media/image46.png){width="6.5in" height="5.875694444444444in"}

Figure C‑30 The FireView map page containing the title and description

####### Fire Restrictions Map {#fire-restrictions-map-1 .ListParagraph}

> For the Fire Restrictions page, the **Title** is set to "Fire
> Restrictions Map" and the **Description** can be found by locating the
> \<div\> tag with id "main-content" and then grabbing the text in the
> first \<p\> element.

####### Wildlife Management Map {#wildlife-management-map .ListParagraph}

> Extracting the Wildlife Management map is the similar to the previous
> maps. The items can be found on the map's parent page.
>
> Here are the different elements for the specific information (numbers
> correspond to Figure 1‑5):

1.  For the **Title**, locate the \<h2\> tag in the \<div\> with class
    "body" on the page and extract its text.

2.  For the **Description**, locate the first \<p\> element in the
    \<div\>.

![](media/image47.png){width="6.5in" height="5.875694444444444in"}

Figure C‑31 The Wildlife Management Areas page

####### Beach Monitoring Map {#beach-monitoring-map-1 .ListParagraph}

> For the Beach Monitoring map, the information is extracted from both
> the parent page and the map page.
>
> The information is extracted from the following locations:

1.  The **Description** is taken from the parent page by locating the
    \<div\> with class "body" and then getting the text from the first
    \<p\> in the \<div\>.

2.  The **Title** is taken from the map page under the first \<h1\> in
    the \<div\> with id "main-content".

### Map Services {#map-services-3 .ListParagraph}

#### Description {#description-30 .ListParagraph}

> There are 2 maps services for the Province of Manitoba and both are
> ESRI REST Services.

#### URLs {#urls-17 .ListParagraph}

##### Petroleum ESRI REST Service {#petroleum-esri-rest-service .ListParagraph}

> <http://maps.gov.mb.ca/arcgis/rest/services/MG_PETROLEUM_CLIENT/MapServer>

##### ESRI REST Service {#esri-rest-service .ListParagraph}

> <https://services.arcgis.com/mMUesHYPkXjaFGfS/ArcGIS/rest/services>

#### Extraction Process {#extraction-process-22 .ListParagraph}

##### Query to Get JSON Data {#query-to-get-json-data-5 .ListParagraph}

> ESRI REST services can be returned in multiple formats. Again, for
> Python scripting, the best option is JSON format.
>
> The JSON results can be accessed by adding "**?f=pjson" to the service
> URL and subsequent Mapserver URLs.**
>
> **The** access\_rest.py **script contains a set of methods which will
> take the home page of the service, cycle through each folder and
> collect all the mapservices found under any folders and subfolders.**

##### Extract Results {#extract-results-8 .ListParagraph}

> As with other JSON results, all necessary information is contained in
> its keys and values.
>
> The following items can be found in the Mapserver JSON data:

-   **Title** (or "mapName" as it appears in the JSON results)

-   **Description** (or "serviceDescription")

-   **Available formats**

    -   Determined by the type of service:

        -   Mapserver: **KMZ**, **LYR**, **NMF**, **AMF**

        -   Imagerserver: KMZ, LYR

        -   Geometryserver or Featureserver: None

-   **Publisher** (or in this case "Author")

### Municipal Web Pages {#municipal-web-pages .ListParagraph}

#### Description {#description-31 .ListParagraph}

> The City of Brandon has several interactive maps, a REST map service
> and a list of open data on its municipal website. The City of Winnipeg
> offers several interactive maps and an open data catalogue.

#### URLs {#urls-18 .ListParagraph}

##### City of Winnipeg Open Data Catalogue {#city-of-winnipeg-open-data-catalogue .ListParagraph}

> <https://data.winnipeg.ca/browse>

##### City of Winnipeg - Property Map / Aerial Photography {#city-of-winnipeg---property-map-aerial-photography .ListParagraph}

> <http://winnipeg.ca/ppd/maps_aerial.stm>

##### City of Winnipeg - ServiceStat {#city-of-winnipeg---servicestat .ListParagraph}

> <http://winnipeg.ca/Interhom/serviceStat/>

##### City of Brandon Open Data List {#city-of-brandon-open-data-list .ListParagraph}

> <http://opengov.brandon.ca/OpenDataService/opendata.html>

##### City of Brandon ESRI REST Services {#city-of-brandon-esri-rest-services .ListParagraph}

> <https://gisapp.brandon.ca/arcgis/rest/services>

##### City of Brandon GIS Page {#city-of-brandon-gis-page .ListParagraph}

> <http://gis.brandon.ca/>

##### City of Brandon - Tax and Assessment Map {#city-of-brandon---tax-and-assessment-map .ListParagraph}

> <https://gisapp.brandon.ca/webmaps/TaxAssessmentMap/PropertySearch.html>

##### City of Brandon -- Cemetery Map {#city-of-brandon-cemetery-map .ListParagraph}

> <https://gisapp.brandon.ca/webmaps/CemeteryMap/index.htm>

##### City of Brandon -- Recreation Map {#city-of-brandon-recreation-map .ListParagraph}

> <http://www.arcgis.com/home/webmap/viewer.html?webmap=216328b495fa4d53b94c1ec783ca9999>

##### City of Brandon -- Recycling Depots {#city-of-brandon-recycling-depots .ListParagraph}

> <http://www.arcgis.com/home/webmap/viewer.html?webmap=ae2e308954ac4788b914539d5e0a7b9b>

##### City of Brandon -- Ward Map {#city-of-brandon-ward-map .ListParagraph}

> [[http://www.arcgis.com/home/webmap/viewer.html?webmap=31fe008833674707be86dfd7a0a3b5cd]{.underline}](http://www.arcgis.com/home/webmap/viewer.html?webmap=31fe008833674707be86dfd7a0a3b5cd)

##### City of Brandon Map {#city-of-brandon-map .ListParagraph}

> <http://www.arcgis.com/home/webmap/viewer.html?webmap=9a54b2369f5a442eb5008947e051436e>

##### City of Brandon - Brandon Snow Operations {#city-of-brandon---brandon-snow-operations .ListParagraph}

> <https://gisapp.brandon.ca/webmaps/snowclearing/index.html>

#### Extraction Process {#extraction-process-23 .ListParagraph}

##### City of Winnipeg {#city-of-winnipeg .ListParagraph}

###### Open Data Catalogue {#open-data-catalogue-1 .ListParagraph}

> Scraping Winnipeg's Open Data Catalogue page is very similar to other
> provincial open data catalogues, such as Alberta.
>
> The query URL has the following parameters:

-   **q**: Filter the results by key word search.

-   **category**: Filter the results by category (found on the catalogue
    page)

-   **sortBy**: Sort the results by 'alpha', 'most\_accessed',
    'relevance', 'newest', 'last\_modified'.

-   **limitTo**: Filter the results by View Type.

-   **Department\_Department**: Filter the results by Department.

-   **Department\_Group**: Filter the results by Group.

-   **tags**: Filter results by Tag.

-   **Page**: Specify the page of the results.

> For the inventory, the search is limited to geospatial data or in this
> case "maps". The query URL for extracting the Open Data Catalogue is:
>
> <https://data.winnipeg.ca/browse?limitTo=maps>
>
> Here are the steps for extracting the Open Data Catalogue (see Figure
> 4‑1 and Figure 4‑2):

1.  For the Open Data site, the total number of pages is determined by
    getting the total number of results. The number of results is listed
    at the top of the page in a \<div\> tag with class
    "browse2-results-title". To get the page count, this number is
    divided by 10 (the total number of results per page).

2.  The results are extracted by getting all the \<div\> tags with class
    "browse2-result-content".

3.  For each result, get the dataset's link by getting the \<h2\> with
    class "browse2-result-name" and open the page.

4.  Get the **Title** and **Description** from the \<meta\> tags of the
    dataset's page.

5.  The **Publisher** is extracted from the \<dd\> whose previous
    sibling is the \<dt\> with text "Department".

6.  The **Date** is located in a \<span\> with class "aboutUpdateDate".

7.  The **Licence** is located in a \<dd\> whose \<dt\> has text
    "Licence".

![](media/image48.png){width="6.5in" height="5.6875in"}

Figure C‑32 The Winnipeg Open Data Catalogue results

![](media/image49.png){width="6.5in" height="5.6875in"}

Figure C‑33 The dataset map page

###### Interactive Maps {#interactive-maps-4 .ListParagraph}

> The City of Winnipeg has 2 interactive maps, one for their aerial
> photographs index and one for available city services. Both maps are
> Google API Maps.
>
> Here are the steps for extracting both Winnipeg maps:

1.  Extract the layers in the Legend by locating all the \<table\> tags
    with class "legenditem".

2.  For each layer, get the id from the \<table\> and remove "tbl" from
    the id text.

3.  Get the **Title** of the dataset from the layer's text.

4.  Query <https://mapapi.winnipeg.ca/mapapi/wfs.ashx> URL using these
    parameters:

    a.  output = "json"

    b.  maptypeid = "2"

    c.  coordinates = ""

    d.  g = "n"

    e.  featurelist = the extract table ID

5.  The query URL should be similar to
    <https://mapapi.winnipeg.ca/mapapi/wfs.ashx?output=json&maptypeid=2&coordinates=&g=n&featurelist=13937>

6.  The query will return text in JSON format. From the JSON text, the
    **Description** and **Type** can be extracted.

##### City of Brandon {#city-of-brandon .ListParagraph}

###### Open Data Page {#open-data-page .ListParagraph}

> The City of Brandon's Open Data page is a single site with a list of
> datasets. The extraction process only requires scraping the one page.
>
> The steps for extracting the Open Data page are:

1.  Locate the \<table\> with id "datasetTable" and get its rows (\<tr\>
    tags).

2.  Go through each row and locate the one with the second column
    containing "Shapefile".

3.  For all shapefiles, get the **Title** (from the first column), the
    **Type** (from the second column) and the **Download** (from one of
    the row's \<a\> tags).

![](media/image50.png){width="6.5in" height="5.6875in"}

Figure C‑34 The City of Brandon\'s Open Data Catalogue page

###### ESRI REST Map Service {#esri-rest-map-service .ListParagraph}

> The City of Brandon offers several ESRI REST Services at
> <https://gisapp.brandon.ca/arcgis/rest/services>. The extraction
> process for these services is the same as mentioned in Map Services.

###### Interactive Maps {#interactive-maps-5 .ListParagraph}

> Listed on Brandon's GIS page are 9 interactive maps for various
> municipal services and information.
>
> Here are the steps for extracting these maps (see Figure 4‑3):

1.  On the GIS page, location the \<section\> with class "mainContent".

2.  Get all the \<li\> tags in the \<section\> element.

3.  For each item, determine the type of map:

    a.  If the map is a Google map, ignore it since the link leads to
        the Google Maps Transit page and not an actual municipal
        dataset.

    b.  If the map is an ArcGIS Online map, get its data in JSON format
        and extract the information from it.

    c.  If the map is an Adobe Flash map, extract the information from
        the map page itself. The **Title** is taken from the page's
        \<title\>, the **Description** is taken from the page's \<meta\>
        tag with name "description" and the **Date** is taken from a
        \<div\> with id "updateDiv".

![](media/image51.png){width="6.5in" height="5.6875in"}

Figure C‑35 The map links on Brandon\'s GIS page

New Brunswick {#new-brunswick .ListParagraph}
-------------

### Web Pages {#web-pages-3 .ListParagraph}

#### NB Survey Control Network {#nb-survey-control-network .ListParagraph}

##### Description {#description-32 .ListParagraph}

> This NB Survey Control Network page contains links to different search
> functions for the network. However, there is only one item on the page
> which contains geospatial data.

##### URLs {#urls-19 .ListParagraph}

> <https://www.pxw1.snb.ca/webnbcontrol/snbe/home.asp>

##### Extraction Process {#extraction-process-24 .ListParagraph}

> Here are the steps to extract the single item on the page:

1.  Locate the \<b\> containing text "Database Information".

2.  Locate the next \<a\> sibling of the \<b\> to get the link to the
    dataset.

3.  The **Title** for the page is hard-coded as "NB Survey Control
    Network - Database Information".

    ![](media/image52.png){width="6.5in" height="5.655555555555556in"}

Figure C‑36 The NB Survey Control Network page showing the only
geospatial download on the page

#### GeoNB Data Catalogue {#geonb-data-catalogue .ListParagraph}

##### Description {#description-33 .ListParagraph}

> The GeoNB Data Catalogue page contains a list of the geographic
> datasets for the Province of New Brunswick. (Since this page contains
> no search capabilities and only contains a list of downloads, it is
> listed under the Web Pages portion of this SOP instead of the
> Catalogue section.)

##### URLs {#urls-20 .ListParagraph}

> <http://www.snb.ca/geonb1/e/DC/catalogue-E.asp>

##### Extraction Process {#extraction-process-25 .ListParagraph}

> Here are the steps for extracting this page:

1.  Get the \<table\> on the page containing the downloads.

2.  Use the table\_to\_dict method in the shared.py script to get a list
    of rows containing dictionaries of the column in the table. The keys
    in the dictionary are the headings at the top of the table.

3.  Each row contains the **Title** and a link to more info. Get the
    More Info link from the \<a\> under the "Details" column.

4.  Get the rest of the information for the inventory from the More Info
    page (see Figure 1‑3).

    ![](media/image53.png){width="6.5in" height="5.655555555555556in"}

Figure C‑37 The Data Catalogue page for New Brunswick

![](media/image54.png){width="6.5in" height="5.029861111111111in"}

Figure C‑38 One of the datasets More Info page

### Interactive Maps {#interactive-maps-6 .ListParagraph}

#### Description {#description-34 .ListParagraph}

> The Province of New Brunswick contains a page with a list of mapping
> applications similar to the Open Catalogue page. The rest of the
> interactive maps are listed in a CSV file under
> "PT\_WebExtractor\\files\\NB\_Interactive\_Maps.csv".

#### URLs {#urls-21 .ListParagraph}

##### Main URL {#main-url-5 .ListParagraph}

> <http://www.snb.ca/geonb1/e/apps/apps-E.asp>

#### Extraction Process {#extraction-process-26 .ListParagraph}

##### Application List Page {#application-list-page .ListParagraph}

> The extraction process is similar to the Open Data Catalogue page. The
> steps for extracting the interactive maps are:

1.  Get the \<table\> on the page.

2.  Use the table\_to\_dict method in the shared.py script to get a list
    of rows containing dictionaries of the column in the table. The keys
    in the dictionary are the headings at the top of the table.

3.  Locate the \<a\> under the "Details" column to get the More Info
    link.

4.  On the More Info page:

    a.  Get the **Description** from the next sibling of the \<strong\>
        with text "Application description:"

    b.  Get the **Title** from the \<td\> in the \<tr\> with class
        'toprowtext'.

    c.  Get the map URL from either a link in the \<div\> with id
        'boxes' or by getting the previous sibling \<a\> of an \<a\>
        with class 'close'. If the latter choice, remove the
        "javascript:myPopup" from the link.

    d.  If there is an \<iframe\> with an ArcGIS Map link, get the
        ArcGIS JSON and replace the **Title** with the title of the
        ArcGIS data. Also, grab the **Date**, **Type** and **Spatial**
        **Reference** from the JSON data.

##### CSV Interactive Maps List {#csv-interactive-maps-list .ListParagraph}

> These are the steps for extracting the CSV list of interactive maps:

1.  Open the CSV file located at
    "PT\_WebExtractor\\files\\NB\_Interactive\_Maps.csv".

2.  Go through each row in the CSV file and grab the URLs. The first
    column is the map URL and the second column is the service URL, if
    applicable.

3.  If the map has no service URL, get the **Title** and **Description**
    from the metadata (\<meta\>) of the page.

4.  If the map has a service URL, get the information from the service
    JSON data.

### Map Services {#map-services-4 .ListParagraph}

#### Description {#description-35 .ListParagraph}

> The Province of New Brunswick has three Map Services.

#### URLs {#urls-22 .ListParagraph}

##### GeoNB Map Services URL {#geonb-map-services-url .ListParagraph}

> <http://geonb.snb.ca/arcgis/rest/services>

##### Department of Natural Resources Map Services URL {#department-of-natural-resources-map-services-url .ListParagraph}

> <http://maps-dnr-mrn.gnb.ca/arcgis/rest/services>

##### Energy & Resource Development Map Services URL {#energy-resource-development-map-services-url .ListParagraph}

> <https://gis-erd-der.gnb.ca/arcgis/rest/services>

#### Extraction Process {#extraction-process-27 .ListParagraph}

> The extraction process for the map services is the same as the other
> map services from other provinces. For each URL, use the get\_data
> method under the MyREST Python class to get all the information.

Newfoundland & Labrador {#newfoundland-labrador .ListParagraph}
-----------------------

### Open Data Catalogue {#open-data-catalogue-2 .ListParagraph}

#### Description {#description-36 .ListParagraph}

> Newfoundland & Labrador's Open Data site contains the province's open
> datasets. It contains geospatial datasets and open data applications.
> Unlike other catalogues, there is no search functionality.

#### URLs {#urls-23 .ListParagraph}

##### Home URL {#home-url .ListParagraph}

> <http://opendata.gov.nl.ca/public/opendata/page/?page-id=home>

##### Geospatial URL {#geospatial-url .ListParagraph}

> <http://opendata.gov.nl.ca/public/opendata/page/?page-id=datasets-spatial>

#### Extraction Process {#extraction-process-28 .ListParagraph}

> All the province's geospatial datasets are listed on a single page.
> The steps for scraping the page are:

1.  Locate all \<div\> tags containing the class "well". The \<div\>
    tags containing this class are each of the items in the search
    results.

2.  Cycle through each result and extract the metadata link from the
    'View Full Metadata and File(s)' button.

3.  On the metadata page, all the inventory information is located in
    \<dt\> tags in each result.

    ![](media/image55.png){width="6.5in" height="5.655555555555556in"}

Figure C‑39 The GeoSpatial results of the Newfoundland & Labrador open
data

![](media/image56.png){width="6.5in" height="5.655555555555556in"}

Figure C‑40 The metadata of one of the datasets in the NL open data
catalogue

### Web Pages {#web-pages-4 .ListParagraph}

#### Fisheries & Land Resources -- Digital Map Index {#fisheries-land-resources-digital-map-index .ListParagraph}

##### Description {#description-37 .ListParagraph}

> The Digital Map Index for the Department of Fisheries and Land
> Resources contains various Google Earth Files (KML & KMZ).

##### URLs {#urls-24 .ListParagraph}

> <http://www.flr.gov.nl.ca/lands/maps/digital_map.html>

##### Extraction Process {#extraction-process-29 .ListParagraph}

> The script basically scrapes the website for the links to the KML and
> KMZ files. The specific steps are:

1.  To get the description, search for the first \<p\> element which
    contains the description of the web page.

2.  Get a list of anchors and extract each of the href if they contain
    '.kmz' or '.kml'.

#### Municipal Affairs & Environment - GIS Data - Public Water Supplies {#municipal-affairs-environment---gis-data---public-water-supplies .ListParagraph}

##### Description {#description-38 .ListParagraph}

This website contains a single link to the Public Water Supply Area
shapefile which is updated daily.

##### URLs {#urls-25 .ListParagraph}

<http://www.mae.gov.nl.ca/waterres/gis/gis.html>

##### Extraction Process {#extraction-process-30 .ListParagraph}

For this site, basic scraping is used to extract the link of the
zipfile. Here are the steps:

1.  Open the page and soup it up.

2.  Unfortunately, there are no 'id' or 'class' values for the zipfile
    link so the previous element needs to be found first. The previous
    element is a 'strong' with text value '**ILUC'.**

3.  Get the parent of the 'strong' element.

4.  Locate the anchor from the parent which will contain the zipfile
    link.

#### Municipal Affairs & Environment - Flood Risk Mapping Studies / Public Information Maps {#municipal-affairs-environment---flood-risk-mapping-studies-public-information-maps .ListParagraph}

##### Description {#description-39 .ListParagraph}

> This website contains links to all the studies and mapping associated
> with flood risk mapping in the Province. Most files are in Autocad DWG
> format and a few are shapefiles.

##### URLs {#urls-26 .ListParagraph}

> <http://www.mae.gov.nl.ca/waterres/flooding/frm.html>

##### Extraction Process {#extraction-process-31 .ListParagraph}

> The script scrapes the website looking for any links containing a DWG
> file or a shapefile. The information is contained in a table and each
> dataset is a separate row. The steps are:

1.  Extract the description by finding the first \<p\> element.

2.  Extract all the \<tr\> (rows) elements on the page.

3.  Cycle through each row and get the \<td\> (column) element.

4.  Find all the anchors that contain either 'DWG' or 'Shapefile' in
    their text and extract their URLs.

#### Environment & Climate Change -- Water Resources Portal {#environment-climate-change-water-resources-portal .ListParagraph}

##### Description {#description-40 .ListParagraph}

> This page contains links to various water resource maps in different
> formats, such as KMZ, LYR and WMS.

##### URLs {#urls-27 .ListParagraph}

> <http://maps.gov.nl.ca/water/mapservices.htm>

##### Extraction Process {#extraction-process-32 .ListParagraph}

> The steps for scraping this page are:

1.  The map datasets are located in the \<table\> elements of the page.

2.  The **Title** is found in the first \<h3\> in the \<table\> element.

3.  The rest of the information for the inventory CSV file is located in
    the \<tr\> elements (rows) of each table.

### Interactive Maps {#interactive-maps-7 .ListParagraph}

#### Education & Early Childhood Development - Early Learning and Child Care Directory {#education-early-childhood-development---early-learning-and-child-care-directory .ListParagraph}

##### Description {#description-41 .ListParagraph}

> The page contains an interactive Google Map with locations of
> regulated child care services throughout the province. The map
> contains the locations of Child Care Centres, Family Resource Centres,
> Satellite Locations and Family Child Care Providers.

##### URLs {#urls-28 .ListParagraph}

> <http://childcare.gov.nl.ca/public/ccr/>

##### Extraction Process {#extraction-process-33 .ListParagraph}

> Since the map is a Google Map, the data cannot be extracted into JSON
> formatted results. The inventory information is located in different
> elements on the page. The extraction steps are:

1.  The **Title** of the map is found getting the \<h1\> element's text
    in a \<div\> with id containing "gnlcontent".

2.  The **Description** is located in a \<p\> within the same \<div\> as
    the previous step.

#### Data Visualization and Mapping Suite {#data-visualization-and-mapping-suite .ListParagraph}

##### Description {#description-42 .ListParagraph}

> The Data Visualization and Mapping Suite page is part of the Community
> Accounts project. The project is an online data retrieval system for
> locating, sharing and exchanging information regarding the people of
> the province.

##### URLs {#urls-29 .ListParagraph}

###### Main URL {#main-url-6 .ListParagraph}

> <http://nl.communityaccounts.ca/mapcentre/>

###### About URL {#about-url .ListParagraph}

> <http://nl.communityaccounts.ca/about_us.asp>

##### Extraction Process {#extraction-process-34 .ListParagraph}

> The main page contains drop-down lists to determine which datasets to
> load into the mapping suite. Here are the steps for extracting this
> map suite:

1.  Each dataset is contained in the \<option\> elements within the
    \<select\> element drop-down list that contains id "s\_g".

2.  Cycle through each \<option\> element which contains text that will
    be used for the **Title** of the dataset in the inventory.

3.  The **Description** is located in the \<p\> element of the About
    page.

#### Education & Early Childhood Development - Early Childhood Programs and Services {#education-early-childhood-development---early-childhood-programs-and-services .ListParagraph}

##### Description {#description-43 .ListParagraph}

> This page contains a Google Map which contains the locations of Early
> Childhood Programs and Services throughout the province.

##### URLs {#urls-30 .ListParagraph}

> <http://www.ed.gov.nl.ca/edu/earlychildhood/guide.html>

##### Extraction Process {#extraction-process-35 .ListParagraph}

> This list contains the element locations on the page for the inventory
> information:

1.  The **Title** is contained in the \<h1\> on the page.

2.  The **Description** is in a \<div\> with class "section\_divider".

#### Western NL Onshore Petroleum Data {#western-nl-onshore-petroleum-data .ListParagraph}

##### Description {#description-44 .ListParagraph}

> This ArcGIS Online Map contains the various information for the
> province's petroleum activities.

##### URLs {#urls-31 .ListParagraph}

> <http://www.arcgis.com/home/webmap/viewer.html?webmap=f6e1e859a7c24ca89b5d9d8b93148731>

##### Extraction Process {#extraction-process-36 .ListParagraph}

> The extraction process is the same as all other ArcGIS Online Map
> extractions. The data URL, determined by the webmap ID, is used to
> obtain the JSON formatted map information.

#### Petroleum Geology of Newfoundland's Onshore Basins {#petroleum-geology-of-newfoundlands-onshore-basins .ListParagraph}

##### Description {#description-45 .ListParagraph}

> This ArcGIS Online Map contains the onshore basins on the west coast
> of Newfoundland.

##### URLs {#urls-32 .ListParagraph}

> <http://www.arcgis.com/apps/MapJournal/index.html?appid=98298581238b45f89aeadfb33e5036b9>

##### Extraction Process {#extraction-process-37 .ListParagraph}

> The extraction process is the same as all other ArcGIS Online Map
> extractions. The data URL, determined by the appid ID, is used to
> obtain the JSON formatted map information.

#### Community Infrastructure Mapping System (CIMS) {#community-infrastructure-mapping-system-cims .ListParagraph}

##### Description {#description-46 .ListParagraph}

> The CIMS map is a Google Map with locations throughout the province
> for health, education, heritage, tourism, and transportation.

##### URLs {#urls-33 .ListParagraph}

###### Parent URL {#parent-url .ListParagraph}

> <http://www.nlcims.ca/>

###### Map URL {#map-url .ListParagraph}

> <http://nlcims.ca/CIMS.aspx>

##### Extraction Process {#extraction-process-38 .ListParagraph}

> The following are the steps for extracting the information from the
> CIMS map:

1.  The **Description** is extracted from the parent page where the
    element \<h3\> contains text "About CIMS". The description text is
    in the \<p\> element under the \<h3\>.

2.  On the map page, get a list of layers by finding all \<a\> elements
    with class "groupToggle" under the \<ul\> with id "layerGroups".

3.  Cycle through each layer and save it to the CSV file with the
    **Title** taken from the text of the \<a\>.

#### Topographic Map Viewer {#topographic-map-viewer .ListParagraph}

##### Description {#description-47 .ListParagraph}

> The Topographic Map Viewer contains a topographic map of the entire
> province of Newfoundland and Labrador.

##### URLs {#urls-34 .ListParagraph}

> <http://mapsnl.ca/mapguide/Topo/>

##### Extraction Process {#extraction-process-39 .ListParagraph}

> The only item that can be extracted from the map viewer is the title
> (and of course the map URL). The **Title** is taken from the web
> page's \<title\>.

### Web Map Services {#web-map-services .ListParagraph}

#### Description {#description-48 .ListParagraph}

> The Province of Newfoundland & Labrador contains 3 ESRI REST Map
> Services: the Department of Natural Resources, Land Use Atlas and
> Water Resources Portal.

#### URLs {#urls-35 .ListParagraph}

##### Department of Natural Resources {#department-of-natural-resources .ListParagraph}

> <http://dnrmaps.gov.nl.ca/arcgis/rest/services>

##### Land Use Atlas {#land-use-atlas .ListParagraph}

> <https://www.gov.nl.ca/landuseatlasmaps/rest/services>

##### Water Resources Portal {#water-resources-portal .ListParagraph}

> <http://maps.gov.nl.ca/gsdw/rest/services/water>

#### Extraction Process {#extraction-process-40 .ListParagraph}

> The extraction process for the web map services is in Section 3.6.

### Municipal Pages {#municipal-pages .ListParagraph}

#### Gander Map Viewer {#gander-map-viewer .ListParagraph}

##### Description {#description-49 .ListParagraph}

> The Gander Map Viewer is the main map for the City of Gander and
> includes land uses, roads, air photos and many other datasets related
> to the city.

##### URLs {#urls-36 .ListParagraph}

###### Main URL {#main-url-7 .ListParagraph}

> <http://geonl.net/mapguide/GanderPublic>

###### Layers List URL {#layers-list-url .ListParagraph}

> <http://geonl.net/mapguide/GanderPublic/Gander_LayerUpdates.php>

##### Extraction Process {#extraction-process-41 .ListParagraph}

> In the Extractor object for Newfoundland & Labrador, a method called
> parse\_legend is used to extract the layers from the layer list page.
>
> Here are the steps in the parse\_legend method:

1.  Get all the \<p\> elements on the layer list page.

2.  The **Spatial Reference** is in the second \<p\>.

3.  Go through the rest of the \<p\> elements and add them to the CSV
    inventory file.

#### Labrador City Map Viewer {#labrador-city-map-viewer .ListParagraph}

##### Description {#description-50 .ListParagraph}

> Like the Gander Map Viewer, the Labrador City Map Viewer is the main
> map for the city and includes land uses, roads, air photos and many
> other datasets.

##### URLs {#urls-37 .ListParagraph}

###### Main URL {#main-url-8 .ListParagraph}

> <http://labcitymaps.ca>

###### Layers List URL {#layers-list-url-1 .ListParagraph}

> <http://labcitymaps.ca/mapguide/LabCityPublic/LayerUpdates.php>

##### Extraction Process {#extraction-process-42 .ListParagraph}

> The extraction process for this map viewer is the same as the Gander
> Map Viewer.

### Other Pages {#other-pages .ListParagraph}

#### Iceberg Finder Map {#iceberg-finder-map .ListParagraph}

##### Description {#description-51 .ListParagraph}

> The Iceberg Finder map contains the location of icebergs found by
> satellite imagery or by photos on the ground provided by users.

##### URLs {#urls-38 .ListParagraph}

> <http://www.icebergfinder.com>

##### Extraction Process {#extraction-process-43 .ListParagraph}

> The inventory information is only extracted from the \<meta\> element
> of the page. The two items in the metadata are the **Title** and the
> **Description**.

Northwest Territories {#northwest-territories .ListParagraph}
---------------------

### NWT Discovery Portal {#nwt-discovery-portal .ListParagraph}

#### Description {#description-52 .ListParagraph}

> The Discovery Portal is a search tool that provides access to data,
> metadata and reports of the Northwest Territories.

#### URLs {#urls-39 .ListParagraph}

##### Main URL {#main-url-9 .ListParagraph}

> <http://nwtdiscoveryportal.enr.gov.nt.ca>

##### Query URL {#query-url-1 .ListParagraph}

> <http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/rest/find/document>

#### Extraction Process {#extraction-process-44 .ListParagraph}

##### Query to Get JSON Data {#query-to-get-json-data-6 .ListParagraph}

> The query URL for NWT Discovery Portal is similar to other provincial
> geoportals. **The query string can include the following parameters:**

-   **f**: The output format of the results

-   **max**: The number of items to return in the results

-   **cpublisher**: Filter the results by publication organization.

-   **dataCategory**: Filters the results by Data Category.

-   **kwcustom**: Filters the results by Data Type or Subject Area.

-   **start**: The number of the item to start at.

-   **orderBy**: Sort results by relevance, title, format,
    dateAscending, dateDescending, areaAscending and areaDescending.

-   **after**: Remove results before this date.

-   **before**: Remove results after this date.

-   **spatialRel**: Spatial relation to the bounding box. The options
    are:

    -   Anywhere: Default, no value needed.

    -   Intersecting: esriSpatialRelOverlaps

    -   Fully within: esriSpatialRelWithin

-   **bbox**: The bounding box in which to search (minx, miny, maxx,
    maxy).

-   **maxSearchTimeMilliSec**: The maximum amount of time in
    milliseconds the search will take.

-   **showRelativeUrl**: Determines whether relative paths should be
    used in the results.

-   **searchText**: The search text used to filter the results.

> Here's an example of a query URL for the NWT Discovery Portal:

-   Query URL:
    [http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/rest/find/document?f=pjson&start=1&max=100&kwcustom=\"Geospatial
    Data (Raster)\",\"Geospatial Data
    (Vector)\"](http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/rest/find/document?f=pjson&start=1&max=100&kwcustom=%22Geospatial%20Data%20(Raster)%22,%22Geospatial%20Data%20(Vector)%22)

<!-- -->

-   Results:

> The results are provided in a JSON format containing information on
> the query (title, description, source, number of results, etc.) and
> the records are in a list under the "records" field.

##### Extract Results {#extract-results-9 .ListParagraph}

> The next step is to extract the information from the JSON results
> using Python. The process is the same as other portals:

5.  Using the JSON results in a Python script, grab the "records" list
    mentioned above.

6.  The JSON results for the portal includes the title, summary, date
    and metadata link.

7.  The metadata link provides the metadata as an XML.

8.  Scrape the XML metadata using BeautifulSoup and use it to retrieve
    the rest of the information, such as the metadata type, spatial
    reference, download link, available formats, date type, licensing
    and publisher.

### Web Pages {#web-pages-5 .ListParagraph}

#### Environment & Natural Resources {#environment-natural-resources .ListParagraph}

##### Description {#description-53 .ListParagraph}

> The Environment & Natural Resources site has a GPS file which contains
> the Mobile Core Bathurst Caribou Management Zone.

##### URLs {#urls-40 .ListParagraph}

> <http://www.enr.gov.nt.ca/en/services/mobile-core-bathurst-caribou-management-zone>

##### Extraction Process {#extraction-process-45 .ListParagraph}

> The steps for extracting this GPS file is:

1.  Locate an \<a\> containing text with ".gpx" and get its download
    link.

2.  Get the **Title** from a \<h1\> in the \<div\> with class
    "service-banner-title".

3.  The **Description** is found by:

    a.  Locating an \<a\> with id "what-is-the-mobile-zone"

    b.  Getting the \<a\> parent, a \<h2\>

    c.  Getting the next sibling of the \<h2\>, a \<p\>

    d.  Getting the text of the next sibling of the \<p\>, another
        \<p\>.

#### Centre of Geomatics {#centre-of-geomatics .ListParagraph}

##### Description {#description-54 .ListParagraph}

> The Centre of Geomatics contains a list of geospatial datasets for
> download. However, registration is required to access the list.

##### URLs {#urls-41 .ListParagraph}

###### Main URL {#main-url-10 .ListParagraph}

> <http://www.geomatics.gov.nt.ca/>

###### Login URL {#login-url .ListParagraph}

> <http://www.geomatics.gov.nt.ca/dldsoptions.aspx>

##### Extraction Process {#extraction-process-46 .ListParagraph}

> For the inventory, the page of the list has been saved in the "files"
> folder of the FGP P/T Web Extractor and is called "NWT Centre for
> Geomatics.html".
>
> Using the saved HTML file, these are the steps for extracting the
> datasets:

1.  Get the \<table\> with id
    "MainContent\_HeadLoginView\_gv\_dlcatlisting".

2.  Use table\_to\_dict in the shared.py to extract the table for the
    inventory.

3.  The **Title** is taken from the "category" column and the
    **Description** is taken from the "description" column.

### Interactive Maps {#interactive-maps-8 .ListParagraph}

#### NWT Fish Consumption Notices {#nwt-fish-consumption-notices .ListParagraph}

##### Description {#description-55 .ListParagraph}

> In this map, the Department of Health and Social Services provides
> fish consumption notices which specify the safe consumption limits for
> various lakes throughout the territory.

##### URLs {#urls-42 .ListParagraph}

> <http://www.arcgis.com/home/webmap/viewer.html?webmap=7199b8175dac48dc8513c824e39aa3fd>

##### Extraction Process {#extraction-process-47 .ListParagraph}

> The extraction process for this map is the same process as other
> ArcGIS Online maps (see 3.5.2.1).

#### NT GoMap {#nt-gomap .ListParagraph}

##### Description {#description-56 .ListParagraph}

> The NT GoMap provides access to geospatial datasets and reports of the
> Northwest Territories Geological Survey. The GoMap only loads in
> Firefox.

##### URLs {#urls-43 .ListParagraph}

###### Map URL {#map-url-1 .ListParagraph}

> <http://ntgomap.nwtgeoscience.ca/>

###### Layer List URL {#layer-list-url .ListParagraph}

> <http://ntgomap.nwtgeoscience.ca/config/layerList.xml>

##### Extraction Process {#extraction-process-48 .ListParagraph}

> All the layers of the map can be accessed from layer list XML page.
>
> The steps for extracting the layers are:

1.  Get a list of all the layers by finding all the \<layer\> elements
    on the XML page.

2.  In each layer, the **Title** can be found under the \<layerID\>
    element.

#### ArcGIS Hub {#arcgis-hub .ListParagraph}

##### Description {#description-57 .ListParagraph}

> The Northwest Territories Geological Survey (NTGS) has over 40
> interactive maps in the ArcGIS Hub.

##### URLs {#urls-44 .ListParagraph}

###### NTGS ArcGIS Hub URL {#ntgs-arcgis-hub-url .ListParagraph}

> <https://datahub-ntgs.opendata.arcgis.com/datasets>

###### ArcGIS Hub Datasets URL {#arcgis-hub-datasets-url .ListParagraph}

> <https://opendata.arcgis.com/api/v2/datasets>

##### Extraction Process {#extraction-process-49 .ListParagraph}

> While the datasets are listed on the NTGS ArcGIS Hub page, the
> information for the inventory can be extracted using the Datasets URL
> which returns the info in a JSON format.
>
> Here are the steps for extracting the Hub:

1.  Create the query string using the ArcGIS Hub Datasets URL with the
    following parameters:

    -   **filter\[catalog\]**: The domain of the NTGS ArcGIS Hub
        ("datahub-ntgs.opendata.arcgis.com")

    -   **include**: Include certain categories
        (sites,organizations,groups)

    -   **page\[number\]**: Number of pages.

    -   **page\[size\]**: Number of items per page.

    -   Ex:
        [https://opendata.arcgis.com/api/v2/datasets?filter\[catalogs\]=datahub-ntgs.opendata.arcgis.com&include=sites,organizations,groups&page\[number\]=1&page\[size\]=310](https://opendata.arcgis.com/api/v2/datasets?filter%5bcatalogs%5d=datahub-ntgs.opendata.arcgis.com&include=sites,organizations,groups&page%5bnumber%5d=1&page%5bsize%5d=310)

2.  Get all the datasets from the 'data' item in the JSON.

3.  For each dataset, get the following inventory items from the
    'attributes' item:

    -   **Title** from 'name'

    -   **Description** from 'description'

    -   **Type** from 'dataType'

    -   **Date** from 'updateAt'

    -   **Web Page URL** from 'landingPage'

    -   **Web Service URL** from 'url'

### Map Services {#map-services-5 .ListParagraph}

#### Description {#description-58 .ListParagraph}

> The Northwest Territories includes 2 ESRI REST services and 1
> Geocortex service.

#### URLs {#urls-45 .ListParagraph}

##### ESRI REST URLs {#esri-rest-urls .ListParagraph}

> <https://www.apps.geomatics.gov.nt.ca/ArcGIS/rest/services>
>
> <https://www.image.geomatics.gov.nt.ca/ArcGIS/rest/services>

##### Geocortex URL {#geocortex-url .ListParagraph}

> <http://apps.geomatics.gov.nt.ca/Geocortex/Essentials/REST/sites>

#### Extraction Process {#extraction-process-50 .ListParagraph}

> The extraction process for the Northwest Territories is the same as
> other service extractions (see Section 3.6).

Nova Scotia {#nova-scotia .ListParagraph}
-----------

### Catalogues {#catalogues-1 .ListParagraph}

#### Description {#description-59 .ListParagraph}

> Nova Scotia's Open Data Portal provides access to over 500 datasets
> using a search engine.

#### URLs {#urls-46 .ListParagraph}

##### Main URL {#main-url-11 .ListParagraph}

> <https://data.novascotia.ca/browse>

#### Extraction Process {#extraction-process-51 .ListParagraph}

> The extraction process for the Nova Scotia Data Portal is similar to
> other provincial/territorial catalogues.
>
> The steps for extraction are:

1.  Build the query URL string using the main URL and these parameters:

-   **q**: Filter the results by key word search.

-   **category**: Filter the results by the category.

-   **limitTo**: Filter by a specific type.

-   **tags**: Filter the results by tag.

-   **sortBy**: Specifies how to sort the results.

2.  Soup the results of the query and determine the page count.

3.  For each page:

    a.  Get the results of the page by finding all the \<div\> elements
        with class "browse2-result".

    b.  Find the **Title** of each result in the \<a\> with class
        "browse2-result-name-link".

    c.  Using the link from the \<a\> element, get the JSON data of the
        result.

    d.  Using the JSON data, get:

        -   the **Description** from the "description" key

        -   the **Date** from the "indexUpdatedAt" key

        -   the **Licensing** from the "name" under "license"

        -   the **Spatial Reference** from the "bboxCrs" under "geo"
            which is under "metadata"

        -   the **Publisher** from the "displayName" under
            "tableAuthor".

### Web Pages {#web-pages-6 .ListParagraph}

#### Department of Natural Resources {#department-of-natural-resources-1 .ListParagraph}

##### Description {#description-60 .ListParagraph}

> The Department of Natural Resources contains several pages with
> geospatial datasets for download.

##### URLs {#urls-47 .ListParagraph}

> See the extraction process

##### Extraction Process {#extraction-process-52 .ListParagraph}

###### Ecological Land Classification {#ecological-land-classification .ListParagraph}

> URL: <https://novascotia.ca/natr/forestry/ecological/ecolandclass.asp>
>
> The Ecological Land Classification (ELC) is a mapping tool that
> identifies areas with similar physical attributes. The site contains 4
> geospatial downloads: 2 for the 2007 report and 2 for the 2015 report.
>
> The steps for extracting the ELC site are:

1.  Find a \<div\> with id "main" and then get the \<p\> to get the
    **Description**.

2.  Locate the \<h3\> with text "Ecological Land Classification for Nova
    Scotia:"

3.  Get the next sibling \<p\> of the \<h3\> to get the **Licensing**
    link (usually the Licensing value is text however since the
    licensing for the ELC has its own page, the URL is used).

4.  Find all the \<strong\> elements on the page and use the text of
    each \<strong\> element for the **Title** of datasets.

###### Forest Inventory {#forest-inventory-1 .ListParagraph}

> URL:
>
> Cycle 1:
> <https://novascotia.ca/natr/forestry/gis/DL_forestry-cycle1.asp>
>
> Cycle 2:
> <https://novascotia.ca/natr/forestry/gis/DL_forestry-cycle2.asp>
>
> Cycles 2 & 3:
> <https://novascotia.ca/natr/forestry/gis/dl_forestry.asp>
>
> The Forest Inventory Program of Nova Scotia monitors changes in the
> province's forests to help make choices on sustainable forest
> management. The site contains sub-pages to 3 cycles of data
> acquisition.
>
> Each cycle page contains a \<map\> element with \<area\> elements for
> each county in the province. Here are the steps for extracting each
> page of cycles:

1.  Get the cycle number by parsing the page's URL. Separate the URL by
    the "-" and then get the second item in the split. Remove the ".asp"
    from the text.

2.  The **Description** for these items is found in a PDF file on the
    page. To get the PDF:

    a.  Locate the \<a\> with text "View Attribute Descriptions and
        Coding"

    b.  Use the link of the \<a\> to open the PDF using the
        PdfFileReader object in Python.

    c.  In the PDF file, go through each page and search for the
        position of the text "Description/Source". Once found get all
        the text after this position.

3.  Go through each \<area\> getting a list of counties.

4.  Go through each county, using the county name for the **Title** of
    each dataset.

![](media/image57.png){width="6.5in" height="7.086805555555555in"}

Figure 2‑1 The 1st Cycle of the Forest Inventory of Nova Scotia

###### Fernow Forest Cover {#fernow-forest-cover .ListParagraph}

> URL: <https://novascotia.ca/natr/forestry/gis/fernow.asp>
>
> This site contains downloads for the digitized documents of the
> "Forest Conditions of Nova Scotia" report published in 1912.

The steps for extracting the inventory information for this page are:

1.  Get the **Download** link from an \<a\> with text "Download data".

2.  Get the **Metadata URL** from the next sibling \<a\> of the previous
    step's element.

3.  Open the metadata XML page to get the following:

    -   **Title** from \<title\>

    -   **Description** from \<abstract\>

    -   **Type** from \<geoform\>

    -   **Publisher** from \<origin\>

    -   **Date** from \<caldate\>

    -   **Metadata Type** from \<metsdn\>

    -   **Spatial Reference** from \<projcsn\>

###### Hurricane Juan Imagery {#hurricane-juan-imagery .ListParagraph}

> URL: <https://novascotia.ca/natr/forestry/gis/juanimg.asp>
>
> This page contains orthomosaics of photos flown between October and
> November 2003 showing the damage caused by Hurricane Juan in September
> 2003.
>
> The downloads are located in a table with no header information and
> each cell is a separate orthomosaic download. The steps for extracting
> these downloads are:

1.  Find the main \<div\> with id "main".

2.  Locate the first \<p\> element in the main \<div\> to get the
    **Description**.

3.  Locate all the \<td\> elements (columns in the table) in the main
    \<div\>.

4.  Go through each column in the table and get the \<a\> to get the
    **Title** and the **Download** link.

###### Land Capability for Forestry {#land-capability-for-forestry .ListParagraph}

> URL: <https://novascotia.ca/natr/forestry/gis/landcap.asp>
>
> The Land Capability for Forestry site has digitized maps at 1:50,000
> scale from the federal Canada Land Inventory program carried out from
> 1963 to 1994.
>
> The page contains a \<map\> with the counties of Nova Scotia in
> \<area\> elements. To obtain the inventory information for these
> counties, use the following steps:

1.  Get the Metadata URL from the \<a\> with text "View metadata".

2.  Open the metadata XML page to get the following:

    a.  **Title** from \<title\>

    b.  **Description** from \<abstract\>

    c.  **Type** from \<geoform\>

    d.  **Publisher** from \<origin\>

    e.  **Date** from \<caldate\>

    f.  **Metadata Type** from \<metsdn\>

    g.  **Spatial Reference** from \<projcsn\>

3.  Get a list of counties from the \<area\> elements on the \<map\>.

4.  Go through each county and get the county name. Append the county
    name to the existing **Title** so it is "\<title\_from\_metadata\> -
    \<county\_name\>".

###### Wet Areas Mapping {#wet-areas-mapping .ListParagraph}

> URL: <https://novascotia.ca/natr/forestry/gis/wamdownload.asp>
>
> This page contains datasets from the wet areas mapping project
> conducted by the University of New Brunswick.
>
> The extraction process is similar to the Land Capability for Forestry
> site. The page contains a \<map\> with the counties of Nova Scotia in
> \<area\> elements. To obtain the inventory information for these
> counties, use the following steps:

1.  Get the Metadata URL from the \<a\> with text "View WAM metadata".

2.  Open the metadata XML page to get the following:

    a.  **Title** from \<title\>

    b.  **Description** from \<abstract\>

    c.  **Type** from \<geoform\>

    d.  **Publisher** from \<origin\>

    e.  **Date** from \<caldate\>

    f.  **Metadata Type** from \<metsdn\>

    g.  **Spatial Reference** from \<projcsn\>

3.  Get a list of counties from the \<area\> elements on the \<map\>.

4.  Go through each county and get the county name. Append the county
    name to the existing **Title** so it is "\<title\_from\_metadata\> -
    \<county\_name\>".

###### Significant Species and Habitats Database {#significant-species-and-habitats-database .ListParagraph}

> URL: <https://novascotia.ca/natr/wildlife/habitats/hab-data>
>
> The datasets on this page contain locations throughout Nova Scotia of
> sites where species are at risk, where unusually large concentrations
> of wildlife occur and where habitats are rare in the province.
>
> The information for this page can be obtained by following these
> steps:

1.  Locate the \<strong\> with text "Download ArcView Shapefiles - (UTM,
    NAD83, Zone 20)".

2.  Find the next sibling \<strong\> of the previous element to get the
    **Date** for all the datasets.

3.  Get the parent of the \<strong\> in step 2 and then get the next
    sibling \<ul\>.

4.  Go through all the \<a\> elements under the \<ul\> and:

    a.  Find a \<p\> with text "Significant habitats include;" for the
        **Description**.

    b.  Find the next sibling \<ol\>, get all the \<li\> and add their
        text to the **Description**.

#### Geographic Data Directory {#geographic-data-directory .ListParagraph}

##### Description {#description-61 .ListParagraph}

> The Geographic Data Directory contains a list of about 50 geospatial
> datasets for the province of Nova Scotia.

##### URLs {#urls-48 .ListParagraph}

###### Main URL {#main-url-12 .ListParagraph}

> <https://nsgi.novascotia.ca/gdd>

###### JSON URL {#json-url .ListParagraph}

> <https://nsgi.novascotia.ca/WSF_DDS/DDS.svc/ListData?tkey=kNNpTdP4QuNRSYtt>

##### Extraction Process {#extraction-process-53 .ListParagraph}

> These are the step for extracting the Geographic Data Directory:

1.  Get the JSON results using the get\_json method in the shared.py
    script.

2.  Parse the JSON URL to get the tkey value.

3.  For each result in the results item in the JSON:

    a.  Get the **Title** from the 'title' item.

    b.  Get the **Description** from the 'description' item.

    c.  Get the **Date** from the 'published' item.

    d.  Get the **Service URL** from the 'map\_service\_url' item.

    e.  Get the **Service** from the 'ms\_layer\_type\' item.

### Interactive Maps {#interactive-maps-9 .ListParagraph}

#### Description {#description-62 .ListParagraph}

#### URLs {#urls-49 .ListParagraph}

> See the extraction processes below.

#### Extraction Process {#extraction-process-54 .ListParagraph}

##### Nova Scotia Provincial Map {#nova-scotia-provincial-map .ListParagraph}

> URL: <https://www.novascotia.com/map>
>
> The Nova Scotia Provincial Map contains various locations containing
> information for tourism, points of interest, hotels, parks,
> recreation, restaurants, etc.
>
> Both the **Title** and **Description** is taken from the page's
> metadata.

##### Confederacy of Mainland Mi\'kmaq - Member Communities {#confederacy-of-mainland-mikmaq---member-communities .ListParagraph}

> URL: <http://cmmns.com/member-communities>
>
> The map on this page shows the location of the seven member
> communities of The Confederacy of Mainland Mi'kmaq.
>
> The only inventory item to extract from this page is the **Title**
> which is taken from page's title. All other information is determined
> by the map being a Google Map, such as the **Spatial Reference** and
> the **Type**. The **Web Map URL** is the page's URL.

##### EcoSystem Indicator Partnership {#ecosystem-indicator-partnership .ListParagraph}

> URL: <http://www2.gulfofmaine.org/esip/reporting/gmap2.php>
>
> The map on the EcoSystem Indicator Partnership page contains
> indicators for the Gulf of Maine. The indicators focus on coastal
> development, contaminants and pathogens, eutrophication, aquatic
> habitat, fisheries and aquaculture, and climate change.
>
> The **Title** for the map is taken from the title of the web page. The
> **Description** is taken from a \<p\> under a \<div\> with id
> "help-box-about-esip".

##### DataLocator {#datalocator .ListParagraph}

> URL:
> <https://gis8.nsgc.gov.ns.ca/esrimap/esrimap.dll?name=DataLocator&cmd=0&t=5330999&b=4728598&l=169676&r=915634&nt=0&nb=0&nl=0&nr=0&action=overview&X=0&Y=0&ind=0&objid=0&DIon=True&NDIon=False&PIon=False&la=&hPid=0&pb=&sz=1&ind=25&searchType=pn&sI=&st=pn&County=&zR=2&il=25>
>
> The DataLocator page contains links to help search for geographic data
> collections available in Nova Scotia. The page contains links to 2
> interactive maps.
>
> The steps for extracting the DataLocator page are:

1.  Find all the \<div\> elements with class "item".

2.  For each item:

    a.  Get the **Title** from the \<a\> with class "item\_title".

    b.  Get the **Description** from the \<p\> with class "description".

    c.  Get the **Web Map URL** from the title \<a\>.

##### Map of First Nations in Nova Scotia {#map-of-first-nations-in-nova-scotia .ListParagraph}

> URL: <https://novascotia.ca/abor/aboriginal-people/community-info>
>
> The map on this page contains the locations of Mi'kmaq First Nations
> communities across Nova Scotia.
>
> The **Title** for the inventory is located in an \<h1\> with id
> "page-title". The **Web Map URL** is the page's URL.

##### Map of Nova Scotia's Counties and Municipalities {#map-of-nova-scotias-counties-and-municipalities .ListParagraph}

> URL: <https://novascotia.ca/dma/government/map.asp>
>
> This page contains a map showing the location of Nova Scotia's
> Counties and Municipalities. However, as of August 24, 2018, the map
> does not load (the location on the page where the map should be is
> empty).
>
> The **Title** is taken from the page's title and the **Date** is found
> in the metadata under "dcterms.modified"

##### Provincial Landscape Viewer {#provincial-landscape-viewer .ListParagraph}

> Main URL: <https://nsgi.novascotia.ca/plv>
>
> JSON URL:
> <https://dnr-ns.maps.arcgis.com/sharing/rest/content/items/50cea634ffbf433ba5cde6961a9809b7?f=json>
>
> This map shows the different EcoDistricts of the Ecological Land
> Classification across Nova Scotia.
>
> The instructions for extracting this page are:

1.  Get the JSON data using the JSON URL.

2.  Get the **Title** from the 'title' item in the JSON data.

3.  Get the **Date** from the 'modified' item in the JSON data.

##### Nova Scotia Environment Publicly Featured Maps and Services {#nova-scotia-environment-publicly-featured-maps-and-services .ListParagraph}

> Gallery URL:
> <https://nse.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=true&sortField=relevance>
>
> The Gallery contains almost 40 ArcGIS maps for the province of Nova
> Scotia.
>
> The shared.py script contains a method for extracting ArcGIS
> galleries. The method get\_arcgis\_gallery gets all the maps on the
> page and opens up their ArcGIS JSON data.

### Geoscience & Mines Branch Interactive Maps {#geoscience-mines-branch-interactive-maps .ListParagraph}

#### Description {#description-63 .ListParagraph}

> The Geoscience & Mines Branch contains a page with links to
> downloadable GIS data and interactive maps.

#### URLs {#urls-50 .ListParagraph}

##### Main URL {#main-url-13 .ListParagraph}

> <https://novascotia.ca/natr/meb/download/gis-data-maps.asp>

#### Extraction Process {#extraction-process-55 .ListParagraph}

> The steps for extracting the GIS data page are:

1.  Find all the \<div\> elements with class "block".

2.  For each block \<div\>, find all \<li\> elements.

3.  For each \<li\> element:

    a.  Find the \<a\> and if the \<a\> has href attribute, add the link
        to a sub\_sites list. If the \<a\> has no href attribute, locate
        the \<ul\> in the \<li\>, get the \<a\> under the \<li\> and add
        the link to the sub\_sites list.

    b.  Create a map\_sites list with the following sites:

        -   interactive-bedrock-DNR-map.asp

        -   interactive-bedrock-GSC-map.asp

        -   interactive-map-surficial-data.asp

        -   interactive-map-radar-data.asp

        -   interactive-seismic-map.asp

        -   interactive-gold-district-map-data-east.asp

        -   interactive-gold-district-map-data-west.asp

        -   interactive-agg-gis.asp

        -   interactive-map-airmag-1D-data.asp

        -   interactive-map-airmag-2DD-data.asp

        -   interactive-map-airmag-2DR-data.asp

        -   interactive-map-airmag-TF-data.asp

        -   interactive-map-gravity-BR-data.asp

        -   interactive-map-gravity-RBR-data.asp

        -   interactive-map-airborneVLFR-data.asp

        -   interactive-map-airborneVLFQR-data.asp

4.  For each site in the sub\_sites list:

    c.  If the current sub site URL contains one of the map\_sites, open
        the sub page, locate all the \<area\> elements and use the
        \<area\> link to run the get\_gis\_page method in the Extractor
        class.

    d.  If the current sub site URL contains "geochemistry.asp", locate
        all the \<div\> elements with class "ui-accordion-content", find
        an \<a\> with text "Find Out More" and use its link to run the
        get\_gis\_page method in the Extractor class.

    e.  If the current sub site URL contains
        "gis-data-maps-provincial.asp", locate the \<div\> with id
        "wrapper", find all \<div\> elements with class "block medium"
        and use each \<a\> under the block \<div\> to run the
        get\_gis\_page method.

    f.  If the current sub site URL doesn't contain any of the above,
        use the sub site URL to run the get\_gis\_page method.

![](media/image58.png){width="6.5in" height="6.632638888888889in"}

Figure 4‑1 The Downloadable GIS Data page with links to datasets and
interactive maps

### Map Services {#map-services-6 .ListParagraph}

#### Description {#description-64 .ListParagraph}

> The province of Nova Scotia has several ArcGIS REST Services and one
> Geocortex.

#### URLs {#urls-51 .ListParagraph}

> <https://fletcher.novascotia.ca/arcgis/rest/services>

<https://nsgiwa.novascotia.ca/arcgis/rest/services>

> <https://novarocmaps.novascotia.ca/arcgis/rest/services>
>
> <https://gis7.nsgc.gov.ns.ca/arcgis/rest/services>
>
> <http://sparc.smu.ca:6080/arcgis/rest/services>
>
> <https://fernow.novascotia.ca/arcgis/rest/services>
>
> <https://fletcher.novascotia.ca/Geocortex/Essentials/REST/sites>

#### Extraction Process {#extraction-process-56 .ListParagraph}

> The extraction process for these services is the same as other
> provinces/territories and uses the get\_data method of the MyGeocortex
> and MyREST classes.

Nunavut {#nunavut .ListParagraph}
-------

### Government of Nunavut Community & Government Services Planning & Lands Division  {#government-of-nunavut-community-government-services-planning-lands-division .ListParagraph}

#### Description {#description-65 .ListParagraph}

> On these pages, the Department of Community and Government Services
> (CGS) of Nunavut provides access to community plans, mapping, by-laws
> and guides for Nunavummiut development projects. The main page
> contains a description for 3 categories of Community Planning, Land
> Administration and Data & Mapping. The other page contains a list of
> the datasets.

#### URLs {#urls-52 .ListParagraph}

##### Main URL {#main-url-14 .ListParagraph}

> <https://cgs-pals.ca/>

##### Shapefile Downloads URL {#shapefile-downloads-url .ListParagraph}

> <https://cgs-pals.ca/downloads/gis/>

##### Extraction Process {#extraction-process-57 .ListParagraph}

> Although the main page contains a lot of information about the CGS
> datasets, only the download page needs to be scraped as it includes
> all the necessary information for the inventory (see Figure 1‑1).

1.  Each set of datasets for each community is located under a \<div\>
    with class "download-group".

2.  Each dataset's metadata is in a \<span\> with title "about" under
    the \<div\>. The next steps are for each dataset.

3.  Get the JSON of the dataset from the data-info attribute of the
    \<span\>.

4.  The JSON contains:

    a.  The **Title** under "description" (remove " (Shapefile)" from
        the text to get the title)

    b.  The "metadata" which contains the **Spatial Reference**
        ("Coordinate System") and the **Date** ("Date Acquired")

![](media/image59.png){width="6.5in" height="5.655555555555556in"}

Figure C‑41 The CGS GIS Data page

### Maps & Data - Department of Lands and Resources {#maps-data---department-of-lands-and-resources .ListParagraph}

#### Description {#description-66 .ListParagraph}

> This page contains the map and data for the Department of Lands and
> Resources of Nunavut. There are 2 items on the page which are from the
> province, an interactive map and a shapefile of land parcels. The
> other items on the page are map documents (PDFs) or national datasets.

#### URLs {#urls-53 .ListParagraph}

##### Main URL {#main-url-15 .ListParagraph}

> <http://ntilands.tunngavik.com/maps/>

#### Extraction Process {#extraction-process-58 .ListParagraph}

##### Interactive Map {#interactive-map .ListParagraph}

> Here are the steps to extract the interactive map:

1.  The interactive map is located in an \<a\> with text "Online
    Interactive Map".

2.  The **Title** is the text of the \<a\>.

3.  The **Date** is extracted by locating the parent of the \<a\> and
    then getting the text of the parent and filtering for the date.

> NOTE: As of 2018-07-16, the interactive map is under construction.

##### Shapefile Download {#shapefile-download .ListParagraph}

> Here are the steps to extract the shapefile:

1.  Find the \<h3\> containing the text "GIS Datasets".

2.  Get the sibling \<div\> of the \<h3\>.

3.  The **Title** of the dataset is contained in the text of the
    \<div\>, removing any text after the "(".

4.  The **Date** is the text within the brackets of the \<div\> text.

![](media/image60.png){width="6.5in" height="5.655555555555556in"}

Figure C‑42 Nunavut Maps & Data page

### Nunaliit Atlas Framework  {#nunaliit-atlas-framework .ListParagraph}

#### Description {#description-67 .ListParagraph}

> The Nunaliit Atlas Framework provides users with the ability to build
> their own interactive maps.

#### URLs {#urls-54 .ListParagraph}

##### Main URL {#main-url-16 .ListParagraph}

<http://nunaliit.org/>

#### Extraction Process {#extraction-process-59 .ListParagraph}

For the extraction process, the information will be scraped from the
main URL mention above. The **Title** is taken from the \<p\> with
itemprop "name" and the **Description** is taken from the \<p\> with
itemprop "description".

Ontario {#ontario .ListParagraph}
-------

### Data Catalogue {#data-catalogue-1 .ListParagraph}

#### Description {#description-68 .ListParagraph}

> The Data Catalogue of Ontario is a search engine which locates data
> which is open, will soon be opened, restricted or data under review.

#### URLs {#urls-55 .ListParagraph}

##### Main URL {#main-url-17 .ListParagraph}

> https://www.ontario.[ca](https://www.ontario.ca/search/data-catalogue)/search/data-catalogue

#### Extraction Process {#extraction-process-60 .ListParagraph}

##### Query {#query-1 .ListParagraph}

> The URL for querying Ontario's data catalogue is
> https://www.ontario.[ca](https://www.ontario.ca/search/data-catalogue)/search/data-catalogue.
> The query string can have the following parameters:

-   **query**: Filter the results by key word search.

-   **topic**: Filter the results by topic.

-   **filetype**: Filter results by format type of the files.

-   **status:** Filter results by status. The statuses are represented
    by numbers:

    -   30 -- open

    -   20 -- to be opened

    -   10 -- under review

    -   0 -- restricted

-   **publisher**: Filter results by the publisher.

-   **sort**: Specifies how to sort the results.

> All parameter values, except **sort**, are contained in double-quotes
> and square brackets. For example, the following query URL returns open
> data results with KMLs:
>
> <https://www.ontario.ca/search/data-catalogue?sort=asc&filetype=%5B%22zip%22%5D&status=%5B%2230%22%5D>or
>
> https://www.ontario.ca/search/data-catalogue?sort=asc&filetype=\["zip"\]&status=\["30"\]

![](media/image61.png){width="6.5in" height="6.548611111111111in"}

Figure C‑43 The results of the above query filtering results with KMLs
and are open data

##### Page Loading {#page-loading .ListParagraph}

> For Ontario's data catalogue, the results are returned as a web page.
> However, unlike other provincial catalogues, each page of results is
> loaded by clicking the "Next 20" button at the bottom (see Figure 2).
> The button uses Javascript to expand the page by 20 more results. As a
> result, Selenium and Python is used to continually click the button
> until all the results have been loaded on the page (until the "Next
> 20" button no longer appears).

![](media/image62.png){width="6.5in" height="5.875694444444444in"}

Figure C‑44 Bottom of the data catalogue results with the \"Next 20\"
button

##### Extract Results {#extract-results-10 .ListParagraph}

> To get the information within each result, the different elements in
> the web page have to be scraped.
>
> Here are the scraping procedures for the results page (numbers
> correspond to the numbers in Figure 3):

5)  Each result is contained in a \<li\> under \<ul\> with class
    'results-page'.

6)  The **Title** and **Metadata URL** are both located in the \<h3\> of
    the result \<li\>.

7)  The **Title** is found under the element \<h2\> with class
    \"dataset-heading\".

![](media/image61.png){width="6.5in" height="6.548611111111111in"}

Figure C‑45 The page of results showing the different elements on the
page.

> The rest of the information can be extracted from the metadata page of
> the result.
>
> Here are the scraping procedures for the metadata page (numbers
> correspond to the numbers in Figure 4):

4)  The **Description** is found in the text of a \<div\> with id
    "pagebody".

5)  **For the Date, locate the** \<dt\> **with text "Date added" and
    then extract the text of its sibling** \<dd\>**.**

6)  **For the Publisher, locate the** \<dt\> **with text "Publisher" and
    then extract the text of its sibling** \<dd\>**.**

7)  The downloads can be found in all the \<a\> tags under \<h2\> with
    text "**Download data".**

![](media/image63.png){width="6.5in" height="5.875694444444444in"}

Figure C‑46 The top part of the metadata page.

### Land Information Ontario {#land-information-ontario .ListParagraph}

####  Description {#description-69 .ListParagraph}

> The Land Information Ontario (LIO) Metadata Management Tool is
> geoportal which provides access to GIS data throughout different
> organizations in the Ontario Government and Ontario's municipal
> governments.

#### URLs {#urls-56 .ListParagraph}

##### Main URL {#main-url-18 .ListParagraph}

> <https://www.javacoeapp.lrc.gov.on.ca/geonetwork/srv/en/main.home>

##### Query URL {#query-url-2 .ListParagraph}

> <https://www.javacoeapp.lrc.gov.on.ca/geonetwork/srv/en/main.search.embedded>

#### Extraction Process {#extraction-process-61 .ListParagraph}

##### Categories {#categories .ListParagraph}

> There is an option to query the datasets by different categories. A
> list of the categories of data can be found in the left sidebar of the
> LIO main page (see Figure 5). Each category will be saved to a
> separate CSV file. In the HTML code, the categories are located in
> \<div\> tags with class "arrow" under a the first \<div\> with class
> "geosearchfields**". The category name is extracted from the** onclick
> **method (ex: runCategorySearch(\'GeologyOntario\')).**

![](media/image64.png){width="6.5in" height="5.875694444444444in"}

Figure C‑47 Outlined is the location of the list of categories.

##### Query {#query-2 .ListParagraph}

> Next step is to query the LIO database for each category in the
> previous section.
>
> The following query will return all of the OpenData results on a
> single page (there are about 289 open data datasets so the
> hitsPerPage=1000 will cover all the results):
>
> <https://www.javacoeapp.lrc.gov.on.ca/geonetwork/srv/en/main.search.embedded?category=OpenData&hitsPerPage=1000>
>
> The results are returned in XML format (see Figure 6).

![](media/image65.png){width="6.5in" height="5.875694444444444in"}

Figure C‑48 The XML results of the above query.

##### Extract Results {#extract-results-11 .ListParagraph}

> The XML results can be accessed using BeautifulSoup and Python. The
> **Title** is found in the text of a \<div\> with class "hittitle". The
> rest of the information can be found in the metadata page. The
> metadata page's URL is accessed using the query URL
> <https://www.javacoeapp.lrc.gov.on.ca/geonetwork/srv/en/metadata.show.embedded>?id=\<id\>.
> The ID for the current dataset is found in a \<a\> tag under a \<div\>
> with class "thumbnail\_results".
>
> The rest of the CSV fields are found on the metadata page under the
> following tags:

-   Date: In the adjacent tag to \<th\> with text "Date".

-   Description: In the adjacent tag to \<th\> with text "Abstract".

-   Type: In the adjacent tag to \<th\> with text "Environment
    description".

-   Publisher: In the adjacent tag to \<th\> with text "Organisation
    name".

-   Downloads: In \<a\> tags under \<span\> with text "Data for
    download".

-   Metadata Type: In the adjacent tag to \<th\> with text "Metadata
    standard name".

-   Licensing: In the adjacent tag to \<th\> with text "Access
    constraints".

-   Spatial Reference: In the adjacent tag to \<th\> with text "Code"
    under \<span\> with text "**Reference System Information**".

Prince Edward Island {#prince-edward-island .ListParagraph}
--------------------

### Web Pages {#web-pages-7 .ListParagraph}

#### Survery Monument List {#survery-monument-list .ListParagraph}

##### Description {#description-70 .ListParagraph}

> The site contains several pages of over 4,000 stations throughout the
> survey control network of PEI provided in tables.

##### URLs {#urls-57 .ListParagraph}

###### Main URL {#main-url-19 .ListParagraph}

> <http://eservices.gov.pe.ca/pei-icis/monument/list.do;jsessionid=2FCC7CA75D195DB50EF2D9177B543870>

###### About URL {#about-url-1 .ListParagraph}

> <http://eservices.gov.pe.ca/pei-icis/support/surveymonument.jsp;jsessionid=223C94139B11E10ABDC878FCCABD8A7C>

##### Extraction Process {#extraction-process-62 .ListParagraph}

![](media/image66.png){width="6.5in" height="5.655555555555556in"}

Figure 1‑1 The first page of the Survey Monument List

Although the points are listed on the Survey Monument List, all the
information for extraction is taken from the About page. Here are the
steps for extracting from the About page:

1.  Locate the \<strong\> with text "Brief History".

2.  To get the **Description**, get the next sibling of the \<strong\>
    element 3 times and then grab the text.

3.  For the **Title**, find the \<td\> with class 'header'.

#### GIS Data Catalog {#gis-data-catalog .ListParagraph}

##### Description {#description-71 .ListParagraph}

> The GIS Data Catalog contains links to several pages containing
> geospatial downloads.

##### URLs {#urls-58 .ListParagraph}

> <http://www.gov.pe.ca/gis/index.php3?number=77543&lang=E>

##### Extraction Process {#extraction-process-63 .ListParagraph}

> The steps for extracting the GIS Data Catalog page are:

1.  To get a list of all the sub-pages, find the \<ul\> with id
    'subnavlist' on the page.

2.  Get all the \<a\> elements under the \<ul\> as a list.

3.  Get the two \<a\> elements with text "Free GIS Products" and "Free
    GIS Products (con't)" and add them to the list from the previous
    step.

4.  Go through each \<a\> in the list and get the soup of the sub-page
    (the link in the \<a\>).

> Every sub-page is laid out the same way with a single table containing
> the dataset downloads and their metadata (except for one page which
> contains 2 tables). Therefore, the process for extraction is the same
> for each page:

1.  Find all \<table\> elements on the page.

2.  To convert each row in the table to a dictionary, process the table
    using table\_to\_dict in the shared.py script.

3.  If the table contains a "metadata" column, for each row:

    a.  Open the metadata page.

    b.  Get the **Title** from the \<em\> element with text "Title:".

    c.  Get the **Description** from the \<em\> element with text
        "Abstract:".

    d.  If the **Description** is blank, get the parent of the \<em\>
        and find its next sibling \<dd\>. Get the text from this \<dd\>
        for the **Description**.

4.  If no metadata page exists, get the **Title** from the "data layers"
    column. The description cannot be extracted.

5.  The **Download** and **Available Formats** is taken from the
    "download" column in the table.

6.  Since the sub-pages may contain links to the same datasets, run the
    remove\_duplicates method in the MyCSV object entering the
    "Download\_Link" as the unique field in the CSV file to remove any
    duplicate datasets in the CSV file.

### Interactive Maps {#interactive-maps-10 .ListParagraph}

#### Description {#description-72 .ListParagraph}

> Prince Edward Island contains several interactive maps

#### URLs {#urls-59 .ListParagraph}

> See the extraction process for individual URLs.

#### Extraction Process {#extraction-process-64 .ListParagraph}

##### Gallery for PEI Dept. of Transportation, Infrastructure & Energy {#gallery-for-pei-dept.-of-transportation-infrastructure-energy .ListParagraph}

> URL:
> <https://peitie.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=asc&sortField=title>
>
> The Gallery contains 7 ArcGIS maps for the province of Prince Edward
> Island.
>
> The shared.py script contains a method for extracting ArcGIS
> galleries. The method get\_arcgis\_gallery gets all the maps on the
> page and opens up their ArcGIS JSON data.

##### ArcGIS Maps {#arcgis-maps .ListParagraph}

> URLs:
>
> <http://peitie.maps.arcgis.com/apps/webappviewer/index.html?webmap=d9a9d2edfe494f5e9610c3443a9032e4>
>
> <http://peitie.maps.arcgis.com/apps/MapJournal/index.html?appid=225121b0e2ab415fa48c3d6dad7d5df7>
>
> <https://peitie.maps.arcgis.com/apps/webappviewer/index.html?id=e41b62bff037413884cf8f44b002a200>
>
> This process extracts any ArcGIS map not included in the ArcGIS
> Gallery. The Page object contains a method called get\_arcgis\_urls
> which will get a list of any URL that contains "ArcGIS" in the URL.
> For each URL in this list, the data is extracted using the
> get\_arcgis\_data in shared.py script.

##### Interactive Maps List {#interactive-maps-list .ListParagraph}

URL: <http://www.gov.pe.ca/maps/index.php3>

This map contains a list of links to interactive maps throughout PEI's
web site.

The following are the steps for extracting the list:

1.  Find the \<table\> on the page and run it through the
    table\_to\_dict method in the shared.py script.

2.  There are a few links in the table that go to sub-pages before going
    to the map. For this, create a list of sub-page names \[\'Address
    Locator\', \'Aerial Photos\', Accounts\', \'Drinking Water Quality
    Application\', \'PEI LandOnline\'\]

3.  For each row in the table:

    a.  Get the **Title** from the 'Title' column.

    b.  Get the **Description** from the 'Description' column.

    c.  If the current dataset is not in the sub-page list, get the
        **Web Map URL** from the \<a\> in the 'Title' column.

    d.  If the dataset is in the sub-page list, open the page and locate
        the map link to set the **Web Map URL**.

##### Groundwater Level Data {#groundwater-level-data .ListParagraph}

> URL:
> <https://www.princeedwardisland.ca/en/service/view-groundwater-level-data>
>
> The Groundwater Level Data contains a map of 14 observation wells
> across the province.
>
> The information for the Groundwater Level Data site is found in the
> metadata of the page:

-   **Title** in the "dcterms.title" metadata item

-   **Description** in the "dcterms.description" metadata item

-   **Date** in the "dcterms.modified" metadata item

-   **Publisher** in the "department" metadata item

> The **Web Map URL** is located in an \<a\> with text containing
> "Access Groundwater Data by Reference Map".

##### Island Christmas Trees and Wreaths {#island-christmas-trees-and-wreaths .ListParagraph}

> URL:
> <https://www.princeedwardisland.ca/en/information/communities-land-and-environment/island-christmas-trees-and-wreaths>
>
> The map on this page shows the locations of Christmas Tree Farms
> throughout the province.
>
> The information for this page is found in the metadata of the page
> under the same items as the Groundwater Level page.
>
> Since the map is embedded on the page, the **Web Map URL** will be the
> page URL itself.

##### High Capacity Wells {#high-capacity-wells .ListParagraph}

> URL:
> <https://www.princeedwardisland.ca/en/service/high-capacity-wells>
>
> This page's map contains the locations of High Capacity Wells and
> Wellfields throughout the province.
>
> The information for this map is located in the page's metadata under
> the same items as the Groundwater Level page.
>
> The **Web Map URL** is in an \<a\> with text "View Map".

##### PEI Watershed Group {#pei-watershed-group .ListParagraph}

> URL:
> <https://www.princeedwardisland.ca/en/service/find-pei-watershed-group>
>
> The PEI Watershed Group map allows users to search for a Watershed
> Group anywhere in the province using an address.
>
> The extraction of the PEI Watershed page is similar to the Groundwater
> Level page. The **Title**, **Description**, **Date** and **Publisher**
> are all found in the page's metadata. The **Web Map URL** is found in
> an \<a\> with text containing "Find my Watershed Group".

##### Child Care Registry {#child-care-registry .ListParagraph}

> URL: <http://www.ecdaofpei.ca/registry.php>
>
> The Child Care Registry allows users to search and sign-up for child
> care programs across the province. On the registry page itself, the
> map appears once a set of search criteria are entered by the user,
> such as the Centre Type and Location.
>
> Although the inventory information for this page is in the metadata,
> the items are different from the Groundwater Level page. Here are the
> metadata items for each inventory entry:

-   **Title** is in 'TITLE'

-   **Description** is in 'DESCRIPTION'

-   **Date** is in 'creation date'

-   **Publisher** is in 'copyright'

> The **Web Map URL** is in an \<a\> with text containing "Visit the PEI
> ELCC Registry".

##### PEI\'s Points of Interest Map {#peis-points-of-interest-map .ListParagraph}

> URL: <https://www.princeedwardisland.ca/en/points-of-interest-map>
>
> This map contains various points of interest of different services
> throughout the province. This page does not provide much information
> for the inventory. The **Title** is hard-coded as "Prince Edward
> Island's Points of Interest Map". Since the map is embedded on the
> page, the **Web Map URL** is the page's URL.

#####  Walking and Hiking Map {#walking-and-hiking-map .ListParagraph}

> URL: <https://www.princeedwardisland.ca/en/topic/walking-and-hiking>
>
> This page contains 2 interactive maps however the first map, Active
> Transportation and Active Living Map, was already included in the
> ArcGIS maps extracted above.
>
> Here are the steps for extracting this page:

1.  Find all the links on the page by locating the \<div\> elements with
    class "views-row" and get the sixth item in the list (which is the
    last map link).

2.  Get the **Web Map URL** from the \<a\> under the \<div\>.

3.  Get the **Title** from the text in the \<a\>.

4.  Get the **Description** from the \<span\> under the \<div\>.

#####  Seniors Housing Units {#seniors-housing-units .ListParagraph}

> URL:
> <https://www.princeedwardisland.ca/en/information/family-and-human-services/housing-assistance>
>
> The map on this page contains the locations of Seniors Housing Units
> throughout the province of Prince Edward Island.
>
> The inventory information for this map is located on the larger map
> page's metadata. The steps for extracting this information are:

1.  Get the Web Map URL by locating an \<a\> with text "View a larger
    version of the map".

2.  Open the map page and get its metadata.

3.  Get the **Title** from the "og:title" metadata item and the
    **Description** from the "description" item.

#####  Confederation Trail {#confederation-trail .ListParagraph}

> URL: <https://www.tourismpei.com/pei-confederation-trail>
>
> The Confederation Trail contains an embedded Google Map with the path
> of the Confederation Trail through the entire province.
>
> As with many of the other interactive maps, the information for the
> inventory is found in the metadata of the page:

-   The **Title** is found in metadata item "name".

-   The **Description** is found in "description".

-   The **Date** is found in "article:modified\_time".

### Map Services {#map-services-7 .ListParagraph}

#### Description {#description-73 .ListParagraph}

> There is one ESRI REST Service for the province of Prince Edward
> Island. The service includes a collection of FeatureServers for many
> different types of geospatial datasets.

#### URLs {#urls-60 .ListParagraph}

##### Main URL {#main-url-20 .ListParagraph}

> <https://services5.arcgis.com/6bkn2iYF5h1LCwgM/arcgis/rest/services>

#### Extraction Process {#extraction-process-65 .ListParagraph}

> The extraction process for Prince Edward Island's map service is the
> same as other provincial services.

Québec {#québec .ListParagraph}
------

### Catalogue d\'Information Géographique Gouvernementale (CIGG) {#catalogue-dinformation-géographique-gouvernementale-cigg .ListParagraph}

#### Description {#description-74 .ListParagraph}

> CIGG is a geoportal which allows access to Quebec's geospatial
> documents and data.

#### URLs {#urls-61 .ListParagraph}

##### Main URL {#main-url-21 .ListParagraph}

> [**http://catalogue-geographique.gouv.qc.ca**](http://catalogue-geographique.gouv.qc.ca)

#### Extraction Process {#extraction-process-66 .ListParagraph}

##### Navigate CIGG {#navigate-cigg .ListParagraph}

> CIGG uses forms and JavaServer Faces to query its database. When the
> user submits a query, the resulting page relies on the forms from the
> previous page. The only way to automate this process is by following
> the exact steps the user would use to submit a query in a browser.
> This can be done using Python and Selenium.
>
> Navigating the CIGG geoportal follows these steps:

1.  Open a browser (in this case Firefox) using Selenium and Python and
    load the domain of the CIGG geoportal
    (**<http://catalogue-geographique.gouv.qc.ca>)**.

    **NOTE: If an error occurs saying "Erreur lors de l\'obtention de
    l\'objet de l\'url de la carte: TypeError:
    document.getElementById(\...) is null", run the script again and
    keep running it until this error no longer occurs.**

    ![](media/image67.png){width="5.395833333333333in"
    height="1.307522965879265in"}

2.  **Find the element with** id
    **\"**rechercheCiggForm:lancerRecherche**\" and activate its click()
    command.**

3.  **A message will appear at the top of the page saying "Aucun critère
    de recherche n\'a été sélectionné. Voulez-vous continuer?" which
    translates to "No search criteria was selected. Do you want to
    continue?". Locate the element with** id **"**\_id67:LienOui**\"
    (the "Oui" button) and activate its click() command.**

4.  **Eventually, the search results page will appear. Using
    BeautifulSoup, gather all** \<img\> **with** title **"**Consulter
    les métadonnées**". This will determine the number of results there
    are on the page.**

5.  **For each result, use Selenium to find the element with** id
    **"**formresultats:series:\<res\_number\>:lienMetadonneeDocumentActif**"
    and then activate the element's click() command. The metadata page
    will open which will be used in the next step to extract the
    values.**

##### Extract Results {#extract-results-12 .ListParagraph}

> Using the metadata page from each result, extract the \<tbody\> with
> either id "section\_serie" or id "section\_doc\_" using BeautifulSoup.
> Then extract all \<td\> with both class "niveau\_texte\_2" and
> "niveau\_texte\_3".
>
> Here's a list of CSV columns and the instructions for locating them in
> the metadata page:

-   **Title**: Locate the \<td\> with text "Nom" and then find its next
    sibling with \<td\>.

-   **Description**: Locate the \<td\> with text "Sommaire" and then
    find its next sibling with \<td\>.

-   **Date**: Locate the \<td\> with text "**Type et date
    d\'intervention**" and then find its next sibling with \<td\>.

-   **Publisher**: Locate the \<td\> with text "**Organisme**" and then
    find its next sibling with \<td\>.

-   **Download**: Locate the \<td\> with text "**Titre**" and then find
    its next sibling with \<td\>.

-   **Licensing:** In the \<td\> with class "niveau\_texte\_3", locate a
    \<td\> with text "de prix.

-   **Available Formats**: In the \<td\> with class "niveau\_texte\_3",
    locate a \<td\> with text "Format des fichiers".

### Géoboutique Québec {#géoboutique-québec .ListParagraph}

#### Description {#description-75 .ListParagraph}

> The Géoboutique Québec site offers access to geographic information
> products and services. Its search capabilities work in the same way as
> CIGG geoportal.

#### URLs {#urls-62 .ListParagraph}

##### Main URL {#main-url-22 .ListParagraph}

> <http://geoboutique.mern.gouv.qc.ca>

#### Extraction Process {#extraction-process-67 .ListParagraph}

##### Navigate Géoboutique {#navigate-géoboutique .ListParagraph}

> As with CIGG, Géoboutique uses forms and JavaServer Faces to query its
> database. When the user submits a query, the resulting page relies on
> the forms from the previous page. The only way to automate this
> process is by following the exact steps the user would use to submit a
> query in a browser. This can be done using Python and Selenium.
>
> Navigating the Géoboutique site follows these steps:

1.  Open a browser (in this case Firefox) using Selenium and Python and
    load the domain of the Géoboutique site
    (<http://geoboutique.mern.gouv.qc.ca>**)**.

    **NOTE: If an error occurs saying "Erreur lors de l\'obtention de
    l\'objet de l\'url de la carte: TypeError:
    document.getElementById(\...) is null", run the script again and
    keep running it until this error no longer occurs.**

2.  **Find the element with** id
    **\"**rechercheCiggForm:lancerRecherche**\" and activate its click()
    command.**

3.  **A message will appear at the top of the page saying "Aucun critère
    de recherche n\'a été sélectionné. Voulez-vous continuer?" which
    translates to "No search criteria was selected. Do you want to
    continue?". Locate the element with** id
    **"**messagesForm:LienOui**\" (the "Oui" button) and activate its
    click() command.**

4.  **Eventually, the search results page will appear. Using
    BeautifulSoup, gather all** \<img\> **with** title **"**Consulter
    les métadonnées**". This will determine the number of results there
    are on the page.**

5.  **For each result, use Selenium to find the element with** id
    **"**formresultats:series:\<res\_number\>:lienMetadonneeDocumentActif**"
    and then activate the element's click() command. The metadata page
    will open which will be used in the next step to extract the
    values.**

##### Extract Results {#extract-results-13 .ListParagraph}

> Using the metadata page from each result, extract the \<tbody\> with
> either id "section\_serie" or id "section\_doc\_" using BeautifulSoup.
> Then extract all \<td\> with both class "niveau\_texte\_2" and
> "niveau\_texte\_3".
>
> There are two methods in "shared.py" called "get\_text\_by\_label" and
> "get\_tags\_by\_text". They both locate a specified tag with a
> specified text (the label), find its next sibling (the value) and
> return either the text in the sibling or the sibling tag itself,
> respectively (see Figure 1).

![](media/image68.png){width="6.489583333333333in" height="2.5in"}

Figure C‑49 Example of the label and value the methods in \"shared.py\"
will extract.

> Here's a list of CSV columns and the instructions for locating them in
> the metadata page:

-   **Title**: Located with label "Nom".

-   **Description**: Located with label "Sommaire".

-   **Date**: Located with label "Typ**e et date d\'intervention**".

-   **Publisher**: Located with label "**Organisme**".

-   **Download**: Located with label "**Titre**".

-   **Licensing:** Located with label "de prix".

-   **Available Formats**: Located with label "Format des fichiers".

### Données Québec {#données-québec .ListParagraph}

#### Description {#description-76 .ListParagraph}

> Données Quebec is similar in functionality to Alberta's open data
> site. It is a search engine that allows users to locate Quebec's open
> data collection.

#### URLs {#urls-63 .ListParagraph}

##### Main URL {#main-url-23 .ListParagraph}

> <https://www.donneesquebec.ca/recherche/fr/dataset>

#### Extraction Process {#extraction-process-68 .ListParagraph}

##### Query {#query-3 .ListParagraph}

> The URL for querying Quebec's open data is
> <https://www.donneesquebec.ca/recherche/fr/dataset>. The query string
> can have the following parameters:

-   **q**: Filter the results by key word search.

-   **res\_type**: Filter the results by the information type.

-   **res\_format**: Filter results by format type of the files.

-   **groups:** Filter results by category.

-   **license\_id**: Filter the results by their licensing.

-   **tags**: Filter the results by tag.

-   **organization**: Filter results by the organization.

-   **page**: Specifies the page number of the results to be displayed.

-   **sort**: Specifies how to sort the results.

> For example, the following query URL returns open data results with
> shapefiles:
>
> <https://www.donneesquebec.ca/recherche/fr/dataset?res_type=donnees&res_format=SHP>

![](media/image69.png){width="6.5in" height="5.660416666666666in"}

Figure C‑50 The results of the above query filtering results with
shapefiles and are open data.

> As shown, the results can only be returned as a web page. In order to
> extract the information from these datasets, each result page will
> have to be scraped using BeautifulSoup and Python
>
> **NOTE**: The rest of the instructions assumes understanding of the
> browser's Development Tools, HTML code and its elements.

##### Determine Page Count {#determine-page-count-2 .ListParagraph}

> Like the Alberta open data site, the total number of pages is listed
> at the bottom of the page. The area highlighted in Figure 4 is a
> \<div\> with class name "pagination". Each link in the pagination is
> in a \<li\> element so the total number of pages can be found in the
> second last li element.

![](media/image70.png){width="6.5in" height="5.660416666666666in"}

Figure C‑51 Bottom of the results page containing the links to the
different pages.

##### Extract Results {#extract-results-14 .ListParagraph}

> To get the information within each result, the different elements in
> the web page have to be scraped.
>
> Here are the scraping procedures for the results page (numbers
> correspond to the numbers in Figure 4):

8)  Each result is contained in a \<div\> with class name "bottom17".

9)  For the **Available Formats**, find all the \<span\> elements with
    class "label" and has the attribute data-format. The types of
    formats will determine whether to include this dataset or not.

10) The **Title** is found under the element \<h2\> with class
    \"dataset-heading\".

![](media/image71.png){width="6.5in" height="5.660416666666666in"}

Figure C‑52 The result page showing the different elements on the page.

> The rest of the information can be extracted from the metadata page of
> the result (the link is found under the title \<h3\> element mentioned
> above). There are several tabs on the metadata page however only the
> "Jeu de données" will be used.
>
> Here are the scraping procedures for the metadata page (numbers
> correspond to the numbers in Figure 5 and Figure 6):

8)  For the **Description**, first locate \<div\> with class
    "masquerPourMetMoins" and then find its \<p\> child.

9)  For the **Downloads**, find the \<section\> element with id
    "dataset-resources**".**

10) **Next, find all** \<a\> **with** class **"**piwik\_download**" (the
    Télécharger buttons) to retrieve the download links.**

11) **To retrieve the licensing information, locate** \<a\> **with
    attribute** rel **with value "**dc:rights**" and grab its text.**

12) **For the organization, locate** \<th\> **with text
    "**Organisation**", retrieve its sibling** \<td\> **and then grab
    the text of the child** \<a\> **(as mentioned in Section** **2.2.2,
    the "shared.py" has a method that will locate an element with a
    specified text and then find its adjacent cell value).**

13) **For the date, locate** \<th\> **with text "**Mise à jour**",
    retrieve its sibling** \<td\> **and then grab the text of the
    child** \<a\>.

![](media/image72.png){width="6.033526902887139in"
height="6.979166666666667in"}

Figure C‑53 The top part of the metadata page.

![](media/image73.png){width="6.5in" height="7.51875in"}

Figure C‑54 The bottom part of the metadata page.

### Géoinfo Québec {#géoinfo-québec .ListParagraph}

####  Description {#description-77 .ListParagraph}

> Géoinfo Québec is a research utility that allows users to search
> geographic data related to the Province of Québec. The site includes
> an interactive map which allows the user to refine their search to a
> specific area.

#### URLs {#urls-64 .ListParagraph}

##### Main URL {#main-url-24 .ListParagraph}

> <http://geoinfo.gouv.qc.ca/portail/>

##### Interactive Map Search URL {#interactive-map-search-url .ListParagraph}

> <http://geoinfo.gouv.qc.ca/portail/jsp/geoinfo.jsp>

##### Query URL {#query-url-3 .ListParagraph}

> <http://geoinfo.gouv.qc.ca/portail/jsp/geoinfo.jsp>

#### Extraction Process {#extraction-process-69 .ListParagraph}

##### Query to Get JSON Data {#query-to-get-json-data-7 .ListParagraph}

> Géoinfo includes the ability to query its database using a URL query
> string and return the results in JSON format.
>
> The following query will return the first 10 results starting from the
> first record:
>
> <http://geoinfo.gouv.qc.ca/portail/Search?Request=GetRecords&startPosition=1>
>
> Since the site can only return 10 results at a time, this query must
> be repeated with the startPosition incremented by 10 (1, 11, 21, etc.)
> until all the results (in this case 142) have been collected in a
> list.

##### Extract Results {#extract-results-15 .ListParagraph}

> As with other JSON results, all necessary information is contained in
> its keys and values.
>
> The following items can be found in the JSON data:

-   Title

-   Description (or "abstract" as it appears in the JSON data)

-   Publisher (or "organisation")

-   Web Map URL (or "url" in the first "online\_resource")

Saskatchewan {#saskatchewan .ListParagraph}
------------

### Interactive Maps {#interactive-maps-11 .ListParagraph}

#### Description {#description-78 .ListParagraph}

> The Province of Saskatchewan has a collection of interactive maps for
> different themes, such as administrative boundaries, agriculture,
> cadastral, etc. The list of maps is located at
> <http://www.saskatchewan.ca/government/notarize-documents-publications-saskatchewan-maps-and-other-publications/maps>.
> There are also several interactive maps for the city of Saskatoon.

#### URLs {#urls-65 .ListParagraph}

##### Provincial Maps List {#provincial-maps-list .ListParagraph}

> <http://www.saskatchewan.ca/government/notarize-documents-publications-saskatchewan-maps-and-other-publications/maps>

##### Saskatoon Interactive Maps List {#saskatoon-interactive-maps-list .ListParagraph}

> <https://www.saskatoon.ca/interactive-maps>

##### Saskatoon Address Map {#saskatoon-address-map .ListParagraph}

> <https://www.saskatoon.ca/business-development/planning/planning-publications-maps/address-map>

##### Saskatoon Zoning Map {#saskatoon-zoning-map .ListParagraph}

> <https://www.saskatoon.ca/business-development/planning/planning-publications-maps/zoning-address-map>

##### Saskatoon iMap {#saskatoon-imap .ListParagraph}

> <http://rpbackapps2.saskatoon.ca/lapp/Geocortex/Essentials/GeocortexAnon/COSSV/Viewer.html?Viewer=iMap_GeneralVW>

##### Ducks Unlimited Maps {#ducks-unlimited-maps .ListParagraph}

> <http://www.ducks.ca/initiatives/gis-mapping-applications>

#### Extraction Process {#extraction-process-70 .ListParagraph}

##### Provincial Maps List {#provincial-maps-list-1 .ListParagraph}

> The provincial map page contains a list of several maps, both
> documents and interactive maps. Unfortunately, the site does not
> include descriptions on the maps.
>
> Here are the steps for extracting the provincial maps:

1.  Find \<section\> with class "general-content"

2.  Get all \<a\> under the section

3.  Go through any \<a\> with a link that includes
    "gisappl.saskatchewan.ca", excluding "SilverlightExt" and ".pdf",
    and get the **Title** from the text of the \<a\>

4.  For each valid \<a\> URL, get the network request URLs (see Figure
    1‑1 for an example of a list of network requests in a browser using
    the browser's Development Tools) using the method get\_network\_urls
    in the shared.py script and go through each URL until a URL with
    "Geocortex" is found to get the **Service URL** for the map.

    ![](media/image74.png){width="6.5in" height="5.655555555555556in"}

Figure C‑55 An example of a list of network requests using Chrome\'s
Development Tools

##### Saskatoon Interactive Maps {#saskatoon-interactive-maps .ListParagraph}

> The City of Saskatoon has a page with a list of interactive maps for
> their services and information. The page includes a link and a
> description for each map.
>
> Here are the steps for extracting the maps:

1.  Get all the \<a\> on the page that contain class "btn"

2.  For each \<a\>, get the network request URLs for the link and grab
    all the URLs that contain "MapServer". The map services will be used
    to get the **Spatial Reference** of the interactive map.

3.  If the map is an ArcGIS Online map, use the get\_arcgis\_data method
    in shared.py

4.  Get the **Description** from the page by getting the \<a\>'s parent
    and then finding the \<p\> sibling

##### Saskatoon Address Map and Zoning Map {#saskatoon-address-map-and-zoning-map .ListParagraph}

> The pages containing the links to both the Saskatoon Address map and
> Zoning map are set up in the same structure. The same steps can be
> used to extract both sites:

1.  Get the **Description** from the content of the \<meta\> tag with
    name "description"

2.  Get the \<div\> with id "main-content"

3.  Find the \<a\> in the \<div\> to get the map URL

4.  The map is an ArcGIS Online map so use the get\_arcgis\_data method
    in shared.py to extract the information

##### Saskatoon iMap {#saskatoon-imap-1 .ListParagraph}

> The City of Saskatoon's iMap contains the locations of schools, parks,
> leisure facilities, sports fields, points of interest, and parcels.
> The map uses Silverlight so the map can only be viewed in Internet
> Explorer.
>
> However, Internet Explorer is not needed to extract the information
> for the CSV inventory file. Here are the steps for extracting the iMap
> information:

1.  For the **Title**, locate the \<h3\> with text "Interactive iMap"

2.  For the **Description**, locate the \<p\> sibling of the \<h3\> tag

##### FlySask2 Geoportal Map {#flysask2-geoportal-map .ListParagraph}

> The FlySask Geoportal map is the primary map for accessing imagery of
> the Saskatchewan Geospatial Imagery Collaborative. The data on the map
> is also included as a map service
> (<https://www.flysask2.ca/cubewerx/cubeserv.cgi>).
>
> Here are the steps for extracting information of the FlySask2
> Geoportal map:

1.  To get the **Title**, find the \<div\> with id "cw\_banner" and get
    its text.

2.  To get the **Description**, load the About page
    (<https://www.flysask2.ca/homepage/>) and find the \<div\> with
    class "entry-content" and get its text.

##### Ducks Unlimited Maps {#ducks-unlimited-maps-1 .ListParagraph}

> The Ducks Unlimited page has a list of interactive maps for all across
> Canada. In this instance, only the maps that include Saskatchewan data
> should be extracted.
>
> Here are the steps for extracting these maps:

1.  On the page, gather all the \<a\> tags with text "View Map"

2.  Go through each \<a\> and check if the anchor text is "Smith Creek",
    "Canadian Wetland Inventory", "Waterfowl Migration Map" or "Dip Your
    Paddle Story Map" as these are the only maps which include
    Saskatchewan data

3.  Get the **Description** by finding the \<p\> sibling of each valid
    \<a\>

4.  Get the **Title** from the anchor text

### Web Pages/Catalogues {#web-pagescatalogues .ListParagraph}

#### Elections Saskatchewan {#elections-saskatchewan .ListParagraph}

##### Description {#description-79 .ListParagraph}

> The Elections Saskatchewan site includes a page with a list of
> geospatial datasets used for the 2016 general election and any
> by-elections since then.

##### URLs {#urls-66 .ListParagraph}

###### Maps URL {#maps-url .ListParagraph}

> <http://www.elections.sk.ca/voters/maps/>

##### Extraction Process {#extraction-process-71 .ListParagraph}

> The map list page includes downloads for both shapefiles and PDFs.
> Since only geospatial datasets are included in the inventory, the PDFs
> can be ignored.
>
> Here are the steps for extracting these datasets:

1.  Located the \<h2\> text containing "Regina Northeast" to find the
    first title on the page

2.  Get the parent \<div\> of the \<h2\>

3.  Find all the \<a\> tags under the \<div\> and only include the \<a\>
    with links containing ".zip"

4.  Get the **Title** of each dataset from the text of \<h2\>

5.  Get the **Date** by parsing the text of the \<a\>

#### Open Data Regina {#open-data-regina .ListParagraph}

##### Description {#description-80 .ListParagraph}

> Regina's Open Data catalogue provides the public access to Regina's
> open data collection. The page works similar to a search engine and is
> similar to Alberta's Open Data catalogue and other provincial
> catalogues.

##### URLs {#urls-67 .ListParagraph}

###### Main URL {#main-url-25 .ListParagraph}

> <http://open.regina.ca/>

##### Extraction Process {#extraction-process-72 .ListParagraph}

> The main page of the catalogue contains a set of tiles with links to
> different categories in the catalogue. To get all these different
> tiles, find all \<section\> tags with class "tile-section" (see Figure
> 2‑1).
>
> For each category, follow these steps:

1.  Get the link of the category from the \<a\> in the \<section\>

2.  Use the link to build the query for the catalogue for the following
    formats: XML, SHP, KML, JSON, REST

3.  Get the soup of the results page and get the number of pages by
    locating the \<div\> with class "pagination" (use the
    get\_page\_count method in shared.py) (see Figure 2‑2)

4.  For each page of the results, find all the \<h3\> with class
    "dataset-heading" to get a list of all the results

5.  For each result, soup up the link in the \<h3\> and on the page (see
    Figure 2‑3):

    a.  Get the **Title** from the text in \<h1\> in the \<div\> with
        class "module-content"

    b.  Get the **Description** from the \<div\> with class "notes"

    c.  Get the **Available Formats** from the \<span\> with class
        "formal-label"

    d.  Get the **Date** from the adjacent value of \<th\> with text
        "Last Updated"

    e.  Get the **Download URL** from the text adjacent to \<th\> with
        text "Source" (use the get\_adj\_text\_by\_label method in
        shared.py to get the adjacent element next to the \<th\>)

    f.  If the \<th\> has no text, get the **Download URL** by loading
        the dataset's page (get the link from \<ul\> with class
        "resource-list") and then locating the link in \<h1\> with class
        "page-heading"

![](media/image75.png){width="6.5in" height="5.655555555555556in"}

Figure C‑56 The home page of Regina\'s Open Data catalogue

![](media/image76.png){width="6.5in" height="5.655555555555556in"}

Figure C‑57 The Open Data results page

![](media/image77.png){width="6.5in" height="5.655555555555556in"}

Figure C‑58 The dataset's information page

#### Saskatoon Open Data Catalogue {#saskatoon-open-data-catalogue .ListParagraph}

##### Description {#description-81 .ListParagraph}

> Like Regina's Open Data Catalogue, Saskatoon's catalogue provides
> access to the city's open data collection.

##### URLs {#urls-68 .ListParagraph}

###### Main URL {#main-url-26 .ListParagraph}

> <http://opendata-saskatoon.cloudapp.net/>

###### Query URL {#query-url-4 .ListParagraph}

> <http://opendata-saskatoon.cloudapp.net:8080/v1/SaskatoonOpenDataCatalogueBeta>

##### Extraction Process {#extraction-process-73 .ListParagraph}

> The extraction process for Saskatoon's Open Data catalogue is
> different from other catalogues. The data is divided into different
> collections in different folders. The list of collections can be
> extracted in XML format from the query URL
> (<http://opendata-saskatoon.cloudapp.net:8080/v1/SaskatoonOpenDataCatalogueBeta>).
>
> Follow these steps to extract the datasets:

1.  Get the XML information from the query URL

2.  In the XML, find all \<collection\> elements

3.  For each collection:

    a.  Get the collection's XML URL by adding the collection name to
        the end of the query URL (ex: for the AEDLocations collection,
        <http://opendata-saskatoon.cloudapp.net:8080/v1/SaskatoonOpenDataCatalogueBeta/AEDLocations>)

    b.  Get the dataset's information page by locating the \<id\> and
        replacing its text "v1" with "DataBrowser"

    c.  Get the **Title** from the \<title\> element

    d.  Get the **Date** from the \<updated\> element

    e.  The rest of the information is taken from the dataset's web
        page, locating the **Description** in the \<td\> with text
        "Description", the **Metadata URL** in the \<td\> with text
        "Metadata URL" and the formats under the \<select\> with id
        "eidDownloadType"

#### CommunityView Collaboration Catalogue {#communityview-collaboration-catalogue .ListParagraph}

##### Description {#description-82 .ListParagraph}

> The CommunityView Collaboration is a joint effort between the City of
> Saskatoon, Saskatoon Public School Division, Saskatoon Greater
> Catholic Schools, Saskatoon Regional Intersectoral Committee agencies
> and Public Health Services of the Saskatoon Health Region. The purpose
> of the map is to assemble data from multiple sources and include a
> system supported by appropriate information technologies and tools for
> end-user analysis including the use of a Geographic Information System
> (GIS).

##### URLs {#urls-69 .ListParagraph}

###### Main URL {#main-url-27 .ListParagraph}

> <http://www.communityview.ca/Catalogue>

##### Extraction Process {#extraction-process-74 .ListParagraph}

> There are several categories the datasets are divided into. The
> categories are found at the left sidebar of the home page of the
> catalogue. The categories are listed under the \<ul\> tag with class
> "treeview". Each link for the categories are located in \<a\> tags
> under the \<ul\> with class "TreeRootStandard".
>
> For each category page:

1.  Determine the number of pages of results by locating the \<div\>
    with id "pager" and getting the text of the second last \<a\> in the
    \<div\>

2.  Get all the tables with class "ResourceTable" under the \<div\> with
    class "ResourceList" to get the search results

3.  For each page of results:

    a.  Determine if the result has a map by getting the \<img\> with
        alt "Map".

    b.  Get the URL from the map image's parent (\<a\>) and replace the
        word "Map" in the URL with "Data" to get the data URL,
        "Definition" to get the dataset's definition page and "Details"
        to get its metadata.

    c.  The **Description** is found in the dataset's definition page by
        locating the \<div\> with class "DefinitionDiv".

    d.  The **Date** and **Publisher** is found in the dataset's details
        page by locating the \<td\> with text "Updated On" (or "Created
        On") and the \<td\> with text "Source", respectively.

### Map Services {#map-services-8 .ListParagraph}

#### Description {#description-83 .ListParagraph}

> The Province of Saskatchewan, its municipalities and several
> organizations that manage provincial data have many different types of
> Map Services.

#### URLs {#urls-70 .ListParagraph}

##### Saskatchewan GIS (and GISTest) REST Services {#saskatchewan-gis-and-gistest-rest-services .ListParagraph}

<https://gis.saskatchewan.ca/arcgis/rest/services>

<https://gistest.saskatchewan.ca/arcgis/rest/services>

##### GISAppl Saskatchewan Geocortex Service {#gisappl-saskatchewan-geocortex-service .ListParagraph}

<https://gisappl.saskatchewan.ca/Geocortex/Essentials/EXT/REST/sites>

##### Saskatoon Services {#saskatoon-services .ListParagraph}

> <http://arcgis-cosgis-1729149607.us-west-2.elb.amazonaws.com/arcgis/rest/services>
>
> <http://rpbackgis2.saskatoon.ca/ArcGIS/rest/services>
>
> <http://rpstggis2.saskatoon.ca/ArcGIS/rest/services>

##### Regina Service {#regina-service .ListParagraph}

> <https://opengis.regina.ca/arcgis/rest/services>

##### FlySask Services {#flysask-services .ListParagraph}

> Web Map Service
> <https://www.flysask2.ca/cubewerx/cubeserv.cgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities>
>
> Web Map Tile Service
> <https://www.flysask2.ca/cubewerx/cubeserv.cgi/default/wmts/1.0.0/WMTSCapabilities.xml>

##### Water Security Agency Services {#water-security-agency-services .ListParagraph}

> <https://gis.wsask.ca/arcgiswa/rest/services>
>
> <https://gis.wsask.ca/Geocortex/Essentials/GeocortexEssentials/REST/sites>

##### Ducks Unlimited Service {#ducks-unlimited-service .ListParagraph}

> <http://maps.ducks.ca/arcgis/rest/services>

#### Extraction Process {#extraction-process-75 .ListParagraph}

##### ArcGIS REST Services {#arcgis-rest-services-1 .ListParagraph}

###### Query to Get JSON Data {#query-to-get-json-data-8 .ListParagraph}

> ESRI REST services can be returned in multiple formats. Again, for
> Python scripting, the best option is JSON format.
>
> The JSON results can be accessed by adding "?f=pjson**" to the service
> URL and subsequent Mapserver URLs.**
>
> **The access\_rest.py script contains a set of methods which will take
> the home page of the service, cycle through each folder and collect
> all the mapservices found under any folders and subfolders.**

###### Extract Results {#extract-results-16 .ListParagraph}

> As with other JSON results, all necessary information is contained in
> its keys and values.
>
> The following items can be found in the Mapserver JSON data:

-   **Title** (or "mapName" as it appears in the JSON results)

-   **Description** (or "serviceDescription")

-   **Available Formats**

    -   Determined by the type of service:

        -   Mapserver: **KMZ**, **LYR**, **NMF**, **AMF**

        -   Imagerserver: KMZ, LYR

        -   Geometryserver or Featureserver: None

-   **Publisher** (or in this case "Author")

##### Geocortex Services {#geocortex-services-1 .ListParagraph}

> The querying and extraction process for Geocortex Services is the same
> as ArcGIS REST Service except that the services are called sites and
> some of the keys in the JSON format have different names.
>
> The following items can be found in the GeoCortex JSON data:

-   **Title** (or "displayName" as it appears in the JSON results)

-   **Description** (or "description")

-   **Available Formats** and **Publisher** doesn't apply for GeoCortex
    services

##### FlySask2 Geoportal Services {#flysask2-geoportal-services .ListParagraph}

> The FlySask2 Web Map Service and Web Map Tile Service is extracted
> using BeautifulSoup by getting the data in XML format (see Section
> 3.2.5 for the service URLs).
>
> The following service items is found in the XML under the text of
> these elements:

-   **Service Name**: \<Title\>

-   **Description**: \<Abstract\>

-   **Service**: \<ServiceType\>

-   **Publisher**: \<ProviderName\>

    The layers of service (found under all \<Layer\> elements) contain:

<!-- -->

-   **Title**: \<ows:Title\>

-   **Spatial Reference**: In the crs text of \<ows:BoundingBox\>. The
    text is formatted as "urn:ogc:def:crs:EPSG::26913" and needs to be
    split to get the EPSG code.

Yukon {#yukon .ListParagraph}
-----

### Geoportal {#geoportal .ListParagraph}

#### Description {#description-84 .ListParagraph}

> The functionality of Yukon's Geoportal is very similar to Alberta's
> GeoDiscover.

#### URLs {#urls-71 .ListParagraph}

##### Catalogue Browser URL {#catalogue-browser-url-1 .ListParagraph}

<http://geoweb.gov.yk.ca/geoportal/catalog/search/browse/browse.page>

##### Query URL {#query-url-5 .ListParagraph}

<http://geoweb.gov.yk.ca/geoportal/rest/find/document>

#### Extraction Process {#extraction-process-76 .ListParagraph}

##### Query to Get JSON Data {#query-to-get-json-data-9 .ListParagraph}

> The query URL string for Yukon's Geoportal is similar to other
> provincial geoportals. The URL path for the geoportal is
> <http://geoweb.gov.yk.ca/geoportal/rest/find/document>. **The query
> string can include the following parameters:**

-   **f**: The output format of the results

-   **id**: The unique ID of a record (only used if one record should be
    returned)

-   **start**: The record number on which to start the results

-   **max**: The number of records to return in the results

-   **showRelativeUrl**: Determines whether relative paths should be
    used in the results

-   **searchText**: The search text used to filter the results

> An example of a query URL string for Yukon's Geoportal is:
>
> <http://geoweb.gov.yk.ca/geoportal/rest/find/document?f=pjson&start=1&max=10&showRelativeUrl=True&contentType=downloadableData,offlineData>

##### Extract Results {#extract-results-17 .ListParagraph}

> The first step in the extraction of the JSON data is to grab the
> 'records' list. Then for each record:

1.  Get a list of links from the "links" item.

2.  Locate the link with "type" "metadata" or "fullMetadata"

3.  Load the metadata's XML and get the following items for the
    inventory:

    -   **Title** from the \<title\>

    -   **Description** from the \<abstract\>

    -   **Type** from the text of \<name\> under \<distributorFormat\>

    -   **Date** from \<date\> under \<CI\_Date\>

    -   **Web Map URL** from the \<linkage\> item containing text "map"
        if the link is an interactive map; if not it is the download
        link

    -   **Spatial Reference** from \<referenceSystemIdentifier\>

4.  If the download link leads to an FTP server, get all the files from
    the FTP link to determine the **Available Formats.**

### Yukon Geological Survey Web Pages {#yukon-geological-survey-web-pages .ListParagraph}

#### Databases and GIS {#databases-and-gis .ListParagraph}

##### Description {#description-85 .ListParagraph}

> This page contains the databases and GIS layers created and maintained
> by the Yukon Geological Survey (YGS).

##### URLs {#urls-72 .ListParagraph}

<http://www.geology.gov.yk.ca/databases_gis.html>

##### Extraction Process {#extraction-process-77 .ListParagraph}

> Here are the steps for extracting this page:

1.  Find all \<tbody\> elements and get the first table in the list.

2.  Run the table through the table\_to\_dict method in the shared.py
    script.

3.  Go through each row in the table and:

    a.  Proceed if the "theme" column text is "Geochem".

    b.  Get the link in the "format" column.

    c.  If the link contains ".zip", then get the **Title** from the
        "theme" column and get the **Description** from the
        "description".

    d.  If the link is a sub-page, open it.

    e.  Find the \<div\> with text "Layer Name" and get its next sibling
        \<div\> to get the **Title**.

    f.  Find the \<strong\> with text "Release Date: " and get its
        parent to get the **Date** (removing "Release Date: ").

    g.  Find the \<h3\> with text "Abstract" and get its next sibling
        \<div\> to get the **Description**.

4.  Run the second table on the page through the table\_to\_dict method
    in shared.py script with header \['Theme', 'Description',
    'Format'\].

5.  For each row in the table:

    h.  Determine the **Available Formats** and **Download** based on
        the "Format" column.

    i.  Get the **Title** from the "Theme" column.

    j.  Get the **Description** from the "Description" column.

#### Till Geochemistry/Heavy Minerals {#till-geochemistryheavy-minerals .ListParagraph}

##### Description {#description-86 .ListParagraph}

> This page contains a series of case studies of till geochemistry
> surveys at known mineral deposits. Each study contains a download to
> spreadsheets and databases containing coordinates.

##### URLs {#urls-73 .ListParagraph}

> <http://www.geology.gov.yk.ca/geochemistry.html>

##### Extraction Process {#extraction-process-78 .ListParagraph}

> Each dataset on the page is divided by \<hr\> elements. Once all the
> \<hr\> elements have been collected, go through each and:

1.  Find all the \<a\> elements

2.  Go through each \<a\> and:

    a.  Check if the \<a\> has a name attribute

    b.  Get the text of the \<a\> and check if it contains text

    c.  If the \<a\> has text, use the text for the **Title**

    d.  Get the parent element of \<a\> (which will be a \<strong\>
        element)

    e.  Get a list of \<p\> elements by getting the next siblings of the
        \<strong\> element

    f.  Get the **Description** from the second \<p\>

    g.  Go through each \<p\> element, get its \<a\> and see if its link
        contains '.zip'

    h.  If the \<a\> link contains '.zip', add it to the inventory

#### Community Mapping {#community-mapping .ListParagraph}

##### Description {#description-87 .ListParagraph}

> The Yukon Geological Survey has been mapping local-scale surficial
> geology of several communities throughout the territory since 2010.
> This page contains downloads to these geological maps.

##### URLs {#urls-74 .ListParagraph}

> <http://www.geology.gov.yk.ca/community_mapping.html>

##### Extraction Process {#extraction-process-79 .ListParagraph}

> Here are the steps for extracting the community mapping page:

1.  Locate the \<strong\> with text "Surficial Geology GIS Data:"

2.  Get the parent of the \<strong\> element which is a \<p\>

3.  Locate the next sibling \<ul\> element of the \<p\> element

4.  Get a list of all the \<a\> elements and:

    a.  Get the link of the \<a\> and open the page

    b.  In the page, find the \<div\> with text "Layer Name"

    c.  Use the text of the \<div\> for the **Title**

    d.  Find the \<strong\> with text "Release Date: " and get its next
        sibling to get the **Date**

    e.  For the **Description**, locate the \<h3\> with text "Abstract",
        get its parent, find its next sibling \<div\> and get its text

    f.  For the **Available Formats**, check if the following exists:

        -   \<td\> with text "Geodatabase", add "GDB" to the formats

        -   \<td\> with text "Shapefile", add "SHP" to the formats

        -   \<td\> with text "Google Earth (kmz)", add "KMZ" to the
            formats

#### Stevenson Ridge {#stevenson-ridge .ListParagraph}

##### Description {#description-88 .ListParagraph}

> In 2007, the Yukon Geological Survey began mapping the Quaternary
> geology of the Stevenson Ridge and northern Kluane Lake. The maps are
> provided on this page as ESRI MDB files and Google Earth KMZ files.

##### URLs {#urls-75 .ListParagraph}

> <http://www.geology.gov.yk.ca/stevenson_ridge.html>

##### Extraction Process {#extraction-process-80 .ListParagraph}

> The steps for extracting the Stevenson Ridge page are:

1.  Get the **Description** from the page's metadata

2.  Locate the \<strong\> with text containing "GIS Data"

3.  Get the parent of the \<strong\> and then locate the \<ul\> element

4.  Get a list of the \<li\> and go through each \<li\> and:

    a.  Get the text of the \<li\>, removing the ":", to get the
        **Title**

    b.  Set the **Available Formats** to "ESRI MDB" and "KMZ"

### Yukon Energy, Mines & Resources Web Pages {#yukon-energy-mines-resources-web-pages .ListParagraph}

#### Rights Management Maps and Data {#rights-management-maps-and-data .ListParagraph}

##### Description {#description-89 .ListParagraph}

> This page contains the locations of fall 2016 rights management
> requests throughout the territory.

##### URLs {#urls-76 .ListParagraph}

> <http://www.emr.gov.yk.ca/oilandgas/rights_management_maps_data.html>

##### Extraction Process {#extraction-process-81 .ListParagraph}

> The steps for extracting the rights management page are:

1.  Find all \<tbody\> elements on the page

2.  Go through each \<tbody\> (table) and:

    a.  Run the table through the table\_to\_dict using header
        \[\'Title\', \'Datum\', \'Projection\'\]

    b.  Get the first row of data in the table

    c.  Get the **Title** from the text in the "Title" column

    d.  Get the **Download** from the \<a\> in the "Title" column

    e.  Get the **Spatial Reference** by combining the text in the
        "Projection" column and the "Datum" column

    f.  If the Title contains "ESRI Shapefile", then set the **Available
        Formats** to "SHP", otherwise set it to "FGDB"

#### GIS Data Overview {#gis-data-overview .ListParagraph}

##### Description {#description-90 .ListParagraph}

> This page contains the GIS datasets for the Yukon Department of
> Environment such as the Department's Administrative Boundaries, Base
> or Framework data, Resource Inventory data and Extra-Departmental
> data.

##### URLs {#urls-77 .ListParagraph}

###### Main URL {#main-url-28 .ListParagraph}

> <http://www.env.gov.yk.ca/publications-maps/geomatics/data.php>

###### FTP URL {#ftp-url .ListParagraph}

> [ftp.geomaticsyukon.ca](ftp://ftp.geomaticsyukon.ca)

##### Extraction Process {#extraction-process-82 .ListParagraph}

> The steps for extracting the GIS Data Overview page are:

1.  Create the FTP object using the FTP URL

2.  Find \<ul\> with class 'NavL3'

3.  Get all the \<li\> under the \<ul\>

4.  For each \<li\>:

    a.  Open the page of the \<a\> contained under the \<li\> and get a
        list of all the \<a\> elements under the sub-page

    b.  For each \<a\>, if the link contains "ftp.", get the parent
        element and then find its previous sibling \<h3\>

    c.  The \<h3\> element's text is used for the **Title**

    d.  The **Description** is taken from the \<h3\> next sibling's text
        (which is a \<p\> element)

#### Wildlife Key Area GIS Data Packages {#wildlife-key-area-gis-data-packages .ListParagraph}

##### Description {#description-91 .ListParagraph}

> This site contains the Wildlife Key Area GIS data packages available
> for download.

##### URLs {#urls-78 .ListParagraph}

> <http://www.env.gov.yk.ca/publications-maps/wka_gis_data.php>

##### Extraction Process {#extraction-process-83 .ListParagraph}

> The steps for extracting this page are:

1.  Find the \<div\> with id 'bodyContent'

2.  Under the bodyContent \<div\>, find the \<h2\> to get the **Title**

3.  Locate all the \<p\> elements and grab the third item to get the
    **Description**

### Other Web Pages {#other-web-pages .ListParagraph}

#### Spatial Data - Yukon Land Use Planning Council {#spatial-data---yukon-land-use-planning-council .ListParagraph}

##### Description {#description-92 .ListParagraph}

> This page contains the geospatial data for the Yukon Land Use Planning
> Council. The page is similar in look to a search page but has no
> search capabilities.

##### URLs {#urls-79 .ListParagraph}

> <http://www.planyukon.ca/index.php/documents-and-downloads/spatial>

##### Extraction Process {#extraction-process-84 .ListParagraph}

> Here are the steps for extracting this page:

1.  Get all the \<div\> with class 'docman\_document' to get the results
    on the page

2.  For each results on the page:

    a.  Find the \<span\> with itemprop 'name' and use its text for the
        **Title**

    b.  Skip the dataset if the Title contains "Presentation"

    c.  Get the parent of the \<span\> (which is an \<a\> element) and
        open the link

    d.  In the sub-page, locate the \<time\> tag and get its datetime
        attribute value to get the **Date**

    e.  For the **Description**, get the \<div\> with itemprop
        'description'

    f.  Get the **Download** from the \<a\> with class
        'docman\_download\_\_button'

    g.  Get the **Available Formats** from the Title; if the Title
        contains "kml", set the Available Formats, if the Title contains
        "kmz", set it to "KMZ", otherwise set the Available Formats to
        "SHP"

### Interactive Maps {#interactive-maps-12 .ListParagraph}

#### Description {#description-93 .ListParagraph}

> The Yukon contains several galleries of ArcGIS interactive maps from
> various web pages. There are also individual ArcGIS maps as well.

#### URLs {#urls-80 .ListParagraph}

##### ArcGIS Galleries of Yukon {#arcgis-galleries-of-yukon .ListParagraph}

###### Yukon Government Gallery {#yukon-government-gallery .ListParagraph}

> <http://yukon.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=asc&sortField=title>

###### YGS Gallery {#ygs-gallery .ListParagraph}

> <http://yukon2.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=desc&sortField=numviews>

###### Energy Mines and Resources Gallery {#energy-mines-and-resources-gallery .ListParagraph}

> <http://yukon4.maps.arcgis.com/home/gallery.html?view=grid&sortOrder=asc&sortField=title>

##### Other ArcGIS Maps {#other-arcgis-maps .ListParagraph}

###### YGS Publication Browser {#ygs-publication-browser .ListParagraph}

> <http://deptweb.gov.yk.ca/YGS/Applications/PublicationBrowser>
>
> <http://www.arcgis.com/sharing/rest/content/items/c1f89c570b894b7790a9a885ab685291?f=pjson>

###### YGS Current Field Projects {#ygs-current-field-projects .ListParagraph}

> <http://www.geology.gov.yk.ca/>
>
> <https://yukon2.maps.arcgis.com/sharing/rest/content/items/48e3f508fda64dfc95c6dd0e6f821ff0?f=pjson>

###### Yukon Physiographic Regions {#yukon-physiographic-regions .ListParagraph}

> <http://yukon2.maps.arcgis.com/home/webmap/viewer.html?webmap=02ad68fcb38b40149b5a313c9cbb54bc>

###### Yukon Sedimentary Basins {#yukon-sedimentary-basins .ListParagraph}

> <http://yukon2.maps.arcgis.com/home/webmap/viewer.html?webmap=5113d22270e2400581c0065d6fedfb55>

###### Volcanogenic massive sulphide (VMS) and Orogenic Gold Deposits of Chatham Strait, Southeast Alaska {#volcanogenic-massive-sulphide-vms-and-orogenic-gold-deposits-of-chatham-strait-southeast-alaska .ListParagraph}

> <https://yukon2.maps.arcgis.com/apps/MapTour/index.html?appid=f9a2ada0189f4143ac64e2bc0c9111d7>

###### Yukon Historic Earthquakes {#yukon-historic-earthquakes .ListParagraph}

> <http://yukon2.maps.arcgis.com/apps/Viewer/index.html?appid=ce7893e2b1bf43a582da48fd1165f4df>

###### Yukon Regional Geochemical Survey (RGS) Reanalysis Data {#yukon-regional-geochemical-survey-rgs-reanalysis-data .ListParagraph}

> <http://yukon2.maps.arcgis.com/home/webmap/viewer.html?webmap=470f246f9b0f4987ab2e590df6dd94c4>

###### Indian River Wetlands {#indian-river-wetlands .ListParagraph}

> <http://yukon4.maps.arcgis.com/apps/webappviewer/index.html?id=fde154c2332248899bee6875b314078b>

###### Lots For Sale {#lots-for-sale .ListParagraph}

> <http://yukon4.maps.arcgis.com/apps/webappviewer/index.html?id=2afcf62ef63b46b6bc38b38a5828c628>

#### Extraction Process {#extraction-process-85 .ListParagraph}

##### ArcGIS Galleries of Yukon {#arcgis-galleries-of-yukon-1 .ListParagraph}

> These galleries contain various ArcGIS interactive maps of the Yukon
> Government, the YGS and the Department of Energy, Mines and Resources.
>
> The extraction process is the same as galleries in other
> provinces/territories. With the gallery URL, run the
> get\_arcgis\_gallery method in the shared.py script and go through
> each map and add its information to the inventory.

##### Other ArcGIS Maps {#other-arcgis-maps-1 .ListParagraph}

> The extraction process of the ArcGIS maps for the Yukon is the same as
> other provinces/territories. The process uses the get\_arcgis\_data
> method from the shared.py script. In cases where there are 2 URLs,
> such as the YGS Publication Browser and the YGS Current Field Projects
> maps, the second URL is used to get the ArcGIS data.

### ArcGIS Hub {#arcgis-hub-1 .ListParagraph}

#### Description {#description-94 .ListParagraph}

> The ArcGIS Hub for the Yukon Government contains over 300 ArcGIS
> feature layers throughout the territory.

#### URLs {#urls-81 .ListParagraph}

##### Main URL {#main-url-29 .ListParagraph}

> <https://hub.arcgis.com/datasets?source=Yukon%20Government>

##### Query URL for JSON Data {#query-url-for-json-data .ListParagraph}

> <https://opendata.arcgis.com/api/v2/datasets>

#### Extraction Process {#extraction-process-86 .ListParagraph}

> Here are the steps for extracting the ArcGIS Hub of the Yukon
> Government:

1.  Build the URL query string with the following parameters to get the
    JSON data:

    -   **filter\[source\]**: The source of the Hub, in this case "Yukon
        Government".

    -   **filter\[content\]**: The type of content to filter the Hub
        results, in this case "any(web map,spatial dataset,table,raster
        dataset)"

    -   **include**: The categories to include in the search, in this
        case "sites,organizations,groups"

    -   **page\[number\]**: The number of pages to list, in this case
        "1"

    -   **page\[size**\]: The number of results per page, in this case
        "310"

    -   Query URL Example:
        [https://opendata.arcgis.com/api/v2/datasets?filter\[source\]=Yukon%20Government&filter\[content\]=any(web%20map,spatial%20dataset,table,raster%20dataset)&include=sites,organizations,groups&page\[number\]=1&page\[size\]=300](https://opendata.arcgis.com/api/v2/datasets?filter%5bsource%5d=Yukon%20Government&filter%5bcontent%5d=any(web%20map,spatial%20dataset,table,raster%20dataset)&include=sites,organizations,groups&page%5bnumber%5d=1&page%5bsize%5d=300)

2.  Get the JSON data using the query URL

3.  Get a list of the 'data' results from the JSON data

4.  For each 'data' result:

    a.  Get the 'attributes' item

    b.  Get the **Title** from the 'title' in the attributes

    c.  Get the **Description** from the 'description' in the attributes

    d.  Get the **Type** from the attribute 'dataType'

    e.  Get the **Date** from the attribute 'updatedAt'

    f.  Get the **Spatial Reference** using the get\_spatialref method
        in the shared.py which will search for an item name
        'serviceSpatialReference'

    g.  Get the **Web Page URL** from the attribute 'landingPage'

    h.  Get the **Web Service URL** from the attribute 'url'

### Yukon Government Corporate Spatial Warehouse Gallery {#yukon-government-corporate-spatial-warehouse-gallery .ListParagraph}

#### Description {#description-95 .ListParagraph}

> The layers in this gallery are served out of the Yukon government's
> Corporate Spatial Warehouse.

#### URLs {#urls-82 .ListParagraph}

#####  Main URL {#main-url-30 .ListParagraph}

> <http://yukon.maps.arcgis.com/home/group.html?id=099cc2a078c1432390cdbc90fe114179&start=1&view=list#content>

#####  Query URL {#query-url-6 .ListParagraph}

> <https://yukon.maps.arcgis.com/sharing/rest/search>

#### Extraction Process {#extraction-process-87 .ListParagraph}

> These are the steps for extracting the Spatial Warehouse Gallery:

1.  The maximum number of results per page is 100. To go through all the
    results (about 310), a for loop has to be created with a range of 0
    to 5. The start parameter will be set each time to the current
    value, multiplied by 100 and 1 added to it (ex: 1, 101, 201, ...)
    (although there are not 500 datasets, 5 was chosen for any future
    expansion of the gallery).

2.  Build the URL query string with the following parameters (for a full
    list of parameters, visit
    <https://developers.arcgis.com/rest/users-groups-and-items/search.htm#GUID-A2C8BFD1-89B2-483F-9275-65D2786F6A6C>):

    -   **num**: The number of results to display (maximum is 100)

    -   **start**: The result number to start

    -   **sortField**: Sorts the results by a specified field

    -   **sortOrder**: Sorts the results by this order (asc, desc)

    -   **q**: The text filter for the search

    -   **f**: The format in which the data will be returned

3.  Get a list of results from the JSON data using the query URL

4.  For each result:

    a.  Get the **Date** from the 'modified' item

    b.  Get the **Title** from the 'title' item

    c.  Get the **Type** from the 'type' item

    d.  Get the **Description** from the 'description' item. Use
        BeautifulSoup if the description contains HTML code

    e.  Get the **Service URL** from the 'url' item

### Map Services {#map-services-9 .ListParagraph}

#### Description {#description-96 .ListParagraph}

> Yukon has one ArcGIS REST Service and a Geocortex Service.

#### URLs {#urls-83 .ListParagraph}

#####  ArcGIS REST URL {#arcgis-rest-url .ListParagraph}

> <http://mapservices.gov.yk.ca/ArcGIS/rest/services>

#####  Geocortex URL {#geocortex-url-1 .ListParagraph}

> <http://mapservices.gov.yk.ca/Geocortex/Essentials/REST/sites>

#### Extraction Process {#extraction-process-88 .ListParagraph}

> The extraction process for these two services is the same as other
> provinces/territories. For the ArcGIS REST Service, use the get\_data
> method from the MyREST class. For the Geocortex, use the get\_data
> method from the MyGeocortex class.

### FTP {#ftp-2 .ListParagraph}

#### Description {#description-97 .ListParagraph}

> The Yukon FTP site contains 3 folders with geospatial datasets,
> "Elevation", "GeoYukon" and "Imagery".

#### URLs {#urls-84 .ListParagraph}

#####  Main URL {#main-url-31 .ListParagraph}

> [ftp.geomaticsyukon.ca](ftp://ftp.geomaticsyukon.ca)

#### Extraction Process {#extraction-process-89 .ListParagraph}

> The extraction process for the Yukon FTP site is similar to other
> provinces/territories. The steps are:

1.  Create a list of the folders (\["Elevation", "GeoYukon",
    "Imagery"\])

2.  Create the header list for the RecFTP object (\[\'permissions\',
    \'links\', \'owner\', \'group\', \'filesize\', \'month\', \'day\',
    \'time\', \'filename\'\])

3.  For each folder:

    a.  Create the RecFTP object using the FTP URL, the current folder
        and the header list

    b.  Get a list of files for the current folder and add it to the
        final file list

4.  For each file:

    c.  Get the **Title** from the base-name of the file

    d.  Add the file to the CSV inventory
