from databases import DatabaseURL


def test_database_url_repr():
    u = DatabaseURL("postgresql://localhost/name")
    assert repr(u) == "DatabaseURL('postgresql://localhost/name')"

    u = DatabaseURL("postgresql://username@localhost/name")
    assert repr(u) == "DatabaseURL('postgresql://username@localhost/name')"

    u = DatabaseURL("postgresql://username:password@localhost/name")
    assert repr(u) == "DatabaseURL('postgresql://username:********@localhost/name')"


def test_database_url_properties():
    u = DatabaseURL("postgresql+asyncpg://username:password@localhost:123/mydatabase")
    assert u.dialect == "postgresql"
    assert u.driver == "asyncpg"
    assert u.username == "username"
    assert u.password == "password"
    assert u.hostname == "localhost"
    assert u.port == 123
    assert u.database == "mydatabase"


def test_database_url_options():
    u = DatabaseURL("postgresql://localhost/mydatabase?pool_size=20&ssl=true")
    assert u.options == {"pool_size": "20", "ssl": "true"}


def test_replace_database_url_components():
    u = DatabaseURL("postgresql://localhost/mydatabase")

    assert u.database == "mydatabase"
    new = u.replace(database="test_" + u.database)
    assert new.database == "test_mydatabase"
    assert str(new) == "postgresql://localhost/test_mydatabase"

    assert u.driver == ""
    new = u.replace(driver="asyncpg")
    assert new.driver == "asyncpg"
    assert str(new) == "postgresql+asyncpg://localhost/mydatabase"

    assert u.port is None
    new = u.replace(port=123)
    assert new.port == 123
    assert str(new) == "postgresql://localhost:123/mydatabase"

    u = DatabaseURL("sqlite:///mydatabase")
    assert u.database == "mydatabase"
    new = u.replace(database="test_" + u.database)
    assert new.database == "test_mydatabase"
    assert str(new) == "sqlite:///test_mydatabase"

    u = DatabaseURL("sqlite:////absolute/path")
    assert u.database == "/absolute/path"
    new = u.replace(database=u.database + "_test")
    assert new.database == "/absolute/path_test"
    assert str(new) == "sqlite:////absolute/path_test"

    u = DatabaseURL("MSSQLBackend+aioodbc://localhost/test_database_aioodbc")
    assert u.database == "test_database_aioodbc"
    new = u.replace(database="test_" + u.database)
    assert new.database == "test_test_database_aioodbc"
    assert str(new) == "MSSQLBackend+aioodbc://localhost/test_test_database_aioodbc"
