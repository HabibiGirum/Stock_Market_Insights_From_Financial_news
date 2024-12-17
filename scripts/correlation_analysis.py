import pandas as pd
from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

class NewsStockCorrelation:
    def __init__(self, news_df, stock_df):
        """
        Initialize the NewsStockCorrelation class with news and stock DataFrames.
        """
        if news_df.empty or stock_df.empty:
            raise ValueError("Input DataFrames cannot be empty.")

        self.news_df = news_df.copy()
        self.stock_df = stock_df.copy()
        self.merged_df = None

    def prepare_data(self):
        """
        Normalize and align dates in both datasets to ensure compatibility.
        """
        # Ensure datetime format
        self.news_df['date'] = pd.to_datetime(self.news_df['date']).dt.date
        self.stock_df['Date'] = pd.to_datetime(self.stock_df['Date']).dt.date

        # Group news data by date and aggregate headlines into lists
        grouped_news = self.news_df.groupby('date')['headline'].apply(list).reset_index()

        # Merge stock and grouped news data
        self.merged_df = pd.merge(
            self.stock_df,
            grouped_news,
            left_on='Date',
            right_on='date',
            how='left'
        )

        # Drop duplicate date column
        self.merged_df.drop('date', axis=1, inplace=True)

        print("Data Preparation Complete: Stock and News Data Merged.")
        return self.merged_df.head()

    def perform_sentiment_analysis(self):
        """
        Assign sentiment scores to news headlines using TextBlob.
        """
        def calculate_sentiment(headlines):
            if pd.isna(headlines) or not headlines:  # Handle empty or NaN headlines
                return None
            return np.mean([TextBlob(headline).sentiment.polarity for headline in headlines])

        # Compute sentiment score
        self.merged_df['Sentiment_Score'] = self.merged_df['headline'].apply(calculate_sentiment)

        print("Sentiment Analysis Complete: Sentiment Scores Computed.")
        return self.merged_df[['Date', 'Sentiment_Score']].head()

    def calculate_daily_returns(self):
        """
        Calculate daily percentage change in stock closing prices.
        """
        # Daily percentage return
        self.merged_df['Daily_Return'] = self.merged_df['Close'].pct_change()

        # Shift sentiment scores to align with previous day's stock movement
        self.merged_df['Shifted_Sentiment'] = self.merged_df['Sentiment_Score'].shift(1)

        print("Daily Returns and Sentiment Shift Complete.")
        return self.merged_df[['Date', 'Daily_Return', 'Shifted_Sentiment']].head()

    def analyze_correlation(self):
        """
        Compute Pearson correlation between daily sentiment scores and stock returns.
        """
        # Drop rows with missing values
        analysis_df = self.merged_df.dropna(subset=['Daily_Return', 'Shifted_Sentiment'])

        if analysis_df.empty:
            raise ValueError("No valid data available for correlation analysis.")

        # Calculate Pearson correlation coefficient
        correlation, p_value = pearsonr(analysis_df['Shifted_Sentiment'], analysis_df['Daily_Return'])

        print("Correlation Analysis Complete.")
        return {
            "Correlation_Coefficient": correlation,
            "P_Value": p_value
        }

    def visualize_correlation(self):
        """
        Visualize the relationship between sentiment scores and stock returns.
        """
        analysis_df = self.merged_df.dropna(subset=['Daily_Return', 'Shifted_Sentiment'])

        plt.figure(figsize=(10, 6))
        plt.scatter(analysis_df['Shifted_Sentiment'], analysis_df['Daily_Return'], alpha=0.6, color='blue')
        plt.title('Sentiment Scores vs. Stock Daily Returns')
        plt.xlabel('Shifted Sentiment Score')
        plt.ylabel('Daily Return (%)')
        plt.grid(True)
        plt.show()

    def summarize_analysis(self):
        """
        Summarize key findings from correlation analysis.
        """
        correlation_results = self.analyze_correlation()
        correlation = correlation_results['Correlation_Coefficient']

        # Interpret correlation strength
        if abs(correlation) > 0.5:
            insight = "Strong correlation"
        elif 0.2 < abs(correlation) <= 0.5:
            insight = "Moderate correlation"
        else:
            insight = "Weak or no correlation"

        summary = {
            "Correlation_Coefficient": correlation,
            "P_Value": correlation_results['P_Value'],
            "Insights": insight
        }

        print("Summary of Analysis:")
        return summary
