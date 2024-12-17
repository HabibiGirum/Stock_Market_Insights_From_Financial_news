import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import seaborn as sns

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
        Prepare data by parsing dates and merging news and stock datasets.
        """
        # Parse dates in news_df and stock_df
        self.news_df['date'] = pd.to_datetime(self.news_df['date'], errors='coerce').dt.date
        self.stock_df['Date'] = pd.to_datetime(self.stock_df['Date'], errors='coerce').dt.date

        # Merge datasets on the date column
        self.merged_df = pd.merge(self.news_df, self.stock_df, left_on='date', right_on='Date', how='inner')

        # Perform sentiment analysis
        self.merged_df['sentiment_score'] = self.merged_df['headline'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )

        # Drop rows with NaN values
        self.merged_df.dropna(subset=['sentiment_score', 'Close'], inplace=True)

        print("Data Preparation Completed. Merged Data Preview:")
        print(self.merged_df.head())

    def calculate_daily_returns(self):
        """
        Calculate daily percentage change in stock closing prices.
        """
        # Calculate daily percentage return
        self.merged_df['Daily_Return'] = self.merged_df['Close'].pct_change()

        # Shift sentiment scores to align with previous day's stock movement
        self.merged_df['Shifted_Sentiment'] = self.merged_df['sentiment_score'].shift(1)

        # Drop rows with NaN values
        self.merged_df.dropna(subset=['Daily_Return', 'Shifted_Sentiment'], inplace=True)

        print("Daily Returns and Shifted Sentiment Calculation Complete.")
        print(self.merged_df[['Date', 'Daily_Return', 'Shifted_Sentiment']].head())

    def analyze_correlation(self):
        """
        Compute Pearson correlation between daily sentiment scores and stock returns.
        """
        # Drop rows with missing values
        analysis_df = self.merged_df.dropna(subset=['Daily_Return', 'Shifted_Sentiment'])

        # Calculate Pearson correlation coefficient
        correlation, p_value = pearsonr(analysis_df['Shifted_Sentiment'], analysis_df['Daily_Return'])

        print("Correlation Analysis Complete.")
        return {
            "Correlation_Coefficient": correlation,
            "P_Value": p_value
        }

    def plot_correlation_heatmap(self):
        """
        Plot a refined correlation heatmap focusing on relevant features.
        """
        if self.merged_df is None or self.merged_df.empty:
            raise ValueError("Merged data is not prepared. Run prepare_data() first.")

        # Drop unnecessary columns
        refined_df = self.merged_df.drop(columns=['Unnamed: 0'], errors='ignore')

        # Select only numeric columns for correlation
        numeric_df = refined_df.select_dtypes(include=['number'])

        # Compute correlation matrix
        correlation_matrix = numeric_df.corr()

        # Plot refined heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='viridis', linewidths=0.5, fmt=".2f")
        plt.title("Refined Correlation Heatmap of the Dataset")
        plt.show()


    def summarize_analysis(self):
        """
        Summarize correlation results and insights.
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

        print("\nSummary of Analysis:")
        print(summary)
        return summary
