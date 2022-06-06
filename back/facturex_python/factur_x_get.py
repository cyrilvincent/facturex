from facturx import get_xml_from_pdf

with open("cvc_facturx.pdf", "rb") as f:
    (xml_filename, xml_string) = get_xml_from_pdf(f, False)
print(xml_string)