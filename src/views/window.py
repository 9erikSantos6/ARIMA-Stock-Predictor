import tkinter as tk
from typing import Callable

class Window(tk.Tk):
    def __init__(self, title: str, geometry: str) -> None:
        super().__init__()
        self.title(title)  # Define o título da janela
        self.geometry(geometry)  # Define o tamanho da janela
        self.configure(bg='#f0f0f0')  # Cor de fundo da janela

    def create_label(self, text: str, font=('Arial', 12), app=None) -> tk.Label:
        # 'Método para criar um label'
        self.label = tk.Label(
            self,
            text=text,
            font=font,
            bg='#f0f0f0',
            fg='#333333'
        )
        self.label.pack(pady=10, anchor='center')

        return self.label
    
    def create_entry(self, font=('Arial', 12)) -> tk.Entry:
        # 'Método para criar um campo de entrada'
        self.entry = tk.Entry(
            self, 
            font=font, 
            width=20, 
            justify='center',
            bd=2, 
            relief='flat'  # Usando opções personalizáveis do `tk`
        )
        self.entry.pack(pady=5, anchor='center')

        return self.entry

    def create_button(self, text: str, action: Callable[[], None], font=('Arial', 10),  relief='flat', bg='#45a049', fg='white', activebackground='#45a049', activeforeground='#ffffff') -> tk.Button:
        # 'Método para criar um botão com uma ação'
        self.forecast_button = tk.Button(
            self,
            text=text,
            command=action,
            font=font,
            relief=relief,
            bg=bg,
            fg=fg,
            activebackground=activebackground,
            activeforeground=activeforeground
        )
        self.forecast_button.pack(pady=20, anchor='center')

        return self.forecast_button

    def warning(self, title:str, text:str):
        return tk.messagebox.showwarning(title, text)
    
    def get_symbol(self) -> str:
        # 'Retorna o texto inserido no campo de entrada'
        return self.entry.get()

    def on_closing(self):
        """Este método é chamado quando a janela principal é fechada."""
        print("> Fechando a janela...")
        if self.app:  # Se o controlador foi passado, chama on_close nele
            self.app.on_close()  
        self.destroy()
        print("> Janela fechada!")

