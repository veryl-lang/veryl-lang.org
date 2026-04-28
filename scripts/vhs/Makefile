# Build vhs recordings for the homepage.
#
#   make              - record every recipe
#   make <recipe>     - record a single recipe (e.g. `make diagnostics`)
#   make install      - copy generated gifs into static/img/
#   make clean        - remove generated gifs

RECIPES   := diagnostics format synth translate
STATIC    := ../../static/img
VHS_FLAGS := ROD_BROWSER_FLAGS="--no-sandbox --disable-gpu"

.PHONY: all install clean $(RECIPES)

all: $(RECIPES)

$(RECIPES):
	cd $@ && $(VHS_FLAGS) vhs $@.tape

install:
	@for r in $(RECIPES); do \
	  cp -v $$r/$$r.gif $(STATIC)/$$r.gif; \
	done

clean:
	@for r in $(RECIPES); do \
	  rm -f $$r/$$r.gif; \
	done
