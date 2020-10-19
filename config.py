DATABASE = {
    "provider": 'sqlite',
    "filename": 'db.sqlite3'
}
"""
Variation DATABASE
    provider='sqlite', filename=':memory:'
    provider='sqlite', filename='filename', create_db=True
    provider='mysql', host='', user='', passwd='', db=''
    provider='oracle', user='', password='', dsn=''
    provider='cockroach', user='', password='', host='', database='', sslmode='disable'
"""
