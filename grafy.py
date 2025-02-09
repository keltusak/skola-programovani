import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import numpy as np

def plot_function():
    try:
        func = function_var.get()
        x_min = float(entry_xmin.get())
        x_max = float(entry_xmax.get())
        xlabel = entry_xlabel.get()
        ylabel = entry_ylabel.get()
        if x_min >= x_max:
            messagebox.showerror("Chyba", "Minimální hodnota musí být menší než maximální!")
            return

        x = np.linspace(x_min, x_max, 400)
        if func == "sin(x)":
            y = np.sin(x)
        elif func == "cos(x)":
            y = np.cos(x)
        elif func == "x^2":
            y = x**2
        elif func == "sqrt(x)":
            if x_min < 0:
                messagebox.showerror("Chyba", "sqrt(x) není definována pro záporné hodnoty!")
                return
            y = np.sqrt(x)
        else:
            messagebox.showerror("Chyba", "Neznámá funkce!")
            return

        plt.figure()
        plt.plot(x, y, label=func)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title("Graf matematické funkce")
        plt.legend()
        plt.grid()
        plt.show()
    except ValueError:
        messagebox.showerror("Chyba", "Zadejte platné číselné hodnoty pro mezní hodnoty!")

def plot_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    try:
        x_vals, y_vals = [], []
        with open(file_path, "r") as file:
            for line in file:
                parts = line.split()
                if len(parts) != 2:
                    continue
                x, y = map(float, parts)
                x_vals.append(x)
                y_vals.append(y)

        xlabel = entry_xlabel.get()
        ylabel = entry_ylabel.get()

        plt.figure()
        plt.plot(x_vals, y_vals, "bo-")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title("Graf z datového souboru")
        plt.grid()
        plt.show()
    except Exception as e:
        messagebox.showerror("Chyba", f"Chyba při načítání souboru: {e}")


root = tk.Tk()
root.title("Generátor grafů")

tk.Label(root, text="Vyberte funkci:").grid(row=0, column=0)
function_var = tk.StringVar(value="sin(x)")
functions = ["sin(x)", "cos(x)", "x^2", "sqrt(x)"]
function_menu = tk.OptionMenu(root, function_var, *functions)
function_menu.grid(row=0, column=1)

tk.Label(root, text="x min:").grid(row=1, column=0)
entry_xmin = tk.Entry(root)
entry_xmin.grid(row=1, column=1)

tk.Label(root, text="x max:").grid(row=2, column=0)
entry_xmax = tk.Entry(root)
entry_xmax.grid(row=2, column=1)

tk.Label(root, text="Název osy X:").grid(row=3, column=0)
entry_xlabel = tk.Entry(root)
entry_xlabel.grid(row=3, column=1)

tk.Label(root, text="Název osy Y:").grid(row=4, column=0)
entry_ylabel = tk.Entry(root)
entry_ylabel.grid(row=4, column=1)

plot_button = tk.Button(root, text="Vykreslit funkci", command=plot_function)
plot_button.grid(row=5, column=0, columnspan=2)

file_button = tk.Button(root, text="Načíst data ze souboru", command=plot_from_file)
file_button.grid(row=6, column=0, columnspan=2)

root.mainloop()