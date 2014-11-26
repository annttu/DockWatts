all: build

build: Applications/DockWatts.app

Applications/DockWatts.app:
	/usr/bin/python2.7 setup.py py2app -A -s -d ./Applications

clean:
	-@rm -r build dist Applications/* 2>/dev/null || true

install:
	cp -r Applications/DockWatts.app /Applications/DockWatts.app
