@echo off 
echo Starting data cleaner...
echo.
cd C:\Users\baohu\Desktop\Fall2020\Code\Collector
C:\Users\baohu\anaconda3\envs\collector\python.exe "C:\Users\baohu\Desktop\Fall2020\Code\Collector\datacleaner.py"
C:\Users\baohu\anaconda3\envs\collector\python.exe "C:\Users\baohu\Desktop\Fall2020\Code\Collector\dataplotter.py"
echo.
echo Finished data processing