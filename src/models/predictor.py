from typing import Optional
from statsmodels.tsa.arima.model import ARIMAResultsWrapper

import pandas as pd
import yfinance as yf
import pmdarima as pm
from statsmodels.tsa.arima.model import ARIMA

from .cache_handler import CacheHandler


class Predictor:
    """ Uma classe para predizer os futuros valores de fechamto de uma ação com ARIMA. """
    def __init__(self) -> None:
        self._cache = CacheHandler()  
        self._symbol_on_process = None
        self._data_on_process = None
        self._arima_model = None

        self.get_stock_closing_data = self._cache.memoize(expire=3600)(self.get_stock_closing_data)

    def get_stock_closing_data(self, symbol) -> Optional[pd.Series]:
        """
        Faz o download e preprocessa dados de uma ação

        Args:
            symbol: O simbolo da ação de acordo com o Yahoo finance para download.

        Returns:
            Um Pandas Series preprocessado, contendo os valores de fechamento do último ao primeiro dados.
            Caso ocorra um erro, retorna None

        """
        try:
            self._symbol_on_process = symbol
            data = yf.download(symbol)
            if data.empty:
                raise ValueError(f"No data found for symbol: {symbol}")
            close_prices = self._preprocess_data(data)
            self._data_on_process = close_prices
            print('Dados baixados:', close_prices)
            return close_prices  

        except ValueError as ve:
            print(f"Validation error: {ve}")
            return None

        except Exception as error:
            print(f"Error fetching data for {symbol}: {error}")
            return None

    def _preprocess_data(self, data: pd.Series) -> pd.Series:
        """
        Faz o preprocessamentos dos dados obtidos por download, retornando apenas valores de fechamento da ação.

        Args:
            data: Uma Serie pandas com todos os dados da ação

        Returns:
            Um Pandas Series preprocessado e normalizado, contendo datas como indices dos valores de fechameto.
        """
        symbol = self._symbol_on_process
        if 'Close' not in data.columns:
            raise ValueError(f"No 'Close' column found in data for {symbol}")
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
        pqd_order = None
        cache = self._cache
        pdq_key_in_cache = f'pdq_{self._symbol_on_process}'
        if not cache.get(pdq_key_in_cache):
            auto_model = pm.auto_arima(  
                data, 
                start_p=1, 
                start_d=1, 
                start_q=1, 
                trace=True
            )
            p, d, q = auto_model.order
            pqd_order = (p, d, q)
            cache.insert_tmp({pdq_key_in_cache: pqd_order}, 3600) 
            return pqd_order

        pdq_order = cache.get(pdq_key_in_cache)
        print(f'\nARIMA model selected: ARIMA{pdq_order}')
        return pdq_order

    def autocreate_ARIMA_model(self, data: pd.Series) -> ARIMAResultsWrapper:
        """
        Cria e configura automaticamente um modelo ARIMA com base nos dados forncecidos

        Args:
            data: Um Pandas Series normalizado com index de datas e valores de fechamento.

        Returns:
            Um modelo ARIMA configurado para os dados forncecidos.
        """
        arima_model = self._arima_model
        pdq_order = self.autofit_ARIMA(data=data)
        arima_model = self.create_ARIMA_model(data=data, pdq_order=pdq_order)
        return arima_model

    def create_ARIMA_model(self, data: pd.Series, pdq_order: tuple[int, int, int]):
        """
        Cria um modelo ARIMA com os parâmentros (p, q, d) setados manualmente.

        Args:
            data: Um Pandas Series normalizado com index de datas e valores de fechamento.
            pqd_order: Uma tupla composta por três valores inteiros, que correspondem a (p, q, d).

        Returns:
            Um modelo ARIMA configurado manualmente para os dados fornecidos.
        """
        arima_model = self._arima_model
        arima_model = ARIMA(data, order=pdq_order)
        arima_model = arima_model.fit()
        return arima_model

    def automake_forecast(self, data: pd.Series, years: int=2) -> pd.Series:
        """
        Realiza uma aprevisão automática criando e configurando um modelo ARIMA automaticamente.

        Args:
            data: Um Pandas Series normalizado com index de datas e valores de fechamento.
            years(optional) default 2: Um número inteiro indicando a quantidade de anos no futuro.
        
        Returns:
            Um Pandas Series contendo todos os valores de fechamento previstos pelo modelo ARIMA
        """
        model = self.autocreate_ARIMA_model(data)  
        forecast_months = 12 * years  
        forecast = model.forecast(steps=forecast_months)  
        print(f"\nPrevisões para os próximos {forecast_months} períodos:")
        print(forecast)
        return forecast
    
    def make_forecast(self, model: ARIMAResultsWrapper, years: int=2) -> pd.Series:
        """
        Realiza uma previsão utilizando um modelo ARIMA preconfigurado.

        Args:
            data: Um Pandas Series normalizado com index de datas e valores de fechamento.
            years(optional) default 2: Um número inteiro indicando a quantidade de anos no futuro.
        
        Returns:
            Um Pandas Series contendo todos os valores de fechamento previstos pelo modelo ARIMA.
        """
        forecast_months = 12 * years  
        forecast = model.forecast(steps=forecast_months)  
        print(f"\nPrevisões para os próximos {forecast_months} períodos:")
        print(forecast)
        return forecast

    def make_performance_prediction(self, model: ARIMAResultsWrapper, data: pd.Series) -> pd.Series:
        """
        Realiza uma predição para todas as datas dos indexes dos dados, retornando valores preditos pelo modelo.
        Ajuda a avaliar a qualidade do modelo.

        Args:
            model: Um modelo ARIMA preconfigurado aos dados que quer avaliar
            data: Um Pandas Series normalizado com index de datas e valores de fechamento.
        
        Returns:
            Retorna um Pandas Series contendo todos os valores de fechamento preditos pelo modelo, com indexes de datas reais.
        """
        prediction_steps = len(data)
        performance_prediction = model.predict(start=0, end=prediction_steps - 1)
        return performance_prediction
