from facturx import generate_from_file

with open("docs/factur-x_2_1_basic.xml", "rb") as f:
    xml = f.read()

generate_from_file("docs/FactureCVC875.pdf", xml, output_pdf_file="docs/cvc_facturx.pdf", check_xsd=False)
