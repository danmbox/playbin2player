include local.mk

DISTNAME := $(MYNAME)-$(RELEASE)

TMP_WILD := $(TMP_WILD) *~ *.bak
TMP_PAT  := $(subst *,%,$(TMP_WILD))

PROGS := $(PLAYER)
MANS := $(addprefix man/, $(PROGS:=.1))
ICONS := $(wildcard data/icons/48x48/*.png)
DESKTOPS_IN := $(wildcard data/*.desktop.in)
DESKTOPS := $(DESKTOPS_IN:.in=)

CLEAN_FILES := $(MANS) $(DESKTOPS)

.PHONY: clean all srcdist

all: $(PROGS) $(MANS) $(DESKTOPS) $(ICONS)
	grep -q 'version = "%prog '"$(RELEASE)"'"' $(PLAYER)

man/%.1: % $(filter-out $(wildcard man), man) Makefile
	help2man -N -o $@ $(abspath $<) || { $< --help || :; $< --version || :; false; }

%: %.in
	sed -e 's!@RELEASE@!'"$(RELEASE)"'!g;s!@bindir@!'"$(bindir)"'!g;s!@datadir@!'"$(datadir)"'!g;s!@PLAYER@!'"$(PLAYER)"'!g' <$< >$@

install: all installdirs
	$(INSTALL_PROGRAM) $(PROGS) $(DESTDIR)$(bindir)
	$(INSTALL_DATA) $(MANS) $(DESTDIR)$(man1dir)
	$(INSTALL_DATA) $(DESKTOPS) $(DESTDIR)$(desktopdir)
	$(INSTALL_DATA) $(ICONS) $(DESTDIR)$(datadir)/icons/hicolor/48x48/apps
	$(INSTALL_DATA) LICENSE.txt $(DESTDIR)$(docdir)
	$(INSTALL_DATA) README.org $(DESTDIR)$(docdir)
	$(INSTALL_DATA) README.html $(DESTDIR)$(docdir)

clean:
	set -f; for pat in $(TMP_WILD); do find . -iname $$pat -exec rm {} \; ; done; \
	rm -rf $(CLEAN_FILES)

srcdist: clean
	git archive --format=tar --prefix=$(DISTNAME)/ HEAD | \
	  gzip -c >/tmp/$(DISTNAME).tar.gz

showvars:
	@echo "RELEASE := " $(RELEASE)
	@echo "TMP_PAT := " $(TMP_PAT)

man:
	mkdir man

debuild:
	TMPDIR="/tmp/$(MYNAME)_$(RELEASE).orig"; \
	  rm -rf "$$TMPDIR"; cp -a . "$$TMPDIR"; cd "$$TMPDIR"; \
	  make clean; rm -rf debian; \
	  cd ..; tar cvzf "$$TMPDIR.tar.gz" "$${TMPDIR##*/}"; \
	  cd "$$TMPDIR"; cp -a mydebian debian; debuild -S; debuild -b

installdirs: mkinstalldirs
	./mkinstalldirs $(DESTDIR)$(bindir) $(DESTDIR)$(datadir) \
	  $(DESTDIR)$(mandir) $(DESTDIR)$(man1dir) $(DESTDIR)$(desktopdir) \
	  $(DESTDIR)$(datadir)/icons/hicolor/32x32/apps \
	  $(DESTDIR)$(datadir)/icons/hicolor/48x48/apps \
	  $(DESTDIR)$(docdir)
