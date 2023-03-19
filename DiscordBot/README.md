Currently can only webscrape Instagram.



How it works:
Instagram_Link.py:
  Playwright allows the ability to open up Chromium Browser without actually opening up a Browser. Playwright is originally used to test HTTP/API Requests 
  and button functions but I utilized it to grab the HTML info instead. 
  
  Reason I went this route because I did not want to create methods/functions to "manually" create API requests and just make a Browser create all the correct
  API requests/URLs for me so all I had to do was parse through the HTML and find the Images.
  
  I used Instagram as a practice ground as my final goal was to get picture, videos, and posts from weverse and then post it through Discord.
  

Required Libraries:
playwright
BeautifulSoup
Discord
discord.ext
