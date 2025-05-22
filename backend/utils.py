import pandas as pd
import numpy as np
from typing import Dict
import os
from datetime import datetime
from fastapi.responses import FileResponse
import tempfile

def calculate_volatility_24h_ratio(high: float, low: float, current_price: float) -> float:
    """Calculate 24-hour volatility ratio."""
    return (high - low) / current_price if current_price else None

def process_historical_data(data: Dict, include_pct_change: bool = False) -> pd.DataFrame:
    """Process historical price data."""
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    if include_pct_change:
        df['pct_change'] = df['price'].pct_change() * 100
        df['rolling_avg_3d'] = df['price'].rolling(window=3).mean()
        df['volatility_3d'] = df['pct_change'].rolling(window=3).std()

    return df

def generate_csv(df: pd.DataFrame, is_full: bool = False) -> str:
    """Generate CSV file from DataFrame."""
    temp_dir = tempfile.mkdtemp()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if is_full:
        filename = f"crypto_history_full_{timestamp}.csv"
        columns = ['timestamp', 'price', 'pct_change', 'rolling_avg_3d', 'volatility_3d']
    else:
        filename = f"crypto_history_basic_{timestamp}.csv"
        columns = ['timestamp', 'price']

    filepath = os.path.join(temp_dir, filename)
    df[columns].to_csv(filepath, index=False)
    return filepath

def get_file_response(filepath: str, filename: str) -> FileResponse:
    """Create a file response for downloading."""
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type='text/csv'
    )

def summarize_data(data: dict) -> dict:
    """Summarize key statistics from market data."""
    def safe_float(value):
        return float(value) if isinstance(value, (int, float)) else None

    current_price = safe_float(data.get("current_price"))
    high_24h = safe_float(data.get("high_24h"))
    low_24h = safe_float(data.get("low_24h"))

    volatility = round((high_24h - low_24h) / current_price, 4) \
        if high_24h and low_24h and current_price else None

    return {
        "name": data.get("name"),
        "symbol": data.get("symbol"),
        "current_price": current_price,
        "high_24h": high_24h,
        "low_24h": low_24h,
        "volatility_24h_ratio": volatility,
        "price_change_percentage_1h": data.get("price_change_percentage_1h_in_currency"),
        "price_change_percentage_24h": data.get("price_change_percentage_24h_in_currency"),
        "price_change_percentage_7d": data.get("price_change_percentage_7d_in_currency"),
        "price_change_percentage_30d": data.get("price_change_percentage_30d_in_currency"),
        "market_cap": safe_float(data.get("market_cap")),
        "total_volume": safe_float(data.get("total_volume"))
    }
