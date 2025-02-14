from app.common.utils import read_docx
from pathlib import Path


CUSTOMIZATIONSDOCX_PATH = Path(r"data\raw\Anadea homework  - Tee Customizer Shirts.docx")
CUSTOMIZATIONSTXT_PATH = Path(r"data\processed\customizations_doc.txt")

FAQDOCX_PATH = Path(r"data\raw\Anadea homework  -Tee Customizer FAQ.docx")
FAQTXT_PATH = Path(r"data\processed\faq_doc.txt")

convert_dict = {CUSTOMIZATIONSDOCX_PATH: CUSTOMIZATIONSTXT_PATH,
                FAQDOCX_PATH: FAQTXT_PATH}

def main():
    """
    Script to convert initial .docx files to .txt files.
    """
    for source, new in convert_dict.items():
        content = read_docx(source)
        with open(new, "w", encoding="utf-8-sig") as f:
            f.write(content)

if __name__=="__main__":
    main()