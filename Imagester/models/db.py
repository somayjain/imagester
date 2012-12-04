db = DAL('sqlite://storage.sqlite')

from gluon.tools import Auth, Crud
auth = Auth(db, hmac_key=Auth.get_or_create_key())
auth.define_tables()
crud = Crud(db)
	


db.define_table('image',Field('title', unique=True),Field('file', 'upload', autodelete=True),Field('author'),format = '%(title)s')

db.define_table('comment',Field('image_id', db.image),Field('author'),Field('body', 'text'))

db.define_table('likes',Field('imageid', db.image), Field('authorid', db.auth_user))


db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.comment.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')


db.comment.body.requires = IS_NOT_EMPTY()
db.comment.image_id.writable = db.comment.image_id.readable = False

#db.image.author.default = session.auth.user.first_name + " " + session.auth.user.last_name
#db.comment.author.default = session.auth.user.first_name + " " + session.auth.user.last_name
db.image.author.readable=db.image.author.writable=False
db.comment.author.readable=db.comment.author.writable=False

