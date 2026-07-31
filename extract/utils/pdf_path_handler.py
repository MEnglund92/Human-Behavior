import os
import shutil
import glob


def find_pdfs(directory):
    pdfs = []
    try:
        d = os.fsencode(directory)
        for f in os.listdir(d):
            fname = os.fsdecode(f)
            if fname.lower().endswith(".pdf"):
                full_path = os.path.join(directory, fname)
                pdfs.append(full_path)
    except Exception as e:
        print(f"  WARNING: Cannot read directory {directory}: {e}")
    return sorted(pdfs)


def is_path_accessible(path):
    try:
        with open(path, "rb") as f:
            f.read(4)
        return True
    except Exception:
        return False


def handle_problem_pdfs(source_dirs, pending_dir):
    os.makedirs(pending_dir, exist_ok=True)
    problems = []
    for source_dir in source_dirs:
        if not os.path.isdir(source_dir):
            continue
        for pdf_path in find_pdfs(source_dir):
            if not is_path_accessible(pdf_path):
                fname = os.path.basename(pdf_path)
                dest = os.path.join(pending_dir, fname)
                try:
                    shutil.copy2(pdf_path, dest)
                    problems.append({
                        "original": pdf_path,
                        "copied_to": dest,
                        "reason": "path_encoding_issue",
                    })
                    print(f"  COPIED (encoding issue): {fname[:60]}")
                except Exception as e:
                    print(f"  FAILED to copy {fname[:60]}: {e}")
    return problems


def get_all_pdf_paths(source_dirs, pending_dir):
    all_pdfs = []
    for source_dir in source_dirs:
        all_pdfs.extend(find_pdfs(source_dir))
    if os.path.isdir(pending_dir):
        all_pdfs.extend(find_pdfs(pending_dir))
    seen = set()
    unique = []
    for p in all_pdfs:
        name = os.path.basename(p)
        if name not in seen:
            seen.add(name)
            unique.append(p)
    return unique


def suggest_rename_commands(problems):
    if not problems:
        return
    print("\n=== PDFs with Encoding Issues ===")
    print("These files have special characters in their paths.")
    print("They have been copied to extract/pending_rename/")
    print("To permanently fix, rename the original files:\n")
    for p in problems:
        old = os.path.basename(p["original"])
        clean = old.encode("ascii", "ignore").decode("ascii").strip()
        clean = clean.replace("  ", " ").replace("..", ".")
        print(f"  Original: {old[:60]}...")
        print(f"  Suggested: {clean[:60]}...")
        print()
