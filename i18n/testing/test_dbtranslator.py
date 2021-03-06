from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from i18n.dbtranslator import DBModel, DBTranslator
from i18n.testing.test_translator import add_translation

def pytest_funcarg__engine(request):
    return create_engine('sqlite:///:memory:', echo=True)


def test_DBModel():
    engine1 = create_engine('sqlite:///:memory:', echo=True)
    engine2 = create_engine('sqlite:///:memory:', echo=True)    
    db1 = DBModel(engine1)
    db2 = DBModel(engine2)
    #
    session1 = db1.Session()
    x = db1.TranslationEntry('it_IT', 'hello', 'ciao')
    session1.add(x)
    session1.flush()
    assert session1.query(db1.TranslationEntry).all() == [x]
    #
    session2 = db2.Session()
    y = db2.TranslationEntry('it_IT', 'world', 'mondo')
    session2.add(y)
    session2.flush()
    assert session2.query(db2.TranslationEntry).all() == [y]


def test_DBTranslator(tmpdir, engine):
    tr = DBTranslator(tmpdir, ['it_IT'], engine=engine)
    tr.add_translation('it_IT', 'hello', 'ciao')
    assert tr.gettext('hello') == 'ciao'

def test_delegate_to_gettext(tmpdir, engine):
    tmpdir.join('foo.py').write("print _('hello'), _('world')")
    tr = DBTranslator(tmpdir, ['it_IT'], engine=engine)
    tr.extract()
    it_IT = tr.get_po('it_IT')
    add_translation(it_IT, 'hello', 'ciao')
    add_translation(it_IT, 'world', 'mondo')
    tr.compile()
    tr.reload()
    assert tr.gettext('hello') == 'ciao'
    assert tr.gettext('world') == 'mondo'
    #
    tr.add_translation('it_IT', 'hello', 'salve')
    assert tr.gettext('hello') == 'salve'
    assert tr.gettext('world') == 'mondo'


def test_caching(tmpdir, engine):
    tr = DBTranslator(tmpdir, ['it_IT'], engine=engine)
    tr.add_translation('it_IT', 'hello', 'ciao')
    assert tr.gettext('hello') == 'ciao'
    tr._lookup_entry = None # it'd crash if caching does not work
    assert tr.gettext('hello') == 'ciao'


def test_ngettext(tmpdir, engine):
    tr = DBTranslator(tmpdir, ['it_IT'], engine=engine)
    tr.add_translation('it_IT', 'apple', 'mela', 'mele')
    assert tr.ngettext('apple', 'apples', 0) == 'mele'
    assert tr.ngettext('apple', 'apples', 1) == 'mela'
    tr._lookup_entry = None # check caching
    assert tr.ngettext('apple', 'apples', 2) == 'mele'


def test_singular_vs_plural(tmpdir, engine):
    tr = DBTranslator(tmpdir, ['it_IT'], engine=engine)
    tr.add_translation('it_IT', 'hello', 'ciao')
    tr.add_translation('it_IT', 'apple', 'mela', 'mele')
    #
    # singular entries work only with gettext
    # plural entries work only with ngettext
    assert tr.gettext('apple') == 'apple'
    assert tr.ngettext('hello', 'hellos :-)', 1) == 'hello'
