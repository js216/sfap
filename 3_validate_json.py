#!/usr/bin/env python3
import json
import sys

def clean_merged_file(input_file, output_file=None):
    """
    Reads a file with multiple JSON objects (possibly empty) and merges
    them into a single clean JSON object. Writes to output_file if given.
    """
    merged = {}

    with open(input_file, "r", encoding="utf-8") as f:
        # Each top-level JSON object can span multiple lines
        buffer = ""
        for line in f:
            line = line.strip()
            if not line:
                continue
            buffer += line
            # Try parsing current buffer
            try:
                data = json.loads(buffer)
                buffer = ""  # Reset buffer after successful parse
            except json.JSONDecodeError:
                buffer += " "
                continue  # Wait for more lines

            # Skip empty objects
            if not data:
                continue

            # Merge into main dict
            for key, value in data.items():
                if key in merged and isinstance(value, dict) and isinstance(merged[key], dict):
                    merged[key].update(value)
                else:
                    merged[key] = value

    # Output final JSON
    json_output = json.dumps(merged, indent=2)
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json_output)
    else:
        print(json_output)

    return merged


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    clean_merged_file(input_file, output_file)

