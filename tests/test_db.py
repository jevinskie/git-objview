from git_objview.git import JRepo


def test_import_repodb():
    rdb = JRepo(".")
    assert str(rdb.path) == "."
