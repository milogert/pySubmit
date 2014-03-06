import sqlite3

def getUsers():
  # Open a connection.
  aConn = sqlite3.connect("pySubmit.db")

  # Get a cursor.
  aCursor = aConn.cursor()

  # The sqlite statement.
  aS = "SELECT * FROM users ORDER BY role"

  # Loop through the cursor and append them to a return.
  aRet = []
  for aRow in aCursor.execute(aS):
    aRet.append(aRow)

  return aRet
