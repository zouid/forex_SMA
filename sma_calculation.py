from forex_python.converter import CurrencyRates
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm

# Function to fetch historical exchange rates for EUR/USD
def fetch_exchange_rates():
    currency_rates = CurrencyRates()
    end_date = datetime.now()
    # Fetching more days to ensure we have enough data for 200-day SMA
    start_date = end_date - timedelta(days=300) 
    total_days = (end_date - start_date).days
    rates = []

    for single_date in tqdm((start_date + timedelta(n) for n in range(total_days)), total=total_days, desc="Fetching rates"):
        try:
            rate = currency_rates.get_rate('EUR', 'USD', single_date)
            rates.append((single_date, rate))
        except Exception as e:
            print(f"Error fetching rate for {single_date}: {e}")

    return rates

# Function to calculate SMAs and determine support or resistance
def calculate_smas_and_determine_levels(rates):
    df = pd.DataFrame(rates, columns=['Date', 'Rate'])
    df.set_index('Date', inplace=True)
    df['SMA_100'] = df['Rate'].rolling(window=100).mean()
    df['SMA_200'] = df['Rate'].rolling(window=200).mean()

    # Most recent price
    latest_rate = df.iloc[-1]['Rate']

    # Determine if SMAs are support or resistance
    sma_100_level = "support" if latest_rate > df.iloc[-1]['SMA_100'] else "resistance"
    sma_200_level = "support" if latest_rate > df.iloc[-1]['SMA_200'] else "resistance"

    return df.iloc[-1]['SMA_100'], df.iloc[-1]['SMA_200'], sma_100_level, sma_200_level, latest_rate

# Main execution
if __name__ == "__main__":
    rates = fetch_exchange_rates()
    if rates:
        sma_100, sma_200, sma_100_level, sma_200_level, latest_rate = calculate_smas_and_determine_levels(rates)
        print(f"Latest EUR/USD Rate: {latest_rate}")
        print(f"The 100-day SMA for EUR/USD is: {sma_100} (acting as {sma_100_level})")
        print(f"The 200-day SMA for EUR/USD is: {sma_200} (acting as {sma_200_level})")
    else:
        print("No data fetched.")
