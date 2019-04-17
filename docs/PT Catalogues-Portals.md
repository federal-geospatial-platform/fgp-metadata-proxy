
PT Catalogues/Portals Sources
==========
# Table of Contents
- [Services](#services)
  - [CKAN](#ckan)
    - [P/T Usage](#pt-usage)
    - [Webpage Access](#webpage-access)
    - [API Access](#api-access)
  - [Drupal](#drupal)
    - [P/T Usage](#pt-usage-1)
    - [API Access](#api-access-1)
  - [ESRI Geoportal Server](#esri-geoportal-server)
    - [P/T Usage](#pt-usage-2)
    - [Webpage Access](#webpage-access-1)
    - [API Access](#api-access-2)
  - [Socrata](#socrata)
    - [P/T Usage](#pt-usage-3)
    - [Webpage Access](#webpage-access-2)
    - [API Access](#api-access-3)
- [Provinces](#provinces)
    - [Alberta](#alberta)
      - [GeoDiscover Catalogue](#geodiscover-cataloguehttpsgeodiscoveralbertacageoportalcatalogsearchbrowsebrowsepage)
      - [Open Government](#open-governmenthttpsopenalbertacaopendata)
    - [British Columbia](#british-columbia)
      - [Open Data Catalogue](#open-data-cataloguehttpscataloguedatagovbccadataset)
    - [Manitoba](#manitoba)
    - [New Brunswick](#new-brunswick)
    - [Newfoundland & Labrador](#newfoundland--labrador)
    - [Northwest Territories](#northwest-territories)
      - [Discovery Portal](#discovery-portalhttpnwtdiscoveryportalenrgovntcageoportalcatalogsearchbrowsebrowsepage)
    - [Nova Scotia](#nova-scotia)
      - [Open Data](#open-datahttpsdatanovascotiacabrowse)
    - [Nunavut](#nunavut)
    - [Ontario](#ontario)
      - [Data Catalogue](#data-cataloguehttpswwwontariocasearchdata-catalogue)
      - [Discovering Ontario](#discovering-ontariohttpswwwjavacoeapplrcgovoncageonetworksrvenmainhome)
    - [Prince Edward Island](#prince-edward-island)
      - [Open Catalogue](#open-cataloguehttpsdataprinceedwardislandcabrowse)
    - [Quebec](#quebec)
      - [Données Québec](#données-québec)
    - [Saskatchewan](#saskatchewan)
    - [Yukon](#yukon)
      - [GeoYukon](#geoyukonhttpgeowebgovykcageoportalcatalogsearchbrowsebrowsepage)
   
# Services

## CKAN

### P/T Usage

As of 28 March 2019, the following provincial sites use CKAN API:

-   [Alberta's Open Government](https://open.alberta.ca/opendata)

-   [British Columbia's Open Data Catalogue](https://catalogue.data.gov.bc.ca/dataset)

### Webpage Access

All webpage access is through the "dataset" URL:

```<domain>/dataset/```

#### Search Engine

The CKAN search engine and any of its dataset's webpages are accessed using these URLs:

```<domain>/dataset?<parameters>```

For example, the following URL will return all datasets in Alberta's data catalogue containing the word "roads":

[https://open.alberta.ca/dataset?q=roads]{.underline}

#### Dataset Page

A dataset's page can be accessed using the following URL:

```<domain>/dataset/<dataset_id>```

The following example loads the "Alberta Non-Profit Listing" dataset:

<https://open.alberta.ca/dataset/bcc15e72-fe46-4215-8de0-33951662465e>

### API Access

The CKAN API is accessed using:

```<domain>/api/3/action```

#### JSON Search

The API can be used to search for datasets in the same way as the dataset search engine, except the results are listed in JSON format instead of in a search engine. To perform a search on the CKAN catalogue, enter:

```<domain>/api/3/action/package_search?<parameters>```

For Alberta, the following URL returns the results for all open data in JSON format:

<https://open.alberta.ca/api/3/action/package_search?fq=dataset_type:opendata>

| Parameter | Description | FGP PyCSW Setting |
| --------- | ----------- | ----------------- |
| home | The full filesystem path to pycsw | C:\\pycsw-2.2.0 |
| url | The URL of the resulting service | http://localhost:8000/pycsw/csw.py |
| maxrecords | The maximum number of records to return by default. This value is enforced if a CSW’s client’s maxRecords parameter is greater than server.maxrecords to limit capacity. | 10 |
| logfile | The full file path to the logfile. | C:\\pycsw-2.2.0\\log\\pycsw.log |

The following table contains the parameters for **package_search** query (source: <https://docs.ckan.org/en/ckan-2.7.3/api/#ckan.logic.action.get.package_search>)

| **Parameter**                     | **Description**                   |
| --------------------------------- | --------------------------------- |
| q                                 | The [solr](http://www.solrtutorial.com/solr-query-syntax.html) query. Optional. Default: \"\*:\*\"                        |
| fq                                | Any filter queries to apply.      |
| sort                              | Sorting of the search results. Optional. Default: \'relevance asc, metadata\_modified desc\'. As per the solr documentation, this is a comma-separated string of field names and sort-orderings.                     |
| rows                              | The number of matching rows to return. There is a hard limit of 1000 datasets per query.          |
| start                             | The offset in the complete result for where the set of returned datasets should begin.            |
| facet                             | Whether to enable faceted results. Default: True. |
| facet.mincount                    | The minimum counts for facet fields should be included in the results.                          |
| facet.limit                       | The maximum number of values the facet fields return. A negative value means unlimited. This can be set instance-wide with the search.facets.limit config        option. Default is 50.            |
| facet.field                       | The fields to facet upon. Default empty. If empty, then the         returned facet information is empty.                            |
| include\_drafts                   | If True, draft datasets will be included in the results. A user will only be returned their own draft datasets, and a sysadmin will be returned all draft        datasets. Optional, the default is False.                         |
| include\_private                  | If True, private datasets will be included in the results. Only private datasets from the user's organizations will be returned and sysadmins will be returned all private datasets. Optional, the default is False.             |
| use\_default\_schema              | Use default package schema instead of a custom schema        defined with an IDatasetForm plugin (default: False)           |

#### JSON Dataset

To view a dataset in JSON format, enter:

```<domain>/api/3/action/package_show?id=<id_name>```

The following URL contains the JSON results for the Preliminary Total Housing Starts in Alberta\'s Major Urban Centres dataset:

<https://open.alberta.ca/api/3/action/package_show?id=a4b99aad-3f33-45ea-a5c7-e34a4733d336>

The following table contains the parameters for **package_show** query (source: <https://docs.ckan.org/en/ckan-2.7.3/api/#ckan.logic.action.get.package_show>)

| **Parameter**                     | **Description**                   |
| --------------------------------- | --------------------------------- |
| id                                | The id or name of the dataset.    |
| use\_default\_schema              | Use default package schema instead of a custom schema        defined with an IDatasetForm plugin (default: False)           |
| include\_tracking                 | Add tracking information to dataset and resources (default:   False)                            |

### More Information

For more information on CKAN, visit https://ckan.org/.

## Drupal

### P/T Usage

As of 28 March 2019, the following provincial sites use Drupal API

-   [Ontario's Data Catalogue](https://www.ontario.ca/search/data-catalogue)

### API Access

#### Search

The only way to search using the Drupal API is by sending a POST request to:

```<domain>/es/onesite/_search/template```

The POST request should contain a list of parameters and the template ID in JSON format:

```{"params": {<parameters>}, "template": {"id": "dataset"}}```

For example, to search for datasets containing the word "roads" in the Ontario Data Catalogue, the following POST request is sent:

```{"params": {"lang": "en", "from": 0, "query": "roads", "fileType?": {"list": ["zip"]}, "status?": {"list": [None]}, "size": 0}, "template": {"id": "dataset"}}```

To:

<https://api.ontario.ca/es/onesite/_search/template>

#### Dataset

A specific dataset is accessed in the Drupal API using this URL:

```<domain>/api/drupal/data%2F<id_name>```

For example, to access the "Weather Camera Data" dataset from
Ontario's Data Catalogue, enter:

<https://api.ontario.ca/api/drupal/data%2Fweather-camera-data>

### More Information

For more information on Drupal, visit https://api.drupal.org/.

## ESRI Geoportal Server

### P/T Usage

As of 28 March 2019, the following provincial/territorial sites use ESRI Geoportal Server API:

-   [Alberta's GeoDiscover Catalogue](https://geodiscover.alberta.ca/geoportal/catalog/search/search.page)

-   [Northwest Territories' Discovery Portal](http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/catalog/main/home.page)

-   [Yukon's GeoYukon GeoPortal](http://geoweb.gov.yk.ca/geoportal/catalog/main/home.page)

### Webpage Access

#### Search Engine

The search engine URL for an ESRI Geoportal Server is:

```<domain>/geoportal/catalog/search/search.page```

The URL for Alberta's GeoDiscover search engine is:

<https://geodiscover.alberta.ca/geoportal/catalog/search/search.page>

#### Browser Page

The browser URL for the Server is:

```<domain>/geoportal/catalog/search/browse/browse.page```

For Alberta's GeoDiscover browser, the URL is:

<https://geodiscover.alberta.ca/geoportal/catalog/search/browse/browse.page>

#### Details Page

The URL for the Details page of a dataset is:

```<domain>/geoportal/catalog/search/resource/details.page?uuid=<uuid>```

For example, the URL for the Details page of Alberta's "Greater Short-horned Lizard Habitat" is:

<https://geodiscover.alberta.ca/geoportal/catalog/search/resource/details.page?uuid=%7BD4D78EF6-27C9-4E5B-9A8E-F10466421CF3%7D>

#### Full Metadata

The URL for the Full Metadata page of a dataset is:

```<domain>/geoportal/catalog/search/resource/fullMetadata.page?uuid=<uuid>```

For Alberta's "Greater Short-horned Lizard Habitat" dataset, the Full Metadata page URL is:

<https://geodiscover.alberta.ca/geoportal/catalog/search/resource/fullMetadata.page?uuid=%7BD4D78EF6-27C9-4E5B-9A8E-F10466421CF3%7D>

### API Access

#### Search

The following URL is used to search the datasets using the API; unless specified, the data is returned as an XML:

```<domain>/geoportal/rest/find/document?<parameters>```

This URL returns all datasets in Alberta's GeoDiscover containing the word "roads" in JSON format:

<https://geodiscover.alberta.ca/geoportal/rest/find/document?searchText=roads&f=pjson>

The following table contains the parameters for the REST query (source: <https://github.com/Esri/geoportal-server/wiki/REST-API-Syntax>)

| **requestParameter**  | **Function**          | **Accepted Values**   |
| --------------------- | --------------------- | --------------------- |
| bbox                  | Query by extent specified as two pairs of coordinates (west-south and east-north). | Comma-delimited string of integers between -180,180 and -90, 90. |
| spatialRel            | Query by spatial relationship. Used in conjunction with bbox parameter.            | String value. One of esriSpatialRelWithin (default), esriSpatialRelOverlaps. |
| searchText            | Query by keyword.     | String value representing a keyword. Note, as of version 1.1.1, you can use searchText=sys.schema.key to query for documents that correspond to a specific metadata schema. See [How to find all documents of a particular metadata standard](https://github.com/Esri/geoportal-server/wiki/How-to-find-all-documents-of-a-particular-metadata-standard) for more details. |
| contains              | Keyword concatenation options. This parameter is obsolete with the Lucene syntax (see [Using Lucene Search Text Queries](https://github.com/Esri/geoportal-server/wiki/Using-Lucene-Search-Text-Queries)). | For an exact match use double quotes. For example, see the syntax for two terms, Hawaii and quads:<br>-   Exact: "Hawaii quads"<br>-   Any: Hawaii quads<br>-   All: +Hawaii+quads<br>//<serverName>/geoportal/rest/find/document?searchText="Hawaii quads"&f=georss |
| contentType           | Query by content type. | String value representing an Esri content type. See Javadoc for complete list. |
| dataCategory          | Query by data category (ISO 19115 themes). | Comma-delimited list of strings. Keywords identified by the ISO 19115 specification. See JavaDoc for complete list. |
| after, before         | Query by date.        | Date string in the format yyyy-mm-dd. |
| orderBy               | Result sort options.  | String value. One of areaAscending, areaDescending, dateAscending, dateDescending (default), format, relevance, title. |
| start                 | Specify which item to start the response with out of the entire resultset. | Integer. When used with the max parameter, this provides for pagination of the search results. |
| max                   | Specify max number of records to retrieve. | Integer. There is a limit of max=100 on unqualified queries. An 'unqualified query' is when there are no search parameters set. The limit on qualified queries is max=5000. Default: 10. When used with the start parameter, this provides for pagination of the search results. |
| geometryType          | Defines how spatial data will be represented. | String value. One of esriGeometryPoint, esriGeometryPolygon (default), esriGeometryBox. |
| f                     | The response format.  | String value. One of georss (default), atom, json, pjson, xjson, dcat (1.2.4), kml, html, htmlfragment, searchpage (as of 1.1.1), CSV (as of 1.2), xjson output compliants with geojson 1.0 and contains more detailed information (1.2.4). |
| style                 | CSS stylesheet for HTML results. | String value representing a URL to a stylesheet. |
| target                | Behavior of links (open in same or new window). | String value. One of blank (default), parent, self, top. |
| rid                   | Id associated with the repository. Multiple ridparameters are allowed for comparing results between different repositories. | String value.                      |
| rids                  | Comma Delimited rid. Can be used instead of the multiple ridparameters. | String values. |
| maxSearchTimeMilliSec | Maximum amount of time allowed to retrieve results. | Integer. Default is 5000 milliseconds.                      |
| filter                | Can apply a persistent filter to the search interface. See [URL Filter Customization](https://github.com/Esri/geoportal-server/wiki/Url-filter-customization) | lucene-based query syntax                      |

#### Dataset

##### ISO XML Data

For the full metadata of a dataset in ISO 19115, use:

```<domain>/geoportal/rest/document?id=<uuid>```

If the parameter "f=pjson" is used, a brief metadata page in JSON format will be returned.

For example, this URL returns the full ISO metadata for Alberta's "Castle Region Linear Footprint" in XML:

[https://geodiscover.alberta.ca/geoportal/rest/document?id={0F933555-8715-4E1B-8C43-409591957ECE}](https://geodiscover.alberta.ca/geoportal/rest/document?id=%7b0F933555-8715-4E1B-8C43-409591957ECE%7d)

While the following example returns only a brief metadata of same dataset in JSON format:

[https://geodiscover.alberta.ca/geoportal/rest/document?id={0F933555-8715-4E1B-8C43-409591957ECE}&f=pjson](https://geodiscover.alberta.ca/geoportal/rest/document?id=%7b0F933555-8715-4E1B-8C43-409591957ECE%7d&f=pjson)

### More Information

For more information on ESRI Geoportal Server, visit https://www.esri.com/en-us/arcgis/products/geoportal-server/overview.

## Socrata

### P/T Usage

As of 28 March 2019, the following provincial sites use Socrata:

-   [Nova Scotia's Open Data Catalogue](https://data.novascotia.ca/browse)

-   [Prince Edward Island's Open Data Catalogue](https://data.princeedwardisland.ca/browse)

### Webpage Access

#### Search Engine

Socrata search engine is accessed using:

```<domain>/browse```

#### Dataset Page

Any Socrata dataset's webpage can be accessed using the following URL:

```<domain>\d\<ds_id>```

For example, the URL to access the "Crown Land" dataset in Nova Scotia's
catalogue is:

<https://data.novascotia.ca/d/3nka-59nz>

### API Access

#### JSON Search (Global Catalogue)

The global catalogue includes all data in the Socrata open data portal. To narrow searches to datasets in a particular province/territory, add domains=\<domain\_without\_http\> to the query url:

```<domain>/api/catalog/v1?domains=<domain_without_http>&<parameters>```

Queries can only be done using the global catalogue.

For example, the following URL returns all datasets in the Nova Scotia data catalogue containing the word "roads":

<https://data.novascotia.ca/api/catalog/v1?domains=data.novascotia.ca&q=roads>

For information on the available parameters, visit
<https://socratadiscovery.docs.apiary.io>.

#### JSON Views

The "views" URL returns all the data in a particular Socrata catalogue. However, queries cannot be done using this URL:

```<domain>/api/views/```

For example, the URL for Nova Scotia's view is:

<https://data.novascotia.ca/api/views/>

#### JSON Dataset

To view a dataset in JSON format, use the following URL:

```<domain>/api/views/<ds_id>```

For example, the following URL retrieves the "Crown Land" dataset in JSON format:

<https://data.novascotia.ca/api/views/3nka-59nz>

#### Download

The geospatial link is used to download the dataset in a specified format:

```<domain>/api/geospatial/<id>?method=export&format=<format>```

For example, the following URL will download the "Crown Land" dataset in its original format (in this case a Shapefile in a zip file) from Nova Scotia's data catalogue:

<https://data.novascotia.ca/api/geospatial/3nka-59nz?method=export&format=Original>

The next URL will download a KML version of the same dataset:

<https://data.novascotia.ca/api/geospatial/3nka-59nz?method=export&format=KML>

### More Information

For more information on Socrata, visit https://socrata.com/.

# Provinces

## Alberta

### [GeoDiscover Catalogue](https://geodiscover.alberta.ca/geoportal/catalog/search/browse/browse.page)

-   Powered by ESRI Geoportal Server CSW

-   Search Engine:
    <https://geodiscover.alberta.ca/geoportal/catalog/search/search.page>

-   Browser Page:
    <https://geodiscover.alberta.ca/geoportal/catalog/search/browse/browse.page>

-   Details Page:
    <https://geodiscover.alberta.ca/geoportal/catalog/search/resource/details.page>?uuid={\<uuid\>}

-   Full Metadata Page:
    <https://geodiscover.alberta.ca/geoportal/catalog/search/resource/fullMetadata.page>?uuid={\<uuid\>}

-   API Search:
    <https://geodiscover.alberta.ca/geoportal/rest/find/document>?\<parameters\>

-   API Dataset:
    <https://geodiscover.alberta.ca/geoportal/rest/document>?id={\<uuid\>}

### [Open Government](https://open.alberta.ca/opendata)

-   Powered by [CKAN](https://ckan.org/)

-   Search Engine: <https://open.alberta.ca/dataset>?\<parameters\>

-   Dataset Page: <https://open.alberta.ca/dataset/>\<uuid\>

-   API JSON Search :
    <https://open.alberta.ca/api/3/action/package_search>?\<parameters\>

-   API JSON Dataset:
    <https://open.alberta.ca/api/3/action/package_show>?id=\<uuid\>

## British Columbia

### [Open Data Catalogue](https://catalogue.data.gov.bc.ca/dataset)

-   Powered by [CKAN](https://ckan.org/)

-   Search Engine:
    <https://catalogue.data.gov.bc.ca/dataset>?\<parameters\>

-   Dataset Page: <https://catalogue.data.gov.bc.ca/dataset/>\<uuid\>

-   API JSON Search :
    <https://catalogue.data.gov.bc.ca/api/3/action/package_search>?\<parameters\>

-   API JSON Dataset:
    <https://catalogue.data.gov.bc.ca/api/3/action/package_show>?id=\<uuid\>

## Manitoba

## New Brunswick

## Newfoundland & Labrador

## Northwest Territories

### [Discovery Portal](http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/catalog/search/browse/browse.page)

-   Powered by [ESRI Geoportal Server](https://www.esri.com/en-us/arcgis/products/geoportal-server/overview)

-   Search Engine:
    <http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/catalog/search/search.page>

-   Browser Page:
    <http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/catalog/search/browse/browse.page>

-   Details Page:
    <http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/catalog/search/resource/details.page>?uuid={\<uuid\>}

-   Full Metadata Page:
    <http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/catalog/search/resource/fullMetadata.page>?uuid={\<uuid\>}

-   API Search:
    <http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/rest/find/document>?\<parameters\>

-   API Dataset:
    <http://nwtdiscoveryportal.enr.gov.nt.ca/geoportal/rest/document>?id={\<uuid\>}

## Nova Scotia

### [Open Data](https://data.novascotia.ca/browse)

-   Powered by [Socrata](https://socrata.com/)

-   Search Engine: <https://data.novascotia.ca/browse>

-   Dataset Page: <https://data.novascotia.ca/d/>\<ds\_id\>

-   API JSON Search (Global Catalogue):
    <https://data.novascotia.ca/api/catalog/v1>?domains=\<domain\_without\_http\>&\<parameters\>

-   API JSON Views (all records): <https://data.novascotia.ca/api/views>

-   API JSON Dataset:
    [https://data.novascotia.ca/api/views/\<ds\_id](https://data.novascotia.ca/api/views/%3cds_id)\>

-   API Download:
    <https://data.novascotia.ca/api/geospatial/>\<id\>?method=export&format=\<format\>

## Nunavut

## Ontario

### [Data Catalogue](https://www.ontario.ca/search/data-catalogue)

-   Powered by [Drupal](https://api.drupal.org)

### [Discovering Ontario](https://www.javacoeapp.lrc.gov.on.ca/geonetwork/srv/en/main.home)

-   Powered by [GeoNetwork
    opensource](https://geonetwork-opensource.org/)

## Prince Edward Island

### [Open Catalogue](https://data.princeedwardisland.ca/browse)

-   Powered by [Socrata](https://socrata.com/)

-   Search Engine: <https://data.princeedwardisland.ca/browse>

-   Dataset Page: <https://data.princeedwardisland.ca/d/>\<ds\_id\>

-   API JSON Search (Global Catalogue):
    <https://data.princeedwardisland.ca/api/catalog/v1>?domains=\<domain\_without\_http\>&\<parameters\>

-   API JSON Views (all records):
    <https://data.princeedwardisland.ca/api/views>

-   API JSON Dataset:
    <https://data.princeedwardisland.ca/api/views/>\<ds\_id\>

-   API Download:
    <https://data.princeedwardisland.ca/api/geospatial/>\<id\>?method=export&format=\<format\>

## Quebec

### [Données Québec](https://www.donneesquebec.ca/fr/)
-	Powered by CKAN
-	Domain: https://www.donneesquebec.ca/recherche/fr (in the [CKAN instructions](#ckan) above, replace “domain” with this URL)
-	Search Engine: https://www.donneesquebec.ca/recherche/fr/dataset?<parameters>
-	Dataset Page: https://www.donneesquebec.ca/recherche/fr/dataset/<uuid>
-	API JSON Search :  https://www.donneesquebec.ca/recherche/fr/api/3/action/package_search?<parameters>
-	API JSON Dataset:  https://www.donneesquebec.ca/recherche/fr/api/3/action/package_show?id=<uuid>


## Saskatchewan

## Yukon

### [GeoYukon](http://geoweb.gov.yk.ca/geoportal/catalog/search/browse/browse.page)

-   Powered by [ESRI Geoportal
    Server](https://www.esri.com/en-us/arcgis/products/geoportal-server/overview)

-   Search Engine:
    <http://geoweb.gov.yk.ca/geoportal/catalog/search/search.page>

-   Browser Page:
    <http://geoweb.gov.yk.ca/geoportal/catalog/search/browse/browse.page>

-   Details Page:
    <http://geoweb.gov.yk.ca/geoportal/catalog/search/resource/details.page>?uuid={\<uuid\>}

-   Full Metadata Page:
    <http://geoweb.gov.yk.ca/geoportal/catalog/search/resource/fullMetadata.page>?uuid={\<uuid\>}

-   API Search:
    <http://geoweb.gov.yk.ca/geoportal/rest/find/document>?\<parameters\>

-   API Dataset:
    <http://geoweb.gov.yk.ca/geoportal/rest/document>?id={\<uuid\>}
