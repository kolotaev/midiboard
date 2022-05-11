VENV_ACTIVATE:=. venv/bin/activate

venv-init:
	python3 -m venv venv

run:
	$(VENV_ACTIVATE) && python midiboard/main.py

run-cli:
	$(VENV_ACTIVATE) && python midiboard/main.py cli

deps:
	$(VENV_ACTIVATE) && pip install -r requirements-macos.txt
