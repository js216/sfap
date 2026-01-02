import os
import requests
from urllib.parse import urlparse

# ---------------- GLOBAL VARIABLES ---------------- #

PDF_DIR = "pdf"
os.makedirs(PDF_DIR, exist_ok=True)

# List of op amp datasheet PDF URLs (common/opamp parts)
DATASHEET_URLS = [
    # Industry standard/op‑amps
    "https://www.ti.com/lit/ds/symlink/lm741.pdf",           # LM741 general purpose op‑amp :contentReference[oaicite:0]{index=0}
    "https://www.onsemi.com/download/data-sheet/pdf/lm358-d.pdf",  # LM358 dual op‑amp :contentReference[oaicite:1]{index=1}
    "https://www.ti.com/lit/ds/symlink/lm358.pdf",           # LM358 (TI) :contentReference[oaicite:2]{index=2}
    "https://www.st.com/resource/en/datasheet/tl072.pdf",    # TL072 JFET op‑amp :contentReference[oaicite:3]{index=3}
    "https://www.ti.com/lit/gpn/NE5532",                     # NE5532 low‑noise audio op amp :contentReference[oaicite:4]{index=4}

    # JFET/faster/specialty
    "http://www.ti.com/lit/ds/symlink/tl081.pdf",            # TL081 JFET input :contentReference[oaicite:5]{index=5}
    "http://www.ti.com/lit/ds/symlink/tl071.pdf",            # TL071 single version :contentReference[oaicite:6]{index=6}
    "https://www.ti.com/lit/gpn/LF351",                      # LF351 JFET op amp :contentReference[oaicite:7]{index=7}
    "https://www.ti.com/lit/gpn/LF411",                      # LF411 low offset JFET op amp :contentReference[oaicite:8]{index=8}

    # Precision / audio / op‑amp examples
    "https://www.ti.com/lit/ds/symlink/lm324.pdf",           # LM324 quad op‑amp (multiple inside) :contentReference[oaicite:9]{index=9}
    "https://www.ti.com/lit/ds/symlink/lm833.pdf",           # LM833 dual audio low noise (if available)
    "https://www.ti.com/lit/ds/symlink/opa2134.pdf",         # OPA2134 audio op amp
    "https://www.ti.com/lit/ds/symlink/opa124.pdf",          # OPA124 precision op amp :contentReference[oaicite:10]{index=10}

    # Classic/older and more precision/op amps
    "https://www.ti.com/lit/ds/symlink/lm108.pdf",           # LM108 precision op amp
    "https://www.ti.com/lit/ds/symlink/lm318-n.pdf",         # LM318 wide bandwidth
    "https://www.ti.com/lit/ds/symlink/lm101.pdf",           # LM101 early op amp
    "https://www.ti.com/lit/ds/symlink/op27.pdf",            # OP27 precision op amp
    "https://www.ti.com/lit/ds/symlink/op37.pdf",            # OP37 precision wide op amp

    # Additional variants
    "https://www.ti.com/lit/ds/symlink/lm324-n.pdf",         # Another LM324 source
    "https://www.ti.com/lit/ds/symlink/lm741cn.pdf",         # LM741 variant
    "https://www.ti.com/lit/ds/symlink/ua741.pdf",           # UA741 classic variant
]

# --------------------------------------------------- #

def download_pdf(url):
    """Downloads a PDF from the given URL into pdf/ directory."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        # Try to guess filename from URL or headers
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path) or "datasheet.pdf"
        if not filename.lower().endswith(".pdf"):
            # Fallback: assume PDF
            filename += ".pdf"

        output_path = os.path.join(PDF_DIR, filename)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded {url} → {output_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    print(f"Fetching {len(DATASHEET_URLS)} op amp datasheets...")
    for url in DATASHEET_URLS:
        download_pdf(url)

if __name__ == "__main__":
    main()

