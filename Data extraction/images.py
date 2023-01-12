import pyodbc

bd = input()
conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
                      fr"DBQ=.\bd_{bd}.accdb")
cursor = conn.cursor()
cursor.execute("SELECT * FROM Monedas WHERE IdMoneda = 1135")
for row in cursor.fetchall():
    print(row)

