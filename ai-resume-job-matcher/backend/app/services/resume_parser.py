import pdfplumber
from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE_MB = 10


def parse_pdf(file: UploadFile) -> str:
    # Validate MIME type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Validate size
    file.file.seek(0, 2)
    size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)

    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB")

    try:
        # Ensure pointer at start
        file.file.seek(0)

        text = ""
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="PDF contains no extractable text (possibly scanned)"
            )

        return text

    except HTTPException:
        raise  # rethrow clean errors

    except Exception as e:
        # Convert ALL pdfplumber errors into readable API error
        raise HTTPException(
            status_code=500,
            detail=f"PDF parsing failed: {str(e)}"
        )
