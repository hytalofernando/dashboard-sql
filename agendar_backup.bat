@echo off
REM Script para agendar backup automático diário no Windows
REM Execute este arquivo como Administrador

echo ========================================
echo AGENDAR BACKUP AUTOMATICO - ESTOQUE
echo ========================================
echo.

REM Obtém o diretório atual
set CURRENT_DIR=%CD%

echo Diretorio do projeto: %CURRENT_DIR%
echo.
echo Este script criará uma tarefa agendada que executa
echo backup automatico todos os dias as 23:00
echo.

pause

REM Cria tarefa agendada
schtasks /create /tn "Backup Estoque Diario" /tr "\"%CURRENT_DIR%\venv\Scripts\python.exe\" \"%CURRENT_DIR%\backup.py\"" /sc daily /st 23:00 /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCESSO! Backup agendado para 23:00
    echo ========================================
    echo.
    echo Voce pode verificar a tarefa em:
    echo - Painel de Controle ^> Ferramentas Administrativas ^> Agendador de Tarefas
    echo.
    echo Para testar agora, execute: python backup.py
    echo.
) else (
    echo.
    echo ========================================
    echo ERRO ao criar tarefa agendada
    echo ========================================
    echo.
    echo Execute este arquivo como Administrador
    echo.
)

pause



