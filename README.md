# ARIMA Stock Predictor

This project implements a **Stock Price Predictor** using the **ARIMA (AutoRegressive Integrated Moving Average)** model for time series forecasting. The predictor takes historical stock market data as input and forecasts future stock prices based on this data. The project is built using Python and makes use of the `statsmodels` library for time series modeling and forecasting.

## Features

- Fetches historical stock market data.
- Uses the ARIMA model for time series prediction.
- Can predict future stock prices based on historical data.
- Plots actual vs predicted stock prices for easy visualization, and the model performance prediction.
- Automatically djusts ARIMA parameters (`p`, `d`, `q`) to optimize predictions.
  
## Prerequisites

To run this project, you will need Python 3.x and virtualenv for execute the following commands:

## Installation

```shell
git clone https://github.com/9erikSantos6/ARIMA-Stock-Predictor.git

cd ARIMA-Stock-Predictor/

virtualenv venv 

source venv/bin/activate

pip install -r requirements.txt
```

## To execute tests

```shell
python -m unittest discover -v -s test

```

## Usage

1. Just execute:
```
python src/main.py
```

## ARIMA Model Overview

The **ARIMA** model is a popular statistical method used for time series forecasting. The model consists of three key parameters:

- **p**: The number of lag observations included in the model (AR component).
- **d**: The number of times that the raw observations are differenced to make the time series stationary (I component).
- **q**: The size of the moving average window (MA component).

The ARIMA model is well-suited for time series data with trends and patterns, making it an effective tool for stock price forecasting.

## How to Tune ARIMA Parameters

To optimize the performance of the ARIMA model, you can experiment with different values of `p`, `d`, and `q`. One approach is to use **grid search** or rely on the **AIC (Akaike Information Criterion)** to find the best combination of parameters. In practice, you can also plot the autocorrelation (ACF) and partial autocorrelation (PACF) functions to help choose `p` and `q`.

## Contributing

If you'd like to contribute to this project, feel free to open a pull request. Contributions such as code optimizations, feature additions, or bug fixes are welcome.

---

## License

This project is licensed under the GNU General Public License v2.0 (GPL-2.0). See the [LICENSE](LICENSE) file for details.





