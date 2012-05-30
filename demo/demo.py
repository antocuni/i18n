import sys
import py
# XXX: in a real setup, i18n should be either made a standalone package or put
# into the S3 hierarchy
sys.path.append(str(py.path.local(__file__).dirpath('..')))


from translate import _, ngettext
N = len(sys.argv)

print _("hello world")
print ngettext("there is %d argument", "there are %d arguments", N) % N
