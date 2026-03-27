import pytest
import pandas as pd
from utils.transform import (
    clean_price, clean_rating, clean_colors,
    clean_size, clean_gender, transform
)

def test_clean_price_valid():
    assert clean_price("$50.00") == 50.00 * 16000

def test_clean_price_unavailable():
    assert clean_price("Price Unavailable") is None

def test_clean_price_none():
    assert clean_price(None) is None

def test_clean_rating_valid():
    assert clean_rating("Rating: ⭐ 4.5 / 5") == 4.5

def test_clean_rating_invalid():
    assert clean_rating("Invalid Rating") is None

def test_clean_colors_valid():
    assert clean_colors("3 Colors") == 3

def test_clean_size_valid():
    assert clean_size("Size: M") == "M"

def test_clean_gender_valid():
    assert clean_gender("Gender: Men") == "Men"

def test_transform_removes_unknown():
    data = [
        {"Title": "Unknown Product", "Price": "$100.00", "Rating": "Invalid Rating / 5",
         "Colors": "5 Colors", "Size": "Size: M", "Gender": "Gender: Men", "timestamp": "2024-01-01"},
        {"Title": "T-shirt 1", "Price": "$50.00", "Rating": "Rating: ⭐ 4.5 / 5",
         "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men", "timestamp": "2024-01-01"},
    ]
    df = transform(data)
    assert "Unknown Product" not in df["Title"].values

def test_transform_no_nulls():
    data = [
        {"Title": "T-shirt 1", "Price": "$50.00", "Rating": "Rating: ⭐ 4.5 / 5",
         "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men", "timestamp": "2024-01-01"},
    ]
    df = transform(data)
    assert df.isnull().sum().sum() == 0

def test_transform_price_in_rupiah():
    data = [
        {"Title": "T-shirt 1", "Price": "$50.00", "Rating": "Rating: ⭐ 4.5 / 5",
         "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men", "timestamp": "2024-01-01"},
    ]
    df = transform(data)
    assert df["Price"].iloc[0] == 50.00 * 16000

def test_transform_no_duplicates():
    row = {"Title": "T-shirt 1", "Price": "$50.00", "Rating": "Rating: ⭐ 4.5 / 5",
           "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men", "timestamp": "2024-01-01"}
    df = transform([row, row])
    assert len(df) == 1

def test_clean_price_zero():
    from utils.transform import clean_price
    assert clean_price("$0.00") == 0.0

def test_clean_colors_none():
    from utils.transform import clean_colors
    assert clean_colors(None) is None

def test_clean_size_none():
    from utils.transform import clean_size
    assert clean_size(None) is None

def test_clean_gender_none():
    from utils.transform import clean_gender
    assert clean_gender(None) is None

def test_transform_empty_input():
    from utils.transform import transform
    df = transform([])
    assert df.empty