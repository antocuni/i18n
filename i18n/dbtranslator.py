from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#
from i18n import Translator

def setup_model(engine):

    Base = declarative_base(bind=engine)
    Session = sessionmaker(bind=engine)

    class Translation(Base):
        __tablename__ = 'translations'
        language = Column(String, primary_key=True) # destination language, e.g. it_IT
        msgid = Column(String, primary_key=True)
        msgstr = Column(String)

        def __init__(self, language, msgid, msgstr):
            self.language = language
            self.msgid = msgid
            self.msgstr = msgstr

        def __repr__(self):
            return "<Translation('%s','%s', '%s')>" % (
                self.language, self.msgid, self.msgstr)

    Base.metadata.create_all(engine)
    return locals()



class DBModel(object):

    def __init__(self, engine):
        self.__dict__.update(setup_model(engine))



class DBTranslator(Translator):

    def __init__(self, rootdir, languages, autocompile=True, engine=None):
        if engine is None:
            raise TypeError('the engine parameter is non-optional')
        Translator.__init__(self, rootdir, languages, autocompile)
        self.engine = engine
        self.db = DBModel(engine)
        self.session = self.db.Session()

    def add_translation(self, language, msgid, msgstr):
        x = self.db.Translation(language, msgid, msgstr)
        self.session.add(x)

    def gettext(self, msgid):
        assert len(self.languages) == 1 # fix me
        language = self.languages[0]
        q = self.session.query(self.db.Translation).filter_by(
            language = language, msgid = msgid)
        rows = q.all()
        if len(rows) == 0:
            return Translator.gettext(self, msgid)
        elif len(rows) == 1:
            return rows[0].msgstr
        else:
            # cannot happen because (language, msgid) is the primary key
            assert False, "Multiple translations of %s found: %s" % (msgid, rows)
