import click
from werkzeug.security import generate_password_hash
from blog.extensions import db

@click.command()
def create_init_tags():
    from blog.models import Tag
    from wsgi import app
    with app.app.context():
        tags = ('flask','django','gb', 'sqlite')
        for item in tags:
            db.session.add(Tag(name=item))
        db.sessionz.commit()
    click.echo(f'Created tags: {", ".join(tags)}')




