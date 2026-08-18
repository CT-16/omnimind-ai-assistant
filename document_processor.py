import pypdf
from typing import Tuple, Optional

class DocumentProcessor:
    """Utility class to safely parse and validate uploaded documents."""
    
    @staticmethod
    def extract_text_from_pdf(uploaded_file) -> Tuple[str, int]:
        """Extracts plain text and page count from a PDF file."""
        try:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            num_pages = len(pdf_reader.pages)
            extracted_text = ""
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            return extracted_text.strip(), num_pages
        except Exception as e:
            raise RuntimeError(f"Failed to process PDF document: {str(e)}")

    @staticmethod
    def extract_text_from_txt(uploaded_file) -> str:
        """Extracts text from plain text file."""
        try:
            return uploaded_file.read().decode("utf-8").strip()
        except Exception as e:
            raise RuntimeError(f"Failed to read TXT file: {str(e)}")

    @classmethod
    def process_file(cls, uploaded_file) -> Tuple[Optional[str], dict]:
        """Validates and processes supported file types."""
        if uploaded_file is None:
            return None, {}
            
        filename = uploaded_file.name
        file_extension = filename.split(".")[-1].lower()
        
        metadata = {
            "filename": filename,
            "extension": file_extension,
            "size_kb": round(uploaded_file.size / 1024, 2)
        }
        
        if file_extension == "pdf":
            text, pages = cls.extract_text_from_pdf(uploaded_file)
            metadata["pages"] = pages
            metadata["word_count"] = len(text.split())
            return text, metadata
        elif file_extension in ["txt", "md"]:
            text = cls.extract_text_from_txt(uploaded_file)
            metadata["pages"] = 1
            metadata["word_count"] = len(text.split())
            return text, metadata
        else:
            raise ValueError(f"Unsupported file type: '.{file_extension}'. Please upload a PDF or TXT file.")