import sqlite3
from sqlite3 import Error


# Create a db connection
def create_connection(db_file):
    """Create a databse connection to a SQLite databse specified by a db_file
    :param: db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    
    except Error as e:
        print(e)
        
    return conn

# Create db tables
def create_table(conn, create_table_sql):
    """ create a table from the creat_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Insert data
def register_user(conn, user):
    """
    Create a new user into the users table
    :param conn:
    :param user:
    :return: project id
    """
    sql = ''' INSERT INTO users (username, password)
              VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

# Main
def main():
    database = r"f1.db"
    
    ''' Create Database
    # sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
    #                                     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                                     username text UNIQUE,
    #                                     password text
    #                                 );"""

    # sql_create_user_guesses_table = """CREATE TABLE IF NOT EXISTS user_guesses (
    #                                         guess_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                                         user_id INTEGER,
    #                                         driver1 TEXT,
    #                                         driver2 TEXT,
    #                                         circuit TEXT,
    #                                         FOREIGN KEY (user_id) REFERENCES users (user_id)
    #                                     );"""
    '''
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a a new user
        user = ('admin', 'admin')
        
        # register user
        register_user(conn, user)

    '''Create database tables
        # if conn is not None:
    #     create_table(conn, sql_create_users_table)
    #     create_table(conn, sql_create_user_guesses_table)
    # else:
    #     print("Error!")
    '''


if __name__ == '__main__':
    main()
