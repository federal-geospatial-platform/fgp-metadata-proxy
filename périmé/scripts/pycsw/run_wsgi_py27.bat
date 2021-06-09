set PATH=%PATH:C:\Python37-32;C:\Python37-32\Scripts;=%

SET "PATH=%PATH%;C:\Python27\ArcGIS10.4;C:\Python27\ArcGIS10.4\Scripts;C:\gdal_232;C:\gdal_232\bin;C:\gdal_232\bin\gdal\apps"

cd C:\pycsw

python pycsw/wsgi.py 80

pause