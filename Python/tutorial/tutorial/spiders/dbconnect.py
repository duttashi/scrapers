import pyodbc
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=ASHOO-PC\SQLEXPRESS;"
                      "Database=DB2018;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()
cursor.execute('SELECT * FROM groceries')

for row in cursor:
    print('row = %r' % (row,))