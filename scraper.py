import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://books.toscrape.com/"

response = requests.get(url)

print("Website status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")

data = []

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    rating = book.find("p", class_="star-rating")["class"][1]
    availability = book.find(
        "p",
        class_="instock availability"
    ).text.strip()

    data.append({
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Availability": availability
    })

df = pd.DataFrame(data)
df["Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
df.to_csv("books_dataset.csv", index=False)

print("Dataset created successfully!")
print("Number of records:", len(df))
print(df.head())