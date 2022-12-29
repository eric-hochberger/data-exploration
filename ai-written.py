import requests
from bs4 import BeautifulSoup
import json
import csv

# Open a new CSV file in write mode
with open("/exports/concerts-twinpeaks.csv", "w", newline="") as csv_file:
  # Create a CSV writer
  writer = csv.writer(csv_file)
  # Write the header row
  writer.writerow(["artist", "date", "venue", "city", "region", "country", "performers"])

  # Set the initial page number
  page = 1

  # Set a flag to indicate if we should continue scraping
  keep_scraping = True

  # Start the scraping loop
  while keep_scraping:
    # Construct the URL for the current page
    url = f"https://www.songkick.com/artists/296530-twin-peaks/gigography?page={page}"

    # Make a request to the URL
    response = requests.get(url, allow_redirects=False)

    # Check if the request was successful
    if response.status_code != 200:
      print("Failed to make request")
      exit()

    # Parse the HTML of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the div elements with the class 'microformat'
    concerts = soup.find_all("div", class_="microformat")

    # Iterate over the concerts
    for concert in concerts:
      # Parse the JSON script
      data = json.loads(concert.script.text)[0]
      # print(data, "\n\n")

      # Check if the location @type is "Place"
      if data["location"]["@type"] == "Place":
        # Extract the necessary information
        artist = data["name"]
        city = data["location"]["address"]["addressLocality"]
        country = data["location"]["address"]["addressCountry"]
        date = data["startDate"]
        venue = data["location"]["name"]
        # Check if the address region key exists (USA AND CANADA ONLY)
        region = ""
        if "addressRegion" in data["location"]["address"]:
            region = data["location"]["address"]["addressRegion"]
        # Get performer data and cycle through it getting names
        performers = []
        for performer in data["performer"]:
            performers.append(performer["name"])

        # Write the information to the CSV file as a new record
        writer.writerow([artist, date, venue, city, region, country, performers])

    # Check if there are more pages to scrape
    if len(concerts) < 50:
      # If there are less than 50 concerts on the page, it means we have reached the end of the gigography
      keep_scraping = False
    else:
      # If there are 50 concerts on the page, there may be more pages to scrape
      page += 1
