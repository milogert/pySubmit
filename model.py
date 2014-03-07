import hashlib
import sqlite3


def addUser(theUsername, thePassword, theRole):
  aHash = hashlib.sha224(str(thePassword)).hexdigest()

  aRet = "ii No error."

  # Execute.
  try:
    # Open a connection.
    aConn = sqlite3.connect("pySubmit.db")
    aCursor = aConn.cursor()

    # The sqlite statement.
    aS = """
      INSERT INTO users (username, password, role)
      VALUES (?, ?, ?)
    """
    aQ = (theUsername, aHash, theRole,)

    aCursor.execute(aS, aQ)
    aConn.commit()

    # Commit the changes and close the connection.
    aConn.close()
  except sqlite3.Error as aErr:
    aRet = "-- " + str(aErr)
    print "-- Error " + aRet

  return aRet


def deleteUser(theUsername):
  aRet = "ii No error."

  # Execute.
  try:
    # Open a connection.
    aConn = sqlite3.connect("pySubmit.db")
    aCursor = aConn.cursor()

    # The sqlite statement.
    aS = """
      DELETE FROM users
      WHERE username = ?
    """
    aQ = (theUsername,)

    aCursor.execute(aS, aQ)
    aConn.commit()

    # Commit the changes and close the connection.
    aConn.close()
  except sqlite3.Error as aErr:
    aRet = "-- " + str(aErr)
    print "-- Error " + aRet

  return aRet


def editUser(theUsername, thePassword, theRole):
  aHash = hashlib.sha224(str(thePassword)).hexdigest()

  aRet = "ii No error."

  # Execute.
  try:
    # Open a connection.
    aConn = sqlite3.connect("pySubmit.db")
    aCursor = aConn.cursor()

    # The sqlite statement.
    aS = """
      UPDATE users
      SET password=?, role=?
      WHERE username=?
    """
    aQ = (aHash, theRole, theUsername,)

    aCursor.execute(aS, aQ)
    aConn.commit()

    # Commit the changes and close the connection.
    aConn.close()
  except sqlite3.Error as aErr:
    aRet = "-- " + str(aErr)
    print "-- Error " + aRet

  return aRet


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

  # Close the database connection.
  aConn.close()

  return aRet


if __name__ == '__main__':
  addUser("test", "test", "judge")