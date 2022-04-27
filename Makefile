venv-init:
	python3 -m venv venv

venv-activate:
	bash -c "source venv/bin/activate"

run: venv-activate
	python midiboard/main.py

deps: venv-activate
	pip install -r requirements-macos.txt
