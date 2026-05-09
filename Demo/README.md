### **AI-Powered Sentiment Analysis for Financial Headlines**


This project is a simple AI-driven web application built with Streamlit that analyzes financial news headlines and predicts their sentiment as Positive, Neutral, or Negative.

It uses a machine learning model trained on the Kaggle dataset:
Sentiment Analysis for Financial News (ankurzing/sentiment-analysis-for-financial-news).

This project demonstrates real-world GenAI applications in Finance, NLP, and Market Insights.

  Features

Input any financial news headline

OR load a random headline from the dataset

Sentiment prediction using TF-IDF + Logistic Regression

Displays:

Predicted sentiment

Class probabilities

Short market “insight”

Clean, interactive Streamlit UI

  Project Structure
financial-news-insight/
│
- financial_news_insight_app.py               # Main Streamlit application
- all-data.csv                                # Kaggle dataset (must be downloaded manually)
- requirements.txt                            # List of dependencies
- README.md

  Installation
1. Clone the Repository
git clone <your-repo-url>
cd financial-news-insight

2. Download the Dataset

Download from Kaggle:
https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news

Save the dataset as:

all-data.csv


in the same folder as app.py.

3. Install Dependencies
pip install -r requirements.txt


Or install manually:

pip install streamlit scikit-learn pandas numpy

  Running the Application

Run Streamlit:

streamlit run app.py


  Expected output:

Local URL: http://localhost:8501


Open the link in your browser to access the app.

  Testing the Application
Test 1 — Manual Input

Start the app

Type a custom headline, e.g.
"Tech stocks rally as inflation cools"

Click Analyze Headline

Sentiment + probabilities appear

Test 2 — Random Headline

Turn on "Use a random headline from the dataset" (sidebar)

Click Analyze Headline

Model predicts the sentiment of a dataset example

Test 3 — Edge Cases

Try:

Very short headlines

Headlines with mixed sentiment

Highly technical financial wording

Observe how well the model generalizes.
