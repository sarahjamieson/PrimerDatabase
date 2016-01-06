import sqlite3 as lite
import petl

con = lite.connect('test.db')  # Makes a connection to the test.db database
curs = con.cursor()


# Connects to a database and checks this connection by printing the version number.
def check_connection():
    # This can be used instead of "try, finally" as it automatically releases the resources and provides error handling.
    with con:
        # Uses cursor to select the SQLite version number
        curs.execute('SELECT SQLITE_VERSION()')
        # Fetches the SQLite version number
        version_no = curs.fetchone()
        # Prints the SQLite version number
        print 'SQLite version: %s' % version_no


# Creates two tables called Genes and Primers.
def create_table():
    with con:
        curs.execute('DROP TABLE IF EXISTS Genes')
        curs.execute('DROP TABLE IF EXISTS Primers')
        curs.execute('DROP TABLE IF EXISTS Test')
        curs.execute('CREATE TABLE Genes(Gene TEXT PRIMARY KEY, Chromosome INT)')
        curs.execute(
            'CREATE TABLE Primers(Primer_Id INT PRIMARY KEY, Gene TEXT, Exon INT, Primer_Set TEXT, Direction TEXT, '
            'Primer_seq TEXT, M13_tagged TEXT, Frag_size INT, Anneal_temp INT, Other_info TEXT)')
        curs.execute(
            'CREATE TABLE Test(Gene TEXT, Exon TEXT, Direction TEXT, Version_Number INT, Primer_seq TEXT, Ch INT, '
            'M13_tagged TEXT, Primer_Batch TEXT, Frag_size INT, Anneal_temp INT, Other_info TEXT)')

        con.commit()  # Useful to have when execute statements become more complex
        print "Tables created"


def extract_data_into_table():
    primer_data = petl.io.xlsx.fromxlsx('primer_batch_records.xlsx')
    for row in primer_data:
        con.cursor().execute('INSERT INTO Test VALUES (?,?,?,?,?,?,?,?,?,?,?)', row)
        con.commit()


def display_data():
    curs.execute('SELECT * FROM Test')
    for row in curs:
        print row


check_connection()
create_table()
extract_data_into_table()
display_data()



