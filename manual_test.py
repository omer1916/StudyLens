"""rag_pipeline.py'yi Streamlit'ten bağımsız, terminalden hızlıca denemek için.

Kullanım:
    python manual_test.py ornek.pdf "Bu belge ne anlatıyor?"
"""

import sys

from dotenv import load_dotenv

from rag_pipeline import answer_question

load_dotenv()


def main() -> None:
    if len(sys.argv) < 3:
        print("Kullanım: python manual_test.py <pdf_yolu> <soru>")
        sys.exit(1)

    pdf_path, question = sys.argv[1], " ".join(sys.argv[2:])
    with open(pdf_path, "rb") as pdf_file:
        result = answer_question(pdf_file, question)

    print(f"\nCevap: {result['answer']}")
    print(f"Kaynak: sayfa {result['source_page']}")


if __name__ == "__main__":
    main()
