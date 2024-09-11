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
    plt.figure(figsize=(14, 8))
    forecast_steps = len(forecast)
    forecast_dates = pd.date_range(start=data.index[-1], periods=forecast_steps, freq='B')
    
    plt.plot(data.index, data, label='Valores Reais', color='blue') # Gráfico dos valores reais (dados históricos)
    plt.plot(forecast_dates, forecast, label='Previsão', color='red', linestyle='--') # Gráfico das previsões futuras (dados previstos)
    plt.plot(performance_predict.index, performance_predict, label='Performace do modelo', color='green', linestyle='--')     # Gráfico das predições (modelo ajustado aos dados históricos)
    
    # Configurações do gráfico
    plt.title(f'Previsão de Preços de Ações ({symbol}) com ARIMA', fontsize=18)
    plt.xlabel('Data', fontsize=14)
    plt.ylabel('Preço de Fechamento (R$)', fontsize=14)
    plt.legend(loc='upper left', fontsize=12)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Obtém o símbolo da ação e executar a previsão
def on_button_click():
    symbol = symbol_entry.get()
    if symbol:
        data = get_stock_data(symbol)
        forecast, performance_predict = predict_data(data)
        print(performance_predict)
        plot_graph(symbol, data, forecast, performance_predict)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um símbolo de ação.")

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Previsão de Preços de Ações")

# Label e campo de entrada para o símbolo da ação
tk.Label(root, text="Símbolo da Ação:").pack(pady=10)
symbol_entry = tk.Entry(root)
symbol_entry.pack(pady=5)

# Botão para iniciar a previsão
tk.Button(root, text="Prever e Mostrar Gráfico", command=on_button_click).pack(pady=20)

# Inicia o loop da interface gráfica
root.mainloop()