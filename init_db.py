from backend import db, TodoDAO
db.create_all()


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})
