"""

Em densenvolvimento...

"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_graph(symbol, data, forecast, performance_predict):
    plt.figure(figsize=(7, 4))  # Ajusta o tamanho da janela

    # Definição de cores suaves para o gráfico
    real_color = "#4CAF50"      # Verde suave para os valores reais
    forecast_color = "#FF5722"  # Vermelho suave para as previsões
    predict_color = "#2196F3"   # Azul suave para a performance do modelo

    # Definir os passos de previsão e as datas futuras
    forecast_steps = len(forecast)
    forecast_dates = pd.date_range(
        start=data.index[-1], 
        periods=forecast_steps, 
        freq="B"
    )

    # Gráfico dos valores reais (dados históricos)
    plt.plot(
        data.index, 
        data, 
        label="Valores Reais", 
        color=real_color, 
        linewidth=2
    )

    # Gráfico das previsões futuras (dados previstos)
    plt.plot(
        forecast_dates,
        forecast,
        label="Previsão",
        color=forecast_color,
        linestyle="--",
        linewidth=2,
    )

    # Gráfico das predições (modelo ajustado aos dados históricos)
    plt.plot(
        performance_predict.index,
        performance_predict,
        label="Performance do Modelo",
        color=predict_color,
        linestyle="--",
        linewidth=2,
    )

    # Configurações minimalistas
    plt.title(  # Título com espaçamento e cor suave
        f"Previsão de Preços de Ações ({symbol}) com ARIMA",
        fontsize=16,
        color="#333333",
        pad=20,
    )
    plt.xlabel(  # Rótulo do eixo X
        "Data", 
        fontsize=12,
        color="#555555"
    )         
    plt.ylabel(  # Rótulo do eixo Y
        "Preço de Fechamento (R$)", 
        fontsize=12, 
        color="#555555"
    )  
    plt.legend(   # Remove a caixa em volta da legenda
        loc="upper left", 
        fontsize=10, 
        frameon=False
    ) 
    plt.grid(True)                            # Remover a grade para manter o estilo minimalista
    plt.xticks(rotation=45, color="#666666")  # Ajuste da cor e rotação dos rótulos do eixo X
    plt.yticks(color="#666666")               # Cor suave para os rótulos do eixo Y

    # Remove os contornos do gráfico
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#DDDDDD")
    ax.spines["bottom"].set_color("#DDDDDD")

    # Estilo minimalista nos limites
    plt.tight_layout()
    plt.show()
