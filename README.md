# Cyber City: A Digital Defense Simulator

Cyber City is an offline desktop city-building strategy game that teaches cybersecurity concepts through fictional civic-defense mechanics. Players drag buildings onto a city grid, watch a risk visualization update, and run harmless story incidents featuring fictional characters such as Thief, Spy, Saboteur, and Trickster.

> Safety note: Cyber City does **not** perform real hacking, exploitation, malware behavior, penetration testing, scanning, network access, or real cybersecurity automation. All simulations are educational game mechanics.

## Features

- Modern PySide6 desktop interface
- Drag-and-drop city building palette
- Fictional risk visualization across the city grid
- Animated story incident feedback
- Offline SQLite save and load support
- Modular object-oriented project structure
- Example city layout in `examples/example_city_layout.json`

## Project Structure

```text
assets/        Static assets for the app
models/        Dataclasses and city domain objects
simulation/    Safe fictional game simulation engine
ui/            PySide6 desktop interface
database/      SQLite persistence layer
examples/      Example city layouts
tests/         Automated tests
```

## Installation

Cyber City targets Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Application

```bash
python main.py
```

Use the building palette on the left to drag buildings onto the planning grid. Click **Run Fictional Incident** to launch a safe animated story event, then use the toolbar to save, load, or start a new city.

## Testing

```bash
pytest
```

## Example Layout

An example city layout is provided at `examples/example_city_layout.json`. It can be used as reference data for future import features or demonstrations.
