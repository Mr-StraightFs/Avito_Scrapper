import pandas as pd
import requests
import tkinter as tk
from tkinter import ttk, filedialog
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Union
import schedule
import time

def handle_request_error(func):
    """
    Decorator function to handle request error
    """
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            print(f"Error while getting response: {e}")
            return None
        return response.content
    return wrapper

class AvitoScraper:
    def __init__(self, root: tk.Tk) -> None:

        self.root = root
        self.city_var = tk.StringVar(value="Tout le Maroc")
        self.page_var = tk.IntVar(value=2)
        self.keyword_var = tk.StringVar(value="Type a keyword or choose one from the list ...")
        self.message_label = tk.Label(root, text="", font=('verdana', 10))
        self.start_button = tk.Button(root, text="Scrape", font=('verdana', 8, 'bold'), bg="#3b5998", fg="white",
                                      width=15, height=2, command=self.scrape)
        self.save_button = tk.Button(root, text="Save to Excel", font=('verdana', 8, 'bold'), bg="#006400", fg="white",
                                     width=15, height=2, command=self.save_to_excel, state=tk.DISABLED)
        self.create_widgets()

    def schedule_scrape(self) -> None:
        """
        Schedules the scrape method to run at 8 am every day
        """
        schedule.every().day.at("08:00").do(self.scrape)
        while True:
            schedule.run_pending()
            time.sleep(60)

    def create_widgets(self) -> None:
        self.root.title("Avito Auto Scraper")
        self.root.geometry("600x400")
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        inner_frame = tk.LabelFrame(main_frame, text="Settings", highlightbackground="white", highlightcolor="white")
        inner_frame.pack(pady=20, padx=10)

        default_keywords = ["Voitures", "TV", "PC", "Téléphone portable"]
        tk.Label(inner_frame, text="Type a keyword:").grid(row=0, column=0, padx=5, pady=5)
        keyword_entry = ttk.Combobox(inner_frame, textvariable=self.keyword_var, values=default_keywords)
        keyword_entry.grid(row=0, column=1, padx=5, pady=5)

        cities = ["Casablanca", "Rabat", "Marrakesh", "Fès", "Tanger", "Agadir", "Oujda", "Kenitra", "Tetouan",
                  "Mohammedia", "Tout le Maroc"]
        tk.Label(inner_frame, text="Select a city:").grid(row=1, column=0, padx=5, pady=5)
        city_dropdown = ttk.Combobox(inner_frame, textvariable=self.city_var, values=cities)
        city_dropdown.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(inner_frame, text="Page Limit:").grid(row=2, column=0, padx=5, pady=5)
        page_dropdown = ttk.Combobox(inner_frame, textvariable=self.page_var, values=list(range(2, 4000, 50)))
        page_dropdown.grid(row=2, column=1, padx=5, pady=5)
        self.start_button.pack(pady=10)
        self.save_button.pack( pady=10)
        self.message_label.pack(pady= 5)

    def scrape(self) -> None:
        """
        Scrapes Avito website for cars or other items based on user's selected city and keyword
        """
        # Get user input values
        city = self.city_var.get().lower() if self.city_var.get() != 'Tout le Maroc' else 'maroc'
        page_limit = int(self.page_var.get())
        keywords = str(self.keyword_var.get()).lower()

        # Construct the URL with user input
        base_url = f'https://www.avito.ma/fr/{city}/{keywords}-%C3%A0_vendre'

        # Set headers for the requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        # Initialize data and page number
        global df
        data = []
        page_number = 1

        # Loop through all pages until page_limit is reached or no more pages are found
        while True:
            # Check if page_limit has been reached
            if page_number > page_limit:
                break

            # Get the URL for the current page
            url = base_url + '?o=' + str(page_number)
            print(url)

            # Make the request and handle any errors
            response_content = handle_request_error(requests.get)(url, headers=headers)
            #print(response_content)
            if not response_content:
                break

            # Parse the response content using BeautifulSoup
            soup = BeautifulSoup(response_content, 'html.parser')

            # Find the div containing the listings
            listing_div = soup.find('div', {'class': 'sc-1nre5ec-1 crKvIr listing'}) or \
                          soup.find('div', {'class': 'sc-1nre5ec-1 fzpnun listing'})

            # If no listings are found, break the loop
            if not listing_div:
                #print(listing_div)
                # set the message label text
                self.message_label.configure(text="No Matches Found ! ")
                break
            else:
                urls = [a['href'] for a in listing_div.find_all('a', href=True)]

            # If no URLs are found, break the loop
            if not urls:
                break

            # Loop through all URLs found
            for url in urls:
                # Make a request for the current URL and handle any errors
                response_content = handle_request_error(requests.get)(url, headers=headers)

                if not response_content:
                    continue

                # Parse the response content using BeautifulSoup
                soup = BeautifulSoup(response_content, 'html.parser')

                if keywords == "voitures":


                    price = soup.find('p', {'class': 'sc-1x0vz2r-0 lnEFFR sc-1g3sn3w-13 czygWQ'})
                    price = price.text.strip() if price else ''

                    print(price)

                    # get the time and date of the ad
                    time_div = soup.find('div', {'class': 'sc-1g3sn3w-7 bNWHpB'})
                    print(time_div)
                    time_element = time_div.find('time')
                    date_time = datetime.strptime(time_element['datetime'], '%m/%d/%Y, %I:%M:%S %p')

                    print(time)


                    carburant_bvm_puissance = soup.find_all('span', {'class': 'sc-1x0vz2r-0 kuCwGF'})
                    puissance, bvm_bva, carburant = '', '', ''
                    for item in carburant_bvm_puissance:
                        if 'CV' in item.text.strip():
                            puissance = item.text.strip()
                        elif item.text.strip().lower() in ['manuelle', 'automatique']:
                            bvm_bva = item.text.strip()
                        else:
                            carburant = item.text.strip()


                    # get all items
                    details_div = soup.find('div', {'class': 'sc-1g3sn3w-4 etbZjx'})
                    items = details_div.find_all('li', {'class': 'sc-qmn92k-1 ldnQxr'})

                    row: Dict[str, Union[str, datetime, float]] = {}
                    for item in items:
                        label = item.find('span', {'class': 'sc-1x0vz2r-0 brylYP'}).text.strip()
                        value = item.find('span', {'class': 'sc-1x0vz2r-0 jsrimE'}).text.strip()
                        row['Ville'] = city
                        row[label] = value
                        row['Prix'] = price
                        row['Boite à Vitesse'] = bvm_bva
                        row['Puissance fiscale'] = puissance
                        row['Carburant'] = carburant
                        row["lien de l'annonce"] = url
                        row['date'] = date_time.date()
                        row['ad_life'] = (datetime.today() - date_time).days

                    data.append(row)

                else:
                    title_div = soup.find('div', {'class': 'sc-1g3sn3w-9 gIlAYt'})
                    title = title_div.text.strip() if title_div else ''
                    print(title)

                    details_div = soup.find('div', {'class': 'sc-1g3sn3w-4 eTmXXQ'})
                    description_div = soup.find('div', {'class': 'sc-1g3sn3w-16 leVIwi'})
                    description = description_div.text.strip() if description_div else ''
                    print(details_div)

                    items = details_div.find_all('li', {'class': 'sc-qmn92k-1 ldnQxr'})
                    price = soup.find('p', {'class': 'sc-1x0vz2r-0 dYtyob sc-1g3sn3w-13 kliyMh'})
                    price = price.text.strip() if price else ''

                    # get the time and date of the ad
                    time_div = soup.find('div', {'class': 'sc-1g3sn3w-7 NuEic'})
                    time_element = time_div.find('time')
                    date_time = datetime.strptime(time_element['datetime'], '%m/%d/%Y, %I:%M:%S %p')

                    row: Dict[str, Union[str, datetime, float]] = {}
                    for item in items:
                        label = item.find('span', {'class': 'sc-1x0vz2r-0 brylYP'}).text.strip()
                        value = item.find('span', {'class': 'sc-1x0vz2r-0 jsrimE'}).text.strip()
                        row['Title'] = title
                        row['Description'] = description
                        row['Prix'] = price
                        row['Ville'] = city
                        row[label] = value
                        row['date'] = date_time.date()
                        row['ad_life'] = (datetime.today() - date_time).days
                        row["lien de l'annonce"] = url

                        data.append(row)

            page_number += 1

            df = pd.DataFrame(data)
            # set the message label text
            self.message_label.configure(
                text=f"Download completed, {len(df)} results were found. Click to Save to Excel")
            # enable the save button
            self.save_button.config(state=tk.NORMAL)

    def save_to_excel(self) -> None:
        """
        Saves the scraped data to an Excel file
        """
        # Get today's date and format it as a string
        date_str = datetime.now().strftime("%Y-%m-%d")
        export_path = f'avito_cars_for_sale_{date_str}.xlsx'
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', initialfile=export_path)
        if file_path:
            df.to_excel(file_path, index=False)
            # set the message label text
            self.message_label.configure(text=f"Data saved to {file_path}")

        else:
            self.message_label.configure(text="Save cancelled by user")
