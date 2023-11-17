VENV_ACTIVATE:=. venv/bin/activate

venv-init:
	python3 -m venv venv

run:
	$(VENV_ACTIVATE) && python main.py

run-cli:
	$(VENV_ACTIVATE) && python main.py cli

deps:
	$(VENV_ACTIVATE) && pip3 install --upgrade pip
	$(VENV_ACTIVATE) && pip install -r requirements-macos.txt

# install:
# 	$(VENV_ACTIVATE) && python setup.py install

# build: clean install
# 	pyinstaller main.py --windowed \
# 	--name=Midiboard \
# 	--icon=resources/midiboard.icns \
# 	--add-data=resources:resources \
# 	--paths=./venv/lib/python3.9/site-packages \
# 	--hidden-import=mido.backends.rtmidi \

# clean:
# 	rm -rf build dist *.spec
