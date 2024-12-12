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
    
    