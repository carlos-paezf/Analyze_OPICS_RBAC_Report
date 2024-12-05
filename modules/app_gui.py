import tkinter as tk
import threading

from tkinter import ttk
from utils import RBAC_Keys, OPICS_Keys
from .compare_data import Compare_Data


class App_GUI(tk.Tk):
    def __init__(self, compare_data: Compare_Data):
        super().__init__()

        self.compare_data = compare_data

        self.title("Nombre de la aplicación")
        self.geometry("1200x900")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.last_selected = None
        self.create_widgets()

    
    