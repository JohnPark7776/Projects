Original plan to create a bot which can webscrape Instagram. 

Did not have the necessary skills to webscrape past basic HTML.parsing. It requires knowledge of accessing Server SQL to access the video/reels of instagram posts.

Did found a workaround utilizing gallery-dl but was unable to find a suitable cheap/free way to host discord bot that allows playwright.


How it works:
Instagram_Link.py:
  Playwright allows the ability to open up Chromium Browser without actually opening up a Browser. Playwright is originally used to test HTTP/API Requests 
  and button functions but I utilized it to grab the HTML info instead. 
  
  Reason I went this route because I did not want to create methods/functions to "manually" create API requests and just make a Browser create all the correct
  API requests/URLs for me so all I had to do was parse through the HTML and find the Images.
  

Required Libraries:
playwright
BeautifulSoup
Discord
discort.ext
