@echo off
set SCRIPTS_DIR=scripts
set LLM_ROUTER_DIR=llm_router

if exist "%SCRIPTS_DIR%\windows_install.bat" (
    echo Running Windows installation script...
    call "%SCRIPTS_DIR%\windows_install.bat"
    cd "%LLM_ROUTER_DIR%" && call dl_safetensors.bat
) else (
    echo Error: %SCRIPTS_DIR%\windows_install.bat not found!
    exit /b 1
)
