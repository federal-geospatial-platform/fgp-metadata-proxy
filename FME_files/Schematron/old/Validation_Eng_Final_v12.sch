<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
    <sch:ns uri="http://www.isotc211.org/2005/gmd" prefix="gmd"/>
    <sch:ns uri="http://www.isotc211.org/2005/gco" prefix="gco"/>
    <sch:ns uri="http://www.w3.org/2001/XMLSchema-instance" prefix="xsi"/>
    <sch:ns uri="http://www.opengis.net/gml/3.2" prefix="gml"/>
    <sch:ns uri="http://www.w3.org/1999/xlink" prefix="xlink"/>

    <sch:pattern>
        <sch:rule context="gmd:MD_Metadata">
            <!-- Règle d'affaire #28, Licence du jeu de données - Test proper license used -->
            <sch:assert test="
                //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Government of Canada')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Open Government Licence - Canada (http://open.canada.ca/en/open-government-licence-canada)']
                or
                //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Government of Ontario')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Open Government Licence - Ontario (https://www.ontario.ca/page/open-government-licence-ontario)']
                or
                //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Government of Nova Scotia')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Open Government Licence - Nova Scotia (https://novascotia.ca/opendata/licence.asp)']
                or
                //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Government of Prince Edward Island')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Open Government Licence - Prince Edward Island (https://www.princeedwardisland.ca/en/information/finance/open-government-licence-prince-edward-island)']
                or
                //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Government of Newfoundland and Labrador')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Open Government Licence - Newfoundland and Labrador (https://opendata.gov.nl.ca/public/opendata/page/?page-id=licence)']
                or
                //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Government of Alberta')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Open Government Licence - Alberta (https://open.alberta.ca/licence)']
                or
				        //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Quebec Government and Municipalities')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Creative Commons 4.0 Attribution (CC-BY) licence – Quebec (https://www.donneesquebec.ca/fr/licence/)']
                or
                //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Government of British Columbia')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Open Government Licence - British Columbia (https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc)']
                or
                //*[gmd:contact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString[starts-with(text(),'Government of New Brunswick')]]
                [gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gco:CharacterString = 'Open Government Licence - New Brunswick (http://www.snb.ca/e/2000/data-E.html)  NOTE: Subject to change']
                ">
                Error in business rule #28, Dataset license | Erreur dans la règle d’affaire #28, Licence du jeu de données (Bad license used for rule #5 / mauvaise licence utilisée pour règle #5)
            </sch:assert>
            <sch:assert test="gmd:identificationInfo/gmd:MD_DataIdentification/gmd:resourceConstraints/gmd:MD_LegalConstraints/gmd:useLimitation/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']">Error in business rule #28, License name | Erreur dans la règle d’affaire #28, Nom de la license (Bilinguisme)</sch:assert>

            <!--  and //*[ = ('')] -->
            <!-- Règle d'affaire #1, Format du l'identifiant unique -->
            <sch:let name="UUIDpattern" value="'^[0-9a-fA-F]{8}-[0-9a-fA-f]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'"/>
            <sch:assert test="gmd:fileIdentifier/gco:CharacterString"> Error in business rule #1, Unique identifier format | Erreur dans la règle d’affaire #1, Format du l'identifiant unique (format) </sch:assert>
            <sch:assert test="matches(gmd:fileIdentifier/gco:CharacterString,$UUIDpattern)"> Error in business rule #1, Unique identifier format | Erreur dans la règle d’affaire #1, Format du l'identifiant unique (format)</sch:assert>
            <sch:assert test="not(gmd:fileIdentifier/gco:CharacterString) or not(matches(gmd:fileIdentifier/gco:CharacterString,$UUIDpattern) and matches(gmd:fileIdentifier/gco:CharacterString,'[A-F]'))"> Error in business rule #1, Unique identifier format | Erreur dans la règle d’affaire #1, Format du l'identifiant unique (format)</sch:assert>

            <!-- Règle d'affaire #2 , Langue de la métadonnée -->
            <sch:assert test="count(gmd:language) = 1">Error in business rule #2, Metadata language | Erreur dans la règle d’affaire #2, Langue de la métadonnée (cardinalité)</sch:assert>
            <sch:assert test="gmd:language/gco:CharacterString/text() = 'eng; CAN'">Error in business rule #2, Metadata language | Erreur dans la règle d’affaire #2, Langue de la métadonnée (valeur)</sch:assert>

            <!-- Règle d'affaire #3 , Encodage de la métadonnée -->
            <sch:assert test="gmd:characterSet/gmd:MD_CharacterSetCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_95' and @codeListValue='RI_458']/text()= 'utf8; utf8' ">Error in business rule #3, Metadata encoding | Erreur dans la règle d’affaire #3, Encodage de la métadonnée (valeur)</sch:assert>

            <!-- Règle d'affaire #4 , Porté hiérarchique du jeu de donnée -->
            <sch:assert test="gmd:hierarchyLevel/gmd:MD_ScopeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_108' and @codeListValue='RI_622'] and gmd:hierarchyLevel[gmd:MD_ScopeCode = ('dataset; jeuDonnées')]
                or gmd:hierarchyLevel/gmd:MD_ScopeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_108' and @codeListValue='RI_623'] and gmd:hierarchyLevel[gmd:MD_ScopeCode = ('series; série')]">
               Error in business rule #4, Hierarchical scope of the data set | Erreur dans la règle d’affaire #4, Porté hiérarchique du jeu de donnée (valeur)
            </sch:assert>

            <!-- Règle d'affaires #10 , Définition de la langue secofndaire de la métadonnée -->
            <sch:assert test="count(gmd:locale/gmd:PT_Locale) = 1">Error in business rule #10, Definition of the secondary language of the metadata | Erreur dans la règle d’affaire #10, Définition de la langue secondaire de la métadonnée </sch:assert>

            <!-- Règle d'affaire #14-1 , Référence spatiale-->
            <sch:assert test="(count(gmd:referenceSystemInfo)  >= 1
                and (gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_635']/text() = 'vector; vecteur'
                or gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_636']/text() = 'grid; grille'
                or gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_638']/text() = 'tin; tin'))
                or  (count(gmd:referenceSystemInfo) = 0
                or (gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_634']/text() = 'napMD_RepresentationTypeCode; pnaMD_CodeTypeReprésentation'
                or gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_637']/text() = 'textTable; texteTable'
                or gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_639']/text() = 'stereoModel; stéréomodèle'
                or gmd:identificationInfo/gmd:MD_DataIdentification/gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_640']/text() = 'video; vidéo'))
                ">Error in business rule #14-1, Spatial reference  | Erreur dans la règle d'affaire #14-1, Référence spatiale (cardinalité)</sch:assert>

       </sch:rule>

        <!-- Règle d'affaire #5 , Nom de l'organisation (cardinalite) -->
        <sch:rule context="gmd:CI_ResponsibleParty">
            <sch:assert test="count(gmd:organisationName) = 1">Error in business rule #5, Name of the organization | Erreur dans la règle d’affaire #5, Nom de l'organisation (cardinalité)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #5 , Nom de l'organisation (validate organisms)-->
        <sch:rule context="gmd:CI_ResponsibleParty/gmd:organisationName">
            <sch:assert test="//*[@xsi:type='gmd:PT_FreeText_PropertyType'] and gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']">Error in business rule #5, Name of the organization | Erreur dans la règle d’affaire #5, Nom de l'organisation (Bilinguisme)</sch:assert>
            <sch:assert test="gco:CharacterString[starts-with(text(),'Government of Canada; Accessibility Standards Canada')
                or starts-with(text(),'Government of Canada; Administrative Tribunals Support Service of Canada')
                or starts-with(text(),'Government of Canada; Agriculture and Agri-Food Canada')
                or starts-with(text(),'Government of Canada; Atlantic Pilotage Authority Canada')
                or starts-with(text(),'Government of Canada; Business Development Bank of Canada')
                or starts-with(text(),'Government of Canada; Canada Border Services Agency')
                or starts-with(text(),'Government of Canada; Canada Deposit Insurance Corporation')
                or starts-with(text(),'Government of Canada; Canada Development Investment Corporation')
                or starts-with(text(),'Government of Canada; Canada Economic Development for Quebec Regions')
                or starts-with(text(),'Government of Canada; Canada Employment Insurance Commission')
                or starts-with(text(),'Government of Canada; Canada Energy Regulator')
                or starts-with(text(),'Government of Canada; Canada Mortgage and Housing Corporation')
                or starts-with(text(),'Government of Canada; Canada Post')
                or starts-with(text(),'Government of Canada; Canada Science and Technology Museum')
                or starts-with(text(),'Government of Canada; Canadian Air Transport Security Authority')
                or starts-with(text(),'Government of Canada; Canadian Commercial Corporation')
                or starts-with(text(),'Government of Canada; Canadian Dairy Commission')
                or starts-with(text(),'Government of Canada; Canadian Food Inspection Agency')
                or starts-with(text(),'Government of Canada; Canadian Heritage')
                or starts-with(text(),'Government of Canada; Canadian Museum for Human Rights')
                or starts-with(text(),'Government of Canada; Canadian Museum of History')
                or starts-with(text(),'Government of Canada; Canadian Museum of Immigration at Pier 21')
                or starts-with(text(),'Government of Canada; Canadian Museum of Nature')
                or starts-with(text(),'Government of Canada; Canadian Northern Economic Development Agency')
                or starts-with(text(),'Government of Canada; Canadian Nuclear Safety Commission')
                or starts-with(text(),'Government of Canada; Canadian Radio-television and Telecommunications Commission')
                or starts-with(text(),'Government of Canada; Canadian Security Intelligence Service')
                or starts-with(text(),'Government of Canada; Canadian Space Agency')
                or starts-with(text(),'Government of Canada; Canadian Transportation Agency')
                or starts-with(text(),'Government of Canada; Civilian Review and Complaints Commission for the RCMP')
                or starts-with(text(),'Government of Canada; Communications Security Establishment Canada')
                or starts-with(text(),'Government of Canada; Copyright Board Canada')
                or starts-with(text(),'Government of Canada; Correctional Service Canada')
                or starts-with(text(),'Government of Canada; Courts Administration Service')
                or starts-with(text(),'Government of Canada; Crown-Indigenous Relations and Northern Affairs Canada')
                or starts-with(text(),'Government of Canada; Defence Construction Canada')
                or starts-with(text(),'Government of Canada; Department of Finance Canada')
                or starts-with(text(),'Government of Canada; Department of Justice Canada')
                or starts-with(text(),'Government of Canada; Destination Canada')
                or starts-with(text(),'Government of Canada; Employment and Social Development Canada')
                or starts-with(text(),'Government of Canada; Environment and Climate Change Canada')
                or starts-with(text(),'Government of Canada; Export Development Canada')
                or starts-with(text(),'Government of Canada; Farm Credit Canada')
                or starts-with(text(),'Government of Canada; Farm Products Council of Canada')
                or starts-with(text(),'Government of Canada; Federal Bridge Corporation')
                or starts-with(text(),'Government of Canada; Federal Economic Development Agency for Southern Ontario')
                or starts-with(text(),'Government of Canada; Financial Consumer Agency of Canada')
                or starts-with(text(),'Government of Canada; Financial Transactions and Reports Analysis Centre of Canada')
                or starts-with(text(),'Government of Canada; Fisheries and Oceans Canada')
                or starts-with(text(),'Government of Canada; Freshwater Fish Marketing Corporation')
                or starts-with(text(),'Government of Canada; Global Affairs Canada')
                or starts-with(text(),'Government of Canada; Government of Canada')
                or starts-with(text(),'Government of Canada; Great Lakes Pilotage Authority Canada')
                or starts-with(text(),'Government of Canada; Health Canada')
                or starts-with(text(),'Government of Canada; Immigration and Refugee Board of Canada')
                or starts-with(text(),'Government of Canada; Immigration, Refugees and Citizenship Canada')
                or starts-with(text(),'Government of Canada; Impact Assessment Agency of Canada')
                or starts-with(text(),'Government of Canada; Indigenous Services Canada')
                or starts-with(text(),'Government of Canada; Infrastructure Canada')
                or starts-with(text(),'Government of Canada; Innovation, Science and Economic Development Canada')
                or starts-with(text(),'Government of Canada; Laurentian Pilotage Authority Canada')
                or starts-with(text(),'Government of Canada; Law Commission of Canada')
                or starts-with(text(),'Government of Canada; Library and Archives Canada')
                or starts-with(text(),'Government of Canada; Military Grievances External Review Committee')
                or starts-with(text(),'Government of Canada; Military Police Complaints Commission of Canada')
                or starts-with(text(),'Government of Canada; National Capital Commission')
                or starts-with(text(),'Government of Canada; National Defence')
                or starts-with(text(),'Government of Canada; National Gallery of Canada')
                or starts-with(text(),'Government of Canada; National Research Council Canada')
                or starts-with(text(),'Government of Canada; Natural Resources Canada')
                or starts-with(text(),'Government of Canada; Natural Sciences and Engineering Research Council of Canada')
                or starts-with(text(),'Government of Canada; Northern Pipeline Agency Canada')
                or starts-with(text(),'Government of Canada; Office of the Auditor General of Canada')
                or starts-with(text(),'Government of Canada; Office of the Commissioner for Federal Judicial Affairs Canada')
                or starts-with(text(),'Government of Canada; Office of the Commissioner of Lobbying of Canada')
                or starts-with(text(),'Government of Canada; Office of the Public Sector Integrity Commissioner of Canada')
                or starts-with(text(),'Government of Canada; Office of the Secretary to the Governor General')
                or starts-with(text(),'Government of Canada; Office of the Superintendent of Financial Institutions Canada')
                or starts-with(text(),'Government of Canada; Pacific Pilotage Authority Canada')
                or starts-with(text(),'Government of Canada; Parks Canada')
                or starts-with(text(),'Government of Canada; Parole Board of Canada')
                or starts-with(text(),'Government of Canada; Patented Medicine Prices Review Board Canada')
                or starts-with(text(),'Government of Canada; Polar Knowledge Canada')
                or starts-with(text(),'Government of Canada; Privy Council Office')
                or starts-with(text(),'Government of Canada; Public Health Agency of Canada')
                or starts-with(text(),'Government of Canada; Public Prosecution Service of Canada')
                or starts-with(text(),'Government of Canada; Public Safety Canada')
                or starts-with(text(),'Government of Canada; Public Service Commission of Canada')
                or starts-with(text(),'Government of Canada; Public Services and Procurement Canada')
                or starts-with(text(),'Government of Canada; RCMP External Review Committee')
                or starts-with(text(),'Government of Canada; Secretariat of the National Security and Intelligence Committee of Parliamentarians')
                or starts-with(text(),'Government of Canada; Shared Services Canada')
                or starts-with(text(),'Government of Canada; Social Sciences and Humanities Research Council of Canada')
                or starts-with(text(),'Government of Canada; Statistics Canada')
                or starts-with(text(),'Government of Canada; The Correctional Investigator Canada')
                or starts-with(text(),'Government of Canada; The National Battlefields Commission')
                or starts-with(text(),'Government of Canada; Transport Canada')
                or starts-with(text(),'Government of Canada; Transportation Safety Board of Canada')
                or starts-with(text(),'Government of Canada; Treasury Board of Canada Secretariat')
                or starts-with(text(),'Government of Canada; Veterans Affairs Canada')
                or starts-with(text(),'Government of Canada; Western Economic Diversification Canada')
                or starts-with(text(),'Government of Canada; Windsor-Detroit Bridge Authority')
                or starts-with(text(),'Government of Canada; Women and Gender Equality Canada')
                or starts-with(text(),'Government of Ontario; Government of Ontario')
                or starts-with(text(),'Government of Nova Scotia; Government of Nova Scotia')
                or starts-with(text(),'Government of Prince Edward Island; Government of Prince Edward Island')
                or starts-with(text(),'Government of Newfoundland and Labrador ; Government of Newfoundland and Labrador')
                or starts-with(text(),'Government of Alberta; Government of Alberta')
                or starts-with(text(),'Government of British Columbia; Government of British Columbia')
                or starts-with(text(),'Government of New Brunswick; Government of New Brunswick')
				        or starts-with(text(),'Quebec Government and Municipalities; Quebec Government and Municipalities')

                ]">Error in business rule #5, Name of the organization | Erreur dans la règle d’affaire #5, Nom de l'organisation (valeur)</sch:assert>

            <sch:assert test="(
                count(gco:CharacterString[starts-with(text(),'Government of Canada; Administrative Tribunals Support Service of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Service canadien d''appui aux tribunaux administratifs')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Agriculture and Agri-Food Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agriculture et Agroalimentaire Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Accessibility Standards Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Normes d''accessibilité Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Atlantic Pilotage Authority Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Administration de pilotage de l''Atlantique Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Business Development Bank of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Banque de développement du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Border Services Agency')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agence des services frontaliers du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Deposit Insurance Corporation')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Société d''assurance-dépôts du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Development Investment Corporation')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Corporation de développement des investissements du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Economic Development for Quebec Regions')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Développement économique Canada pour les régions du Québec')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Employment Insurance Commission')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission de l''assurance-emploi du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Energy Regulator')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Régie de l''énergie du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Mortgage and Housing Corporation')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Société canadienne d''hypothèques et de logement')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Post')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Postes Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canada Science and Technology Museum')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Musée des sciences et de la technologie du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Air Transport Security Authority')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Administration canadienne de la sûreté du transport aérien')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Commercial Corporation')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Corporation commerciale canadienne')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Dairy Commission')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission canadienne du lait')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Food Inspection Agency')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agence canadienne d''inspection des aliments')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Heritage')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Patrimoine canadien')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Museum for Human Rights')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Musée canadien pour les droits de la personne')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Museum of History')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Musée canadien de l''histoire')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Museum of Immigration at Pier 21')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Musée canadien de l''immigration du Quai 21')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Museum of Nature')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Musée canadien de la nature')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Northern Economic Development Agency')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agence canadienne de développement économique du Nord')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Nuclear Safety Commission')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission canadienne de sûreté nucléaire')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Radio-television and Telecommunications Commission')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Conseil de la radiodiffusion et des télécommunications canadiennes')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Security Intelligence Service')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Service canadien du renseignement de sécurité')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Space Agency')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agence spatiale canadienne')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Canadian Transportation Agency')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Office des transports du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Civilian Review and Complaints Commission for the RCMP')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission civile d’examen et de traitement des plaintes relatives à la GRC')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Copyright Board Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission du droit d''auteur Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Correctional Service Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Service correctionnel Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Courts Administration Service')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Service administratif des tribunaux judiciaires')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Crown-Indigenous Relations and Northern Affairs Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Relations Couronne-Autochtones et Affaires du Nord Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Defence Construction Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Construction de Défense Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Department of Finance Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Ministère des Finances Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Department of Justice Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Ministère de la Justice Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Destination Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Destination Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Employment and Social Development Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Emploi et Développement social Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Environment and Climate Change Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Environnement et Changement climatique Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Export Development Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Exportation et développement Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Farm Credit Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Financement agricole Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Farm Products Council of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Conseil des produits agricoles du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Federal Bridge Corporation')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Société des ponts fédéraux')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Federal Economic Development Agency for Southern Ontario')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agence fédérale de développement économique pour le Sud de l''Ontario')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Financial Consumer Agency of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agence de la consommation en matière financière du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Financial Transactions and Reports Analysis Centre of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Centre d''analyse des opérations et déclarations financières du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Fisheries and Oceans Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Pêches et Océans Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Freshwater Fish Marketing Corporation')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Office de commercialisation du poisson d''eau douce')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Global Affairs Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Affaires mondiales Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Government of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Gouvernement du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Great Lakes Pilotage Authority Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Administration de pilotage des Grands Lacs Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Health Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Santé Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Immigration and Refugee Board of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission de l''immigration et du statut de réfugié du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Immigration, Refugees and Citizenship Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Immigration, Réfugiés et Citoyenneté Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Impact Assessment Agency of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agence d''évaluation d''impact du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Indigenous Services Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Services aux Autochtones Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Infrastructure Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Infrastructure Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Innovation, Science and Economic Development Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Innovation, Sciences et Développement économique Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Laurentian Pilotage Authority Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Administration de pilotage des Laurentides Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Law Commission of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission du droit du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Library and Archives Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Bibliothèque et Archives Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Military Grievances External Review Committee')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Comité externe d''examen des griefs militaires')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Military Police Complaints Commission of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission d''examen des plaintes concernant la police militaire du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; National Capital Commission')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission de la capitale nationale')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; National Defence')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Défense nationale')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; National Gallery of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Musée des beaux-arts du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; National Research Council Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Conseil national de recherches Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Natural Resources Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Ressources naturelles Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Natural Sciences and Engineering Research Council of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Conseil de recherches en sciences naturelles et en génie du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Northern Pipeline Agency Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Administration du pipe-line du Nord Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Office of the Auditor General of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Bureau du vérificateur général du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Office of the Commissioner for Federal Judicial Affairs Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commissariat à la magistrature fédérale Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Office of the Commissioner of Lobbying of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commissariat au lobbying du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Office of the Public Sector Integrity Commissioner of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commissariat à l''intégrité du secteur public du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Office of the Secretary to the Governor General')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Bureau du secrétaire du gouverneur général')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Office of the Superintendent of Financial Institutions Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Bureau du surintendant des institutions financières Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Pacific Pilotage Authority Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Administration de pilotage du Pacifique Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Parks Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Parcs Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Parole Board of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission des libérations conditionnelles du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Patented Medicine Prices Review Board Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Conseil d''examen du prix des médicaments brevetés Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Polar Knowledge Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Savoir polaire Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Privy Council Office')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Bureau du Conseil privé')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Public Health Agency of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Agence de la santé publique du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Public Prosecution Service of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Service des poursuites pénales du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Public Safety Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Sécurité publique Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Public Service Commission of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission de la fonction publique du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Public Services and Procurement Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Services publics et Approvisionnement Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; RCMP External Review Committee')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Comité externe d''examen de la GRC')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Secretariat of the National Security and Intelligence Committee of Parliamentarians')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Secrétariat du Comité des parlementaires sur la sécurité nationale et le renseignement')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Shared Services Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Services partagés Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Social Sciences and Humanities Research Council of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Conseil de recherches en sciences humaines du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Statistics Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Statistique Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; The Correctional Investigator Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; L''Enquêteur correctionnel Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; The National Battlefields Commission')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Commission des champs de bataille nationaux')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Transport Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Transports Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Transportation Safety Board of Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Bureau de la sécurité des transports du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Treasury Board of Canada Secretariat')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Secrétariat du Conseil du Trésor du Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Veterans Affairs Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Anciens Combattants Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Western Economic Diversification Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Diversification de l''économie de l''Ouest Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Windsor-Detroit Bridge Authority')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Autorité du pont Windsor-Détroit')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Canada; Women and Gender Equality Canada')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Canada; Femmes et Égalité des genres Canada')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Ontario; Government of Ontario')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement de l''Ontario; Gouvernement de l''Ontario')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Nova Scotia; Government of Nova Scotia')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement de la Nouvelle-Écosse; Gouvernement de la Nouvelle-Écosse')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Prince Edward Island; Government of Prince Edward Island')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement de l''Île-du-Prince-Édouard; Gouvernement de l''Île-du-Prince-Édouard')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Newfoundland and Labrador; Government of Newfoundland and Labrador')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement de Terre-Neuve-et-Labrador; Gouvernement de Terre-Neuve-et-Labrador')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of Alberta; Government of Alberta')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement de l''Alberta; Gouvernement de l''Alberta')]) = 1)

				        or (count(gco:CharacterString[starts-with(text(),'Quebec Government and Municipalities; Quebec Government and Municipalities')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement et municipalités du Québec; Gouvernement et municipalités du Québec')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of New Brunswick; Government of New Brunswick;')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement du Nouveau-Brunswick; Gouvernement du Nouveau-Brunswick')]) = 1)

                or (count(gco:CharacterString[starts-with(text(),'Government of British Columbia; Government of British Columbia')]) = 1
                and count(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[starts-with(text(),'Gouvernement de la Colombie-Britannique; Gouvernement de la Colombie-Britannique')]) = 1)">

                Error in business rule #5, Name of the organization | Erreur dans la règle d’affaire #5, Nom de l'organisation (Correspondance/ valeur)
            </sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #6 , Adresse courriel du contact -->
        <sch:rule context="gmd:electronicMailAddress">

            <sch:let name="EmailPattern" value="'^[a-zA-Z0-9~#$^*()_+=\{}|\\,.?:-]*[@][a-zA-Z0-9_.-]*[.][a-zA-Z]*$'"/>
            <sch:assert test="matches(gco:CharacterString,$EmailPattern)"> Error in business rule #6, Contact email address | Erreur dans la règle d’affaire #6, Adresse courriel du contact (format)</sch:assert>
            <sch:assert test="matches(gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString,$EmailPattern)">Error in business rule #6, Contact email address | Erreur dans la règle d’affaire #6, Adresse courriel du contact (format)</sch:assert>
            <sch:assert test="//*[@xsi:type='gmd:PT_FreeText_PropertyType'] and gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']">Error in business rule #6, Contact email address | Erreur dans la règle d’affaire #6, Adresse courriel du contact (Bilinguisme)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #6 ,Cardinalité Adresse courriel du contact -->
        <sch:rule context="gmd:contactInfo">
            <sch:assert test="count(gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress) = 1">Error in business rule #6, Contact email address | Erreur dans la règle d’affaire #6, Adresse courriel du contact (cardinalité)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #7, Rôle du contact -->
        <sch:rule context="gmd:role">
            <sch:assert test="
                gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_407'] and gmd:CI_RoleCode/text()= 'napCI_RoleCode; pnaCI_CodeRôle'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_408'] and gmd:CI_RoleCode/text()= 'resourceProvider; fournisseurRessource'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_409'] and gmd:CI_RoleCode/text()= 'custodian; conservateur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_410'] and gmd:CI_RoleCode/text()= 'owner; propriétaire'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_411'] and gmd:CI_RoleCode/text()= 'user; utilisateur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_412'] and gmd:CI_RoleCode/text()= 'distributor; distributeur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_413'] and gmd:CI_RoleCode/text()= 'originator; créateur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_414'] and gmd:CI_RoleCode/text()= 'pointOfContact; contact'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_415'] and gmd:CI_RoleCode/text()= 'principalInvestigator; chercheurPrincipal'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_416'] and gmd:CI_RoleCode/text()= 'processor; traiteur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_417'] and gmd:CI_RoleCode/text()= 'publisher; éditeur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_418'] and gmd:CI_RoleCode/text()= 'author; auteur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_419'] and gmd:CI_RoleCode/text()= 'collaborator; collaborateur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_420'] and gmd:CI_RoleCode/text()= 'editor; réviseur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_421'] and gmd:CI_RoleCode/text()= 'mediator; médiateur'
                or gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90'and @codeListValue='RI_422'] and gmd:CI_RoleCode/text()= 'rightsHolder; détenteurDroits'
                ">Error in business rule #7, Role of the contact | Erreur dans la règle d’affaire #7, Rôle du contact (valeur)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaires #8, Format de date -->
        <sch:rule context="gmd:CI_Date">
            <sch:let name="DatePattern1" value="'^[0-9]{4}[-][0-9]{2}[-][0-9]{2}$'"/>
            <sch:let name="DatePattern2" value="'^[0-9]{4}[-][0-9]{2}$'"/>
            <sch:let name="DatePattern3" value="'^[0-9]{4}$'"/>
            <sch:assert test="matches(gmd:date/gco:Date,$DatePattern1) or matches(gmd:date/gco:Date,$DatePattern2) or matches(gmd:date/gco:Date,$DatePattern3)">Error in business rule #8, Date format | Erreur dans la règle d’affaire #8, Format de date</sch:assert>

            <!-- Règle d'affaires #27 , Type de la date -->
            <sch:assert test="
                     gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_365'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'napCI_DateTypeCode; pnaCI_CodeTypeDate'
                     or gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_366'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'creation; création'
                     or gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_367'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'publication; publication'
                     or gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_368'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'revision; révision'
                     or gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_369'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'notAvailable; nonDisponible'
                     or gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_370'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'inForce; enVigueur'
                     or gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_371'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'adopted; adoptée'
                     or gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_372'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'deprecated; réprouvée'
                     or gmd:dateType/gmd:CI_DateTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87' and @codeListValue='RI_373'] and gmd:dateType/gmd:CI_DateTypeCode/text() = 'superseded; remplacée'
                     ">Error in business rule #27, Date type | Erreur dans la règle d’affaire #27, Type de la date  (valeur) </sch:assert>
        </sch:rule>

        <!-- Règle d'affaires #9, Standard de métadonnée -->
        <sch:rule context="gmd:metadataStandardName">
            <sch:assert test="//*[@xsi:type='gmd:PT_FreeText_PropertyType'] and gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']">Error in business rule #9, Metadata standard | Erreur dans la règle d’affaire #9, Standard de métadonnée </sch:assert>
        </sch:rule>

        <sch:rule context="gmd:locale">
            <!-- Règle d'affaires #10 , Définition de la langue secofndaire de la métadonnée -->
            <sch:assert test="gmd:PT_Locale[@id='fra']">Error in business rule #10, Definition of the secondary language of the metadata | Erreur dans la règle d’affaire #10, Définition de la langue secondaire de la métadonnée  (valeur)</sch:assert>

          <!-- Règle d'affaires #11 , Code de langue secondaire -->
            <sch:assert test="count(gmd:PT_Locale/gmd:languageCode) = 1">Error in business rule #11, Secondary language code | Erreur dans la règle d’affaire #11, Code de langue secondaire (cardinalité)</sch:assert>
            <sch:assert test="gmd:PT_Locale/gmd:languageCode/gmd:LanguageCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_116' and @codeListValue='fra']/text()='French; Français'">Error in business rule #11, Secondary language code | Erreur dans la règle d’affaire #11, Code de langue secondaire (valeur)</sch:assert>

        <!-- Règle d'affaires #12 , Pays de la langue secondaire -->
            <sch:assert test="count(gmd:PT_Locale/gmd:country) = 1">Error in business rule #12, Secondary language country | Erreur dans la règle d’affaire #12, Pays de la langue secondaire (cardinalité)</sch:assert>
            <sch:assert test="//*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_117' and @codeListValue='CAN']/text()='Canada; Canada'">Error in business rule #12, Secondary language country | Erreur dans la règle d’affaire #12, Pays de la langue secondaire (valuer)</sch:assert>

        <!-- Voir règle d'affaires #13 , Encodage de la langue secondaire -->
            <sch:assert test="count(gmd:PT_Locale/gmd:characterEncoding) = 1">Error in business rule #13, Secondary language encoding | Erreur dans la règle d’affaire #13, Encodage de la langue secondaire  (cardinalité)</sch:assert>
            <sch:assert test="gmd:PT_Locale/gmd:characterEncoding/gmd:MD_CharacterSetCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_95' and @codeListValue='RI_458']/text()= 'utf8; utf8'">Error in business rule #13, Secondary language encoding | Erreur dans la règle d’affaire #13, Encodage de la langue secondaire  (valeur)</sch:assert>
        </sch:rule>

        <sch:rule context="gmd:referenceSystemInfo">
            <!-- Règle d'affaire #14-2 , Référence spatiale-->
            <sch:let name="SpacialPattern1" value="'^[E][P][S][G][:][0-9]*$'"></sch:let>
            <sch:let name="SpacialPattern2" value="'^[S][R][-][O][R][G][:][0-9]*$'"></sch:let>
            <sch:let name="SpacialPattern3" value="'unknown'"></sch:let>

            <sch:assert test="matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern1)
                or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern2)
                or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern3)">Error in business rule #14-2, Spatial reference system code | Erreur dans la règle d’affaire #14-2, Code du système de référence spatiale (format) </sch:assert>

            <!-- Règle d'affaires #15 , Codespace du système de référence spatiale-->
            <!--<sch:assert test="matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern1) and gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString = 'http://www.epsg-registry.org' and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace) = 1
                or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern2) and gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString = 'http://www.spatialreference.org' and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace) = 1
                or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern3) and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace) = 0 ">Error in business rule #15, Codespace of the spatial reference system | Erreur dans la règle d’affaire #15, Codespace du système de référence spatiale
            </sch:assert>-->
			<sch:assert test="matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern1) and gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString = 'http://www.epsg-registry.org' and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace) = 1
				or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern1) and gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString = 'EPSG' and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace) = 1
                or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern2) and gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString = 'http://www.spatialreference.org' and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace) = 1
				or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern3) and gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace/gco:CharacterString = 'unknown' and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace) = 1
                or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern3) and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:codeSpace) = 1 ">Error in business rule #15, Codespace of the spatial reference system | Erreur dans la règle d’affaire #15, Codespace du système de référence spatiale
            </sch:assert>

            <!--  Règle d'affaires #16 , Version du système de référence spatiale -->
            <!--<sch:assert test="(matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern1) and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 1 and not(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version/gco:CharacterString = ''))
                or (matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern2) and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 1 or count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 1 and not(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version/gco:CharacterString = ''))
                or (matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern3) and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 0 and not(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version/gco:CharacterString = ''))">Error in business rule #16, Version of the spatial reference system | Erreur dans la règle d’affaire #16, Version du système de référence spatiale </sch:assert>
        </sch:rule>-->
			<sch:assert test="(matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern1) and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 1 and not(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version/gco:CharacterString = ''))
                or (matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern2) and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 1 or count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 1 and not(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version/gco:CharacterString = ''))
				or matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern3) and gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version/gco:CharacterString = 'unknown' and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 1
                or (matches(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/gco:CharacterString,$SpacialPattern3) and count(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:version) = 1)">Error in business rule #16, Version of the spatial reference system | Erreur dans la règle d’affaire #16, Version du système de référence spatiale </sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #18, Résumé du jeu de donnée -->
        <sch:rule context="gmd:abstract">
            <sch:assert test="//*[@xsi:type='gmd:PT_FreeText_PropertyType'] and gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']">Error in business rule #18, Summary of the dataset | Erreur dans la règle d’affaire #18, Résumé du jeu de donnée</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #19, Statut du jeu donnée -->
        <sch:rule context="gmd:status">
            <sch:assert test="
                //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_592' ] and gmd:MD_ProgressCode/text() = 'napMD_ProgressCode; pnaMD_CodeÉtatAvancement'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_593' ] and gmd:MD_ProgressCode/text() = 'completed; complété'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_594' ] and gmd:MD_ProgressCode/text() = 'historicalArchive; archiveHistorique'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_595' ] and gmd:MD_ProgressCode/text() = 'obsolete; périmé'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_596' ] and gmd:MD_ProgressCode/text() = 'onGoing; enContinue'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_597' ] and gmd:MD_ProgressCode/text() = 'planned; planifié'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_598' ] and gmd:MD_ProgressCode/text() = 'required; requis'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_599' ] and gmd:MD_ProgressCode/text() = 'underDevelopment; enProduction'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106' and @codeListValue='RI_600' ] and gmd:MD_ProgressCode/text() = 'proposed; proposé'
                ">Error in business rule #19, Dataset status  | Erreur dans la règle d’affaire #19, Statut du jeu donnée (valeur) </sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #20, Maintenance du jeu donnée -->
        <sch:rule context="gmd:resourceMaintenance">
            <sch:assert test="
                   //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_531'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'napMD_MaintenanceFrequencyCode; pnaMD_CodeFréquenceMiseÀJour'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_532'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'continual; continue'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_533'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'daily; quotidien'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_534'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'weekly; hebdomadaire'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_535'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'fortnightly; quinzomadaire'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_536'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'monthly; mensuel'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_537'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'quarterly; trimestriel'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_538'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'biannually; semestriel'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_539'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'annually; annuel'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_540'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'asNeeded; auBesoin'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_541'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'irregular; irrégulier'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_542'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'notPlanned; nonPlanifié'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_543'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'unknown; inconnu'
                or //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102' and @codeListValue='RI_544'] and //*/gmd:MD_MaintenanceFrequencyCode/text()= 'semimonthly; bimensuel'
                ">Error in business rule #20, Dataset maintenance  | Erreur dans la règle d’affaire #20, Maintenance du jeu donnée (valeur)</sch:assert>
            <sch:assert test="count(//*/gmd:MD_MaintenanceFrequencyCode) = 1 "> Error in business rule #20, Dataset maintenance  | Erreur dans la règle d’affaire #20, Maintenance du jeu donnée (cardinalité)</sch:assert>
        </sch:rule>

        <sch:rule context="gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword">
            <!-- Règle d'affaire #21, Mots-clés libres -->
            <sch:assert test="count(../gmd:thesaurusName) > 0
                or (count(../gmd:thesaurusName) = 0
                and @xsi:type='gmd:PT_FreeText_PropertyType'
                and gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra'] != '')">
                Error in business rule #21, Free Keywords | Erreur dans la règle d’affaire #21, Mots-clés libres (bilinguisme)
            </sch:assert>

            <!-- Règle d'affaire #23, Mots-clés du thesaursus (builingisme - valeur) -->
            <sch:assert test="count(../gmd:thesaurusName) = 0
                or (count(../gmd:thesaurusName) > 0
                and @xsi:type='gmd:PT_FreeText_PropertyType'
                and ((document('http://canada.multites.net/tsb/EAEAD1E6-7DD2-4997-BE7F-40BFB1CBE8A2/TSB20160704.xml')//CONCEPT/DESCRIPTOR = gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']
                and document('http://canada.multites.net/tsb/EAEAD1E6-7DD2-4997-BE7F-40BFB1CBE8A2/TSB20160704.xml')//CONCEPT/Anglais = gco:CharacterString)
                or (document('http://canada.multites.net/tsb/EAEAD1E6-7DD2-4997-BE7F-40BFB1CBE8A2/TSB20160704.xml')//CONCEPT/DESCRIPTOR = gco:CharacterString
                and document('http://canada.multites.net/tsb/EAEAD1E6-7DD2-4997-BE7F-40BFB1CBE8A2/TSB20160704.xml')//CONCEPT/Anglais = gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#eng'])))">
                Error in business rule #23, thesaursus keywords | Erreur dans la règle d’affaire #23, Mots-clés du thesaursus (builingisme - valeur)
            </sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #22, Type de mots-clés  -->
        <sch:rule context="gmd:descriptiveKeywords/gmd:MD_Keywords">
            <sch:assert test="count(gmd:type) = 1
                and count(gmd:type/gmd:MD_KeywordTypeCode) = 1
                and gmd:type/gmd:MD_KeywordTypeCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_101' and @codeListValue='RI_528']/text() = 'theme; thème'">
                Error in business rule #22, Type of keywords | Erreur dans la règle d’affaire #22, Type de mots-clés (valeur)
            </sch:assert>

            <!-- Règle d'affaire #24, Définition du Thesaurus Développée par CGI mais trop restrictive. Remplacée par autre règle d'affaire #24 développée par Nicolas Gariépy
            <sch:assert test="count(gmd:thesaurusName) = 1">
                Error in business rule #24, Thesaurus definition | Erreur dans la règle d’affaire #24, Définition du Thesaurus (cardinalité thesaurusName)
            </sch:assert> -->

            <!-- Règle d'affaire #23, Mots-clés du thesaursus (cardinalité) -->
            <sch:assert test="count(gmd:thesaurusName) = 0 or (count(gmd:thesaurusName) > 0 and count(gmd:keyword) > 0)">
                Error in business rule #23, thesaursus keywords | Erreur dans la règle d’affaire #23, Mots-clés du thesaursus (cardinalité)
            </sch:assert>
        </sch:rule>

        <!--Règle d'affaire #24 , Au  moins un thesaurus de défini . Règcle produite par Nicolas -->

        <sch:rule context="gmd:MD_Metadata/gmd:identificationInfo/gmd:MD_DataIdentification">
            <sch:assert test="count(gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:thesaurusName) >=1">
                Error in business rule #24, Thesaurus definition | Erreur dans la règle d’affaire #24, Définition du Thesaurus (cardinalité thesaurusName)
            </sch:assert>
        </sch:rule>


        <!-- Regles d'affaire #24, #25, #26 -->
        <sch:rule context="gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:thesaurusName">
            <sch:assert test="count(gmd:CI_Citation/gmd:title) = 1 and gmd:CI_Citation/gmd:title[gco:CharacterString = ('Government of Canada Core Subject Thesaurus')] ">
                Error in business rule #24, Thesaurus definition | Erreur dans la règle d’affaire #24, Définition du Thesaurus (cardinalité TITRE)
            </sch:assert>
            <sch:assert test="gmd:CI_Citation/gmd:title[@xsi:type='gmd:PT_FreeText_PropertyType']
                and count(gmd:CI_Citation/gmd:title/gmd:PT_FreeText/gmd:textGroup[gmd:LocalisedCharacterString[@locale='#fra'] = 'Thésaurus des sujets de base du gouvernement du Canada']) = 1">
                Error in business rule #24, Thesaurus definition | Erreur dans la règle d’affaire #24, Définition du Thesaurus (cardinalité TITLE LOCALE FRA)
            </sch:assert>

            <sch:assert test="count(gmd:CI_Citation/gmd:date[descendant::gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/text() = 'creation; création' and  gmd:CI_Date/gmd:date/gco:Date/text() = '2004']) = 1">
                Error in business rule #26, Date Information | Erreur dans la règle d’affaire #26, Information de date (DATE DE CRÉATION doit être 2004)
            </sch:assert>
            <sch:assert test="count(gmd:CI_Citation/gmd:date[descendant::gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/text() = 'publication; publication' and gmd:CI_Date/gmd:date/gco:Date/text() = '2016-04-21']) = 1">
                Error in business rule #26, Date Information | Erreur dans la règle d’affaire #26, Information de date (DATE DE PUBLICATION doit être 2016-04-21)
            </sch:assert>

            <sch:assert test="count(gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName) = 1
                and count(gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName[@xsi:type='gmd:PT_FreeText_PropertyType']) = 1
                and count(gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString) = 1
                and gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName[@xsi:type='gmd:PT_FreeText_PropertyType']/gco:CharacterString = 'Government of Canada; Library and Archives Canada'">
                Error in business rule #24, Thesaurus definition | Erreur dans la règle d’affaire #24, Définition du Thesaurus (cardinalité NOM ORGANISATION)
            </sch:assert>

            <sch:assert test="count(gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName[@xsi:type='gmd:PT_FreeText_PropertyType']/gmd:PT_FreeText/gmd:textGroup[gmd:LocalisedCharacterString[@locale='#fra']]) = 1
                and gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:organisationName[@xsi:type='gmd:PT_FreeText_PropertyType']/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra'] = 'Gouvernement du Canada; Bibliothèque et Archives Canada'">
                Error in business rule #24, Thesaurus definition | Erreur dans la règle d’affaire #24, Définition du Thesaurus (cardinalité NOM ORGANISATION LOCALE FRA)
            </sch:assert>

            <sch:assert test="count(gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:role) = 1
                and count(gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode) = 1
                and count(gmd:CI_Citation/gmd:citedResponsibleParty/gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90' and @codeListValue='RI_409']) = 1 ">
                Error in business rule #24, Thesaurus definition | Erreur dans la règle d’affaire #24, Définition du Thesaurus (cardinalité ROLE)
            </sch:assert>

            <!-- Voir règle d'affaire #25, Titre du thesaurus -->
            <sch:assert test="count(gmd:CI_Citation/gmd:title) = 1 and gmd:CI_Citation/gmd:title[gco:CharacterString = ('Government of Canada Core Subject Thesaurus')] ">
                Error in business rule #25, Thesaurus title | Erreur dans la règle d’affaire #25, Titre du thesaurus (cardinalité)
            </sch:assert>
            <sch:assert test="gmd:CI_Citation/gmd:title[@xsi:type='gmd:PT_FreeText_PropertyType']
                and count(gmd:CI_Citation/gmd:title/gmd:PT_FreeText/gmd:textGroup[gmd:LocalisedCharacterString[@locale='#fra'] = 'Thésaurus des sujets de base du gouvernement du Canada']) = 1">
                Error in business rule #25, Thesaurus title | Erreur dans la règle d’affaire #25, Titre du thesaurus (Bilinguisme)
            </sch:assert>

            <!-- Règle d'affaire #26, Information de date -->
            <sch:assert test="count(gmd:CI_Citation/gmd:date[descendant::gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/text() = 'creation; création'  and gmd:CI_Date/gmd:date/gco:Date != '']) = 1
                and count(gmd:CI_Citation/gmd:date[descendant::gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/text() = 'publication; publication'  and gmd:CI_Date/gmd:date/gco:Date != '']) = 1">
                Error in business rule #26, Date information | Erreur dans la règle d’affaire #26, Information de date  (cardinalité)
            </sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #28 #29 #30 cardinalité -->
        <sch:rule context="gmd:resourceConstraints">
            <sch:assert test="count(gmd:MD_LegalConstraints/gmd:accessConstraints) = 1"> Error in business rule #29, Type of access constraint | Erreur dans la règle d’affaire #29, Type de contrainte d'acces | Erreur dans la règle d’affaire #29, Type de contrainte d'acces(cardinalité)</sch:assert>
            <sch:assert test="count(gmd:MD_LegalConstraints/gmd:useConstraints) = 1"> Error in business rule #30, Type of usage constraint | Erreur dans la règle d’affaire #30, Type de contrainte d'utilisation (cardinalité)</sch:assert>
            <sch:assert test="count(gmd:MD_LegalConstraints/gmd:useLimitation) = 1 ">Error in business rule #28, Dataset license | Erreur dans la règle d’affaire #28, Licence du jeu de données (cardinalité) </sch:assert>

            <sch:assert test="
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Open Government Licence - Canada (http://open.canada.ca/en/open-government-licence-canada)']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence du gouvernement ouvert - Canada (http://ouvert.canada.ca/fr/licence-du-gouvernement-ouvert-canada)']
                or
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Open Government Licence - British Columbia (https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc)']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence du gouvernement ouvert - Colombie-Britannique (https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc)']
				or
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Creative Commons 4.0 Attribution (CC-BY) licence – Quebec (https://www.donneesquebec.ca/fr/licence/)']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence Creative Commons 4.0 Attribution (CC-BY) – Québec (https://www.donneesquebec.ca/fr/licence/)']
                or
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Open Government Licence - Alberta (https://open.alberta.ca/licence)']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence du gouvernement ouvert - Alberta (https://open.alberta.ca/licence)']
                or
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Open Government Licence - Ontario (https://www.ontario.ca/page/open-government-licence-ontario)']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence du gouvernement ouvert - Ontario (https://www.ontario.ca/fr/page/licence-du-gouvernement-ouvert-ontario)']
                or
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Open Government Licence - Prince Edward Island (https://www.princeedwardisland.ca/en/information/finance/open-government-licence-prince-edward-island)']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence du gouvernement ouvert - Île-du-Prince-Édouard (https://www.princeedwardisland.ca/fr/information/finances/licence-du-gouvernement-ouvert-ile-du-prince-edouard)']
                or
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Open Government Licence - Nova Scotia (https://novascotia.ca/opendata/licence.asp)']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence du gouvernement ouvert - Nouvelle-Écosse (https://novascotia.ca/opendata/licence.asp)']
                or
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Open Government Licence - New Brunswick (http://www.snb.ca/e/2000/data-E.html)  NOTE: Subject to change']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence du gouvernement ouvert – Nouveau-Brunswick (http://www.snb.ca/f/2000/data-F.html)  NOTE: Subject to change']
                or
                gmd:MD_LegalConstraints/gmd:useLimitation[gco:CharacterString = 'Open Government Licence - Newfoundland and Labrador (https://opendata.gov.nl.ca/public/opendata/page/?page-id=licence)']
                [gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'Licence du gouvernement ouvert - Terre-Neuve-et-Labrador (https://opendata.gov.nl.ca/public/opendata/page/?page-id=licence']
                ">
                Error in business rule #28, Dataset license | Erreur dans la règle d’affaire #28, Licence du jeu de données (Correspondance/valeur)
            </sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #29, Type de contrainte d'acces -->
        <sch:rule context="gmd:accessConstraints">
            <sch:assert test="gmd:MD_RestrictionCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_107' and @codeListValue='RI_606' ]/text() = 'license; licence'">Error in business rule #29, Type of access constraint | Erreur dans la règle d’affaire #29, Type de contrainte d'acces | Erreur dans la règle d’affaire #29, Type de contrainte d'acces(valeur)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #30 , Type de contrainte d'utilisation-->
        <sch:rule context="gmd:useConstraints">
            <sch:assert test="gmd:MD_RestrictionCode[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_107' and @codeListValue='RI_606' ]/text() = 'license; licence'">Error in business rule #30, Type of usage constraint | Erreur dans la règle d’affaire #30, Type de contrainte d'utilisation (valeur)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaires #26 , Information de date -->
        <sch:rule context="gmd:identificationInfo">
            <sch:assert test="count(gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:date) =2 and not(gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date = '')">Error in business rule #26, Date information | Erreur dans la règle d’affaire #26, Information de date  (cardinalité)</sch:assert>

            <!-- Règle d'affaire #33, Étendu spatial -->
            <sch:assert test="count(gmd:MD_DataIdentification/gmd:extent/gmd:EX_Extent/gmd:geographicElement)=1"> Error in business rule #33, Spatial extent | Erreur dans la règle d’affaire #33, Étendu spatial  (cardinalité)</sch:assert>
            <!-- Règle d'affaires #17 , Titre du jeu de donnée -->
            <sch:assert test="gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title[@xsi:type='gmd:PT_FreeText_PropertyType'] and gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']">Error in business rule #17, Title of the dataset | Erreur dans la règle d’affaire #17, Titre du jeu de donnée (bilinguisme)</sch:assert>

            <!-- Règle d'affaire #31, Type de représentation spatiale -->
            <sch:assert test="count(gmd:MD_DataIdentification/gmd:spatialRepresentationType)=1">Error in business rule #31, Type of spatial representation | Erreur dans la règle d’affaire #31, Type de représentation spatiale (cardinalité)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #31, Type de représentation spatiale -->
        <sch:rule context="gmd:spatialRepresentationType">
            <sch:assert test="
                //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_634'] and //*/gmd:MD_SpatialRepresentationTypeCode/text() = 'napMD_RepresentationTypeCode; pnaMD_CodeTypeReprésentation'
                or  //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_635'] and //*/gmd:MD_SpatialRepresentationTypeCode/text() = 'vector; vecteur'
                or  //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_636'] and //*/gmd:MD_SpatialRepresentationTypeCode/text() = 'grid; grille'
                or  //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_637'] and //*/gmd:MD_SpatialRepresentationTypeCode/text() = 'textTable; texteTable'
                or  //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_638'] and //*/gmd:MD_SpatialRepresentationTypeCode/text() = 'tin; tin'
                or  //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_639'] and //*/gmd:MD_SpatialRepresentationTypeCode/text() = 'stereoModel; stéréomodèle'
                or  //*[@codeList='http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109' and @codeListValue='RI_640'] and //*/gmd:MD_SpatialRepresentationTypeCode/text() = 'video; vidéo'
                ">Error in business rule #31, Type of spatial representation | Erreur dans la règle d’affaire #31, Type de représentation spatiale (valeur)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #32, Catégorie thématique  -->
        <sch:rule context="gmd:topicCategory">
            <sch:assert test="//*[gmd:MD_TopicCategoryCode =('napMD_TopicCategoryCode','farming','biota','boundaries','climatologyMeteorologyAtmosphere','economy','elevation','environment','geoscientificInformation','health','imageryBaseMapsEarthCover','intelligenceMilitary','inlandWaters','location','oceans','planningCadastre','society','structure','transportation','utilitiesCommunication') ]">
                Error in business rule #32, Topic category | Erreur dans la règle d’affaire #32, Catégorie thématique  (valeur)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #33, Étendu spatial -->
        <sch:rule context="gmd:geographicElement">
            <!-- cardinalité -->
            <sch:assert test="count(gmd:EX_GeographicBoundingBox) = 1 "> Error in business rule #33, Spatial extent | Erreur dans la règle d’affaire #33, Étendu spatial  (cardinalité)</sch:assert>
            <sch:assert test="count(gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude) = 1 "> Error in business rule #33, Spatial extent (west) | Erreur dans la règle d’affaire #33, Étendu spatial  (cardinalité)</sch:assert>
            <sch:assert test="count(gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude) = 1 "> Error in business rule #33, Spatial extent (east) | Erreur dans la règle d’affaire #33, Étendu spatial  (cardinalité)</sch:assert>
            <sch:assert test="count(gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude) = 1 "> Error in business rule #33, Spatial extent (south)| Erreur dans la règle d’affaire #33, Étendu spatial  (cardinalité)</sch:assert>
            <sch:assert test="count(gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude) = 1 "> Error in business rule #33, Spatial extent (north)| Erreur dans la règle d’affaire #33, Étendu spatial  (cardinalité)</sch:assert>
            <!-- check values -->

            <sch:assert test=" number(gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal)> number(gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal) and  number(gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal) > number(gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal)"  >Error in business rule #33, Spatial extent | Erreur dans la règle d’affaire #33, Étendu spatial  (valeur)</sch:assert>
        </sch:rule>

        <!-- Règle d'affaire #34,  Étendu temporel -->
        <sch:rule context="gmd:temporalElement">
            <sch:assert test="count(gmd:EX_TemporalExtent)=1">Error in business rule #34, Temporal Extent | Erreur dans la règle d’affaire #34, Étendu temporel (cardinalité 1) </sch:assert>
            <sch:assert test="gmd:EX_TemporalExtent/gmd:extent/gml:TimePeriod[@gml:id='timeperiod1']">Error in business rule #34, Temporal Extent | Erreur dans la règle d’affaire #34, Étendu temporel (cardinalité 2)</sch:assert>
        </sch:rule>

        <sch:rule context="gml:TimePeriod">
            <!-- Date format -->
            <sch:let name="DatePattern1" value="'^[0-9]{4}[-][0-9]{2}[-][0-9]{2}$'"/>
            <sch:let name="DatePattern2" value="'^[0-9]{4}[-][0-9]{2}$'"/>
            <sch:let name="DatePattern3" value="'^[0-9]{4}$'"/>
            <sch:assert test="matches(gml:beginPosition,$DatePattern1) or matches(gml:beginPosition,$DatePattern2) or matches(gml:beginPosition,$DatePattern3)"> Error in business rule #34, Temporal Extent | Erreur dans la règle d’affaire #34, Étendu temporel (format)</sch:assert>
            <!-- cardinalité -->
            <sch:assert test="count(gml:beginPosition) = 1 and count(gml:endPosition) = 1 or count(gml:endPosition) = 0 ">Error in business rule #34, Temporal Extent | Erreur dans la règle d’affaire #34, Étendu temporel (cardinalité 3)</sch:assert>
        </sch:rule>

        <sch:rule context="gmd:distributionInfo/gmd:MD_Distribution/gmd:distributionFormat">
            <!-- Règle d'affaire #35-1,  Format de distribution du jeu de données -->
            <sch:let name="format" value="string-join([';', gmd:MD_Format/gmd:name/gco:CharacterString, ';'])"/>
            <sch:assert test="count(gmd:MD_Format) = 1
                and count(gmd:MD_Format/gmd:name) = 1
                and count(gmd:MD_Format/gmd:name/gco:CharacterString) = 1
                and gmd:MD_Format/gmd:name[gco:CharacterString = ('AAC', 'AI', 'AIFF', 'AMF', 'APK', 'ASCII Grid', 'AVI', 'BAG', 'Blackberry', 'BMP', 'BWF', 'CCT', 'CDED ASCII', 'CDF', 'CDR', 'COD', 'CSV', 'DBD', 'DBF', 'DICOM', 'DNG', 'DOC', 'DOCX', 'DXF', 'E00', 'ECW', 'EDI', 'EMF', 'EPS', 'EPUB2', 'EPUB3', 'ESRI REST', 'EXE', 'FGDB/GDB', 'Flat raster binary', 'GDB', 'GEOJSON', 'GeoPDF', 'GeoRSS', 'GeoTIF', 'GIF', 'GML', 'GPKG', 'GRD', 'GRIB1', 'GRIB2', 'HDF', 'HTML', 'IATI', 'IOS', 'IPA', 'JAR', 'JFIF', 'JP2', 'JPEG 2000', 'JPG', 'JP2', 'JSON', 'JSON Lines', 'JSONL', 'JSON-LD', 'KML', 'KMZ', 'LAS', 'LYR', 'MOV', 'MP3', 'MPEG', 'MPEG-1', 'MXD', 'MXF', 'NetCDF', 'NT', 'ODP', 'ODS', 'ODT', 'other', 'PDF', 'PDF/A-1', 'PDF/A-2', 'PDF/UA', 'PNG', 'PPT', 'PPTX', 'RDF', 'RDFa', 'RSS', 'RTF', 'SAR', 'SAV', 'SEGY', 'SHP', 'SQL', 'SQLITE', 'SQLITE3', 'SVG', 'TAB', 'TFW', 'TIFF', 'TRIG', 'TRIX', 'TTL', 'TXT', 'VPF', 'WAV', 'WCS', 'Web App', 'WFS', 'WMS', 'WMTS', 'WMV', 'WPS', 'XLS', 'XLSM', 'XLSX', 'XML', 'ZIP')]
                and count(../gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description[contains(gco:CharacterString, $format)]) > 0">
                Error in business rule #35-1, Dataset distribution format | Erreur dans la règle d’affaire #35-1, Format de distribution du jeu de données
            </sch:assert>

            <!-- Règle d'affaire #35-1,  Format de distribution du jeu de données (doublons)-->
            <sch:report test="gmd:MD_Format/gmd:name/gco:CharacterString = preceding-sibling::gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString
                or gmd:MD_Format/gmd:name/gco:CharacterString = following-sibling::gmd:distributionFormat/gmd:MD_Format/gmd:name/gco:CharacterString">
                Error in business rule #35-1, Dataset distribution format (duplicates) | Erreur dans la règle d’affaire #35-1, Format de distribution du jeu de données (doublons)
            </sch:report>

            <!-- Règle d'affaire #35-2,  Version du format de distribution du jeu de données -->
            <sch:assert test="count(gmd:MD_Format) = 1
                and count(gmd:MD_Format/gmd:version) = 1
                and count(gmd:MD_Format/gmd:version/gco:CharacterString) = 1
                and gmd:MD_Format/gmd:version/gco:CharacterString != ''
                and gmd:MD_Format/gmd:version/gco:CharacterString != 'missing'">
                Error in business rule #35-2, Version of the dataset distribution format | Erreur dans la règle d’affaire #35-2, Version du format de distribution du jeu de données (cardinalité)
            </sch:assert>
        </sch:rule>

        <sch:rule context="gmd:distributionInfo">
            <!-- Règle d'affaire #36-1, Service web bilingue -->
            <sch:assert test="count(gmd:MD_Distribution/gmd:transferOptions[descendant::gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:fra-CAN']/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString = 'ESRI REST: Map Service'])
                = count(gmd:MD_Distribution/gmd:transferOptions[descendant::gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:eng-CAN']/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString = 'ESRI REST: Map Service'])
                and count(gmd:MD_Distribution/gmd:transferOptions[descendant::gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:fra-CAN']/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString = 'OGC:WMS'])
                = count(gmd:MD_Distribution/gmd:transferOptions[descendant::gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:eng-CAN']/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString = 'OGC:WMS'])
                and count(gmd:MD_Distribution/gmd:transferOptions[descendant::gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:fra-CAN']/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString = 'ESRI REST: Map Service']) &lt;= 1
                and count(gmd:MD_Distribution/gmd:transferOptions[descendant::gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:fra-CAN']/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString = 'OGC:WMS']) &lt;= 1">
                Error in business rule #36-1, Bilingual web service | Erreur dans la règle d’affaire #36-1, Service web bilingue (valeur)
            </sch:assert>

            <!-- Règle d'affaire #39, Contact du distributeur -->
            <sch:assert test="count(gmd:MD_Distribution/gmd:distributor/gmd:MD_Distributor) >= 1">Error in business rule #39, Distributor contact | Erreur dans la règle d’affaire #39, Contact du distributeur (cardinalité)</sch:assert>
        </sch:rule>

        <sch:rule context="gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions">
            <!-- Règle d'affaire #36-2, Service web bilingue -->
            <sch:assert test="(gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:fra-CAN']
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol[gco:CharacterString = ('ESRI REST: Map Service', 'OGC:WMS')])
                or (gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:eng-CAN']
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol[gco:CharacterString = ('ESRI REST: Map Service', 'OGC:WMS')])
                or ((gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role]
                and gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role!='urn:xml:lang:fra-CAN']
                and gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role!='urn:xml:lang:eng-CAN']
                or gmd:MD_DigitalTransferOptions/gmd:onLine[not(@xlink:role)])
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString != ''
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:protocol/gco:CharacterString != 'missing')">
                Error in business rule #36-2, Bilingual web service | Erreur dans la règle d’affaire #36-2, Service web bilingue (valeur)
            </sch:assert>

            <!-- Règle d'affaire #37, Nom de la ressource du jeu de donnée (cardinalité)-->
            <sch:assert test="count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name) = 1
                and count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gco:CharacterString) = 1
                and count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString) = 1

                and ((gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gco:CharacterString = ''
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = '')

                or (gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gco:CharacterString = 'missing'
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString = 'missing')

                or (gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gco:CharacterString != ''
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gco:CharacterString != 'missing'
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString != ''
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString != 'missing'))">
                Error in business rule #37, Name of the dataset resource | Erreur dans la règle d’affaire #37, Nom de la ressource du jeu de donnée (cardinalité)
            </sch:assert>
            <!-- Règle d'affaire #37, Nom de la ressource du jeu de donnée (bilinguisme)-->
            <sch:assert test="count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name[@xsi:type='gmd:PT_FreeText_PropertyType']) = 1
                and count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:name/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']) = 1">
                Error in business rule #37, Name of the dataset resource | Erreur dans la règle d’affaire #37, Nom de la ressource du jeu de donnée (bilinguisme)
            </sch:assert>

            <!-- Règle d'affaire #38, Description de la ressource du jeu de donnée (cardinalité) -->
            <sch:assert test="count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description)=1">
                Error in business rule #38, Description of the dataset resource | Erreur dans la règle d’affaire #38, Description de la ressource du  jeu de donnée (cardinalité)
            </sch:assert>

            <!-- Règle d'affaire #38, Description de la ressource du jeu de donnée (bilinguisme) -->
            <sch:assert test="gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description[@xsi:type='gmd:PT_FreeText_PropertyType']
                and count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gco:CharacterString) = 1
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gco:CharacterString != ''
                and count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString) = 1
                and count(gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra']) = 1
                and gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString[@locale='#fra'] != ''">
                Error in business rule #38, Description of the dataset resource | Erreur dans la règle d’affaire #38, Description de la ressource du jeu de donnée (bilinguisme)
            </sch:assert>

            <sch:let name="Pattern"
                value="'^[\w ]+;(AAC|AI|AIFF|AMF|Android|APK|ASCII Grid|AVI|BAG|Blackberry|BMP|BWF|CCT|CDED ASCII|CDF|CDR|COD|CSV|DBD|DBF|DICOM|DNG|DOC|DOCX|DXF|E00|ECW|EDI|EMF|EPS|EPUB2|EPUB3|ESRI REST|EXE|FGDB/GDB|Flat raster binary|GDB|GEOJSON|GeoPDF|GeoRSS|GeoTIF|GIF|GML|GPKG|GRD|GRIB1|GRIB2|HDF|HTML|IATI|IOS|IPA|JAR|JFIF|JP2|JPEG 2000|JPG|JP2|JSON|JSON Lines|JSONL|JSON-LD|KML|KMZ|LAS|LYR|MOV|MP3|MPEG|MPEG\-1|MXD|MXF|NetCDF|NT|ODP|ODS|ODT|other|PDF|PDF/A\-1|PDF/A\-2|PDF/UA|PNG|PPT|PPTX|RDF|RDFa|RSS|RTF|SAR|SAV|SEGY|SHP|SQL|SQLITE|SQLITE3|SVG|TAB|TFW|TIFF|TRIG|TRIX|TTL|TXT|VPF|WAV|WCS|Web App|WFS|WMS|WMTS|WMV|WPS|XLS|XLSM|XLSX|XML|ZIP);(eng|fra|eng,fra)$'"/>
            <sch:let name="Type1" value="substring-before((gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gco:CharacterString)[1], ';')"/>
            <sch:let name="Temp1" value="substring-after((gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gco:CharacterString)[1], ';')"/>
            <sch:let name="Format1" value="substring-before($Temp1, ';')"/>
            <sch:let name="Langue1" value="substring-after($Temp1, ';')"/>

            <sch:let name="Type2" value="substring-before((gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString)[1], ';')"/>
            <sch:let name="Temp2" value="substring-after((gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString)[1], ';')"/>
            <sch:let name="Format2" value="substring-before($Temp2, ';')"/>
            <sch:let name="Langue2" value="substring-after($Temp2, ';')"/>

            <!-- Règle d'affaire #38, Description de la ressource du jeu de donnée (valeur) -->
            <sch:assert test="matches((gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gco:CharacterString)[1], $Pattern)
                and matches((gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource/gmd:description/gmd:PT_FreeText/gmd:textGroup/gmd:LocalisedCharacterString)[1], $Pattern)
                and (($Type1 = 'Supporting Document' and $Type2='Document de soutien')
                or ($Type1 = 'Dataset' and $Type2='Données')
                or ($Type1 = 'Web Service' and $Type2='Service Web')
                or ($Type1 = 'API' and $Type2='API')
                or ($Type1 = 'Application' and $Type2='Application'))

				and ((gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:fra-CAN'])
                or (gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:eng-CAN'])
                or (gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role]
                and gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role!='urn:xml:lang:fra-CAN']
                and gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role!='urn:xml:lang:eng-CAN']
                or gmd:MD_DigitalTransferOptions/gmd:onLine[not(@xlink:role)]))

                and count(../gmd:distributionFormat[gmd:MD_Format/gmd:name/gco:CharacterString = $Format1]) > 0">
                Error in business rule #38, Description of the dataset resource | Erreur dans la règle d’affaire #38, Description de la ressource du jeu de donnée (valeur)
                <!--and ((gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:fra-CAN'] and $Langue1 = 'fra')
                or (gmd:MD_DigitalTransferOptions/gmd:onLine[@xlink:role='urn:xml:lang:eng-CAN'] and $Langue1 = 'eng')-->
				
            </sch:assert>
        </sch:rule>
    </sch:pattern>
</sch:schema>
