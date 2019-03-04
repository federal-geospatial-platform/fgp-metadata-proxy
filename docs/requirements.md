# Requirements

## FGP UX
https://gcgeo.gc.ca/geonetwork/search/eng
* Refine results by organization – add faceted search for non-fed agencies
* Disclaimer – non triple AAA
* Disclaimer – language for auto-translate and for external links
* Bilingual content for web presence content

## DataBC 
https://catalogue.data.gov.bc.ca/dataset?download_audience=Public
* Compliance  with licence agreement [OGL-BC](https://www2.gov.bc.ca/gov/content/data/open-data/open-government-license-bc)
* Presentation of results in test stage (pre-prod)

## Open Government Portal – Open Maps 
https://open.canada.ca/en/open-maps
* BC Content is not pushed to Open Maps until MOU signed between TBS and BC
* Auto (DEEPL) generated translations are noted as such (no quality control)
* Incoming metadata will map to OGMES metadata profile – validates on ingest

## EODMS 
https://www.eodms-sgdot.nrcan-rncan.gc.ca/index_en.jsp
* Access to only open data
* Metadata assessment for conformance with HNAP

Collective expectation should be that RADARSAT-1 will be listed in the anonymous open call to https://www.eodms-sgdot.nrcan-rncan.gc.ca/wes/rapi/collections?format=json by March 31, 2019.

Specifically, it ought to look like the other listed collections:
{"title":"RADARSAT-1","collectionId":"Radarsat1","description":"Developed and operated by the Canadian Space Agency, it is Canada's first commercial Earth observation satellite.","url":"https://www.eodms-sgdot.nrcan-rncan.gc.ca/wes/rapi/collections/Radarsat1"}

## FGP Catalogue 
https://gcgeo.gc.ca/geonetwork/login/eng
* Release approval process for non-fed data will be bypassed or automated
* Textual content of metadata will be translated and available in both OL (using DEEPL as in OGP example with Alberta)
* DCAT metadata will map to and trigger necessary signals for RAMP, OGL ingest, data content type, etc. Refer to HNAP specification for rules (https://gcdocs.gc.ca/nrcan-rncan/llisapi.dll/link/21920784).

## Open Science Data Platform 
https://gcdocs.gc.ca/nrcan-rncan/llisapi.dll/link/26141853
* OSDP-specific data classification or keywords to be added (emerging requirement – plan for it in DCAT metadata)
