import py
import sys
from i18n.dbtranslator import DBTranslator
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db.sqlite')

ROOT = py.path.local(__file__).dirpath()
LANGUAGES = ['it_IT', 'fr_FR', 'de_DE']
DEST_LANGUAGE = 'it_IT'

tr = DBTranslator(ROOT, LANGUAGES, DEST_LANGUAGE, engine=engine)
_ = tr._
ngettext = tr.ngettext

#_tr.add_translation('it_IT', 'hello world', 'salve mondo')

if __name__ == '__main__':
    tr.cmdline(sys.argv)
