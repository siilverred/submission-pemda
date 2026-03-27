import pytest
import pandas as pd
import os
from utils.load import load_to_csv

@pytest.fixture
def sample_df():
    return pd.DataFrame([{
        "Title": "T-shirt 1",
        "Price": 800000.0,
        "Rating": 4.5,
        "Colors": 3,
        "Size": "M",
        "Gender": "Men",
        "timestamp": "2024-01-01T00:00:00"
    }])

def test_load_to_csv_creates_file(sample_df, tmp_path):
    filepath = str(tmp_path / "test_products.csv")
    load_to_csv(sample_df, filepath)
    assert os.path.exists(filepath)

def test_load_to_csv_correct_content(sample_df, tmp_path):
    filepath = str(tmp_path / "test_products.csv")
    load_to_csv(sample_df, filepath)
    loaded = pd.read_csv(filepath)
    assert "Title" in loaded.columns
    assert loaded.iloc[0]["Title"] == "T-shirt 1"

def test_load_to_csv_empty_df():
    df = pd.DataFrame()
    # Tidak crash, hanya print error
    load_to_csv(df, "dummy.csv")

def test_load_to_csv_row_count(sample_df, tmp_path):
    filepath = str(tmp_path / "test_products.csv")
    load_to_csv(sample_df, filepath)
    loaded = pd.read_csv(filepath)
    assert len(loaded) == 1

def test_load_to_csv_multiple_rows(tmp_path):
    df = pd.DataFrame([
        {"Title": "A", "Price": 100.0, "Rating": 4.0, "Colors": 2, "Size": "S", "Gender": "Men", "timestamp": "2024-01-01"},
        {"Title": "B", "Price": 200.0, "Rating": 3.5, "Colors": 1, "Size": "L", "Gender": "Women", "timestamp": "2024-01-01"},
    ])
    filepath = str(tmp_path / "multi.csv")
    load_to_csv(df, filepath)
    loaded = pd.read_csv(filepath)
    assert len(loaded) == 2

def test_load_to_postgresql_empty_df():
    from utils.load import load_to_postgresql
    df = pd.DataFrame()
    load_to_postgresql(df, "postgresql://fake")

def test_load_to_google_sheets_empty_df():
    from utils.load import load_to_google_sheets
    df = pd.DataFrame()
    load_to_google_sheets(df, "fake_id")