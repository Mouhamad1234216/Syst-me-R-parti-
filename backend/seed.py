from app import app, db, User, Product

def seed():
    with app.app_context():
        # Sample users
        users = [
            User(name='Alice'),
            User(name='Bob'),
            User(name='Charlie')
        ]
        # Sample products
        products = [
            Product(name='Widget A'),
            Product(name='Widget B')
        ]

        # Avoid duplicating: only add if table empty
        if User.query.count() == 0:
            db.session.add_all(users)
        if Product.query.count() == 0:
            db.session.add_all(products)
        db.session.commit()
        print('Seeding complete')

if __name__ == '__main__':
    seed()
