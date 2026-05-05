import re
import os

base_dir = "/Users/kaushalnandaniya/Desktop/MnC/sem-6/AF/HedgeFund_TimeSeriesForcasting/report/chapters/"
files = ["01_introduction.tex", "02_data_source.tex", "03_methodology.tex", "04_results.tex", "05_actions.tex", "06_future_work.tex", "07_references.tex"]

for filename in files:
    filepath = os.path.join(base_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()
    
    # Replace in reverse order of depth to avoid double replacement
    content = re.sub(r'\\subsubsection', r'\\paragraph', content)
    content = re.sub(r'\\subsection', r'\\subsubsection', content)
    content = re.sub(r'\\section', r'\\subsection', content)
    content = re.sub(r'\\chapter', r'\\section', content)
    
    # Also replace \label{ch:...} with \label{sec:...}
    content = re.sub(r'\\label\{ch:', r'\\label{sec:', content)
    
    # Also replace references \ref{ch:...} with \ref{sec:...}
    content = re.sub(r'\\ref\{ch:', r'\\ref{sec:', content)
    
    with open(filepath, "w") as f:
        f.write(content)

print("Downgraded headings in 7 files.")
