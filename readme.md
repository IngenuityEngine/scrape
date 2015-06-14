# Scrape
Screen Scrape content from the internet

### Use
1. Run Chrome without security
%HOME%\AppData\Local\Google\Chrome\Application\chrome.exe --disable-web-security
2. Load 127.0.0.1:3000
3. Scrape away


Access-Control-Allow-Origin: *


Get Board Urls:

var boardUrls=[];$('.boardLinkWrapper').each(function(){boardUrls.push('https://www.pinterest.com' + $(this).attr('href'));});console.log(boardUrls)