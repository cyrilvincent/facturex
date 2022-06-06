from facturx import generate_from_file

with open("factur-x_2_1_basic.xml", "rb") as f:
    xml = f.read()

generate_from_file("FactureCVC875.pdf", xml, output_pdf_file="cvc_facturx.pdf", check_xsd=False)
