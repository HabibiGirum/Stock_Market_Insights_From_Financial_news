# week-1 project stock market price and news correlation 
## stock market price prediction based on financial news

![Build Status](https://github.com/HabibiGirum/Stock_Market_Insights_From_Financial_news/actions/workflows/unittests.yml/badge.svg)

Financial News and Stock Price prediction is a project that leverages financial news to predict stock market prices. 
By analyzing the sentiment and content of news headline, this project aims to provide insights and predictions about stock market trends.


## Installation and Usage

### Prerequisites

- Python 3.8 or higher
- Git installed
- A virtual environment tool (e.g., `venv`)

### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/HabibiGirum/Stock_Market_Insights_From_Financial_news.git
   cd Stock_Market_Insights_From_Financial_news
   ```

2. **first Create and Activate Virtual Environment**

   ```bash
  
   python -m venv env # python 2 version
   python3 -m venv env # python3 version
   source venv/bin/activate  # for macOS and linux platforms
   venv\Scripts\activate # for Windows
   ```

3. **Install Dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```



## Dataset Requirements

### News Dataset

| **Column**   | **Description**                         |
|--------------|-----------------------------------------|
| `headline`   | News article headline                   |
| `url`        | Source URL of the article               |
| `publisher`  | Publisher of the article                |
| `date`       | Publication date (YYYY-MM-DD format)    |
| `stock`      | Related stock name or ticker            |

### Stock Dataset

| **Column**       | **Description**                         |
|------------------|-----------------------------------------|
| `Date`          | Stock trading date (YYYY-MM-DD)         |
| `Open`          | Opening price of the stock              |
| `High`          | Highest price of the stock              |
| `Low`           | Lowest price of the stock               |
| `Close`         | Closing price of the stock              |
| `Adj Close`     | Adjusted closing price of the stock     |
| `Volume`        | Trading volume                          |
| `Dividends`     | Dividends paid (if any)                 |
| `Stock Splits`  | Stock splits (if any)                   |

---

In detail document explore with this link [google docs](https://drive.google.com/file/d/1YP59-FNSFEq7LBXRs-64W57DEhUs6EUC/view?usp=sharing)


### References
- [yfinance Library](https://pypi.org/project/yfinance/)
- [Ta-lib](https://pypi.org/project/ta-lib/)
- [sentiment analysis](https://www.analyticsvidhya.com/blog/2022/07/sentiment-analysis-using-python/)

Python Libraries

```pandas``` for data manipulation
```matplotlib``` and ```seaborn``` for data visualization





## Author  
GitHub: [HabibiGirum](https://github.com/HabibiGirum)

Email:  habtamugirum478@gmail.com

