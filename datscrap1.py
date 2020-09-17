from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver import DesiredCapabilities
import time
from selenium.webdriver.chrome.options import Options

capabilities = DesiredCapabilities.CHROME  # lines 8-11 allow the browser to bypass websites without certificates
capabilities['loggingPrefs'] = {'performance': 'ALL'}
capabilities['acceptInsecureCerts'] = True

options = Options()  # allows headless browser to run with lines 12-15
options.headless = True
options.add_argument('window-size=1920x1080')
options.add_argument("--ignore-certificate-errors")

# For the executable path you need to download and path chrome driver in your own OS.
driver = webdriver.Chrome(executable_path="C:/Users/KD/Documents/Drivers/chromedriver.exe", options=options)

job_title = []
functions = []
categories = []
reqs_id = []
jobs_id = []
countries = []
states = []
cities = []

driver.get('https://www.kpmg.monstermediaworks.ca/')
driver.implicitly_wait(2)
driver.find_element_by_css_selector("select#dd-countries > option[value='United States']").click()
driver.find_element_by_css_selector('[id="btn-search"]').click()
driver.find_element_by_css_selector('[id="perPg-100"]').click()
df = None
for num in range(1, 7):  # loops through scraper and allows it to click through multiple pages.
    if num < 7:
        break
    time.sleep(1)
    driver.find_element_by_css_selector('[id="pagination-next"]').click()
    time.sleep(1)
    content = driver.page_source
    time.sleep(1)
    soup = BeautifulSoup(content, 'lxml')

    job_elements = soup.find_all('a', attrs={'class': 'job'})

    for job in job_elements:
        pass
        jobs_title = job.find('div', attrs={'class': 'col1'})
        location = job.find('div', attrs={'class': 'col2'}).text
        country, state, city = location.split(',')
        country = country.strip('_').lower()
        state = state.strip('_').lower()
        city = city.strip('_').lower()
        country = country.replace(' ', ' ')
        state = state.replace(' ', ' ')
        city = city.replace(' ', ' ')
        rating = job.find('div', attrs={'class': 'col3'})
        category = job.find('div', attrs={'class': 'col4'})
        job_id = job.find('div', attrs={'class': 'col5'})
        req_id = job.attrs['id']  # used when extracting info from an attribute inside a

        job_title.append(jobs_title.string)
        functions.append(rating.string)
        categories.append(category.string)
        jobs_id.append(job_id.string)
        reqs_id.append(req_id)
        countries.append(country)
        states.append(state)
        cities.append(city)

        df = pd.DataFrame(
            {
                'Job Title': job_title,
                'Function': functions,
                'Category': categories,
                'Req Id': jobs_id,
                'Job Id': reqs_id,
                'Country': countries,
                'State': states,
                'City': cities
                }
            )

df.to_csv('products.csv', index=False, encoding='utf-8')  # writes the data to a csv file
