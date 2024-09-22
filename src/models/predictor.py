from typing import Optional
from statsmodels.tsa.arima.model import ARIMAResultsWrapper

import pandas as pd
import yfinance as yf
import pmdarima as pm
from statsmodels.tsa.arima.model import ARIMA

from .cache_handler import CacheHandler


class Predictor:
    """ A class to predict future closure values ​​of an action with ARIMA. """
    def __init__(self) -> None:
        self._cache = CacheHandler()
        self._data_on_process = None
        self._arima_model = None

        self.download_stock_closing_data = self._cache.memoize(expire=3600)(self.download_stock_closing_data)

    def download_stock_closing_data(self, symbol) -> Optional[pd.Series]:
        """
        Downloads and preprocess the data of an action

        Args:
            symbol: The symbol of action according to Yahoo Finance for download.

        Returns:
            A preopcessed Pandas Series, containing the closing values ​​of the latter to the first data.
            If an error occurs, returns none
        """

        try:
            cache = self._cache
            cache.insert_tmp({'symbol_on_process': symbol}, 3600)
            
            data = yf.download(symbol)
            if data.empty:
                raise ValueError(f"No data found for symbol: {symbol}")
            
            close_prices = self._preprocess_data(data)
            cache.insert_tmp({f'{symbol}_close_prices': close_prices}, 3600)
            return close_prices  

        except ValueError as ve:
            print(f"Validation error: {ve}")
            return None

        except Exception as error:
            print(f"Error fetching data for {symbol}: {error}")
            return None

    def _preprocess_data(self, data: pd.Series) -> pd.Series:
        """
        Preprocess the data obtained in the download.
        
        Args:
            data: A Pandas Series with all data action data

        Returns:
            A preprocessed Pandas Series with stock closing dates.
        """

        symbol_on_process = self._cache.get(keys='symbol_on_process')
        
        if 'Close' not in data.columns:
            raise ValueError(f"No 'Close' column found in data for {symbol_on_process}")
        
        close_prices = data["Close"].dropna()
        close_prices.index = pd.to_datetime(close_prices.index)
        close_prices = close_prices.asfreq("B")
        close_prices = close_prices.ffill()
        
        return close_prices

    def autofit_ARIMA(self, data: pd.Series) -> tuple[int, int, int]:
        """
        Auto configura os parâmetros (p, q, d) do modelo ARIMA com força bruta.

        Args:
            data: Um Pandas Series normelizado com index de datas e valores de fechamento.

        Returns:
            Uma tupla contendo três valores inteiros, são os parâmentros (p, q, d).
        """

        pdq_key_in_cache = self._cache.get(f'pdq_{self.get_symbol_on_process()}')
        
        if not pdq_key_in_cache:
            auto_model = pm.auto_arima(  
                data, 
                start_p=1, 
                start_d=1, 
                start_q=1, 
                trace=True
            )
            p, d, q = auto_model.order
            pqd_order = (p, d, q)
            self._cache.insert_tmp({pdq_key_in_cache: pqd_order}, 3600) 
            return pqd_order

        pdq_order = pdq_key_in_cache
        print(f'\nARIMA model selected: ARIMA{pdq_order}')
        return pdq_order

    def autocreate_ARIMA_model(self, data: pd.Series) -> ARIMAResultsWrapper:
        """
        Automatically creates and configures an ARIMA model based on the provided data.

        Args:
            data: A normalized Pandas Series with indexed dates and closing values.

        Returns:
            An ARIMA model configured for the provided data.
        """

        pdq_order = self.autofit_ARIMA(data=data)
        self._arima_model = self.create_ARIMA_model(data=data, pdq_order=pdq_order)
        return self._arima_model

    def create_ARIMA_model(self, data: pd.Series, pdq_order: tuple[int, int, int]):
        """
        Creates an ARIMA model with the parameters (p, q, d) set manually.

        Args:
            data: A normalized Pandas Series with date index and closing values.
            pqd_order: A tuple composed of three integer values, corresponding to (p, q, d).

        Returns:
            A manually configured ARIMA model for the given data.
                """

        self._arima_model = ARIMA(data, order=pdq_order)
        self._arima_model = self._arima_model.fit()
        return self._arima_model

    def automake_forecast(self, data: pd.Series, years = 2) -> pd.Series:
        """
        Performs an automatic forecast by creating and configuring an ARIMA model automatically.

        Args:
            data: A normalized Pandas Series with indexed dates and closing values.
            years(optional) default 2: An integer indicating the number of years in the future.

        Returns:
            A Pandas Series containing all closing values ​​predicted by the ARIMA model
        """

        model = self.autocreate_ARIMA_model(data)  
        forecast_months = 12 * years  
        forecast = model.forecast(steps=forecast_months)  
        print(f"\nPrevisões para os próximos {forecast_months} períodos:")
        print(forecast)
        return forecast
    
    def make_forecast(self, model: ARIMAResultsWrapper, years: int=2) -> pd.Series:
        """
        Performs a forecast using a preconfigured ARIMA model.

        Args:
            data: A normalized Pandas Series with indexed dates and closing values.
            years(optional) default 2: An integer indicating the number of years in the future.

        Returns:
            A Pandas Series containing all closing values ​​predicted by the ARIMA model.
        """

        forecast_months = 12 * years  
        forecast = model.forecast(steps=forecast_months)  
        print(f"\nPrevisões para os próximos {forecast_months} períodos:")
        print(forecast)
        return forecast

    def make_performance_prediction(self, model: ARIMAResultsWrapper, data: pd.Series) -> pd.Series:
        """
        Performs a prediction for all index dates in the data, returning values ​​predicted by the model.
        Helps to evaluate the quality of the model.

        Args:
            model: An ARIMA model preconfigured for the data you want to evaluate
            data: A normalized Pandas Series with index dates and closing values.

        Returns:
            Returns a Pandas Series containing all closing values ​​predicted by the model, with real date indexes.
        """

        prediction_steps = len(data)
        performance_prediction = model.predict(start=0, end=prediction_steps - 1)
        return performance_prediction
    
    def clear_cache(self) -> None:
        return self._cache.clear()
    
    # GETs:
    def get_symbol_on_process(self) -> str:
        return self._cache.get('symbol_on_process')
    
    def get_arima_model(self) -> ARIMAResultsWrapper:
        return self._arima_model
    
    def get_data_on_process(self) -> Optional[pd.Series]:
        symbol = self.get_symbol_on_process()
        if symbol:
            return self._cache.get(f'{self.get_symbol_on_process()}_close_prices')
        return None

