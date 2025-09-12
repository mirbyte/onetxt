from __future__ import annotations

from pathlib import Path
import sys
import argparse

# github/mirbyte
# v0.2

def find_text_files(cwd: Path, pattern: str, output_name: str):
    """Find text files matching pattern, excluding the output file."""
    for p in sorted(cwd.glob(pattern)):
        if p.name == output_name:
            continue
        if p.is_file():
            yield p

def merge_files(cwd: Path, output_name: str, pattern: str, encoding: str, errors: str) -> int:
    """Merge all matching text files into a structured context file."""
    txt_files = list(find_text_files(cwd, pattern, output_name))
    
    if not txt_files:
        print(f"No files matched pattern '{pattern}' in {cwd} (nothing to merge).")
        return 0

    out_path = cwd / output_name
    with out_path.open("w", encoding="utf-8") as out:
        out.write("<context>\n")
        
        for i, path in enumerate(txt_files):
            name = path.stem  # base filename without extension
            doc_id = i + 1    # numeric doc id starting at 1
            out.write(f'  <doc id="{doc_id}" name="{name}">\n')

            # Stream input to avoid holding large files in memory
            last_line_ends_with_newline = True
            with path.open("r", encoding=encoding, errors=errors) as src:
                for line in src:
                    out.write(line)
                    last_line_ends_with_newline = line.endswith("\n")

            # Add newline if last line didn't end with one
            if not last_line_ends_with_newline:
                out.write("\n")

            out.write("  </doc>\n")
            
            # Blank line between docs, but not after the last one
            if i != len(txt_files) - 1:
                out.write("\n")

        out.write("</context>\n")

    print(f"Created {output_name} with {len(txt_files)} documents.")
    return len(txt_files)

def pause_if_needed(enable_pause: bool):
    """Keep console open when double-clicked; allow disabling for CLI workflows."""
    if enable_pause:
        try:
            print("")
            input("Press Enter to exit...")
        except EOFError:
            pass

def parse_args():
    """Parse command line arguments."""
    p = argparse.ArgumentParser(description="Merge *.txt files into a single structured context file.")
    p.add_argument("--out", default="merged_file.txt", 
                   help="Output filename (default: merged_file.txt)")
    p.add_argument("--pattern", default="*.txt", 
                   help="Glob pattern for input files (default: *.txt)")
    p.add_argument("--encoding", default="utf-8", 
                   help="Input file encoding (default: utf-8)")
    p.add_argument("--errors", default="replace", 
                   choices=("strict", "ignore", "replace"),
                   help="Decoding error handling (default: replace)")
    p.add_argument("--no-pause", action="store_true", 
                   help="Do not prompt to press Enter before exit")
    return p.parse_args()




def main():
    """Main entry point."""
    args = parse_args()
    cwd = Path.cwd()
    merged = merge_files(cwd=cwd,
                         output_name=args.out,
                         pattern=args.pattern,
                         encoding=args.encoding,
                         errors=args.errors)
    pause_if_needed(enable_pause=not args.no_pause)


if __name__ == "__main__":
    main()

