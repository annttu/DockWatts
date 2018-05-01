all: build

# For some reason MacOS System integrity protection (SIP) don't allow building with system python2.7
PYTHON=/usr/local/Cellar/python/2.7.14/bin/python2.7

build: Applications/DockWatts.app

Applications/DockWatts.app:
	$(PYTHON) setup.py py2app -d ./Applications

clean:
	-@rm -r build dist Applications/* 2>/dev/null || true

install:
	cp -r Applications/DockWatts.app /Applications/DockWatts.app
