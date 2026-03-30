import pandas as pd
from pathlib import Path
import math
import glob
import os
from pypdf import PdfReader, PdfWriter


def cards_to_sheets(
    card_paths: list[str],
    output_path: str,
    cols: int = 2,
    rows: int = 2,
    margin_pt: float = 0.0,
    gap_pt: float = 0.0,
) -> None:
    """
    Arrange a list of single-page card PDFs into sheet PDFs (cols × rows per sheet).

    Cards are placed left-to-right, top-to-bottom, unmodified — no scaling,
    no re-encoding.  The sheet size is inferred from the first card's media box.

    Args:
        card_paths:  Ordered list of PDF file paths (one card per file).
        output_path: Destination PDF file path.
        cols:        Cards across each sheet (default 2).
        rows:        Cards down each sheet (default 2).
        margin_pt:   Outer margin in points (default 0).
        gap_pt:      Gap between cards in points (default 0).
    """
    if not card_paths:
        raise ValueError("card_paths is empty")

    # ── Determine card size from first card ──────────────────────────────────
    first_reader = PdfReader(card_paths[0])
    first_page   = first_reader.pages[0]
    card_w = float(first_page.mediabox.width)
    card_h = float(first_page.mediabox.height)

    # ── Sheet dimensions ─────────────────────────────────────────────────────
    sheet_w = margin_pt * 2 + cols * card_w + (cols - 1) * gap_pt
    sheet_h = margin_pt * 2 + rows * card_h + (rows - 1) * gap_pt

    cards_per_sheet = cols * rows
    writer = PdfWriter()

    # ── Chunk cards into sheets ───────────────────────────────────────────────
    for sheet_idx in range(math.ceil(len(card_paths) / cards_per_sheet)):
        sheet_page = writer.add_blank_page(width=sheet_w, height=sheet_h)

        chunk = card_paths[
            sheet_idx * cards_per_sheet : (sheet_idx + 1) * cards_per_sheet
        ]

        for slot, card_path in enumerate(chunk):
            col = slot % cols
            row = slot // cols

            # PDF y-axis: origin at bottom-left, so row 0 → top of sheet
            x = margin_pt + col * (card_w + gap_pt)
            y = sheet_h - margin_pt - (row + 1) * card_h - row * gap_pt

            card_reader = PdfReader(card_path)
            card_page   = card_reader.pages[0]

            # merge_transformed_page places the card at (x, y) with no scaling
            sheet_page.merge_transformed_page(
            card_page,
            pypdf_translate(x, y),
            )
    with open(output_path, "wb") as f:
        writer.write(f)

    total_sheets = math.ceil(len(card_paths) / cards_per_sheet)
    print(f"Written {total_sheets} sheet(s) → {output_path}")


# ── Helper: build a translation-only CTM ─────────────────────────────────────
def pypdf_translate(tx: float, ty: float):
    """Return a translation matrix tuple (a, b, c, d, e, f) for merge_transformed_page."""
    from pypdf import Transformation
    return Transformation().translate(tx, ty)


# ── Convenience wrapper: folder of cards → sheets ────────────────────────────
def folder_to_sheets(
    folder: str,
    output_path: str,
    pattern: str = "*.pdf",
    sort: bool = True,
    **kwargs,
) -> None:
    """
    Glob all PDFs in *folder* and pass them to cards_to_sheets.

    Args:
        folder:      Directory containing card PDFs.
        output_path: Destination PDF file path.
        pattern:     Glob pattern (default "*.pdf").
        sort:        Sort files alphabetically (default True).
        **kwargs:    Forwarded to cards_to_sheets (cols, rows, margin_pt, gap_pt).
    """
    paths = glob.glob(os.path.join(folder, pattern))
    if sort:
        paths.sort()
    if not paths:
        raise FileNotFoundError(f"No files matching {pattern!r} in {folder!r}")
    cards_to_sheets(paths, output_path, **kwargs)

    
def csv_to_dict(csv_path):
    """
    Reads a CSV file and converts it into a dictionary of lists.

    Assumes:
    - First row contains column headers (categories)
    - Each column contains values for that category

    Returns:
        dict[str, list[str]]
    """
    csv_path = Path(csv_path)

    df = pd.read_csv(csv_path)

    # Convert each column into a list, dropping NaNs
    categories = {
        col: df[col].dropna().astype(str).tolist()
        for col in df.columns
    }
    lengths = {len(v) for v in categories.values()}
    if len(lengths) != 1:
        raise ValueError("All columns must have the same number of entries")
    return categories
