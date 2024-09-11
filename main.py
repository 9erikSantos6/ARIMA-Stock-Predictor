"""

AVISO DE BUG AO PLOTAR GRÁFICO

"""

import pandas as pd
import yfinance as yf
import pmdarima as pm
import matplotlib.pyplot as plt
from diskcache import Cache
from statsmodels.tsa.arima.model import ARIMA
import tkinter as tk
from tkinter import messagebox

# Cache para evitar repetidas requisições de dados
cache_dir = '.financeai_tmp_cache'
cache = Cache(directory=cache_dir, size_limit=int(1024 * 1e6))

# Função para buscar dados das ações com cache
@cache.memoize(expire=3600)
def get_stock_data(symbol):
    print('Data: ', symbol)
    try:
        data = yf.download(symbol)  # Baixa os dados históricos da ação usando o Yahoo Finance
        if data.empty:  # Validação de dados
            raise ValueError(f"No data found for symbol: {symbol}")
        data = preprocess_data(data)
        return data  # Retorna apenas os preços de fechamento já processados
    except Exception as error:
        print(f"Error fetching data for {symbol}: {error}")
        return None

# Preprocessa e faz o tratamento os dados
def preprocess_data(data):
    close_prices = data['Close'].dropna() # Pega os preços de fechamento e remove NaNs
    close_prices.index = pd.to_datetime(close_prices.index) # Converte o índice para datetime e ajusta a frequência para dias úteis
    close_prices = close_prices.asfreq('B')  # Define a frequência para dias úteis (B = business days)
    close_prices = close_prices.ffill()  # Preenche dados faltantes (forward fill)
    return close_prices

# Autoconfigura o modelo ARIMA
@cache.memoize(expire=3600)
def autofit_model_arima(data): 
    auto_model = pm.auto_arima(
        data,
        start_p=1, 
        start_d=1,
        start_q=1, 
        trace=True
    )
    p, d, q = auto_model.order
    model = ARIMA(data, order=(p, d, q))
    model = model.fit()
    return model

# Realiza a predição com base nos dados
def predict_data(data):
    close_prices = data  # Pega os dados de fechamento
    model = autofit_model_arima(close_prices)  # Autoconfigura o modelo ARIMA
    forecast_steps = 12 * 2  # Aproximadamente 2 anos de previsões
    forecast = model.forecast(steps=forecast_steps)  # Faz a previsão
    performance_predict = model.predict(start=0, end=len(close_prices)-1)  # Predições de performance

    # Exibindo previsões
    print(f"Previsões para os próximos {forecast_steps} períodos:")
    print(forecast)

    return (forecast, performance_predict)

def plot_graph(symbol, data, forecast, performance_predict):
    plt.figure(figsize=(7, 4))
    
    # Definição de cores suaves para o gráfico
    real_color = "#4CAF50"     # Verde suave para os valores reais
    forecast_color = "#FF5722" # Vermelho suave para as previsões
    predict_color = "#2196F3"  # Azul suave para a performance do modelo

    # Definir os passos de previsão e as datas futuras
    forecast_steps = len(forecast)
    forecast_dates = pd.date_range(start=data.index[-1], periods=forecast_steps, freq='B')

    # Gráfico dos valores reais (dados históricos)
    plt.plot(data.index, data, label='Valores Reais', color=real_color, linewidth=2)

    # Gráfico das previsões futuras (dados previstos)
    plt.plot(forecast_dates, forecast, label='Previsão', color=forecast_color, linestyle='--', linewidth=2)

    # Gráfico das predições (modelo ajustado aos dados históricos)
    plt.plot(performance_predict.index, performance_predict, label='Performance do Modelo', color=predict_color, linestyle='--', linewidth=2)

    # Configurações minimalistas
    plt.title(f'Previsão de Preços de Ações ({symbol}) com ARIMA', fontsize=16, color="#333333", pad=20)  # Título com espaçamento e cor suave
    plt.xlabel('Data', fontsize=12, color="#555555")  # Rótulo do eixo X
    plt.ylabel('Preço de Fechamento (R$)', fontsize=12, color="#555555")  # Rótulo do eixo Y
    plt.legend(loc='upper left', fontsize=10, frameon=False)  # Remove a caixa em volta da legenda
    plt.grid(False)  # Remover a grade para manter o estilo minimalista
    plt.xticks(rotation=45, color="#666666")  # Ajuste da cor e rotação dos rótulos do eixo X
    plt.yticks(color="#666666")  # Cor suave para os rótulos do eixo Y
    
    # Remove os contornos do gráfico
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color("#DDDDDD")
    ax.spines['bottom'].set_color("#DDDDDD")

    # Estilo minimalista nos limites
    plt.tight_layout()
    plt.show()

# Obtém o símbolo da ação e executar a previsão
def on_button_click():
    print("Botão pressionado!")
    symbol = symbol_entry.get()
    if symbol:
        data = get_stock_data(symbol)
        forecast, performance_predict = predict_data(data)
        print(performance_predict)
        plot_graph(symbol, data, forecast, performance_predict)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um símbolo de ação.")

# Cria a janela principal
janela = tk.Tk()
janela.geometry("500x400")
janela.title("Previsão de Ações")
janela.configure(bg="#f0f0f0")  # Fundo suave

# Fonte personalizada para título e outros widgets
title_font = ("Arial", 20, "bold")  # Fonte padrão Arial
label_font = ("Arial", 12)
button_font = ("Arial", 10)

# Título
title_label = tk.Label(
    janela, 
    text="Previsão de Preços de Ações", 
    font=title_font, 
    bg="#f0f0f0",  # Cor de fundo do label
    fg="#333333"   # Cor do texto (cinza escuro)
)
title_label.pack(pady=20)

# Label e campo de entrada para o símbolo da ação
symbol_label = tk.Label(
    janela, 
    text="Digite o símbolo da ação:", 
    font=label_font, 
    bg="#f0f0f0", 
    fg="#555555"
)
symbol_label.pack(pady=10)

symbol_entry = tk.Entry(janela, font=("Arial", 12), width=20, bd=2, relief="flat", justify="center")
symbol_entry.pack(pady=5)

# Botão para iniciar a previsão
prever_button = tk.Button(
    janela, 
    text="Prever e Mostrar Gráfico", 
    command=on_button_click, 
    font=button_font, 
    bg="#4CAF50",  # Cor de fundo do botão (verde suave)
    fg="white",    # Cor do texto do botão (branco)
    activebackground="#45a049",  # Cor de fundo quando pressionado
    relief="flat", 
    padx=10, 
    pady=5
)
prever_button.pack(pady=20)

# Centraliza todos os elementos
title_label.pack(pady=20, anchor="center")
symbol_label.pack(pady=10, anchor="center")
symbol_entry.pack(pady=5, anchor="center")
prever_button.pack(pady=20, anchor="center")

# Inicia o loop da interface gráfica
janela.mainloop()