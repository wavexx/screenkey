# This Makefile regenerates the template (screenkey.pot) *and* updates all
# available translations in one go as a more convenient tool for translators.
#
# This is redundant: "setup.py build_i18n" does the first and it's done
# automatically during install, while "intltool-update lang" would be the
# official way to do the second.

SOURCES = $(shell sed -e 's/^/..\//' POTFILES.in)
POFILES = $(wildcard *.po)

all: $(POFILES)

%.po: screenkey.pot
	msgmerge --previous -F -N -U $@ $<

screenkey.pot: $(SOURCES)
	xgettext -L python -F -o $@ $<
