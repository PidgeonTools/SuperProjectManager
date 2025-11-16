BLENDER := $(shell command -v blender || echo "flatpak run org.blender.Blender")

all:
	$(BLENDER) --command extension build

clean:
	rm -f ./*.zip

.PHONY: all clean
