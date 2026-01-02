PDF_DIR  := pdf
MD_DIR   := md
TXT_DIR  := txt
JSON_DIR := json

PDFS  := $(wildcard $(PDF_DIR)/*.pdf) $(wildcard $(PDF_DIR)/*.PDF)
MDS   := $(patsubst $(PDF_DIR)/%.pdf,$(MD_DIR)/%.md,$(PDFS))
TXTS  := $(patsubst $(PDF_DIR)/%.pdf,$(TXT_DIR)/%.txt,$(PDFS))
JSONS := $(patsubst $(PDF_DIR)/%.pdf,$(JSON_DIR)/%.json,$(PDFS))

.PHONY: all clean mds txts jsons

# Keep intermediate TXT files; don't auto-delete
.SECONDARY: $(TXTS)

# Default target: full pipeline
all: $(JSONS)

# Phony targets for each stage
mds: $(MDS)       # PDF → MD
txts: $(TXTS)     # MD → TXT
jsons: $(JSONS)   # TXT → JSON

# Create directories if they don't exist
$(MD_DIR):
	mkdir -p $(MD_DIR)

$(TXT_DIR):
	mkdir -p $(TXT_DIR)

$(JSON_DIR):
	mkdir -p $(JSON_DIR)

# Step 1: PDF → Markdown
$(MD_DIR)/%.md: $(PDF_DIR)/%.pdf | $(MD_DIR)
	python3 1_pdf_to_raw.py $< > $@ || { echo "Error, deleting $@"; rm -f $@; exit 1; }

# Step 2: Markdown → concatenated JSON txt
$(TXT_DIR)/%.txt: $(MD_DIR)/%.md | $(TXT_DIR)
	python3 2_run_llama.py $< > $@ || { echo "Error, deleting $@"; rm -f $@; exit 1; }

# Step 3: Concatenated JSON txt → validated JSON
$(JSON_DIR)/%.json: $(TXT_DIR)/%.txt | $(JSON_DIR)
	python3 3_validate_json.py $< > $@ || { echo "Error, deleting $@"; rm -f $@; exit 1; }

# Clean all intermediate and output files
clean:
	rm -rf $(MD_DIR) $(TXT_DIR) $(JSON_DIR)
