from webtest import TestApp

import os
import arapi

os.environ['ARAPI_CONFIG'] = './arapi/conf/arapi_dev.cfg'

def test_arapi():
    app = TestApp(arapi.GetMainApp())
    get_str = '/help'
    assert app.get(get_str).status == '200 OK'


def test_get():
    app = TestApp(arapi.GetMainApp())
    get_str = '/get/files/etc/hosts/1/ipaddr'
    resp = app.get(get_str)
    assert resp.status == '200 OK'
    resp.mustcontain == '127.0.0.1'

