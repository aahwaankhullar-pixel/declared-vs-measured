"""Extract district indicators directly from the official NFHS-5 district fact sheets (IIPS PDFs).
Usage: python extract_pdfs.py <pdf_root> <out_csv>
Values in parentheses (based on 25-49 unweighted cases) are kept but flagged; '*' (suppressed) becomes missing."""
import os, re, sys, subprocess
import pandas as pd

ROOT, OUT = sys.argv[1], sys.argv[2]
PATTERNS = {
    "electricity": r"households with electricity",
    "water": r"improved drinking.?water source",
    "sanitation": r"improved sanitation facility",
    "clean_fuel": r"using clean fuel for cooking",
    "women_school10": r"Women with 10 or more years of schooling",
    "diarrhoea": r"Prevalence of diarrhoea in the 2 weeks",
    "stunted": r"who are stunted",
    "underweight": r"who are underweight",
}


def parse(text, pat):
    for line in text.splitlines():
        if re.search(pat, line, re.I):
            # take the last two numeric tokens on the line (NFHS-5, NFHS-4)
            toks = re.findall(r"\(?\d+\.\d\)?|\*|\bna\b", line)
            if not toks:
                continue
            v5 = toks[-2] if len(toks) >= 2 else toks[-1]
            v4 = toks[-1] if len(toks) >= 2 else None
            return v5, v4
    return None, None

def clean(v):
    if v is None or v in ("*", "na"):
        return None, False
    small = v.startswith("(")
    return float(v.strip("()")), small

rows = []
for st in sorted(os.listdir(ROOT)):
    sp = os.path.join(ROOT, st)
    if not os.path.isdir(sp):
        continue
    for dt in sorted(os.listdir(sp)):
        f = os.path.join(sp, dt)
        if not os.path.isfile(f):
            continue
        text = subprocess.run(["pdftotext", "-layout", f, "-"], capture_output=True, text=True).stdout
        row = {"state_folder": st, "district_folder": dt}
        for k, pat in PATTERNS.items():
            v5, v4 = parse(text, pat)
            row[f"{k}_5"], row[f"{k}_5_small"] = clean(v5)
            row[f"{k}_4"], row[f"{k}_4_small"] = clean(v4)
        rows.append(row)
pd.DataFrame(rows).to_csv(OUT, index=False)
print(len(rows), "district fact sheets parsed")
