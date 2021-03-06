import py
import time
from i18n.translator import Translator

def add_translation(po, msgid, msgstr):
    src = str(py.code.Source("""
        msgid "%s"
        msgstr ""
    """ % msgid))
    dst = str(py.code.Source("""
        msgid "%s"
        msgstr "%s"
    """ % (msgid, msgstr)))
    text = po.read()
    text = text.replace(src, dst)
    assert msgstr in text
    po.write(text)


def test_extract_and_update(tmpdir):
    languages = ['it_IT']
    tmpdir.join('foo.py').write("print _('hello')")
    tr = Translator(tmpdir, languages, autocompile=False)
    tr.extract()
    # check that the template was extracted
    pot = tmpdir.join('languages', 'template.pot')
    assert 'hello' in pot.read()
    # check that the various translations has been initialized from the template
    it_IT = tmpdir.join('languages', 'it_IT', 'LC_MESSAGES', 'messages.po')
    it_IT_text = it_IT.read()
    assert 'hello' in it_IT_text
    #
    add_translation(it_IT, 'hello', 'ciao')
    #
    # add another string to translate in the source and extract again
    tmpdir.join('foo.py').write("print _('hello'), _('world')")
    tr.extract()
    assert 'world' in pot.read()
    #
    # check that it_IT has been merged correctly
    it_IT_text = it_IT.read()
    assert 'world' in it_IT_text
    assert 'ciao' in it_IT_text

def test_extract_from_method_calls(tmpdir):
    tmpdir.join('foo.py').write("""
print tr._('hello')
print tr.gettext('world')
print tr.ngettext('orange', 'oranges', 1)
""")
    tr = Translator(tmpdir, ['it_IT'], autocompile=False)
    tr.extract()
    pot = tmpdir.join('languages', 'template.pot').read()
    assert 'hello' in pot
    assert 'world' in pot
    assert 'orange' in pot


def test_compile(tmpdir):
    class MyTranslator(Translator):
        compile_count = 0
        def _do_compile(self, *args):
            self.compile_count += 1
            Translator._do_compile(self, *args)
    #
    languages = ['it_IT']
    tmpdir.join('foo.py').write("print _('hello')")
    tr = MyTranslator(tmpdir, languages, autocompile=False)
    tr.extract()
    tr.compile()
    assert tr.compile_count == 1
    tr.compile()
    assert tr.compile_count == 1 # no recompilation needed
    #
    time.sleep(0.1)
    it_IT = tr.get_po('it_IT')
    it_IT.setmtime()
    tr.compile()
    assert tr.compile_count == 2

    
def test_translate_string(tmpdir):
    languages = ['it_IT']
    tmpdir.join('foo.py').write("print _('hello')")
    tr = Translator(tmpdir, languages, autocompile=False)
    tr.extract()
    it_IT = tr.get_po('it_IT')
    it_IT_text = it_IT.read()
    assert 'hello' in it_IT_text
    #
    add_translation(it_IT, 'hello', 'ciao')
    tr.compile()
    tr.reload()
    assert tr._('hello') == 'ciao'


def test_pass_string_to_init(tmpdir):
    path = str(tmpdir)
    tr = Translator(path, ['it_IT'])
    assert tr.rootdir.strpath == path
    

def test_cmdline():
    class MyTranslator(Translator):
        def __init__(self):
            pass

        def compile(self):
            self.cmd = 'compile'

        def extract(self):
            self.cmd = 'extract'

    tr = MyTranslator()
    tr.cmdline(['foo.py', 'compile'])
    assert tr.cmd == 'compile'
    tr.cmdline(['foo.py', 'extract'])
    assert tr.cmd == 'extract'
    py.test.raises(SystemExit, "tr.cmdline(['foo.py', 'foobar'])")
    
    
