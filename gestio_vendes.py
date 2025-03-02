import tkinter as tk
from tkinter import ttk, messagebox
from database import connectar_bbdd

def mostrar_interficie_vendes(main_frame):
    # Netejar el contingut anterior del main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Registrar vendes", font=("Arial", 16, "bold"), bg="#34495E", fg="white").pack(pady=10)

    # Frame per als camps d'entrada
    entrada_frame = tk.Frame(main_frame)
    entrada_frame.pack(fill="x", padx=20, pady=10)

    # Menú desplegable de productes
    tk.Label(entrada_frame, text="Selecciona Producte:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    productes = carregar_productes()
    producte_combo = ttk.Combobox(entrada_frame, values=[f"{p[0]} - {p[1]} ({p[2]:.2f} €)" for p in productes], state="readonly", width=40)
    producte_combo.grid(row=0, column=1, padx=5, pady=5)

    # Menú desplegable de clients
    tk.Label(entrada_frame, text="Selecciona Client:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    clients = carregar_clients()
    client_combo = ttk.Combobox(entrada_frame, values=[f"{c[0]} - {c[1]} {c[2]}" for c in clients], state="readonly", width=40)
    client_combo.grid(row=1, column=1, padx=5, pady=5)

    # Camp per a la quantitat
    tk.Label(entrada_frame, text="Quantitat:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    quantitat_entry = tk.Entry(entrada_frame)
    quantitat_entry.grid(row=2, column=1, padx=5, pady=5)

    # Camp per al total
    tk.Label(entrada_frame, text="Total:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    total_label = tk.Label(entrada_frame, text="0.00 €", font=("Arial", 12))
    total_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Funció per calcular el total
    def calcular_total():
        try:
            producte_id = producte_combo.get().split(" - ")[0]
            quantitat = int(quantitat_entry.get())
            preu = next(p[2] for p in productes if str(p[0]) == producte_id)
            total = quantitat * preu
            total_label.config(text=f"{total:.2f} €")
        except Exception as e:
            messagebox.showerror("Error", "Revisa els camps introduïts.")

    # Botó per calcular el total
    calcular_button = tk.Button(entrada_frame, text="Calcular Total", command=calcular_total)
    calcular_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Botó per registrar la venda
    def registrar_venda():
        try:
            producte_id = producte_combo.get().split(" - ")[0]
            client_id = client_combo.get().split(" - ")[0]
            quantitat = int(quantitat_entry.get())
            total = float(total_label.cget("text").replace("€", "").strip())

            connection = connectar_bbdd()
            cursor = connection.cursor()
            query = "INSERT INTO vendes_particulars (id_client, id_producte, quantitat, total, data_venda) VALUES (%s, %s, %s, %s, CURDATE())"
            cursor.execute(query, (client_id, producte_id, quantitat, total))
            connection.commit()
            cursor.close()
            connection.close()

            carregar_vendes()
            messagebox.showinfo("Èxit", "Venda registrada correctament!")
        except Exception as e:
            messagebox.showerror("Error", "No s'ha pogut registrar la venda. Revisa els camps.")

    registrar_button = tk.Button(entrada_frame, text="Registrar Venda", command=registrar_venda, bg="green", fg="black")
    registrar_button.grid(row=5, column=0, columnspan=2, pady=10)

    # TreeView per mostrar les vendes
    tree_frame = tk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

    columns = ("ID", "Producte", "Client", "Quantitat", "Total", "Data")
    vendes_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        vendes_tree.heading(col, text=col)
        vendes_tree.column(col, width=150)

    vendes_tree.pack(fill="both", expand=True)

    # Funció per carregar les vendes
    def carregar_vendes():
        vendes_tree.delete(*vendes_tree.get_children())
        connection = connectar_bbdd()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT v.id_venda, i.nom_producte, CONCAT(c.nom, ' ', c.cognoms), v.quantitat, v.total, v.data_venda
            FROM vendes_particulars v
            JOIN inventari i ON v.id_producte = i.id
            JOIN clients_particulars c ON v.id_client = c.id_client;
        """)
        resultats = cursor.fetchall()
        for venda in resultats:
            vendes_tree.insert("", "end", values=venda)
        cursor.close()
        connection.close()

    carregar_vendes()

# Funcions per carregar clients i productes
def carregar_clients():
    connection = connectar_bbdd()
    cursor = connection.cursor()
    cursor.execute("SELECT id_client, nom, cognoms FROM clients_particulars")
    clients = cursor.fetchall()
    cursor.close()
    connection.close()
    return clients

def carregar_productes():
    connection = connectar_bbdd()
    cursor = connection.cursor()
    cursor.execute("SELECT id, nom_producte, preu FROM inventari WHERE quantitat > 0")
    productes = cursor.fetchall()
    cursor.close()
    connection.close()
    return productes


