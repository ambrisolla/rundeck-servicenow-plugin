all: install

clean:
	rm -rf build

build:
	mkdir -p build/libs build/zip-content/servicenow-change-plugin
	cp -r contents resources plugin.yaml build/zip-content/servicenow-change-plugin
	cd build/zip-content; zip -r servicenow-change-plugin.zip *
	mv build/zip-content/servicenow-change-plugin.zip build/libs