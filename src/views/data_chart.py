import matplotlib.pyplot as plt
import pandas as pd

class DataChart:
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots()

    def create_plot(self, dates, data, label, color, line_style='solid', line_width=2) -> None:
        """
        Creates a plot on the chart

        Args:
            dates: Dates index
            data: The data
            label: Legend of what the data represents
            color: Color representation
            line_style(optional): Line tipe
            line_width(optional): Line width
        """
        plt.plot(
            dates, 
            data,
            label=label,
            color=color,
            linestyle=line_style,
            linewidth=line_width 
        )

    def generate_dates(self, start: str, periods: int) -> pd.DatetimeIndex:
        """
        Generate business dates 

        Args:
            start: In date format, the start date
            periods: Number of periods to be generated.
        """
        self.generated_dates = pd.date_range(
            start=start,
            periods=periods,
            freq='B'
        )
        return self.generated_dates

    def show(self, symbol: str) -> None:
        """
        Show chart

        Args: 
            symbol: The symbol of the stock
        """
        self.fig.set_size_inches(7, 4)  # Sets the size of the figure.
        self.ax.set_title(  # Chart title
            f'Previsão de Preços de Ações ({symbol}) com ARIMA',
            fontsize=16,
            color='#333333',
            pad=20,
        )
        self.ax.set_xlabel(  # X-axis label
            'Data', 
            fontsize=12,
            color='#555555'
        )         
        self.ax.set_ylabel(  # Y-axis label
            'Preço de Fechamento (R$)', 
            fontsize=12, 
            color='#555555'
        )
        self.ax.legend(  # Remove the box around the caption
            loc='upper left', 
            fontsize=10, 
            frameon=False
        )
        self.ax.grid(True)  # Activate the grid

        # Styles the X and Y axis
        self.ax.tick_params(axis='x', rotation=45, colors='#666666')
        self.ax.tick_params(axis='y', colors='#666666')

        # Removes the outlines from the chart
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#DDDDDD')
        self.ax.spines['bottom'].set_color('#DDDDDD')

        # Adjust the layout and display the chart
        plt.tight_layout()
        plt.show()
