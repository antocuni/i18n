from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#
from i18n.translator import Translator

def setup_model(engine):

    Base = declarative_base(bind=engine)
    Session = sessionmaker(bind=engine)

    class TranslationEntry(Base):
        __tablename__ = 'translation_entries'
        language = Column(String, primary_key=True) # destination language, e.g. it_IT
        msgid = Column(String, primary_key=True)
        msgstr = Column(String)
        msgstr_plural = Column(String)

        def __init__(self, language, msgid, msgstr, msgstr_plural=None):
            self.language = language
            self.msgid = msgid
            self.msgstr = msgstr
            self.msgstr_plural = msgstr_plural

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
        self._cache = {}

    def reload(self):
        Translator.reload(self)
        self.clear_cache()

    def clear_cache(self):
        self._cache.clear()

    def add_translation(self, language, msgid, msgstr, msgstr_plural=None):
        x = self.db.TranslationEntry(language, msgid, msgstr, msgstr_plural)
        self.session.add(x)
        self.clear_cache()

    def gettext(self, msgid):
        try:
            return self._cache[msgid]
        except KeyError:
            entry = self._lookup_entry(msgid)
            if entry is not None:
                msgstr = entry.msgstr
            else:
                msgstr = Translator.gettext(self, msgid)
            self._cache[msgid] = msgstr
            return msgstr

    def ngettext(self, msgid, msgid_plural, n):
        entry = self._lookup_entry(msgid, msgid_plural)
        if entry is not None:
            if n == 1:
                return entry.msgstr
            else:
                return entry.msgstr_plural
        else:
            return Translator.ngettext(self, msgid, msgid_plural, n)

    def _lookup_entry(self, msgid, msgid_plural=None):
        assert len(self.languages) == 1 # fix me
        language = self.languages[0]
        Entry = self.db.TranslationEntry
        q = self.session.query(Entry).filter_by(language = language, msgid = msgid)
        if msgid_plural is None:
            q = q.filter(Entry.msgstr_plural == None)
        else:
            q = q.filter(Entry.msgstr_plural != None)
        rows = q.all()
        if len(rows) == 0:
            return None
        elif len(rows) == 1:
            return rows[0]
        else:
            # cannot happen because (language, msgid) is the primary key
            assert False, "Multiple translations of %s found: %s" % (msgid, rows)
