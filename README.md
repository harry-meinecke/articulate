# Articulate

A Python project for generating Articulate-style game content and printable assets.

---

##  Project Structure

```
articulate/
├── articulate/
│   └── utils/
├── scripts/
├── data/
├── environment.yml
└── README.md
```

### Description

* **articulate/**
  Main Python package containing core logic.

* **articulate/utils/**
  Helper modules (e.g. categories, shared utilities).

* **scripts/**
  Entry-point scripts (e.g. PDF/card generation).

* **data/**
  Input data (word lists, categories, etc.).
  Typically tracked with Git LFS if large.

---

## Setup

### 1. Create environment

```bash
conda env create -f environment.yml
conda activate articulate
```

---

### 2. Install package (editable mode)

```bash
pip install -e .
```

This allows you to modify the code and immediately see changes without reinstalling.

---

## Usage

Run scripts from the project root:

```bash
python -m scripts.articulate_gen
```

or (after installation):

```bash
python scripts/articulate_gen.py
```

---

##  Dependencies

Managed via `conda` and listed in:

```
environment.yml
```

---

## Notes

* The project is structured as an installable Python package.
* Paths (e.g. to `data/`) should be handled relative to the package, not the working directory.
* Avoid running scripts from arbitrary directories — use the project root.


