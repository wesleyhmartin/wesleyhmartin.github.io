@echo off
cd /d "C:\users/jmart/onedrive/documents/github/wesleyhmartin.github.io/media"  REM 👈 Change this to your repo path
echo [%date% %time%] Running RSS feed generator...

REM Run the Python script
python duvall-rss-generator.py 

REM Add, commit, and push the updated file
git add lotw.xml
git commit -m "Automated RSS update"
git push origin main

echo Done. RSS updated and pushed.
pause