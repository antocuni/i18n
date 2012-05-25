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
        id = Column(Integer, primary_key=True)
        language = Column(String) # destination language, e.g. it_IT
        msgid = Column(String)
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

