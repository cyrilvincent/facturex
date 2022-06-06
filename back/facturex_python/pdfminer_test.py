from pdfminer import high_level

local_pdf_filename = "FactureCVC875.pdf"
pages = [0] # just the first page

extracted_text = high_level.extract_text(local_pdf_filename, "", pages)
print(extracted_text)