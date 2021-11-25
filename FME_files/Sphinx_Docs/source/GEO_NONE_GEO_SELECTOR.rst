GEO_NONE_GEO_SELECTOR
=====================

Documentation du Custom Transformer FME
#######################################

**Description**

This custom transformer fans out the metadata records between two types of metadata (GeoSpatial and None GeoSpatial).  When a metadata record cannot be validates as GeoSpatial it is declared None Geospatial. In order to determine the type of metadata record, the transformer analyse attributes according to the YAML directives.  See the section Content of the YAML directives below for a complete description of the YAML directives.


**Input Ports** 

* DATA_INPUT: The input metadata records to process.


**Output Ports** 

* GEOSPATIAL: Output port for all gepspatial metadata records;

* NON-GEOSPATIAL: Output port for all none geospatial metadata records;

* ERROR_LOG: Output port for metadata records that need to be logged according to the YAML directives.

Note: All the input records will go through either the GeoSpatial the None GeoSpatial port.  Some input records may be duplicated and sent through the LOG_ERROR port  if requested by the YAML directives.


**Parameters**

* YAML_DIRECTIVES: YAML directives for determining the Geospatial and None Geospatial records.  See the section Content of the YAML directives below for a description of the YAML directives.

**Content of the YAML directives**

The YAML directives are used by the custom transformer to decide the type of the metadata records: GeoSpatial or None GeoSpatial.  Here's an exemple of a YAML directives::

 resources{}.format:
   domain: LOOKUP_TABLE_FORMAT
   spatial_type: overwrite
   not_found: log
   search_type: equals
 #
 description:
   domain: [spatial, geographic]
   spatial_type: no_overwrite
   not_found: no_log
   search_type: contains


**Description of the YAML directives**

The first part of the YAML is the name of the FME attribute to use to validate the record, it can be a list attribute (ex.: resources{}..format) or a simple  attribute (ex.: description). If it's a list attribute,the name must contain the 2 characters:"{}".  The content of that attribute will be used to determine if the record is GeoSpatial or None GeoSpatial.

Following the FME attribute to validate, there are 4 keywords: domain, spatial_type, not_found and search_type.

* The first keyword domain defines the domain of values that are used to determine if a metadata record is GeoSpatial or None GeoSpatial. Two values are possible: LOOKUP_TABLE_FORMAT or a list of word defining the domain between brackets (ex.: [point, line, poygone]).  When using the keyword LOOKUP_TABLE_FORMAT, the custom transformer will use the content of the column name format of the CSV fileto define the domain of values. The record type will be GeoSpatial if the column fgp_publish is set to "oui".  When using a domain list, the metadata record will be GeoSpatial if the value of the FME attribute is contained in the domain list.

* The second keyword spatial_type defines how to set the spatial type when there is a domain match of the FME attribute.  Three values are possible: no_overwite, overwrite and if_null_overwrite.  no_overwite means that even if there is a match do not try to overwrite the spatial type.  overwite means that if there is a match, take the spatial type value associated in the CSV file (column name: spatial_type) and assign it (or create it if empty) to the corresponding FME attribute.  if_null_overwite as the same meaning as overwrite but only when the content of the spatial type is empty or missing.  The values overwrite and if_null_overwrite can only be used when the domain keyword value is LOOKUP_TABLE_FORMAT.

* The third keyword not_found defines how the custom transformer behaves when an FME attribute is not found in the domain of values.  Two values are possible: log and no_log. log means create a duplicate (clone) of the record and send it through the LOG_ERROR output port. no_log means do not log any error when the FME attribute is not found in the domain of values.

* The fourth keyword search type defines how to search the content of the FME attribute.  Two values are possible: equals or contains. equals means that the value of the FME attribute must be exactly the same.  contains means that one of the word the FME attribute must be in the domain values (usefull when we search for one word in a sentence).

You can define more than one FME attribute to search.  Do not duplicate the FME attribute name, the last one overwrite the others.

Documentation du code GEO_NONE_GEO_SELECTOR.py
##############################################

.. autosummary::
   GEO_NONE_GEO_SELECTOR.GeoNoneGeoSelector
 
.. automodule:: GEO_NONE_GEO_SELECTOR
   :members:
   :special-members: __init__
   :show-inheritance:
    
