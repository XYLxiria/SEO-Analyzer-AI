# SEO-Analyzer-AI

This application is based on python 3.12, the purpose of this application is to map several visuals containing the results of scraping using a request parser and beautifulsoup4, assisted by pyQt5 as the main GUI, and AI to filter words / keywords that have been parsed. 

The code is still in-line based, I'm still new to using python and github, feel free if you want to request or improve as a contributor, suggestion can do so.

This is an application created to complete studies at the Faculty of Engineering - Wiralodra University. The exact build still developing for future, and maybe in the future this application will maintainly updated (I'm still learning about updater in python).

This application uses some of the main libraries in python 3.12, such as:

1. nltk (punkt and stopwords)
2. spaCy (removed in v3beta - see release)
3. Beautifulsoup4
4. requests
5. reportlab
6. pyQt5 as main GUI
7. matplotlib
8. skicit-learn
9. numpy

*Note if you do research for this code :*
>- Refer the nltkdownload.py for manually or make choice of yours for directory that nltk placed later
>- You must change the line of directory on main.py (whatever version) to directories of yours, it will provide the AI from local
>- If you want still use spaCy, then you can install it, but the main source I use en-core-web-sm

Please see changelog in English or Indonesian, it may not be very complete as the pulls were done simultaneously (I only save and always debug in local mode). Feel free to use as the code releases under the MIT License.

If you want to straight to app release, you can download from link below here :

[Download V1 Alpha](https://github.com/XYLxiria/SEO-Analyzer-AI/releases/download/publish/SEOAnalyzerInstaller.exe) for Alpha release (Based .py files from 01-05)

[Download V3 Beta](https://github.com/XYLxiria/SEO-Analyzer-AI/releases/download/lastestpublish/SEOAnalyzerInstallerV3-beta.exe) for Beta release (Based .py files from 06)

[Download V1 Final](https://github.com/XYLxiria/SEO-Analyzer-AI/releases/download/publishfinal/SEOAnalyzerInstallerV1Final.exe) for Final release (Based lastest .py file from 06)

*Error note from the installer :*
>- Error 225 : Turn off the Antivirus, this app not digital trusted by windows, dev brokes /yea
>- Error 740 : Run as Administrator, but it's have been fixed (check the .iss file)
