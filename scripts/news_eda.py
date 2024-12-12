import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud

class NewsEDA:
    def __init__(self, dataframe):
        """
        Initialize the class with a pandas DataFrame.
        """
        self.df = dataframe
    
    def calculate_headline_length(self):
        """
        Add a column for headline length and return descriptive statistics.
        """
        self.df['headline_length'] = self.df['headline'].apply(len)
        return self.df['headline_length'].describe()
    
    def count_articles_per_publisher(self, top_n=10):
        """
        Count the number of articles per publisher and return the top publishers.
        """
        publisher_counts = self.df['publisher'].value_counts()
        publisher_counts.head(top_n).plot(kind='bar', figsize=(10, 6), color='skyblue')
        plt.title('Top Publishers')
        plt.xlabel('Publisher')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
        plt.show()
        return publisher_counts
    
    def analyze_publication_dates(self):
        """
        Analyze publication trends over days of the week.
        """
        self.df['date'] = pd.to_datetime(self.df['date'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        articles_by_day = self.df['day_of_week'].value_counts()
        articles_by_day.plot(kind='bar', figsize=(8, 5), color='orange')
        plt.title('Articles Published by Day of the Week')
        plt.xlabel('Day')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
        plt.show()
        return articles_by_day
    
    def perform_sentiment_analysis(self):
        """
        Perform sentiment analysis on headlines and categorize the sentiment.
        """
        self.df['sentiment'] = self.df['headline'].apply(lambda x: TextBlob(x).sentiment.polarity)
        self.df['sentiment_category'] = pd.cut(
            self.df['sentiment'], bins=[-1, -0.1, 0.1, 1], labels=['Negative', 'Neutral', 'Positive']
        )
        sentiment_counts = self.df['sentiment_category'].value_counts()
        sentiment_counts.plot(kind='bar', figsize=(8, 5), color=['red', 'gray', 'green'])
        plt.title('Sentiment Distribution')
        plt.xlabel('Sentiment')
        plt.ylabel('Number of Articles')
        plt.show()
        return sentiment_counts
    
    