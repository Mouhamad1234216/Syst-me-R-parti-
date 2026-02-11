from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/postgres')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

@app.route('/api/users')
def get_users():
    users = User.query.limit(10).all()
    if not users:
        # return sample data if DB empty
        return jsonify([{'id':1,'name':'Alice'},{'id':2,'name':'Bob'}])
    return jsonify([{'id':u.id,'name':u.name} for u in users])

@app.route('/api/products')
def get_products():
    products = Product.query.limit(10).all()
    if not products:
        return jsonify([{'id':1,'name':'Demo Product'}])
    return jsonify([{'id':p.id,'name':p.name} for p in products])

if __name__ == '__main__':
    # Create tables if not exists (safe for demo)
    try:
        db.create_all()
    except Exception:
        pass
    app.run(host='0.0.0.0', port=5000)
