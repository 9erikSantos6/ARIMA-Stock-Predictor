from ..models.predictor import Predictor
from ..views.data_chart import DataChart
from ..views.window import Window

class PredictorController:
    def __init__(self) -> None:
        self.main_window = Window(title='ARIMA Stock Predictor', geometry='500x400')
        self.predictor = Predictor()
        self.data_chart = DataChart()

    def create_main_window(self) -> Window:
        # Creating widgets 
        self.main_window.create_label('Previsão de Preços de Ações', ('Arial', 20, 'bold'))
        self.main_window.create_label('Digite o símbolo da ação:')
        self.main_window.create_entry()
        self.main_window.create_button('Prever e Mostrar Gráfico', self._on_button_click)
        return self.main_window

    def _on_button_click(self) -> None:
        symbol = self.main_window.get_entry_data()
        if symbol:
            close_prices = self.predictor.download_stock_closing_data(symbol=symbol)
            forecast_prices = self.predictor.automake_forecast(data=close_prices)
            model = self.predictor.get_arima_model()
            performance_predicit = self.predictor.make_performance_prediction(data=close_prices, model=model)

            forecast_dates = self.data_chart.generate_dates(close_prices.index[-1], len(forecast_prices))

            self.data_chart.create_plot(
                dates=close_prices.index, 
                data=close_prices, 
                label='Valores Reais',
                color='#4CAF50',
            )
            self.data_chart.create_plot(
                dates=performance_predicit.index, 
                data=performance_predicit, 
                label='Performance do Modelo',
                color='#2196F3',
                line_style='--'

            )
            self.data_chart.create_plot(
                dates=forecast_dates, 
                data=forecast_prices, 
                label='Previsão',
                color='#FF5722',
                line_style='--'
            )

            self.data_chart.show(symbol)

        else:
            self.main_window.warning("Aviso", "Por favor, insira um símbolo de ação!")

