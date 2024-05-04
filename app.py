
from flask import Flask, request
from flask_restx import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SECRET_KEY'] = 'test'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String(1000), nullable = True)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Note (id = {self.id}, title = {self.title}, content = {self.content})"


db.create_all()

noteArgs = reqparse.RequestParser()
noteArgs.add_argument("title", type = str, help = "Title is required for the note", required = True)
noteArgs.add_argument("content", type = str, help = "")
noteArgs.add_argument("user_id", type = str, help = "Note needs user")

updateArgs = reqparse.RequestParser()
updateArgs.add_argument("title", type = str, help = "Title is required for the note")
updateArgs.add_argument("content", type = str, help = "")


resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "user_id": fields.Integer
}

def encode_auth_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, 'your_secret_key', algorithm='HS256')
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, 'your_secret_key', algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be blank.")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")
        data = parser.parse_args()

        if UserModel.query.filter_by(username=data['username']).first():
            abort(409, message="A user with that username already exists.")

        hashed_password = generate_password_hash(data['password'], method='sha256')
        user = UserModel(username=data['username'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 201

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be blank.")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")
        data = parser.parse_args()

        user = UserModel.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            abort(401, message="Invalid Credentials!")

        token = encode_auth_token(user.id)
        return {"token": token}, 200

class Notes(Resource):
    @marshal_with(resource_fields)
    def get(self, note_id = None):

        if note_id == 999:
            result = NoteModel.query.all()
            return result

        if note_id or note_id == 0:
            result = NoteModel.query.filter_by(id = note_id).first()
            if not result:
                abort(404, message = "Note id not found")
            return result
    
    @marshal_with(resource_fields)
    def post(self, note_id):
        args = noteArgs.parse_args()
        result = NoteModel.query.filter_by(id = note_id).first()

        if result:
            abort(409, message = "Note is missing fields")

        note = NoteModel(id= note_id, title = args['title'], content=args['content'], user_id = args['user_id'])

        db.session.add(note)
        db.session.commit()
        return note, 201

    @marshal_with(resource_fields)
    def patch(self, note_id):
        args = updateArgs.parse_args()
        result = NoteModel.query.filter_by(id=note_id).first()
        if not result:
            abort(404, message="Note doesn't exist, cannot update")

        if args['title']:
            result.title = args['title']
        if args['content']:
            result.content = args['content']

        db.session.commit()

        return result
  

    def delete(self, note_id):
        result = NoteModel.query.filter_by(id=note_id).first()
        
        if not result:
            abort(404, message="Note not found")

        db.session.delete(result)
        db.session.commit()
        
        return {'message': 'Note deleted'}, 204

class NoteSearch(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, required=True, help='Search query is required')
        args = parser.parse_args()
        search_query = args['query']
        results = NoteModel.query.filter(NoteModel.content.like(f'%{search_query}%')).all()
        return {'Note(s) with the keyword': [{'id': note.id, 'title': note.title, 'content': note.content} for note in results]}

api.add_resource(Notes, "/notes/<int:note_id>")
api.add_resource(NoteSearch, '/noteSearch/search')
api.add_resource(UserRegister, '/api/auth/signup')
api.add_resource(UserLogin, '/api/auth/login')

if __name__ == '__main__':
    app.run(debug=True)
