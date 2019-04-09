rem SET "PATH=%PATH%;C:\Python34;C:\Python34\Scripts;C:\gdal_232;C:\gdal_232\bin;C:\gdal_232\bin\gdal\apps"

echo %GEOS_LIBRARY_PATH%

cd C:\pycsw-2.2.0

C:\Python37-32\python pycsw/wsgi.py 8000

pause