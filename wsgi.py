from werkzeug.security import generate_password_hash

from blog.app import create_app, db

app = create_app()


# @app.cli.command('init-db')
# def init_db():
#     db.create_all()


@app.cli.command('create-users')
def create_users():
    from blog.models import User

    db.session.add(User(name='Ivan', email='ivan@email.com', password=generate_password_hash('test123')))
    db.session.add(
        User(name='localadmin', email='locadm@email.com', password=generate_password_hash('test123'), admin=True))

    db.session.commit()


@app.cli.command()
def create_init_tags():
    from blog.models import Tag
    tags = ('flask', 'django', 'gb', 'sqlite')
    for item in tags:
        db.session.add(Tag(name=item))
    db.session.commit()
