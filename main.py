import tkinter as tk
from vendes import mostrar_seccio_vendes
from personal import mostrar_seccio_personal
from clients import mostrar_seccio_clients
from inventari import mostrar_seccio_inventari
from gestio_vendes import mostrar_interficie_vendes

# Configuració de la finestra principal
root = tk.Tk()
root.title("CRM/ERP - Gestió Empresarial")
root.geometry("1000x600")
root.configure(bg="#ECECEC")

# Barra de navegació
sidebar = tk.Frame(root, width=200, bg="#F6F8FA", relief="sunken", borderwidth=2)
sidebar.pack(expand=False, fill="y", side="left", anchor="nw")

# Botons de navegació
seccions = ["Inici", "Gestió de Vendes", "Gestió de Personal", "Gestió de Clients", "Gestió d'Inventari", "Interfície de Vendes"]
for section in seccions:
    btn = tk.Button(
        sidebar, text=section, bg="#F6F8FA", fg="black", relief="flat",
        font=("Arial", 10), activeforeground="white",
        command=lambda sec=section: mostrar_seccio(sec)
    )
    btn.pack(fill="x", pady=5)


main_frame = tk.Frame(root, bg="#ECECEC")
main_frame.pack(expand=True, fill="both", side="right")

# Funció per canviar entre seccions
def mostrar_seccio(seccio):
    """Mostra la secció seleccionada en el marc principal."""
    for widget in main_frame.winfo_children():
        widget.destroy()  # Neteja el contingut anterior
    if seccio == "Inici":
        mostrar_inici()
    elif seccio == "Gestió de Vendes":
        mostrar_seccio_vendes(main_frame)
    elif seccio == "Gestió de Personal":
        mostrar_seccio_personal(main_frame)
    elif seccio == "Gestió de Clients":
        mostrar_seccio_clients(main_frame)
    elif seccio == "Gestió d'Inventari":
        mostrar_seccio_inventari(main_frame)
    elif seccio == "Interfície de Vendes":
        mostrar_interficie_vendes(main_frame)

# Funció per mostrar la pantalla d'inici
def mostrar_inici():
    for widget in main_frame.winfo_children():
        widget.destroy()
    tk.Label(main_frame, text="Benvingut al CRM/ERP", font=("Arial", 16, "bold"), bg="#F6F8FA", fg="black").pack(pady=20)

# Mostra la pantalla d'inici en arrencar el programa
mostrar_inici()
root.mainloop()

