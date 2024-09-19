import matplotlib.pyplot as plt
import pandas as pd

class DataChart:
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()

    def create_plot(self, dates, data, label, color, line_style='solid', line_width=2) -> None:
        plt.plot(
            dates, 
            data,
            label=label,
            color=color,
            linestyle=line_style,
            linewidth=line_width 
        )

    def generate_dates(self, start, periods) -> pd.DatetimeIndex:
        self.generated_dates = pd.date_range(
            start=start,
            periods=periods,
            freq='B'
        )
        return self.generated_dates

    def show(self, symbol) -> None:
        self.fig.set_size_inches(7, 4)  # Define o tamanho da figura
        self.ax.set_title(  # Título do gráfico
            f'Previsão de Preços de Ações ({symbol}) com ARIMA',
            fontsize=16,
            color='#333333',
            pad=20,
        )
        self.ax.set_xlabel(  # Rótulo do eixo X
            'Data', 
            fontsize=12,
            color='#555555'
        )         
        self.ax.set_ylabel(  # Rótulo do eixo Y
            'Preço de Fechamento (R$)', 
            fontsize=12, 
            color='#555555'
        )
        self.ax.legend(  # Remove a caixa em volta da legenda
            loc='upper left', 
            fontsize=10, 
            frameon=False
        )
        self.ax.grid(True)  # Ativa a grade

        # Estiliza o eixo X e Y
        self.ax.tick_params(axis='x', rotation=45, colors='#666666')
        self.ax.tick_params(axis='y', colors='#666666')

        # Remove os contornos do gráfico
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#DDDDDD')
        self.ax.spines['bottom'].set_color('#DDDDDD')

        # Ajusta o layout e mostra o gráfico
        plt.tight_layout()
        plt.show()
