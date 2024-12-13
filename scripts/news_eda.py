import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud

class NewsEDA:
    def __init__(self, dataframe):
        """
        Initialize the class with a pandas DataFrame.
        """
        self.df = dataframe
        self.analyzer = SentimentIntensityAnalyzer()

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
        def analyze_sentiment(headline):
            scores = self.analyzer.polarity_scores(headline)
            return scores['compound']

        self.df['sentiment'] = self.df['headline'].apply(analyze_sentiment)
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

    def extract_keywords(self, max_features=20):
        """
        Extract common keywords from headlines.
        """
        vectorizer = CountVectorizer(stop_words='english', max_features=max_features)
        X = vectorizer.fit_transform(self.df['headline'])
        keywords = vectorizer.get_feature_names_out()
        return keywords

    def analyze_publication_trends(self):
        """
        Analyze publication frequency over time.
        """
        self.df['date'] = pd.to_datetime(self.df['date'])
        publication_trends = self.df.resample('D', on='date').size()
        publication_trends.plot(figsize=(12, 6), color='blue')
        plt.title('Publication Frequency Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.show()
        return publication_trends

    def analyze_publishing_times(self):
        """
        Analyze publishing times by hour.
        """
        self.df['hour'] = self.df['date'].dt.hour
        articles_by_hour = self.df['hour'].value_counts().sort_index()
        articles_by_hour.plot(kind='bar', figsize=(10, 6), color='purple')
        plt.title('Publication Frequency by Hour')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Articles')
        plt.show()
        return articles_by_hour

    def generate_wordcloud_for_publishers(self, top_n=10):
        """
        Generate word clouds for top publishers.
        """
        top_publishers = self.df['publisher'].value_counts().head(top_n)
        for publisher in top_publishers.index:
            text = " ".join(self.df[self.df['publisher'] == publisher]['headline'])
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.title(f'WordCloud for {publisher}')
            plt.axis('off')
            plt.show()

    def extract_unique_domains(self):
        """
        Extract unique domains from publisher email addresses.
        """
        self.df['domain'] = self.df['publisher'].str.extract(r'@(.+)$')
        domain_counts = self.df['domain'].value_counts()
        return domain_counts

    