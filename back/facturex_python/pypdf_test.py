print("Hello")
import PyPDF2

# creating a pdf file object
pdfFileObj = open('FactureEdf.pdf', 'rb') # Ne marche pas pour CVC

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
print(pdfReader.numPages)

# creating a page object
pageObj = pdfReader.getPage(0)

# extracting text from page
s = pageObj.extractText()

print(s)

# closing the pdf file object
pdfFileObj.close()