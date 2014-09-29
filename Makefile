all: build

build: Applications/DockNetStat.app

Applications/DockNetStat.app:
	python2.7 setup.py py2app -A -s -d ./Applications

clean:
	-@rm -r build dist Applications/* 2>/dev/null || true
