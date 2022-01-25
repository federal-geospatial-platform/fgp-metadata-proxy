ping -n 1 %1 | find "TTL=" > NUL
if errorlevel 0 (echo %1 is up) else (echo %1 is down)
)