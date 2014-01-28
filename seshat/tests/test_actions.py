import seshat.actions as actions

def test_redirect():
    a = actions.Redirect("/")
    assert a.head is not None
    assert a.head.status == "303 SEE OTHER"
    assert a.head.headers[0] == ("Location", "/")

def test_note_found():
    a = actions.NotFound()
    assert a.head is not None
    assert a.head.status == "404 NOT FOUND"
