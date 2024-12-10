import requests
from bs4 import BeautifulSoup
import os

file_path = r'path.html'

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.prettify())
product_links = soup.find_all('a', href=True)
# print(product_links)
base_url = 'baseurl'

full_product_links = []
for link in product_links:
    href = link.get('href')  # Use .get() to safely retrieve the href attribute
    if href and href.startswith('./products/'):  # Ensure it's a product link
        full_url = base_url + href.lstrip('.')  # Construct the full URL
        full_product_links.append(full_url)

print(full_product_links[0])
# Function to fetch product data from each product link
def fetch_product_data(product_url):
    # Send a GET request to the product page
    response = requests.get(product_url)

    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title
    title_tag = soup.find('h1', {'itemprop': 'name'})
    title = title_tag.get_text(strip=True) if title_tag else "No Title Found"  # Safely extract title

    # Extract price
    price_tag = soup.find('div', {'class': 'price', 'id': 'PDP_productPrice'})
    price = float(price_tag.get_text(strip=True).replace('£', '').strip()) if price_tag else 0.0  # Safely extract price
    price_unit = '£'  # Assuming GBP for now, adjust as needed

    # Extract short description
    short_desc_tag = soup.find('p', {'itemprop': 'description', 'id': 'product_shortdescription_2264934'})
    short_desc = short_desc_tag.get_text(
        strip=True) if short_desc_tag else "No Description Found"  # Safely extract short description

    # Extract rating
    rating_tag = soup.find('div', {'itemprop': 'ratingValue', 'class': 'bv_avgRating_component_container notranslate'})
    rating = float(rating_tag.get_text(strip=True)) if rating_tag else 0.0  # Safely extract rating

    # Calculate page size in KB
    page_size_kb = len(response.content) / 1024

    # Create a product dictionary
    product_data = {
        "Title": title,
        "Price": price,
        "Price_Unit": price_unit,
        "Short_Desc": short_desc,
        "Rating": rating,
        "Page_Size": round(page_size_kb, 2)  # Round to 2 decimal places
    }

    return product_data


# List to store product details
products = []

# Iterate over product HTML file paths (full_product_links contains the local file paths now)
for product_file in full_product_links:
    # Remove 'file://' prefix if present
    if product_file.startswith("file://"):
        product_file = product_file[7:]

    product_data = fetch_product_data(product_file)
    if product_data:
        products.append(product_data)

# Calculate the median price
prices = [product["Price"] for product in products]
prices.sort()
n = len(prices)
if n % 2 == 1:
    median = prices[n // 2]
else:
    median = (prices[n // 2 - 1] + prices[n // 2]) / 2

# Create the final data structure
final_data = {
    "Products": products,
    "Median": round(median, 2)
}

print(final_data)