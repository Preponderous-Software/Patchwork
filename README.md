# Patchwork

**Patchwork** is a lightweight tool for visualizing 2D environments, built with Python. It serves as a testbed for experimenting with graphical rendering of grids and virtual environments using various graphics libraries—starting with **Pygame**.

This project is part of the [Viron](https://github.com/Preponderous-Software/Viron) ecosystem and provides a visual layer to its simulated environments.

## Features

- Grid-based rendering of 2D environments
- Initial support for **Pygame**
- Interactive toggling of cell states
- Modular structure designed for future support of other graphics libraries
- Clean interface for testing Viron entity placement and behavior

## Getting Started

### Prerequisites

- Python 3.10+
- [Viron](https://github.com/Preponderous-Software/Viron)
- [Pygame](https://www.pygame.org/) (`pip install pygame`)

### Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/dmccoystephenson/testing-drawing-grid.git
cd testing-drawing-grid
pip install -r requirements.txt  # if a requirements file exists
```

### Running

To launch the Patchwork visualization:

```bash
bash run.sh
```

Or run it directly:

```bash
python main.py
```

Make sure Viron is running or properly configured for environment data access.

## Use Cases

- Visualization of entity grids and spatial data from Viron
- Debugging simulations in real-time
- Prototyping user interfaces or tile-based systems
- Educational demos of 2D virtual environments

## Roadmap

- [ ] Add support for other graphics libraries (Tkinter, OpenGL, etc.)
- [ ] Layered rendering and animation
- [ ] Customizable grid styling
- [ ] Real-time interaction with live Viron simulations

## 📄 License

This project is licensed under the **Preponderous Non-Commercial License (Preponderous-NC)**.  
It is free to use, modify, and self-host for **non-commercial** purposes, but **commercial use requires a separate license**.

> **Disclaimer:** *Preponderous Software is not a legal entity.*  
> All rights to works published under this license are reserved by the copyright holder, **Daniel McCoy Stephenson**.

Full license text:  
[https://github.com/Preponderous-Software/preponderous-nc-license/blob/main/LICENSE.md](https://github.com/Preponderous-Software/preponderous-nc-license/blob/main/LICENSE.md)

---

**Created by [Daniel McCoy Stephenson](https://github.com/dmccoystephenson)** as part of the Preponderous ecosystem.
