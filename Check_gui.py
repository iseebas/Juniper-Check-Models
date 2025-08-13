import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import Juniper_check_model as logica  # tu script de lógica

def seleccionar_archivo():
    ruta = filedialog.askopenfilename(title="Seleccionar archivo de IPs", filetypes=[("Archivos txt", "*.txt")])
    if ruta:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, ruta)

def iniciar_revision():
    usuario = entry_usuario.get()
    password = entry_password.get()
    ruta_ips = entry_archivo.get()

    if not usuario or not password or not ruta_ips:
        messagebox.showwarning("Atención", "Completar todos los campos")
        return

    try:
        ips = logica.leer_ips(ruta_ips)
    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
        return

    resultados_texto.delete(1.0, tk.END)  # limpiar área de texto
    with open("resultados.txt", "w") as salida:
        for ip in ips:
            resultados_texto.insert(tk.END, f"Conectando a {ip}...\n")
            resultados_texto.update()
            modelo = logica.obtener_modelo_switch(ip, usuario, password)
            resultado = f"{ip} --> {modelo}"
            resultados_texto.insert(tk.END, resultado + "\n")
            salida.write(resultado + "\n")

    messagebox.showinfo("Finalizado", "Revisión completada y resultados guardados en resultados.txt")

# --- Crear ventana ---
ventana = tk.Tk()
ventana.title("Revisión de Switches Juniper")
ventana.geometry("800x550")

# Usuario y contraseña
tk.Label(ventana, text="Usuario SSH:").pack()
entry_usuario = tk.Entry(ventana)
entry_usuario.pack()

tk.Label(ventana, text="Password SSH:").pack()
entry_password = tk.Entry(ventana, show="*")
entry_password.pack()

# Archivo de IPs
tk.Label(ventana, text="Archivo de IPs:").pack()
frame_archivo = tk.Frame(ventana)
frame_archivo.pack(pady=5)
entry_archivo = tk.Entry(frame_archivo, width=40)
entry_archivo.pack(side=tk.LEFT)
tk.Button(frame_archivo, text="Examinar", command=seleccionar_archivo).pack(side=tk.LEFT, padx=5)

# Área de texto para resultados
resultados_texto = scrolledtext.ScrolledText(ventana, width=120, height=15)
resultados_texto.pack(pady=10)

# Botón iniciar
tk.Button(ventana, text="Iniciar Revisión", command=iniciar_revision).pack(pady=5)

ventana.mainloop()
