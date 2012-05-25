import py
import os
import gettext
from babel.messages.frontend import CommandLineInterface

babel_cli = CommandLineInterface()

class Translator(object):

    def __init__(self, rootdir, languages, autocompile=True):
        self.rootdir = rootdir
        self.languages = languages
        self.langdir = rootdir.join('languages').ensure(dir=True)
        self.pot = self.langdir.join('template.pot')
        if autocompile:
            self.compile()
        self.reload()

    def reload(self):
        self.tr = gettext.translation('messages', str(self.langdir),
                                      self.languages, fallback=True)

    def gettext(self, msgid):
        return self.tr.ugettext(msgid)

    def _(self, msgid):
        return self.gettext(msgid)

    def ngettext(self, msgid1, msgid2, n):
        return self.tr.ungettext(msgid1, msgid2, n)

    def _run(self, cmd, *args):
        babel_cli.run(['pybabel', cmd] + list(args))

    def _do_extract(self):
        self._run('extract', '-o', str(self.pot), str(self.rootdir))

    def _do_init(self, lang):
        self._run('init', '-i', str(self.pot), '-l', lang, '-d', str(self.langdir))

    def _do_update(self, lang):
        self._run('update', '-i', str(self.pot), '-l', lang, '-d', str(self.langdir))

    def _do_compile(self, po, lang):
        self._run('compile', '-f', '-i', str(po), '-l', lang, '-d', str(self.langdir))

    def get_po(self, lang):
        return self.langdir.join(lang, 'LC_MESSAGES', 'messages.po')

    def extract(self):
        self._do_extract()
        for lang in self.languages:
            dst = self.get_po(lang)
            if dst.check(file=False):
                self._do_init(lang)
            else:
                self._do_update(lang)

    def compile(self):
        for po in self.langdir.visit('*.po', rec=True):
            mo = po.new(ext='mo')
            if mo.check(exists=True) and mo.mtime() >= po.mtime():
                # the .mo is up to date
                continue
            lang = po.dirpath('..').basename
            self.langdir.join(lang, 'LC_MESSAGES').ensure(dir=1)
            print 'compiling language %s' % po.basename
            self._do_compile(po, lang)
