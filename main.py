import csv
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    # JSON state will be stored after initial run using username and password to save storage state
    # This will save login data and the effort of loging in everytime
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.goto("https://www.swiggy.com/my-account")

    # Store price and date information to a list
    price_list = []
    date_list = []

    while page.locator("text=Show More Orders"):
        page.is_visible("div._3tDvm" )
        html = page.inner_html("._1stFr")
        soup = BeautifulSoup(html, "html.parser")
        prices = soup.find_all("span", {"class": "_3Hghg"})
        for price in prices:
            price_list.append(int(price.text))
        dates = soup.find_all("div", {"class": "_2fkm7"})
        for date in dates:
            spans = date.find_all("span")
            date_list.append(spans[0].text)
        with open("swiggy_data.csv", "w", newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(["price", "date"])
            for i in range(len(price_list)):
                csvwriter.writerow([price_list[i], date_list[i]])
        page.locator("text=Show More Orders").click()
        price_list = []
        date_list = []

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
