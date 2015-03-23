:; #!/bin/bash
:; chmod +x `dirname $0`/scripts/setup.py
:; args=${*:-"-h"}
:; echo here
:; `dirname $0`/scripts/setup.py $args
:; exit
@echo off
setlocal
set "args=%*"
if "%1"=="" set "args=-h"
python %~dp0\scripts\setup.py %args%
endlocal