# import sqlite3
import ast
import sqlite3

conn = sqlite3.connect('oauth_tokens.db')
cursor = conn.cursor()

# Create the token cache table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS oauth_tokens (
        access_token TEXT,
        rar_object TEXT
    )
''')

conn.commit()

def cache_token(access_token, rar_object):
    cursor.execute('''INSERT OR REPLACE INTO oauth_tokens (access_token, rar_object)
        VALUES (?, ?)''', (access_token, rar_object))
    conn.commit()


def get_cached_rar_object(access_token):
    cursor.execute('SELECT rar_object FROM oauth_tokens WHERE access_token = ?', (access_token,))
    row = cursor.fetchone()
    if row is not None:
        rar_object, = row
        return ast.literal_eval(rar_object)
    return None
