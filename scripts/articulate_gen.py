from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

# ── CONFIG ──────────────────────────────────────────────────────────────────
BACKGROUND_IMAGE = "C:/Users/hmein/OneDrive/Documents/Articulate/basecard.jpg"
OUTPUT_FOLDER    = "C:/Users/hmein/OneDrive/Documents/Articulate/pythoncards/"

CARD_W = 857
CARD_H = 550

COLS, ROWS     = 3, 4
PAGE_W, PAGE_H = A4
MARGIN_X       = (PAGE_W - COLS * CARD_W) / 2
MARGIN_Y       = (PAGE_H - ROWS * CARD_H) / 2

WORD_FONT      = ("Helvetica-Bold", 50)
TEXT_COLOR     = colors.black

CARD_PADDING   = 12
LEFT_MARGIN    = 150    # distance from left edge to start of text
VERTICAL_OFFSET = -8    # shift all labels up (+) or down (-) from centre
LABEL_SPACING  = 4     # extra vertical gap between labels (added to natural row height)

# ── YOUR WORD LISTS ─────────────────────────────────────────────────────────
categories = {
    "Person": ["Elvis", "Cleopatra", "Einstein", "Picasso", "Newton"],
    "World":  ["Sahara", "Amazon", "Vatican", "Everest", "Havana"],
    "Object": ["Telescope", "Compass", "Abacus", "Lantern", "Anvil"],
    "Action": ["Juggling", "Surfing", "Knitting", "Skydiving", "Fencing"],
    "Nature":  ["Monsoon", "Magma", "Eclipse", "Tundra", "Quasar"],
    "Random": ["Kazoo", "Platypus", "Haiku", "Limerick", "Bonsai"],
}

# ── DRAW A SINGLE CARD ──────────────────────────────────────────────────────
def draw_card(c, card_index):
    c.drawImage(BACKGROUND_IMAGE, 0, 0, width=CARD_W, height=CARD_H,
                preserveAspectRatio=False, mask="auto")

    num_categories = len(categories)
    content_height = CARD_H - 2 * CARD_PADDING
    row_h = content_height / num_categories

    for row, (category, words) in enumerate(categories.items()):
        y_center = CARD_H - CARD_PADDING - (row + 0.5) * row_h
        y = y_center + VERTICAL_OFFSET - row * LABEL_SPACING

        # Separator line between rows
        if row > 0:
            line_y = CARD_H - CARD_PADDING - row * row_h
            c.setStrokeColor(colors.HexColor("#CCCCCC"))
            c.setLineWidth(0.4)
            c.line(CARD_PADDING, line_y, CARD_W - CARD_PADDING, line_y)

        # Word anchored from LEFT_MARGIN
        c.setFont(*WORD_FONT)
        c.setFillColor(TEXT_COLOR)
        c.drawString(LEFT_MARGIN, y, words[card_index])

# ── GENERATE ONE PDF PER CARD ────────────────────────────────────────────────
def generate_pdfs(output_folder):
    os.makedirs(output_folder, exist_ok=True)

    num_cards = len(next(iter(categories.values())))

    for i in range(num_cards):
        filename = f"card_{i+1:02d}.pdf"
        output_path = os.path.join(output_folder, filename)

        c = canvas.Canvas(output_path, pagesize=(CARD_W, CARD_H))
        draw_card(c, i)
        c.save()

        print(f"Saved: {output_path}")

    print(f"\nDone — {num_cards} cards saved to '{output_folder}'")

generate_pdfs(OUTPUT_FOLDER)