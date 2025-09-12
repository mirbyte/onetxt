# onetxt

Hit chat‑AI attachment limits? Merge a directory of text files into one clean context file for easy ingestion with local or hosted models.

## Overview

onetxt scans the current directory for a glob pattern (default *.txt), concatenates matches, ensures clean trailing newlines, and skips the output file to avoid self‑append loops. It’s a single‑file, zero‑dependency Python CLI using standard library modules like argparse and pathlib for portability.

## Features

- Merge all files matching a glob while excluding the output filename if present.
- Stream line by line to handle large files without high memory usage.
- Auto‑add a newline if a file’s last line lacks one, and insert a blank line between documents.
- Control input encoding and decode behavior via --encoding and --errors.


## Install

Place onetxt.py with the source files and run with Python.

## Usage

- Basic: run from the directory containing the files to merge; the default writes merged_file.txt.

```bash
python onetxt.py
```

- Custom output and pattern.

```bash
python onetxt.py --out all_notes.txt --pattern "*.txt"
```

- Merge Markdown with strict decoding and no pause (good for scripts/CI).

```bash
python onetxt.py --out dataset.md --pattern "*.md" --encoding utf-8 --errors strict --no-pause
```

- Windows: double‑click onetxt.py to run with defaults if no parameters are needed; the console stays open with a “Press Enter to exit...” prompt to prevent the window from closing immediately, and use --no-pause when launching from a terminal or automation to disable the prompt.


## Formatting example

- Example output structure (merged_file.txt) showing per‑document wrappers suitable for chunking and retrieval.

```txt
<context>
  <doc id="file1" name="file1">
contents1
  </doc>

  <doc id="file2" name="file2">
contents2
  </doc>

  <doc id="file3" name="file3">
contents3
  </doc>
</context>
```

- Each document is wrapped in a <doc> element with id/name derived from the base filename, and documents are separated by blank lines for clean boundaries.


## Options

- --out: Output filename, default merged_file.txt.
- --pattern: Glob for inputs, default *.txt.
- --encoding: Input encoding, default utf‑8.
- --errors: strict | ignore | replace (default replace).
- --no-pause: Do not prompt before exit (useful for scripted runs).


## Notes

onetxt writes a blank line between documents and guarantees each file ends with a newline so downstream chunkers and parsers see clean boundaries on the merged output.
