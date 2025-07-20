from git_objview.git import Repo


def test_import_repodb():
    rdb = Repo(".")
    assert str(rdb.path) == "."
