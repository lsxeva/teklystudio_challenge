import requests
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    def get_crypto_summary(symbol: str) -> Dict:
        """Fetch real-time market data for a cryptocurrency."""
        try:
            response = requests.get(
                f"{CoinGeckoAPI.BASE_URL}/coins/markets",
                params={
                    "vs_currency": "usd",
                    "ids": symbol,
                    "price_change_percentage": "1h,24h,7d,30d"
                }
            )
            response.raise_for_status()
            data = response.json()
            if not data:
                raise ValueError(f"Symbol '{symbol}' not found.")
            return data[0]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching crypto summary: {str(e)}")
            raise

    @staticmethod
    def get_historical_data(symbol: str, days: int) -> Dict:
        """Fetch historical market data for a cryptocurrency."""
        try:
            response = requests.get(
                f"{CoinGeckoAPI.BASE_URL}/coins/{symbol}/market_chart",
                params={
                    "vs_currency": "usd",
                    "days": days,
                    "interval": "daily"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            raise
