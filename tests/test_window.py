import unittest
import tkinter as tk
from src.views.window import Window

class TestWindow(unittest.TestCase):
    def setUp(self):
        self.window = Window('ARIMA Stock Predicor', "500x400")

    def test_title(self):
        title = self.window.title() 
        self.assertEqual(title, 'ARIMA Stock Predicor')

    def test_create_label(self):
        label = self.window.create_label('Test Label')
        self.assertTrue(isinstance(label, tk.Label))
        self.assertEqual(label.cget("text") ,'Test Label')

    def test_create_entry(self):
        entry = self.window.create_entry()
        self.assertTrue(isinstance(entry, tk.Entry))

    def test_create_button(self):
        self.clicked = False
        def on_click():
            self.clicked = True
        button = self.window.create_button(text='Button1', action=on_click)
        button.invoke() # Pressiona o botão

        self.assertTrue(isinstance(button, tk.Button))
        self.assertEqual(button.cget("text"), "Button1")
        self.assertTrue(self.clicked)

    def test_get_symbol(self):
        entry = self.window.create_entry()
        entry.insert(0, 'AAPL')
        self.assertEqual(self.window.get_symbol(), 'AAPL')


    def tearDown(self):
        self.window.destroy()


if __name__ == '__main__':
    unittest.main()