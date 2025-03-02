import tkinter as tk
from tkinter import ttk
from database import connectar_bbdd


def mostrar_seccio_clients(main_frame):
    """Funció per mostrar la secció de clients en el marc principal."""

    # Neteja el contingut existent
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Títol principal
    tk.Label(main_frame, text="Gestió de Clients", font=("Arial", 16, "bold"), bg="#F6F8FA", fg="white").pack(pady=10)

    # Frame per a clients particulars
    frame_particulars = tk.LabelFrame(main_frame, text="Clients Particulars", font=("Arial", 12, "bold"))
    frame_particulars.pack(fill="both", expand=True, padx=10, pady=10)

    # Scrollbars per a clients particulars
    scrollbar_vertical_particulars = ttk.Scrollbar(frame_particulars, orient="vertical")
    scrollbar_vertical_particulars.pack(side="right", fill="y")

    scrollbar_horizontal_particulars = ttk.Scrollbar(frame_particulars, orient="horizontal")
    scrollbar_horizontal_particulars.pack(side="bottom", fill="x")

    # Treeview per a clients particulars
    columns_particulars = (
        "ID", "Nom", "Cognoms", "DNI", "Email", "Telèfon", "Direcció", "Data Registre", "Actiu", "Comentaris"
    )
    tree_particulars = ttk.Treeview(
        frame_particulars, columns=columns_particulars, show="headings",
        yscrollcommand=scrollbar_vertical_particulars.set, xscrollcommand=scrollbar_horizontal_particulars.set
    )

    for col in columns_particulars:
        tree_particulars.heading(col, text=col)
        tree_particulars.column(col, width=120)

    tree_particulars.pack(fill="both", expand=True)
    scrollbar_vertical_particulars.config(command=tree_particulars.yview)
    scrollbar_horizontal_particulars.config(command=tree_particulars.xview)

    # Frame per a clients empreses
    frame_empreses = tk.LabelFrame(main_frame, text="Clients Empreses", font=("Arial", 12, "bold"))
    frame_empreses.pack(fill="both", expand=True, padx=10, pady=10)

    # Scrollbars per a clients empreses
    scrollbar_vertical_empreses = ttk.Scrollbar(frame_empreses, orient="vertical")
    scrollbar_vertical_empreses.pack(side="right", fill="y")

    scrollbar_horizontal_empreses = ttk.Scrollbar(frame_empreses, orient="horizontal")
    scrollbar_horizontal_empreses.pack(side="bottom", fill="x")

    # Treeview per a clients empreses
    columns_empreses = (
        "ID", "Nom Empresa", "CIF", "Email", "Telèfon", "Direcció", "Data Registre", "Actiu", "Comentaris"
    )
    tree_empreses = ttk.Treeview(
        frame_empreses, columns=columns_empreses, show="headings",
        yscrollcommand=scrollbar_vertical_empreses.set, xscrollcommand=scrollbar_horizontal_empreses.set
    )

    for col in columns_empreses:
        tree_empreses.heading(col, text=col)
        tree_empreses.column(col, width=120)

    tree_empreses.pack(fill="both", expand=True)
    scrollbar_vertical_empreses.config(command=tree_empreses.yview)
    scrollbar_horizontal_empreses.config(command=tree_empreses.xview)

    # Funció per carregar dades de clients particulars
    def carregar_clients_particulars():
        tree_particulars.delete(*tree_particulars.get_children())
        connexio = connectar_bbdd()
        if connexio:
            cursor = connexio.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clients_particulars")
            for client in cursor.fetchall():
                tree_particulars.insert("", "end", values=(
                    client["id_client"], client["nom"], client["cognoms"], client["dni"], client["email"],
                    client["telefon"], client["direccio"], client["data_registre"],
                    "Sí" if client["actiu"] else "No", client["comentaris"]
                ))
            connexio.close()

    # Funció per carregar dades de clients empreses
    def carregar_clients_empreses():
        tree_empreses.delete(*tree_empreses.get_children())
        connexio = connectar_bbdd()
        if connexio:
            cursor = connexio.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clients_empreses")
            for empresa in cursor.fetchall():
                tree_empreses.insert("", "end", values=(
                    empresa["id_empresa"], empresa["nom_empresa"], empresa["cif"], empresa["email_empresa"],
                    empresa["telefon_empresa"], empresa["direccio_empresa"], empresa["data_registre"],
                    "Sí" if empresa["actiu"] else "No", empresa["comentaris"]
                ))
            connexio.close()

    # Carregar les dades inicialment
    carregar_clients_particulars()
    carregar_clients_empreses()

