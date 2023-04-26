import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver


# fixed your zoo of a function
def get_product_info(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    products = soup.find_all("div", {'data-testid': 'product-pod'})

    product_info = []
    try:
        for product in products:
            name_tag = product.find(
                "div", {'data-testid': 'product-header'}).text
            try:
                model = product.find(
                    'div', {'style': 'min-height:21px'}).text.translate(str.maketrans("", "", "Model# "))
            except:
                model = None
            price = product.find(
                'div', class_="price-format__main-price").text

            product_info.append(
                dict(name_tag=name_tag, model=model, price=price))

        return product_info
    except Exception as e:
        print(e)


# runs your function only if the file itself is called. And not if it is imported
if __name__ == '__main__':
    url = "https://www.homedepot.com/b/Electrical-Wire-Building-Wires-NM-Wires/Pick-Up-Today/250-ft/Pre-Cut-Length/N-5yc1vZ2fkpc4xZ1z0ulq4Z1z175a5Z1z1ugzt"

    print(f"Scraping product information from {url}")
    print(get_product_info(url))

    print("\nDone.")
