import mysql.connector
from tkinter import messagebox

def connectar_bbdd():
    """Connecta a la base de dades MySQL i retorna la connexió."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="crm_mp05",
            user="root",
            password="rootroot",
        )
        return connection
    except mysql.connector.Error as error:
        messagebox.showerror("Error de Connexió", f"No s'ha pogut connectar a la base de dades:\n{error}")
        return None

def obtenir_personal():
    connexio = connectar_bbdd()
    cursor = connexio.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal")
    personal = cursor.fetchall()
    connexio.close()
    return personal

def guardar_canvis_personal(valors, personal_id):
    """Actualitza els registres del personal a la base de dades."""
    try:
        connexio = connectar_bbdd()
        if connexio:
            cursor = connexio.cursor()
            query = """
            UPDATE personal SET nombre=%s, apellidos=%s, dni=%s, email=%s, telefono=%s,
            fecha_contratacion=%s, puesto=%s, salario=%s, departamento=%s,
            fecha_nacimiento=%s, activo=%s WHERE id_personal=%s
            """
            print(valors.keys())
            dades_query = (
                valors["nombre"], valors["apellidos"], valors["dni"], valors["email"], valors["telefono"],
                valors["fecha_contratacion"], valors["puesto"], valors["salario"], valors["departamento"],
                valors["fecha_nacimiento"], valors["activo"], personal_id
            )
            cursor.execute(query, dades_query)
            connexio.commit()
            cursor.close()
            connexio.close()
            return True
    except mysql.connector.Error as error:
        messagebox.showerror("Error en Actualització", f"No s'ha pogut actualitzar el registre:\n{error}")
    return False

def obtenir_registre(id_actual, moviment="actual"):
    """Obté un registre específic segons el moviment ('anterior', 'seguent', 'actual')."""
    connexio = connectar_bbdd()
    if connexio:
        cursor = connexio.cursor(dictionary=True)
        try:
            if moviment == "anterior":
                query = "SELECT * FROM personal WHERE id_personal < %s ORDER BY id_personal DESC LIMIT 1"
            elif moviment == "seguent":
                query = "SELECT * FROM personal WHERE id_personal > %s ORDER BY id_personal ASC LIMIT 1"
            else:
                query = "SELECT * FROM personal WHERE id_personal = %s"

            cursor.execute(query, (id_actual,))
            registre = cursor.fetchone()
            cursor.close()
            connexio.close()
            return registre
        except mysql.connector.Error as error:
            messagebox.showerror("Error de Base de Dades", f"No s'ha pogut obtenir el registre:\n{error}")
            return None
    return None

def obtenir_inventari():
    """Obté totes les dades de l'inventari."""
    connexio = connectar_bbdd()
    cursor = connexio.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventari")
    inventari = cursor.fetchall()
    connexio.close()
    return inventari

def inserir_producte_inventari(nom, desc, cat, preu, quantitat, estoc_minim):
    """Insereix un nou producte a l'inventari."""
    try:
        connexio = connectar_bbdd()
        cursor = connexio.cursor()
        query = """
        INSERT INTO inventari (nom_producte, descripcio, categoria, preu, quantitat, estoc_minim)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nom, desc, cat, preu, quantitat, estoc_minim))
        connexio.commit()
        connexio.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

