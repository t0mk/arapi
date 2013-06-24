import arapi.bottle

app = arapi.bottle.Bottle()

@app.post('/addserver/')
def handle_addhost(augeas_handle):
    print "adding host"
    arapi.bottle.response.conent_type = "text/plain"
    return "added"

@app.post('/removeserver/')
def handle_removehost(augeas_handle):
    print "adding host"
    arapi.bottle.response.conent_type = "text/plain"
    return "removed"
