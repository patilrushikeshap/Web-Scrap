# Web-Scrap
In this repository, you can find my well-structured code for scraping data from Wynk music application. 

Steps:

1) Users can visit the Wynk website (https://wynk.in/) and search for the catalog, which provides A to Z music albums. From there, users need to extract all song links present in the catalog.
2) To gain insight into the Wynk app, you can refer to "https://wynk.in/robots.txt".
3) Extract all music links from the Wynk application into a CSV file and save it on the local system.
4) Provide the CSV file path in the wynk_meta_scrape.py script and run the file.
5) Finally, you can view the extracted metadata from the Wynk music app.
   
Code Explaination:

This code appears to be a web scraping script written in Python using libraries such as BeautifulSoup, pandas, and requests. It's designed to extract metadata from HTML pages, particularly tables within those pages, and save the extracted data to a CSV file.

Here's a breakdown of the functionality and the metadata it extracts:

Reading URLs from CSV: The script reads URLs from a CSV file located at the specified path.
Fetching Web Pages: It iterates through each URL, making a request to fetch the webpage content using the requests.get() method. It handles HTTP errors and connection errors gracefully and retries requests if necessary.
Extracting Metadata: For each webpage, it extracts metadata such as the page title and data from tables on the page. It looks for a table element and iterates through its rows to extract data. It also extracts certain data from the URL itself using regular expressions.

Language Mapping: The script contains a function (map_language) to map short language codes to their full display names.
Data Processing: After extracting the metadata, it processes the data, including mapping language codes to their full names and reformatting the data structure.
Saving Data to CSV: Finally, it saves the extracted metadata to a CSV file. The script ensures that the CSV file contains only desired columns and specifies the desired sequence of columns.

The metadata extracted includes:
{
URL, Title, Album/Movie, Singers, Producer, Lyricist, Language, Music Company, Duration, ISRC (International Standard Recording Code), UPC (Universal Product Code)
}
Other (additional data can be extracted from the table)

Overall, this script is designed to scrape web pages for music-related metadata and organize it into a structured format for further analysis or processing.

