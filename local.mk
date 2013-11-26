### User configurable makefile options

MYNAME   := playbin2player
RELEASE  := 1.0.1
PLAYER   := pb2player

prefix      = /usr

exec_prefix = $(prefix)
bindir      = $(exec_prefix)/bin
sbindir     = $(exec_prefix)/sbin
datarootdir = $(prefix)/share
datadir     = $(datarootdir)
mandir      = $(datarootdir)/man
docdir      = $(datarootdir)/doc/$(MYNAME)
man1dir     = $(mandir)/man1

INSTALL         = install
INSTALL_PROGRAM = $(INSTALL)
INSTALL_DATA    = $(INSTALL) -m 644

DESTDIR =
