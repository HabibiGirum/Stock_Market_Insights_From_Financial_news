import pandas as pd
import matplotlib.pyplot as plt
import talib
import pynance as pn

class StockAnalysis:
    def __init__(self, dataframe):
        """
        Initialize the StockAnalysis class with a pandas DataFrame.
        """
        self.df = dataframe

    def prepare_data(self):
        """
        Ensure data is correctly formatted and check for required columns.
        """
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in self.df.columns for col in required_columns):
            raise ValueError(f"DataFrame must include the following columns: {required_columns}")
        self.df['Date'] = pd.to_datetime(self.df['Date'])  # Ensure the Date column is datetime
        self.df.set_index('Date', inplace=True)
        return self.df.head()

    def calculate_technical_indicators(self):
        """
        Calculate and add common technical indicators using TA-Lib.
        """
        # Moving Averages
        self.df['SMA_20'] = talib.SMA(self.df['Close'], timeperiod=20)
        self.df['EMA_20'] = talib.EMA(self.df['Close'], timeperiod=20)

        # Relative Strength Index (RSI)
        self.df['RSI'] = talib.RSI(self.df['Close'], timeperiod=14)

        # Moving Average Convergence Divergence (MACD)
        self.df['MACD'], self.df['MACD_signal'], self.df['MACD_hist'] = talib.MACD(
            self.df['Close'], fastperiod=12, slowperiod=26, signalperiod=9
        )

        return self.df[['SMA_20', 'EMA_20', 'RSI', 'MACD', 'MACD_signal', 'MACD_hist']].head()

    def calculate_financial_metrics(self):
        """
        Use PyNance to calculate additional financial metrics.
        """
        # Example: Daily returns and volatility
        self.df['Daily_Return'] = self.df['Close'].pct_change()
        self.df['Volatility'] = self.df['Daily_Return'].rolling(window=20).std()

        return self.df[['Daily_Return', 'Volatility']].head()

    def visualize_data(self):
        """
        Create visualizations for stock prices and technical indicators.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.df['Close'], label='Close Price', color='blue')
        plt.plot(self.df['SMA_20'], label='20-day SMA', color='red', linestyle='--')
        plt.plot(self.df['EMA_20'], label='20-day EMA', color='green', linestyle='--')
        plt.title('Stock Price with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

        plt.figure(figsize=(12, 6))
        plt.plot(self.df['RSI'], label='RSI', color='purple')
        plt.axhline(70, color='red', linestyle='--', label='Overbought')
        plt.axhline(30, color='green', linestyle='--', label='Oversold')
        plt.title('Relative Strength Index (RSI)')
        plt.xlabel('Date')
        plt.ylabel('RSI Value')
        plt.legend()
        plt.show()

        plt.figure(figsize=(12, 6))
        plt.plot(self.df['MACD'], label='MACD', color='blue')
        plt.plot(self.df['MACD_signal'], label='Signal Line', color='orange')
        plt.bar(self.df.index, self.df['MACD_hist'], label='Histogram', color='gray', alpha=0.5)
        plt.title('MACD')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.show()

    def validate_indicators(self):
        """
        Validate the accuracy of indicators by checking for completeness and missing values.
        """
        missing_data = self.df.isnull().sum()
        return missing_data[missing_data > 0]

    