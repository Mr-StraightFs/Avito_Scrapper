
# Avito Web Scraper

This repository contains a Python-based web scraper designed for Avito, utilizing a graphical user interface (GUI) built with Tkinter. It allows users to scrape vehicle listings or other categories of items from Avito by setting various search parameters.

## Features

- **User Interface:** Easy-to-use GUI for setting search parameters.
- **Flexible Search:** Users can specify keywords, cities, and the number of pages to scrape.
- **Real-Time Display:** Scraped data is displayed in the GUI.
- **Data Export:** Allows saving the scraped data into an Excel file.

## Prerequisites

Before running the scraper, ensure you have Python 3.x installed along with the following packages:
```bash
pip install pandas requests beautifulsoup4 schedule

## Installation
Clone this repository:
```bash
git clone https://github.com/your-username/avito-scraper.git
Navigate to the scraper directory:
```bash
cd avito-scraper

## Usage
To start the scraper:
```bash
Copier le code
python avito_scraper.py
The GUI will launch, allowing you to enter your search criteria and start scraping.

## GUI Components
- Keyword Entry: Enter or select a keyword for the search.
- City Dropdown: Choose a city or select "Tout le Maroc" for nationwide searches.
- Page Limit Selector: Set the maximum number of pages to scrape.
- Scheduled Scraping
The script includes functionality to schedule scraping tasks daily at a specified time (default is 8 AM). This is managed using the schedule library.

## Output
Results are displayed within the GUI and can be exported to an Excel file via the "Save to Excel" button.

## Contributing
Contributions are welcome! Please fork the project, make your changes, and submit a pull request.

