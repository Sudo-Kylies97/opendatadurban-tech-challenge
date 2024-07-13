from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import json
import psycopg2


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydatabase",
    user="myuser",
    password="mypassword"
)
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS valuations (
            rate_number TEXT PRIMARY KEY,
            legal_description TEXT,
            address TEXT,
            first_owner TEXT,
            use_code TEXT,
            rating_category TEXT,
            market_value TEXT,
            registered_extent TEXT,
            suburb TEXT,
            valuation_roll TEXT
        )
    """)
    conn.commit()


def scrape_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--enable-javascript")
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome()

    driver.get('https://valuation2022.durban.gov.za/')

    time.sleep(15)

    driver.get_screenshot_as_file("screenshot.png")

    print("switching to mainFrame")

    driver.switch_to.frame('mainFrame')

    main_frame_soup = BeautifulSoup(driver.page_source, 'html.parser')

    dropdown = driver.find_element(By.ID, 'drpSearchType')

    headings = [
        "Rate Number", "Legal Description", "Address", "First Owner",
        "Use Code", "Rating Category", "Market Value", "Registered Extent"
    ]
    data = []

    valuations = Select(dropdown)
    print("gettings valuations")
    for valuation_roll in valuations.options:
        if(valuation_roll.text):
            current_valuation = valuation_roll.text
            valuations.select_by_visible_text(current_valuation)
            time.sleep(5)
            button = driver.find_element(By.ID, 'btnGo')
            button.click()
            time.sleep(5)
            driver.get_screenshot_as_file("screenshot.png")

            driver.switch_to.frame('frmSearchCriter')

            dropdown = driver.find_element(By.ID, 'drpSuburb')
            suburbs = Select(dropdown)

            for suburb in suburbs.options:
                if(suburb.text != '[--Select Suburb--]'):
                    current_suburb = suburb.text
                    suburbs.select_by_visible_text(current_suburb)
                    time.sleep(5)
                    button = driver.find_element(By.ID, 'btnSearch')
                    button.click()
                    time.sleep(5)
                    driver.switch_to.default_content()
                    driver.switch_to.frame('mainFrame')
                    driver.switch_to.frame('frameSearch')

                    table = driver.find_element(By.CLASS_NAME, 'searchResultTable')

                    soup = BeautifulSoup(driver.page_source, 'html.parser')

                    rows = soup.find('table', class_='searchResultTable').find_all('tr')
                    try:
                        for row in rows[1:]:
                            cells = row.find_all('td')
                            print("lenght cells",len(cells))
                            print("lenght headings",len(headings))
                            if len(cells) == len(headings): 
                                print(current_valuation, ' in ', current_suburb)
                                row_data = {headings[i]: cells[i].text.strip() for i in range(len(headings))}
                                try:
                                    cur.execute("""
                                        INSERT INTO valuations (rate_number, legal_description, address, first_owner, use_code, rating_category, market_value, registered_extent, suburb, valuation_roll)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        ON CONFLICT (rate_number) DO UPDATE 
                                        SET 
                                            legal_description = EXCLUDED.legal_description,
                                            address = EXCLUDED.address,
                                            first_owner = EXCLUDED.first_owner,
                                            use_code = EXCLUDED.use_code,
                                            rating_category = EXCLUDED.rating_category,
                                            market_value = EXCLUDED.market_value,
                                            registered_extent = EXCLUDED.registered_extent,
                                            suburb = EXCLUDED.suburb,
                                            valuation_roll = EXCLUDED.valuation_roll
                                    """, (
                                        row_data["Rate Number"], row_data["Legal Description"], row_data["Address"],
                                        row_data["First Owner"], row_data["Use Code"], row_data["Rating Category"],
                                        row_data["Market Value"], row_data["Registered Extent"], current_suburb, current_valuation
                                    ))
                                    conn.commit()
                                    print(f"Inserted data for rate number: {row_data['Rate Number']}")
                                except Exception as e:
                                    print(f"Error inserting data: {e}")
                                    conn.rollback()
                    except:
                        pass
                driver.switch_to.default_content()
                driver.switch_to.frame('mainFrame')
                driver.switch_to.frame('frmSearchCriter')

                
        driver.switch_to.default_content()
        driver.switch_to.frame('mainFrame')
    driver.quit()

if __name__ == "__main__":
    create_table()
    scrape_data()
    cur.close()
    conn.close()