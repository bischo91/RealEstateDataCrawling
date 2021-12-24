# Zillow Data Scraper

<p align="center">
  <a href="https://github.com/bischo91/RealEstateDatascraping">
  <h3 align="center">Zillow Data Scraper</h3>
  </a>
</p>
<br>
<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>
<br>


<!-- ABOUT THE PROJECT -->
## About The Project

The goal of the project is to comprehend the trend of housing market in a specific city by visualizing data extracted from the house sale posts on Zillow website.

The project consists of three files:

* Web scraping from Zillow website (zillow_scrape_v3.py)
* Database file as an example      (real_estate_database_example.db)
* Visualization of the database    (data_visualizer_v1.py)

To obtain data, zillow_scrape_v3.py was run periodically since the development of this project. The program was run using the Task Scheduler App. To avoid CAPTCHA being triggered, wait time is randmoly allocated between pages.

Due to the large size of the file, the example database (real_estate_database_example.db) does not include all the data, but it contains all the sales post from 2020/09/20 to 2021/10/30 in Gainesville, FL.
<br>

### Built With
This project is built with Python.
* [Python](https://www.python.org/)
<br><br>

## Getting Started

### Prerequisites

The program requires [Python](https://www.python.org/), and the following Python packages.
* beautifulsoup4 (4.9.3)
* pandas (1.2.4)
* sqlite3 (2.6.0)
* tkinter (8.6)
* tkcalendar (1.6.1)
* Datetime (4.3)
* numpy (1.20.2)
* matplotlib (3.4.1)

[MySQL](https://www.mysql.com/) is not required but recommended to easily visualize and manage the table.
[ChromeDriver](https://chromedriver.chromium.org/) is necessary for web scraping when running 'zillow_scrape_v3.py'


### Installation

There is no need for installation.
The required files are:
* zillow_scrape_v3.py
* data_visualizer_v1.py
* real_estate_database_example.db


<!-- USAGE EXAMPLES -->
## Usage

The data can be visualized in serveral ways. The database has more information than what the current version of visualization graphs present, which can be found manually.

Date vs Trend
* Date
  When 'Date' is selected, the plot presents data based on a single date selected.
  Scatter vs Bar
  * 'Scatter' plots all the data points on the selected 'Date'
  * 'Bar' shows the average and standard deviation of Y data
  Y-axis can be either 'Price' [USD] or 'Price/sqft' [USD/sqft]
  X-axis can be 'bds' (=number of bedrooms), 'ba' (=number of bathrooms), 'location' (=NW/SW/NE/SE/Unknown), 'sqft' (=total sqft of the property)

* Trend
  For 'Trend', Y-axis can be the average 'Price' or 'Price/sqft', and X-axis is the range of the selected date.
  The trend has a legend based on the location, or average of all.


<!-- CONTRIBUTING -->
## Contributing

Any suggestion or contributions are greatly appreciated.


<!-- CONTACT -->
<!-- ACKNOWLEDGEMENTS -->
