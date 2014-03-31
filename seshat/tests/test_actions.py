import seshat.actions as actions

def test_redirect():
    a = actions.Redirect("/")()
    assert a is not None
    assert a.status == "303 SEE OTHER"
    assert "Location" in a.headers

def test_unauth():
    a = actions.Unauthorized()()
    assert a is not None
    assert a.status == "401 UNAUTHORIZED"

def test_bad_request():
    a = actions.BadRequest()()
    assert a is not None
    assert a.status == "400 BAD REQUEST"

def test_forbidden():
    a = actions.Forbidden()()
    assert a is not None
    assert a.status == "403 FORBIDDEN"

def test_not_found():
    a = actions.NotFound()()
    assert a is not None
    assert a.status == "404 NOT FOUND"

def test_method_not_allowed():
    a = actions.MethodNotAllowed(["GET"])()
    assert a is not None
    assert a.status == "405 METHOD NOT ALLOWED"

def test_internal_server_error():
    a = actions.InternalServerError(Exception("one"), "two")()
    assert a is not None
    assert a.status == "500 INTERNAL SERVER ERROR"
    assert a.errors is not None
    assert len(a.errors) == 2
    assert type(a.errors[0]) is Exception
    assert a.errors[1] == "two"
