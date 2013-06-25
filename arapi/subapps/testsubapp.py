import arapi.bottle

app = arapi.bottle.Bottle()
url_base = '/testsubapp/'

@app.get('/help')
def help():
    arapi.bottle.response.content_type = "text/plain"
    return app.config.doc

@app.post('/addserver/')
def handle_addhost(augeas_handle):
    """  Will return "added"
    """
    print "adding host"
    arapi.bottle.response.conent_type = "text/plain"
    return "added"

@app.post('/removeserver/')
def handle_removehost(augeas_handle):
    """  Will return "removed"
    """
    print "adding host"
    arapi.bottle.response.conent_type = "text/plain"
    return "removed"
