# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    session.flash = T(request.args(0))
    unsold = request.args(0) == 'unsold'
    if  unsold:
        session.flash = T("Show unsold")
        forsale=(db.forsale.sold==False)
        button = A('See unsold', _class='btn btn-success', _href=URL('default', 'index'))
    else:
        session.flash = T("Show  All")
        forsale=db.forsale
        button = A('See all', _class='btn btn-warning', _href=URL('default', 'index', args='unsold'))

    grid = SQLFORM.grid(forsale,csv=False,create=False, searchable=False,args=request.args[:1])
    return locals()


@auth.requires_login()
#@auth.requires_signature()
def add():
    """Add a post."""
    form = SQLFORM(db.forsale)
    if form.process().accepted:
        # Successful processing.
        session.flash = T("inserted")
        redirect(URL('default', 'index'))
    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
