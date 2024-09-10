import pandas as pd
import yfinance as yf
import pmdarima as pm
import matplotlib.pyplot as plt
from diskcache import Cache
from statsmodels.tsa.arima.model import ARIMA
import tkinter as tk
from tkinter import messagebox

# Cache para evitar repetidas requisições de dados
cache_dir = '.fincanceai_tmp_cache'
cache = Cache(directory=cache_dir, size_limit=int(1024 * 1e6))

# Função para buscar dados das ações com cache
@cache.memoize(expire=3600)
def get_stock_data(symbol):
    try:
        # Baixa os dados históricos da ação usando o Yahoo Finance
        data = yf.download(symbol)
        if data.empty:
            raise ValueError(f"No data found for symbol: {symbol}")
        return data
    except Exception as error:
        print(f"Error fetching data for {symbol}: {error}")
        return None

def preprocess_data(data):
    # Preprocessa os dados (pegando os preços de fechamento e removendo NaNs)
    close_prices = data['Close'].dropna()
    # Converte o índice para datetime e ajusta a frequência para dias úteis
    close_prices.index = pd.to_datetime(close_prices.index)
    close_prices = close_prices.asfreq('B')  # Define a frequência para dias úteis (B = business days)
    close_prices = close_prices.ffill()  # Preenche dados faltantes (forward fill)

    train, test = close_prices[:int(round(0.8 * len(close_prices)))], close_prices[int(round(0.8*len(close_prices))):]

    return (train, test)

# Função para treinar o modelo ARIMA
@cache.memoize(expire=3600)
def train_ARIMA(data): 
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

def forecast_and_plot(symbol):
    # Coleta dados da ação
    data = get_stock_data(symbol)

    if data is None:
        messagebox.showerror("Erro", f"Não foi possível obter dados para o símbolo '{symbol}'.")
        return

    train, test = preprocess_data(data)

    print('Datasets: ')
    print(f'Total: {len(test) + len(train)}')
    print(f'Train: {len(train)}\nTest: {len(test)}')

    # Junta o traino e o test para fazer os dados reais
    close_prices = pd.concat([train, test])

    # Treina o modelo ARIMA com os parâmetros fornecidos (4, 0, 3)
    model = train_ARIMA(close_prices)

    # Prever 2 anos de dados (em dias úteis) à frente
    forecast_steps = 12 * 2  # Aproximadamente 2 anos de previsões
    forecast = model.forecast(steps=forecast_steps)  # Faz a previsão

    # Predição nos dados de treino
    predict = model.predict(start=0, end=len(close_prices)-1)  # Predições baseadas nos dados de teste

    # Gera datas para os períodos de previsão
    forecast_dates = pd.date_range(start=close_prices.index[-1], periods=forecast_steps, freq='B')

    # Exibe as previsões
    print(f"Previsões para os próximos {forecast_steps} períodos:")
    print(forecast)

    # Visualização dos resultados
    plt.figure(figsize=(14, 8))

    # Gráfico dos valores reais (dados históricos)
    plt.plot(close_prices.index, close_prices, label='Valores Reais', color='blue')

    # Gráfico das previsões futuras (dados previstos)
    plt.plot(forecast_dates, forecast, label='Previsão', color='red', linestyle='--')

    # Gráfico das predições (modelo ajustado aos dados históricos)
    plt.plot(predict.index, predict, label='Predições', color='green', linestyle='--')

    # Configurações do gráfico
    plt.title(f'Previsão de Preços de Ações ({symbol}) com ARIMA', fontsize=18)
    plt.xlabel('Data', fontsize=14)
    plt.ylabel('Preço de Fechamento (R$)', fontsize=14)
    plt.legend(loc='upper left', fontsize=12)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para obter o símbolo da ação e executar a previsão
def on_button_click():
    symbol = symbol_entry.get()
    if symbol:
        forecast_and_plot(symbol)
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
