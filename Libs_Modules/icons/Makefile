PACKAGE=tic-tac-toe
DESTDIR=/usr/share/icons/hicolor

PNG:=$(wildcard *.png)
SIZE:=$(PNG:.png=)

all: install
install:
	@for f in $(SIZE); do \
		if [ ! -f $(DESTDIR)/$$f/apps/$(PACKAGE).png ]; then \
		 cp -v $$f.png $(DESTDIR)/$$f/apps/$(PACKAGE).png 2>/dev/null; \
		fi \
	done
	gtk-update-icon-cache -f $(DESTDIR)
uninstall:
	@for f in $(SIZE); do \
		if [ -f $(DESTDIR)/$$f/apps/$(PACKAGE).png ]; then \
		 rm -vf $(DESTDIR)/$$f/apps/$(PACKAGE).png 2>/dev/null; \
		fi \
	done
	gtk-update-icon-cache -f $(DESTDIR)
