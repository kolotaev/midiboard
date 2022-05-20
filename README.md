### How to run

- `make venv-init`
- `make deps`
- `make run`

### How to run as Application in MacOS

- Create Automator application ("Run Shell Script" type)
- `make venv-init`
- `make deps`
- Here select "In bash shell execute" `/path/to/midiboard/midiboard.sh`
- Save it as "Miniboard.app"
- Add "Miniboard.app" to allowed Input sources listener in System preferences
