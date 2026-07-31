class TableEngine:
    def extract_tables(self, pdf_path, page_classifications=None):
        tables_data = []
        # Use pdfplumber for speed; fall back to camelot only when needed
        tables_data = self._pdfplumber_tables(pdf_path, page_classifications)
        if tables_data:
            return tables_data
        try:
            import camelot
            for flavor in ("lattice", "stream"):
                try:
                    camelot_tables = camelot.read_pdf(
                        pdf_path,
                        pages="1-5",
                        flavor=flavor,
                        strip_text="\n",
                    )
                    for t in camelot_tables:
                        rows = t.data
                        if rows and len(rows) > 1:
                            tables_data.append({
                                "page": t.page,
                                "rows": rows,
                                "source": "camelot_" + flavor,
                            })
                    if tables_data:
                        return tables_data
                except Exception:
                    continue
        except ImportError:
            pass
        except Exception:
            pass
        return tables_data

    def _pdfplumber_tables(self, pdf_path, page_classifications=None):
        import pdfplumber
        tables_data = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    if page_classifications:
                        pc = page_classifications[page_num - 1]
                        if pc.get("class") != "TABLE" and pc.get("char_count", 0) < 100:
                            continue
                    tables = page.extract_tables()
                    for table in tables:
                        rows = []
                        for row in table:
                            cleaned = [
                                (cell.strip() if cell else "") for cell in row
                            ]
                            if any(c for c in cleaned):
                                rows.append(cleaned)
                        if len(rows) > 1:
                            tables_data.append({
                                "page": page_num,
                                "rows": rows,
                                "source": "pdfplumber",
                            })
        except Exception:
            pass
        return tables_data
