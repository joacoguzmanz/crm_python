import tkinter as tk
from tkinter import ttk, messagebox
from database import obtenir_personal, obtenir_registre, guardar_canvis_personal

def mostrar_seccio_personal(main_frame):
    """Mostra la interfície de gestió del personal."""

    # Neteja el contingut existent
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Títol de la secció
    tk.Label(main_frame, text="Gestió de Personal", font=("Arial", 16, "bold"), bg="#34495E", fg="white").pack(pady=10)

    # Marc per al Treeview amb barres de desplaçament
    personal_frame = tk.Frame(main_frame, bg="#BDC3C7")
    personal_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Barra de desplaçament vertical
    scrollbar_vertical = ttk.Scrollbar(personal_frame, orient="vertical")
    scrollbar_vertical.pack(side="right", fill="y")

    # Barra de desplaçament horitzontal
    scrollbar_horizontal = ttk.Scrollbar(main_frame, orient="horizontal")
    scrollbar_horizontal.pack(side="bottom", fill="x")

    # Definició del Treeview
    columnes = (
        "ID", "Nom", "Cognoms", "DNI", "Email", "Telèfon", "Data Contractació",
        "Puesto", "Salari", "Departament", "Data Naixement", "Actiu"
    )
    personal_tree = ttk.Treeview(personal_frame, columns=columnes, show="headings", height=15,
                                 yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

    for col in columnes:
        personal_tree.heading(col, text=col, anchor="center")
        personal_tree.column(col, anchor="center", width=150)  # Ajusta les amplades segons calgui

    personal_tree.pack(side="left", fill="both", expand=True)

    # Vinculació de les barres amb el Treeview
    scrollbar_vertical.config(command=personal_tree.yview)
    scrollbar_horizontal.config(command=personal_tree.xview)

    # Funció per carregar dades
    def carregar_dades():
        personal_tree.delete(*personal_tree.get_children())
        personal = obtenir_personal()
        for persona in personal:
            personal_tree.insert("", "end", values=(
                persona["id_personal"], persona["nombre"], persona["apellidos"],
                persona["dni"], persona["email"], persona["telefono"],
                persona["fecha_contratacion"], persona["puesto"], persona["salario"],
                persona["departamento"], persona["fecha_nacimiento"],
                "Sí" if persona["activo"] else "No"
            ))

    carregar_dades()

    # Funció per obrir la finestra d'edició
    def obrir_finestra_edicio(event):
        seleccionat = personal_tree.selection()
        if not seleccionat:
            return

        # Obtenir ID del registre seleccionat
        dades = personal_tree.item(seleccionat[0], "values")
        personal_id = dades[0]

        # Crear la finestra emergent
        finestra_edicio = tk.Toplevel()
        finestra_edicio.title("Editar Personal")
        finestra_edicio.geometry("600x800")
        finestra_edicio.configure(bg="#f5f5f5")

        # Marc per als camps
        marc = tk.Frame(finestra_edicio, pady=10, padx=10, bg="#f5f5f5")
        marc.pack(fill="both", expand=True)

        # Diccionari de camps
        camps = {
            "Nom": "nombre",
            "Cognoms": "apellidos",
            "DNI": "dni",
            "Email": "email",
            "Telèfon": "telefono",
            "Data Contractació": "fecha_contratacion",
            "Puesto": "puesto",
            "Salari": "salario",
            "Departament": "departamento",
            "Data Naixement": "fecha_nacimiento",
            "Actiu": "activo"
        }
        entrades = {}

        for idx, (camp_formulari, camp_db) in enumerate(camps.items()):
            tk.Label(marc, text=camp_formulari, bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=idx, column=0, pady=5, sticky="w")
            entrada = tk.Entry(marc, font=("Arial", 10))
            entrada.grid(row=idx, column=1, pady=5, padx=10, sticky="ew")
            entrades[camp_db] = entrada

        def guardar_canvis_local():
            valors = {camp_db: entrada.get() for camp_db, entrada in entrades.items()}
            valors["activo"] = 1 if valors["activo"].lower() in ["sí", "1", "true", "actiu"] else 0
            if guardar_canvis_personal(valors, personal_id):
                messagebox.showinfo("Èxit", "Dades actualitzades correctament.")
                finestra_edicio.destroy()
                carregar_dades()
            else:
                messagebox.showerror("Error", "No s'han pogut actualitzar les dades.")

        tk.Button(
            finestra_edicio, text="Guardar Canvis", command=guardar_canvis_local,
            bg="#28a745", fg="white"
        ).pack(pady=20)

    personal_tree.bind("<Double-1>", obrir_finestra_edicio)

    # Botó de refresc
    btn_refrescar = tk.Button(
        main_frame, text="Refrescar llista", command=carregar_dades,
        bg="#17a2b8", fg="white"
    )
    btn_refrescar.pack(pady=10)

