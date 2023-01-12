import pyodbc

bd = input("Base de datos: ")
conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                      fr"DBQ=.\bd_{bd}.accdb")
cursor = conn.cursor()
doc = open(f"{bd}_datos.csv", "w", encoding="utf-8")

cursor.execute("SELECT * FROM Monedas WHERE idMoneda = 1")
n = len(cursor.fetchone())
print(n)
cursor.execute("SELECT * FROM Monedas")
columnas = []
for row in cursor.columns():
    columnas.append(row.column_name)
doc.write("|".join(columnas[:n]) + "\n")

cursor.execute("SELECT * FROM Monedas ORDER BY idMoneda")
for row in cursor.fetchall():
    lst = [str(x).replace("\n", " ").replace("\r", " ") if x is not None else "" for x in row]
    print("|".join(lst))
    doc.write("|".join(lst) + "\n")
cursor.close()
doc.close()
