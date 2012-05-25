from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from i18n.dbtranslator import DBModel

def pytest_funcarg__engine(request):
    def setup():
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        return engine
    return request.cached_setup(setup, scope='session')


def test_DBModel():
    engine1 = create_engine('sqlite:///:memory:', echo=True)
    engine2 = create_engine('sqlite:///:memory:', echo=True)    
    db1 = DBModel(engine1)
    db2 = DBModel(engine2)
    #
    session1 = db1.Session()
    x = db1.Translation('it_IT', 'hello', 'ciao')
    session1.add(x)
    session1.flush()
    assert session1.query(db1.Translation).all() == [x]
    #
    session2 = db2.Session()
    y = db2.Translation('it_IT', 'world', 'mondo')
    session2.add(y)
    session2.flush()
    assert session2.query(db2.Translation).all() == [y]
