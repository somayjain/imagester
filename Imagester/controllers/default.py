@auth.requires_login()
def index():
    response.flash = "Welcome to Imagster!"

    query= (db.image.author== session.auth.user.first_name + " " + session.auth.user.last_name) 
    query2= (db.image.author!= session.auth.user.first_name + " " + session.auth.user.last_name) 
    images=db(query).select(db.image.ALL)
    images2=db(query2).select(db.image.ALL)
    return dict(images=images, images2=images2)


@auth.requires_login()
def show():
    db.comment.author.default = session.auth.user.first_name + " " + session.auth.user.last_name
    image = db(db.image.id==request.args(0)).select().first()
    db.comment.image_id.default = image.id
    form = SQLFORM(db.comment)
    if form.process().accepted:
	response.flash = 'Your Comment Is Posted'
    comments = db(db.comment.image_id==image.id).select()
    return dict(image=image, comments=comments, form=form)

@auth.requires_login()
def up():
    db.image.author.default = session.auth.user.first_name + " " + session.auth.user.last_name
    form=SQLFORM(db.image)
    if form.process().accepted:
	response.flash="Photo Uploaded"
	redirect(URL('index'))
    return dict(form =form)
    
@auth.requires_login()
def delete():
	imageid= request.args(0)
	db(db.image.id==imageid).delete()
	redirect(URL('index'))
	
@auth.requires_login()
def like():
	imageid=request.args(0)
	db.likes.insert(imageid=imageid, authorid=session.auth.user.id)
	response.flash="Liked"
	url = "show/"+str(imageid)
	redirect(URL(url))

@auth.requires_login()
def unlike():
	imageid=request.args(0)
	db(db.likes.imageid==imageid and db.likes.authorid==session.auth.user.id).delete()
	response.flash="UnLiked"
	url = "show/"+str(imageid)
	redirect(URL(url))

@auth.requires_membership('manager')
def manage():
	grid = SQLFORM.smartgrid(db.image)
	query = (db.auth_user.id>0)
	users=db(query).select(db.auth_user.id, db.auth_user.first_name, db.auth_user.last_name, db.auth_user.email)
	
	groupid=db(db.auth_group.role=='manager').select()[0].id
	query = (db.auth_membership.group_id==groupid)
	man =db(query).select()
	
	return dict(grid=grid, users=users, man= man)
		
@auth.requires_membership('manager')
def add_manager():
	userid= request.args(0)
	groupid=request.args(1)
	auth.add_membership(groupid, userid)
	response.flash="Liked"
	redirect(URL('manage'))


def user():
    return dict(form=auth())


def download():
    return response.download(request,db)


def call():
    return service()


@auth.requires_signature()
def data():
    return dict(form=crud())

