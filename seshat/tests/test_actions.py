import seshat.actions as actions

def test_redirect():
    a = actions.Redirect("/")()
    assert a is not None
    assert a.status == "303 SEE OTHER"
    assert "Location" in a.headers

def test_not_found():
    a = actions.NotFound()()
    assert a is not None
    assert a.status == "404 NOT FOUND"

def test_unauth():
    a = actions.Unauthorized()()
    assert a is not None
    assert a.status == "401 UNAUTHORIZED"


#class CustomAction(actions.BaseAction):
    #def __init__(self):
        #self.head = Head("711 WAT")


#def test_custom():
    #a = CustomAction()
    #assert a.head is not None
    #assert a.head.status == "711 WAT"
