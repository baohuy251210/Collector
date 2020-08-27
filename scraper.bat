@echo off 
echo Starting uofu covid-19 web scraper...
echo.
cd C:\Users\baohu\Desktop\Fall2020\Code\Collector
C:\Users\baohu\anaconda3\envs\collector\python.exe "C:\Users\baohu\Desktop\Fall2020\Code\Collector\collectuofu.py"
echo.
echo Making git changes...
echo.
git status
git add .
git commit -m "scheduled scraper"
git push 