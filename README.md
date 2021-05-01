# Real Estate Data Crawling

<br />
<p align="center">
  <a href="https://github.com/bischo91/RealEstateDataCrawling">
    <img src="images/logo.png" alt="Logo" height="80">
  </a>

  <h3 align="center">Real Estate Data</h3>
  <p align="center">
    Real Estate Data 
  </p>
</p>
    <!-- <br />
    <a href="https://github.com/bischo91/RealEstateDataCrawling"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/bischo91/RealEstateDataCrawling">View Demo</a>
    · -->
    
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
<!--         <li><a href="#installation">Installation</a></li> -->
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
<!--     <li><a href="#roadmap">Roadmap</a></li> -->
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
<!--     <li><a href="#acknowledgements">Acknowledgements</a></li> -->
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The goal of the project is to comprehend the trend of housing market in a specific city by visualizing data extracted from the seller's posts on Zillow website.

The project consists of three files:

* Web crawling from Zillow website (zillow_scrape_v1.py)
* Database file as an example      (real_estate_database_example.db)
* Visualization of the database    (data_visualizer_v1.py)

To obtain data, zillow_scrape_v1.py was run almost everyday since 2020/09/20. The python file was run using the Task Scheduler App. Some data are missing because CAPTCHA was triggered. This has been improved by randmoly allocating wait time between pages. However, the automation and web crawling can be further improved.

The example database does not include all the data due to the large size of the file.


### Built With

This project is mainly built with Python.
* [Python](https://www.python.org/)
* [Atom](https://atom.io/)
<!-- * [MySQL] (https://www.mysql.com/) -->
<!-- * [ChromeDriver] (https://chromedriver.chromium.org/) -->


<!-- GETTING STARTED -->
## Getting Started

Web crawling

### Prerequisites

The program requires Python, and some Python packages.
* BeautifulSoup
* pandas
* numpy
* sqlite3
* datetime
* tkinter
* tkcalendar
* matplotlib

[MySQL](https://www.mysql.com/) is not required but recommended to easily visualize and manage the table.
[ChromeDriver](https://chromedriver.chromium.org/) is necessary for web crawling when running 'zillow_scrape_v1.py'


### Installation

There is no need for installation.
The required files are:
* zillow_scrape_v1.py
* data_visualizer_v1.py
* real_estate_database_example.db


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.


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


<!-- ROADMAP -->

<!-- ## Roadmap

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a list of proposed features (and known issues). -->


<!-- CONTRIBUTING -->
## Contributing

Although this project is intended to be personal, any suggestion or contributions are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
<!-- ## License
Distributed under the MIT License. See `LICENSE` for more information. -->

<!-- CONTACT -->
## Contact

Brian (In Sik) Cho - [bischo91@gmail.com](bischo91@gmail.com)

Project Link: [https://github.com/bischo91/RealEstateDataCrawling](https://github.com/bischo91/RealEstateDataCrawling)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- [contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png -->
