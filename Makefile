all: install

clean:
	rm -rf build

build:
	mkdir -p build/libs build/zip-content/servicenow-approval-plugin
	cp -r contents resources plugin.yaml build/zip-content/servicenow-approval-plugin
	cd build/zip-content; zip -r servicenow-approval-plugin.zip *
	mv build/zip-content/servicenow-approval-plugin.zip build/libs