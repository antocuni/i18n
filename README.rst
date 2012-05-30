=============================
i18n - Translations made easy
=============================

This package tries to simplify the workflow and development of
internationalized applications. It is a thin wrapper around existing tools, in
particular gettext_ and pybabel_.


Basic usage
===========

::

    # demo.py
    #
    from i18n.translator import Translator
    supported_languages = ['it_IT', 'fr_FR', 'de_DE']
    # activate italian translations
    tr = Translator('/path/to/root', supported_languages, 'it_IT')
    print tr._('Hello world!')

where ``/path/to/root/`` is the root directory of your project. When
instantiated, the ``Translator`` class automatically creates a directory
called ``/path/to/root/languages`` where the translations are stored.

Extracting messages
===================

Before doing the actual translation, you need to **extract** the messages from
your source files. The ``Translator`` object has a method called ``extract()``
which is a wrapper around ``pybabel extract`` and ``pybabel update``.

::

    >>> from i18n.translator import Translator
    >>> supported_languages = ['it_IT', 'fr_FR', 'de_DE']
    >>> tr = Translator('/path/to/root', supported_languages, 'it_IT')
    >>> tr.extract()

``extract`` looks for all the messages wrapped inside calls to ``_()``,
``gettext()`` or ``ngettext()`` and produces a file called
``languages/template.pot``. This is a standard `gettext po file`` which
contains all the messages found in the application.

Moreover, ``extract()`` also creates a **message catalog** file for each of
the supported languages as ``languages/$CODE/LC_MESSAGES/messages.po``, where
``$CODE`` is one of the languages listed in ``supported_languages`` (it_IT,
fr_FR and de_DE in the example above).

The catalog files are now ready to be translated using one of the many
existing tools, for example `QT Linguist`_ or Poedit_.  For the correct
functioning of the application, the entire ``languages/`` hierarchy needs to
be preserved. We suggest to track the various ``messages.po`` files in Version
Control System together with the other files belonging to the application.


Updating messages
=================

During the development of the application, you will surely add new messages to
be translated. The ``extract()`` method automatically handle this case: if it
finds existing catalog files, their content (including the existing
translations) is merged with the newly extracted messages.


Compiling catalogs
==================

It is necessary to compile the catalog files before using them with
gettext. By default, our ``Translator`` object automatically compiles all the
catalogs found in ``languages/``, producing the corresponding ``.mo``
files. The compilation is done only when the catalog file has been modified.
This means that in most cases you do not have to worry about the compilation
of the catalogs.

If you prefer to have more control on this step, you can pass
``autocompile=False`` to the constructor of ``Translator``. Then, you can
compile the catalogs manually by calling the ``compile()`` method.


Storing translations in a database
==================================

For some applications it is useful to let the user to define new translations
and/or override the default ones. ``i18n`` supports this use case with the
``DBTranslator`` class, which is a subclass of ``Translator``.  When
translating, ``DBTranslator`` first looks in the database: if the message is
not found, it delegates to the standard gettext behavior.

``DBTranslator`` is based on sqlalchemy_. Its constructor takes an additional
``engine`` parameter::

    from i18n.dbtranslator import DBTranslator
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///db.sqlite')
    ROOT = '/path/to/root'
    LANGUAGES = ['it_IT', 'fr_FR']
    DEST_LANGUAGE = 'it_IT'
    tr = DBTranslator(ROOT, LANGUAGES, DEST_LANGUAGE, engine=engine)
    print tr._("hello world")

``DBTranslator`` automatically creates the table ``translation_entries`` in
the DB. Then, it is up to the application to provide an user interface to
manipulate the table.  For testing, you can use the ``add_translation()``
method to insert a new translation in the DB::

    tr.add_translation("it_IT", "hello world", "ciao mondo")
    print tr._("hello world") # prints "ciao mondo"
