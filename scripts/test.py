
from pathlib import Path

from articulate import DATA_DIR
from articulate.utils.io import folder_to_sheets


INPUT_FOLDER= Path(DATA_DIR/ "pythoncards/")
folder_to_sheets(INPUT_FOLDER, DATA_DIR / "pythoncards/sheets/sheets.pdf")
