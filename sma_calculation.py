from forex_python.converter import CurrencyRates
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm  # Import tqdm

# Function to fetch historical exchange rates for EUR/USD
def fetch_exchange_rates():
    currency_rates = CurrencyRates()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=150)  # Adjust as needed to ensure 100 rates
    total_days = (end_date - start_date).days

    rates = []

    # Adding total=total_days to tqdm to ensure the progress bar knows the total count
    for single_date in tqdm((start_date + timedelta(n) for n in range(total_days)), total=total_days, desc="Fetching rates"):
        try:
            rate = currency_rates.get_rate('EUR', 'USD', single_date)
            rates.append(rate)
        except Exception as e:
            print(f"Error fetching rate for {single_date}: {e}")

    return rates

# Function to calculate the SMA
def calculate_sma(values, window):
    return pd.Series(values).rolling(window=window).mean().iloc[-1]

# Main execution
if __name__ == "__main__":
    rates = fetch_exchange_rates()
    if rates:
        sma_100_day = calculate_sma(rates, 100)
        print(f"The 100-day SMA for EUR/USD is: {sma_100_day}")
    else:
        print("No data fetched.")
