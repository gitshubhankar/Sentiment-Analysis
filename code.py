import requests
from bs4 import BeautifulSoup
import re
import nltk
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('vader_lexicon')

# Define the URL of the web page to scrape
url = "https://www.theindiaforum.in/economy/poverty-india-over-last-decade#:~:text=The%20NITI%20Aayog's%20own%20calculation,implies%20around%20145%20million%20people."  # Replace with your URL

# Send a request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')



# Locate the title and content
title = soup.find('h1')
article_title = title.get_text(separator=' ', strip=True) if title else "Title not found"

# Debugging: Print the title to verify it's correct
print("Extracted Title:", article_title)

# Check the specific class in the HTML
article = soup.find('div', class_='layout layout--twocol-section layout--twocol-section--75-25 limited-container pos_relative')
if article:
    article_text = article.get_text(separator=' ', strip=True)
else:
    article_text = "Article content not found"

print("Content:", article_text)

# Function to preprocess the text
def preprocess(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    words = text.split()  # Split into words
    return words

# Preprocess the article text
words = preprocess(article_text)

# Sentiment analysis functions using TextBlob
def textblob_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return polarity, subjectivity

# Sentiment analysis functions using VADER
def vader_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    positive = sentiment_scores['pos']
    negative = sentiment_scores['neg']
    neutral = sentiment_scores['neu']
    compound = sentiment_scores['compound']
    return positive, negative, neutral, compound

# Perform sentiment analysis using TextBlob
polarity, subjectivity = textblob_sentiment(article_text)

# Perform sentiment analysis using VADER
positive, negative, neutral, compound = vader_sentiment(article_text)

# Display sentiment analysis results
print("\nSentiment Analysis (TextBlob):")
print(f"Polarity Score: {polarity}")
print(f"Subjectivity Score: {subjectivity}")

print("\nSentiment Analysis (VADER):")
print(f"Positive Score: {positive}")
print(f"Negative Score: {negative}")
print(f"Neutral Score: {neutral}")
print(f"Compound Score: {compound}")
