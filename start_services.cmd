@echo off

REM Up the provider in windows
start ollama serve

REM Up Docker
cd searxng && docker compose up