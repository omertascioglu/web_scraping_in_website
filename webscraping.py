import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv


def search_marketpaketi_barcode_name(barcode_number):
    url = f"https://www.marketpaketi.com.tr/search?q={barcode_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first search result that contains the barcode number.
    search_result = soup.find("a", class_="urun_gorsel")
    if search_result is None:
        print("Empty search result")
        return None

    # Extract the href attribute value
    link_name = search_result['href']

    return link_name


def link_to_find_name(link_name):
    response = requests.get(link_name)
    soup = BeautifulSoup(response.content, "html.parser")
    search_result = soup.find("h1", class_="detay_baslik")
    if search_result is None:
        print("Empty product name search result")
        return None

    product_name = search_result.text
    return product_name


def link_to_find_brand(link_name):
    response = requests.get(link_name)
    soup = BeautifulSoup(response.content, "html.parser")
    search_result = soup.find("a", class_="detay_kategori")
    if search_result is None:
        print("Empty brand search result")
        return None

    product_brand = search_result.text
    return product_brand


def link_to_find_price(link_name):
    response = requests.get(link_name)
    soup = BeautifulSoup(response.content, "html.parser")
    search_result = soup.find("div", class_="yeni_fiyat")
    if search_result is None:
        print("Empty price search result")
        return None

    product_price = search_result.text
    return product_price


def link_to_find_cat(link_name):
    response = requests.get(link_name)
    soup = BeautifulSoup(response.content, "html.parser")

    category_container = soup.find('div', class_='navigasyon_ic')

    category_links = category_container.find_all('a')

    list_of_categories = []

    for link in category_links:
        category_name = link.text.strip()
        list_of_categories.append(category_name)

    return list_of_categories


def main():
    """Iterates over a list of barcode numbers and checks their names."""
    df = pd.read_csv("trendbox.csv")
    csv_file = "sample_data.csv"

    barcode_numbers = df["BARCODE"]

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["BARCODE", "PRODUCT_NAME", "PRODUCT_BRAND", "PRODUCT_PRICE", "CATEGORIES"])

    for barcode_number in barcode_numbers:
        link_namesp = search_marketpaketi_barcode_name(barcode_number)
        if link_namesp is None:
            continue
        product_name = link_to_find_name(link_namesp)
        product_brand = link_to_find_brand(link_namesp)
        product_price = link_to_find_price(link_namesp)
        product_cat = link_to_find_cat(link_namesp)

        # If the barcode name is found, print it.
        if product_name is not None:
            print(
                f"Barcode name for {barcode_number}: {product_name} and brand is {product_brand} and price is {product_price} and category is {product_cat}")

            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([barcode_number, product_name, product_brand, product_price, ','.join(product_cat)])

    print(f"Data has been written to {csv_file}.")


if __name__ == "__main__":
    main()
