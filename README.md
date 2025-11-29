[![Test](https://github.com/janion/ConversationalGCode/actions/workflows/unittest.yml/badge.svg)](https://github.com/janion/ConversationalGCode/actions/workflows/unittest.yml)

# Conversation GCode
A small project to allow for simple GCode operations to be generated without the need for CAD modelling parts. This should allow for simple parts to be created much faster than using a traditional workflow.

## Operations to Support:
- [X] Milling circular pockets
- [X] Drilling holes
- [ ] Milling surfaces
- [X] milling rectangular pockets
- [X] Milling rectangular profiles
- [X] Milling circular profiles
- [ ] Chamfering circular pockets
- [ ] Chamfering rectangular pockets

## Tests
Install package:
```python -m pip install -e .```

Run tests using:
```python -m unittest discover -s tests```
