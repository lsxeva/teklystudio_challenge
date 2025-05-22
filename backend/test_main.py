from fastapi.testclient import TestClient
import pytest
from main import app
import pandas as pd
import os

client = TestClient(app)

def test_get_crypto_summary():
    """Test cryptocurrency summary endpoint"""
    response = client.get("/crypto/bitcoin")
    assert response.status_code == 200
    data = response.json()
    assert "current_price" in data
    assert "volatility_24h_ratio" in data

def test_get_crypto_history():
    """Test historical data endpoint"""
    response = client.get("/crypto/history/bitcoin?days=7&include_pct_change=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "timestamp" in data[0]
    assert "price" in data[0]

def test_download_basic_csv():
    """Test basic CSV download"""
    response = client.get("/crypto/history/bitcoin/download/basic?days=7")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv"
    assert "bitcoin_basic_history.csv" in response.headers["content-disposition"]

def test_download_full_csv():
    """Test full CSV download"""
    response = client.get("/crypto/history/bitcoin/download/full?days=7")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv"
    assert "bitcoin_full_history.csv" in response.headers["content-disposition"]

def test_invalid_symbol():
    """Test invalid cryptocurrency symbol"""
    response = client.get("/crypto/invalid_symbol")
    assert response.status_code == 500

def test_invalid_days():
    """Test invalid days parameter"""
    response = client.get("/crypto/history/bitcoin?days=400")
    assert response.status_code == 422

def test_symbol_normalization():
    """Test symbol normalization"""
    response = client.get("/crypto/BITCOIN")
    assert response.status_code == 200
    data = response.json()
    assert "current_price" in data 