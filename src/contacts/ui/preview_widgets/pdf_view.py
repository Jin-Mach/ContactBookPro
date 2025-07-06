from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView


class PdfView(QPdfView):
    def __init__(self, pdf_path: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("pdfView")
        self.setPageMode(QPdfView.PageMode.MultiPage)
        self.setZoomMode(QPdfView.ZoomMode.Custom)
        self.setZoomFactor(0.8)
        self.pdf_path = pdf_path
        self.parent = parent
        self.pdf_document = QPdfDocument(self)
        self.pdf_document.load(pdf_path)
        if not self.pdf_document.status().Ready:
            self.document_sate = False
        else:
            self.setDocument(self.pdf_document)
            self.document_sate = True

    def zoom_in(self) -> None:
        if self.zoomFactor() < 2.0:
            self.setZoomFactor(self.zoomFactor() * 1.1)

    def zoom_out(self) -> None:
        if self.zoomFactor() > 0.5:
            self.setZoomFactor(self.zoomFactor() / 1.1)

    def reset_zoom(self) -> None:
        self.setZoomFactor(0.8)