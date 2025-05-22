from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import logging
from coingecko import CoinGeckoAPI
from utils import (
    calculate_volatility_24h_ratio,
    process_historical_data,
    generate_csv,
    get_file_response,
    summarize_data
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Crypto Data API",
    description="API for fetching cryptocurrency data with enhanced CSV export features",
    version="1.0.0"
)

@app.get("/crypto/{symbol}")
async def get_crypto_summary(symbol: str):
    """Get real-time cryptocurrency summary."""
    try:
        symbol = symbol.lower().strip()
        data = CoinGeckoAPI.get_crypto_summary(symbol)
        summary = summarize_data(data)
        return summary
    except Exception as e:
        logger.error(f"Error in get_crypto_summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crypto/history/{symbol}")
async def get_crypto_history(
    symbol: str,
    days: int = Query(1, ge=1, le=365),
    include_pct_change: bool = False
):
    """Get historical price data."""
    try:
        symbol = symbol.lower().strip()
        data = CoinGeckoAPI.get_historical_data(symbol, days)
        df = process_historical_data(data, include_pct_change)
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error in get_crypto_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crypto/history/{symbol}/download/basic")
async def download_basic_csv(symbol: str, days: int = Query(1, ge=1, le=365)):
    """Download basic CSV file."""
    try:
        symbol = symbol.lower().strip()
        data = CoinGeckoAPI.get_historical_data(symbol, days)
        df = process_historical_data(data)
        filepath = generate_csv(df, is_full=False)
        return get_file_response(filepath, f"{symbol}_basic_history.csv")
    except Exception as e:
        logger.error(f"Error in download_basic_csv: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/crypto/history/{symbol}/download/full")
async def download_full_csv(symbol: str, days: int = Query(1, ge=1, le=365)):
    """Download full CSV file with enhanced features."""
    try:
        symbol = symbol.lower().strip()
        data = CoinGeckoAPI.get_historical_data(symbol, days)
        df = process_historical_data(data, include_pct_change=True)
        filepath = generate_csv(df, is_full=True)
        return get_file_response(filepath, f"{symbol}_full_history.csv")
    except Exception as e:
        logger.error(f"Error in download_full_csv: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
