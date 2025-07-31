# Fetching Data Via Post (Bypassing HTML parsing)
I originally thoguht that each site would be fetched via direct HTML parsing. However, the first site I tried to fetch (IBM) disproved that idea. It does not return any useful data with an HTML request.

I manually reloaded the page in my browser while examining the XHR files in the Network tab. Looking through the list (which can be copied to a .har file) I found the POST which is used to fetch job data. The valid POST ran in browser contains all of the payload and header information I need to make an automated POST call within a python script.

This method may not be available on each job board, but it simplifies the retrieval process as the returned data from the POST is simple JSON structured job information, requiring no complex parsing.