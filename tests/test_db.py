from git_objview.db import RepoDB


def test_import_repodb():
    rdb = RepoDB(".")
    assert str(rdb.path) == "."
