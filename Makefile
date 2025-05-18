PLUGIN_NAME = symlink-importer
VERSION = 1.0.0
ZIP_FILE = $(PLUGIN_NAME)_v$(VERSION).zip
SRC_DIR = src

.PHONY: clean build

build: clean
	@echo "Building plugin..."
	cd $(SRC_DIR) && zip -r ../$(ZIP_FILE) * && cd ..
	@echo "Plugin package created: $(ZIP_FILE)"

clean:
	@echo "Cleaning up..."
	rm -f $(ZIP_FILE)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

install: build
	@echo "Installing plugin to Calibre..."
	calibre-customize -a $(ZIP_FILE)
	@echo "Plugin installed successfully"

uninstall:
	@echo "Uninstalling plugin from Calibre..."
	calibre-customize -r $(PLUGIN_NAME)
	@echo "Plugin uninstalled successfully"
