import tkinter as tk
from typing import Callable

class Window(tk.Tk):
    def __init__(self, title: str, geometry: str) -> None:
        super().__init__()
        self.title(title)  # Define window title
        self.geometry(geometry)  # Define window size
        self.configure(bg='#f0f0f0')  # Background color

    def create_label(self, text: str, font=('Arial', 12)) -> tk.Label:
        """
        Creates a label in the window

        Args:
            text: The text that will be contained in the label
            font(optional): A tuple indicating the font of the characters
        Returns: 
            The label
        """

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
        """
        Creates an input field

        Args:
            font(optional): A tuple indicating the font of the input characters
        
        Returns:
            The input field
        """

        self.entry = tk.Entry(
            self, 
            font=font, 
            width=20, 
            justify='center',
            bd=2, 
            relief='flat'
        )
        self.entry.pack(pady=5, anchor='center')

        return self.entry

    def create_button(self, text: str, action: Callable[[], None], font=('Arial', 10),  relief='flat', bg='#45a049', fg='white', activebackground='#45a049', activeforeground='#ffffff') -> tk.Button:
        """
        Creates an action button

        Args:
            text:
            action:
            font(optional): A tuple indicating the font of the characters
            relief(optional): Widget relief type
            bg(optional): Background color
            fg(optional): Foreground color
            activebackground(optional): Background when active
            activeforegroun(optional): Foreground when active

        Returns:
            The button windget
        """

        self.button = tk.Button(
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
        self.button.pack(pady=20, anchor='center')

        return self.button

    def warning(self, title:str, text:str):
        """
        Creates a warning menssage

        Args:
            title: The title od menssage
            text: The content of menssage

        Retruns:
            The warning window
        """
        return tk.messagebox.showwarning(title, text)
    
    def get_entry_data(self) -> str:
        """
        Get the entry data

        Returns:
            The entry data
        """
        return self.entry.get()
