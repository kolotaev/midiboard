VENV_ACTIVATE:=. venv/bin/activate

venv-init:
	python3 -m venv venv

run:
	$(VENV_ACTIVATE) && python midiboard/main.py

deps:
	$(VENV_ACTIVATE) && pip install -r requirements-macos.txt
