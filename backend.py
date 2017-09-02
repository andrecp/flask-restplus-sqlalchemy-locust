from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix

from flask_sqlalchemy import SQLAlchemy

# App definition.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.wsgi_app = ProxyFix(app.wsgi_app)
db = SQLAlchemy(app)


# Db definition.
class TODOModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80))

    def __init__(self, task):
        self.task = task

    def __repr__(self):
        return '<Task %r>' % self.task


# Api definition.
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)

ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class TodoDAO(object):

    @property
    def todos(self):
        return TODOModel.query.all()

    def get(self, id):
        todo = TODOModel.query.filter_by(id=id).first()
        if todo:
            return {"id": todo.id, "task": todo.task}
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = TODOModel(data['task'])
        db.session.add(todo)
        db.session.commit()
        return todo

    def update(self, id, data):
        todo = TODOModel.query.filter_by(id=id).first()
        todo.task = data['task']
        db.session.commit()
        return todo

    def delete(self, id):
        todo = TODOModel.query.filter_by(id=id).first()
        db.session.delete(todo)
        db.session.commit()


DAO = TodoDAO()

@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        print api.payload
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
