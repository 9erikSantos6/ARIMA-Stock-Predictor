import unittest
from pandas import Series
from statsmodels.tsa.arima.model import ARIMAResultsWrapper
from src.models.predictor import Predictor

class TestPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = Predictor()
        self.predictor.clear_cache()

    def test_download_stock_closing_data(self):
        data = self.predictor.download_stock_closing_data('AAPL')
        self.assertTrue(isinstance(data, Series))  
    
    def test_autofit_ARIMA(self):
        data = self.predictor.download_stock_closing_data('AAPL')
        pdq_order = self.predictor.autofit_ARIMA(data)
        self.assertTrue(isinstance(pdq_order, tuple))
        self.assertEqual(len(pdq_order), 3)

    def test_autocreate_ARIMA_model(self):
        data = self.predictor.download_stock_closing_data('AAPL')
        model = self.predictor.autocreate_ARIMA_model(data)
        self.assertTrue(isinstance(model, ARIMAResultsWrapper))

    def test_create_ARIMA_model(self):
        data = self.predictor.download_stock_closing_data('AAPL')
        model = self.predictor.create_ARIMA_model(data, (1, 1, 1))
        self.assertTrue(isinstance(model, ARIMAResultsWrapper))

    def test_automake_forecast(self):
        data = self.predictor.download_stock_closing_data('AAPL')
        forecast = self.predictor.automake_forecast(data=data)
        self.assertTrue(isinstance(forecast, Series))
        self.assertNotIn(forecast.index.to_list(), data.index.to_list())

    def test_make_forecast(self):
        data = self.predictor.download_stock_closing_data('AAPL')
        model = self.predictor.create_ARIMA_model(data, (5, 2, 0))
        forecast = self.predictor.make_forecast(model=model)
        self.assertTrue(isinstance(forecast, Series))
        self.assertNotIn(forecast.index.to_list(), data.index.to_list())

    def test_make_performance_prediction(self):
        data = self.predictor.download_stock_closing_data('AAPL')
        model = self.predictor.autocreate_ARIMA_model(data=data)
        performance_prediction = self.predictor.make_performance_prediction(model=model, data=data)

        self.assertTrue(isinstance(performance_prediction, Series))
        self.assertEqual(performance_prediction.index.tolist(), data.index.tolist())

    def test_get_symbol_on_process(self):
        self.predictor.download_stock_closing_data('AAPL')
        symbol = self.predictor.get_symbol_on_process()
        self.assertEqual(symbol, 'AAPL') 

    def test_get_arima_model(self):
        data = self.predictor.download_stock_closing_data('AAPL')
        real_model = self.predictor.create_ARIMA_model(data, pdq_order=(5, 2, 0))
        expected_model = self.predictor.get_arima_model()
        self.assertEqual(expected_model, real_model)

    def test_get_data_on_process(self):
        self.predictor.download_stock_closing_data('AAPL')
        expected_data = self.predictor.get_data_on_process()
        self.assertTrue(isinstance(expected_data, Series))


if __name__ == '__main__':
    unittest.main()
