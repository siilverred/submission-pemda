import pandas as pd

EXCHANGE_RATE = 16000

def clean_price(price_str):
    """Konversi price dari USD string ke float rupiah."""
    try:
        if pd.isna(price_str) or "Unavailable" in str(price_str):
            return None
        cleaned = str(price_str).replace("$", "").strip()
        return float(cleaned) * EXCHANGE_RATE
    except Exception:
        return None

def clean_rating(rating_str):
    """Ekstrak angka float dari string rating."""
    try:
        if pd.isna(rating_str):
            return None
        import re
        match = re.search(r"(\d+\.\d+|\d+)", str(rating_str))
        if match:
            return float(match.group(1))
        return None
    except Exception:
        return None

def clean_colors(colors_str):
    """Ekstrak angka dari string colors."""
    try:
        if pd.isna(colors_str):
            return None
        import re
        match = re.search(r"(\d+)", str(colors_str))
        return int(match.group(1)) if match else None
    except Exception:
        return None

def clean_size(size_str):
    """Hapus prefix 'Size: '."""
    try:
        if pd.isna(size_str):
            return None
        return str(size_str).replace("Size:", "").strip()
    except Exception:
        return None

def clean_gender(gender_str):
    """Hapus prefix 'Gender: '."""
    try:
        if pd.isna(gender_str):
            return None
        return str(gender_str).replace("Gender:", "").strip()
    except Exception:
        return None

def transform(raw_data):
    """Jalankan seluruh transformasi."""
    try:
        df = pd.DataFrame(raw_data)

        # Bersihkan tiap kolom
        df["Price"] = df["Price"].apply(clean_price)
        df["Rating"] = df["Rating"].apply(clean_rating)
        df["Colors"] = df["Colors"].apply(clean_colors)
        df["Size"] = df["Size"].apply(clean_size)
        df["Gender"] = df["Gender"].apply(clean_gender)

        # Hapus invalid: Unknown Product, null, duplikat
        df = df[df["Title"] != "Unknown Product"]
        df = df.dropna()
        df = df.drop_duplicates()

        # Pastikan tipe data
        df["Price"] = df["Price"].astype(float)
        df["Rating"] = df["Rating"].astype(float)
        df["Colors"] = df["Colors"].astype(int)
        df["Size"] = df["Size"].astype(str)
        df["Gender"] = df["Gender"].astype(str)
        df["Title"] = df["Title"].astype(str)
        df["timestamp"] = df["timestamp"].astype(str)

        print(f"Data setelah transformasi: {len(df)} baris")
        return df
    except Exception as e:
        print(f"[ERROR] transform gagal: {e}")
        return pd.DataFrame()