import pytest
from unittest.mock import MagicMock, patch
from utils.extract import get_page, parse_products, scrape_all

MOCK_HTML = """
<div class="collection-card">
  <h3 class="product-title">T-shirt 1</h3>
  <span class="price">$50.00</span>
  <p>Rating: ⭐ 4.5 / 5</p>
  <p>3 Colors</p>
  <p>Size: M</p>
  <p>Gender: Men</p>
</div>
"""

def test_get_page_success():
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "<html>OK</html>"
    mock_response.raise_for_status = MagicMock()
    mock_session.get.return_value = mock_response

    result = get_page(mock_session, 1)
    assert result == "<html>OK</html>"

def test_get_page_failure():
    import requests
    mock_session = MagicMock()
    mock_session.get.side_effect = requests.exceptions.ConnectionError("fail")

    result = get_page(mock_session, 1)
    assert result is None

def test_parse_products_returns_list():
    result = parse_products(MOCK_HTML, "2024-01-01T00:00:00")
    assert isinstance(result, list)
    assert len(result) > 0

def test_parse_products_fields():
    result = parse_products(MOCK_HTML, "2024-01-01T00:00:00")
    product = result[0]
    assert "Title" in product
    assert "Price" in product
    assert "Rating" in product
    assert "Colors" in product
    assert "Size" in product
    assert "Gender" in product
    assert "timestamp" in product

def test_scrape_all_returns_list():
    with patch("utils.extract.get_page", return_value=MOCK_HTML):
        result = scrape_all()
        assert isinstance(result, list)
        assert len(result) > 0