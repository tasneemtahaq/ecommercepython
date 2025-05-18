@echo off
cd /d D:\quarter3\ecommerce
del /f /q data\ecommerce.db
mkdir data 2>nul
echo Database deleted and folder reset
pause