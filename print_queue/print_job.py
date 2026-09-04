class PrintJob:
    def __init__(self, document_name: str, pages: int, owner: str) -> None:
        if pages <= 0:
            raise ValueError("Number of pages must be positive.")
        if not owner:
            raise ValueError("Owner must be specified.")
        if not document_name:
            raise ValueError("Document must be specified.")
        self.document = document_name
        self.pages = pages
        self.owner = owner
