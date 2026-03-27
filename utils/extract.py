import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://fashion-studio.dicoding.dev"

def get_page(session, page_number):
    """Ambil HTML dari satu halaman."""
    try:
        if page_number == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}/page{page_number}"
        
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal ambil halaman {page_number}: {e}")
        return None

def parse_products(html, timestamp):
    """Parse produk dari HTML satu halaman."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        products = []
        
        cards = soup.find_all("div", class_="collection-card")
        
        for card in cards:
            try:
                title_tag = card.find("h3", class_="product-title")
                title = title_tag.text.strip() if title_tag else None

                price_tag = card.find("span", class_="price")
                if price_tag:
                    price = price_tag.text.strip()
                else:
                    price_unavail = card.find("p", class_="price-unavailable") or \
                                    card.find(string=lambda t: "Price Unavailable" in str(t))
                    price = "Price Unavailable" if price_unavail else None

                rating_tag = card.find("p", string=lambda t: t and "Rating:" in t)
                rating = rating_tag.text.strip() if rating_tag else None

                details = card.find_all("p")
                colors, size, gender = None, None, None
                for p in details:
                    text = p.text.strip()
                    if "Colors" in text:
                        colors = text
                    elif "Size:" in text:
                        size = text
                    elif "Gender:" in text:
                        gender = text

                products.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                    "timestamp": timestamp
                })
            except Exception as e:
                print(f"[WARN] Skip satu produk: {e}")
                continue
        
        return products
    except Exception as e:
        print(f"[ERROR] Gagal parse HTML: {e}")
        return []

def scrape_all():
    """Scrape semua 50 halaman."""
    try:
        session = requests.Session()
        all_products = []
        timestamp = datetime.now().isoformat()

        for page in range(1, 51):
            print(f"Scraping halaman {page}...")
            html = get_page(session, page)
            if html:
                products = parse_products(html, timestamp)
                all_products.extend(products)
            else:
                print(f"[WARN] Halaman {page} dilewati.")

        print(f"Total data terkumpul: {len(all_products)}")
        return all_products
    except Exception as e:
        print(f"[ERROR] scrape_all gagal: {e}")
        return []