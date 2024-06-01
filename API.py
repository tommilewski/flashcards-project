from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    flashcards = db.relationship('FlashCard', backref='user', lazy=True)

class FlashCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not all(key in data for key in ['username', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400

    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not all(key in data for key in ['username', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    
@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    flashcards = FlashCard.query.all()
    flashcards_info = [{'id': flashcard.id, 'title': flashcard.title, 'content': flashcard.content, 'username': flashcard.user.username} for flashcard in flashcards]
    return flashcards_info

@app.route('/flashcards/<string:username>', methods=['GET'])
def get_flashcards_by_username(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    flashcards = FlashCard.query.filter_by(user_id=user.id).all()
    return [{'id': flashcard.id, 'title': flashcard.title, 'content': flashcard.content, 'username': flashcard.user.username} for flashcard in flashcards]


@app.route('/flashcards/add', methods=['POST'])
def add_flashcard():
    data = request.get_json()
    username = data.get('username')
    title = data.get('title')
    content = data.get('content')

    if not all([username, title, content]):
        return jsonify({'message': 'Missing required fields'}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    flashcard = FlashCard(title=title, content=content, user_id=user.id)
    db.session.add(flashcard)
    db.session.commit()
    return jsonify({'message': 'Flashcard added successfully'}), 201

@app.route('/flashcards/search/<string:name>', methods=['GET'])
def findAllByName(name):
    flashcards = FlashCard.query.filter(FlashCard.title.ilike(f"{name}%")).all()
    if not flashcards:
        return []

    return [{'id': flashcard.id, 'title': flashcard.title, 'content': flashcard.content} for flashcard in flashcards]

@app.route('/flashcards/delete/<int:flashcard_id>', methods=['DELETE'])
def delete_flashcard(flashcard_id):
    flashcard = FlashCard.query.get(flashcard_id)
    
    if not flashcard:
        return jsonify({'message': 'Flashcard not found'}), 404
    
    db.session.delete(flashcard)
    db.session.commit()
    
    return jsonify({'message': 'Flashcard deleted successfully'}), 200


@app.route('/flashcards/edit/<int:flashcard_id>', methods=['PUT'])
def edit_flashcard(flashcard_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not all([title, content]):
        return jsonify({'message': 'Missing required fields'}), 400

    flashcard = FlashCard.query.get(flashcard_id)

    if not flashcard:
        return jsonify({'message': 'Flashcard not found'}), 404

    flashcard.title = title
    flashcard.content = content
    db.session.commit()

    return jsonify({'message': 'Flashcard updated successfully'}), 200
    
if __name__ == '__main__':
    app.run(debug=True)