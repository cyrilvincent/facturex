using iText.Kernel.Exceptions;
using iText.Kernel.Pdf;
using iText.Kernel.Pdf.Canvas.Parser;
using iText.Kernel.Pdf.Canvas.Parser.Listener;
using s2industries.ZUGFeRD;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Xml;
using Xunit;

namespace tests
{
    public class UnitTest1
    {
        [Fact]
        public void Itext7PdfTest()
        {
            using(PdfReader reader = new PdfReader("docs/FactureCVC875.pdf"))
            {
                PdfDocument document = new PdfDocument(reader);
                PdfPage page = document.GetPage(1);
                ITextExtractionStrategy strategy = new LocationTextExtractionStrategy(); //new SimpleTextExtractionStrategy();
                string content = PdfTextExtractor.GetTextFromPage(page, strategy);
                Console.WriteLine(content);
                Assert.NotEqual(content, "");
                Assert.Equal(document.GetNumberOfPages(), 1);
                Assert.Equal(document.GetPdfVersion().ToString(), "PDF-1.7");
            }
        }

        [Fact]
        public void Itext7PdfEdfTest()
        {
            using (PdfReader reader = new PdfReader("docs/FactureEdf.pdf"))
            {
                PdfDocument document = new PdfDocument(reader);
                PdfPage page = document.GetPage(1);
                ITextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
                string content = PdfTextExtractor.GetTextFromPage(page, strategy);
                Console.WriteLine(content);
                Assert.NotEqual(content, "");
                Assert.Equal(document.GetNumberOfPages(), 4);
                Assert.Equal(document.GetPdfVersion().ToString(), "PDF-1.7");
                byte[] xmp = document.GetXmpMetadata();
                string s = Encoding.ASCII.GetString(xmp);
                Assert.NotNull(s);

            }
        }

        [Fact]
        public void FacturXZuferd21Read()
        {
            InvoiceDescriptor descriptor = InvoiceDescriptor.Load("docs/factur-x_2_1_basic.xml");
            Assert.NotNull(descriptor);  

        }

        [Fact]
        public void FacturXZuferdGenerate()
        {
            InvoiceDescriptor desc = InvoiceDescriptor.CreateInvoice("471102", new DateTime(2013, 6, 5), CurrencyCodes.EUR, "GE2020211-471102");
            desc.ReferenceOrderNo = "AB-312";
            desc.AddNote("Rechnung gem‰ﬂ Bestellung Nr. 2013-471331 vom 01.03.2013.");
            //desc.AddNote("Es bestehen Rabatt- und Bonusvereinbarungen.", "AAK");
            desc.SetBuyer("Kunden Mitte AG", "69876", "Frankfurt", "15 Kundenstraﬂe",CountryCodes.FR, "88", new GlobalID("EAN", "4000001987658"));
            desc.AddBuyerTaxRegistration("DE234567890", TaxRegistrationSchemeID.VA);
            desc.SetBuyerContact("Hans Muster");

            desc.SetSeller("Lieferant GmbH", "80333", "M¸nchen", "20 Lieferantenstraﬂe", CountryCodes.FR, "88", new GlobalID("EAN", "4000001987659"));
            desc.AddSellerTaxRegistration("201/113/40209", TaxRegistrationSchemeID.FC);
            desc.AddSellerTaxRegistration("DE123456789", TaxRegistrationSchemeID.VA);
            desc.SetBuyerOrderReferenceDocument("2013-471331", new DateTime(2013, 03, 01));
            desc.SetDeliveryNoteReferenceDocument("2013-51111", new DateTime(2013, 6, 3));
            desc.ActualDeliveryDate = new DateTime(2013, 6, 3);
            desc.SetTotals(202.76m, 5.80m, 14.73m, 193.83m, 21.31m, 215.14m, 50.0m, 165.14m);
            desc.AddApplicableTradeTax(10m, 20m, TaxTypes.VAT, TaxCategoryCodes.S);
            desc.AddApplicableTradeTax(20m, 20m, TaxTypes.VAT, TaxCategoryCodes.S);
            //desc.SetLogisticsServiceCharge(5.80m, "Versandkosten", "VAT", "S", 7m);
            desc.SetTradePaymentTerms("Zahlbar innerhalb 30 Tagen netto bis 04.07.2013, 3% Skonto innerhalb 10 Tagen bis 15.06.2013", new DateTime(2013, 07, 04));
            desc.Save("docs/zugferd.xml", ZUGFeRDVersion.Version21, Profile.Basic);
        }

        [Fact]
        public void IText7PdfObject()
        {
            using (PdfReader reader = new PdfReader("docs/cvc_facturx.pdf"))
            {
                PdfDocument document = new PdfDocument(reader);
                int nb = document.GetNumberOfPdfObjects();
                for (int i = 0; i < nb; i++)
                {
                    PdfObject obj = document.GetPdfObject(i);
                    if (obj != null && obj.IsStream())
                    {
                        byte[] b;
                        try
                        {
                            b = ((PdfStream)obj).GetBytes();
                        }
                        catch (PdfException exc)
                        {
                            b = ((PdfStream)obj).GetBytes(false);
                        }
                        XmlDocument doc = new XmlDocument();
                        string xml = Encoding.UTF8.GetString(b);
                        if (xml.Contains("CrossIndustryInvoice"))
                            File.WriteAllText($"docs/cvc_{i}.xml", xml);
                    }
                }

            }

        }

        [Fact]
        public void Itext7DigitsExtractTest()
        {
            using (PdfReader reader = new PdfReader("docs/FactureCVC875.pdf"))
            {
                PdfDocument document = new PdfDocument(reader);
                PdfPage page = document.GetPage(1);
                ITextExtractionStrategy strategy = new LocationTextExtractionStrategy(); //new SimpleTextExtractionStrategy();
                string content = PdfTextExtractor.GetTextFromPage(page, strategy);
                string[] ss = content.Split(new char[] { ' ', '\t', '\n' });
                var l = new List<float>();
                foreach (string s in ss)
                {
                    try
                    {
                        var stemp = s.Replace(",", ".");
                        if (stemp.Contains("."))
                        {
                            var f = float.Parse(stemp);
                            l.Add(f);
                        }
                    }
                    catch (Exception exc) { }
                }
                Assert.True(l.Count > 0);
                Assert.Equal(4500, l.Last());

            }

        }

        [Fact]
        public void Itext7DigitsExtractEdfTest()
        {
            using (PdfReader reader = new PdfReader("docs/FactureEdf.pdf"))
            {
                PdfDocument document = new PdfDocument(reader);
                PdfPage page = document.GetPage(1);
                ITextExtractionStrategy strategy = new LocationTextExtractionStrategy(); //new SimpleTextExtractionStrategy();
                string content = PdfTextExtractor.GetTextFromPage(page, strategy);
                string[] ss = content.Split(new char[] { ' ', '\t', '\n' });
                var l = new List<float>();
                foreach (string s in ss)
                {
                    try
                    {
                        var stemp = s.Replace(",", ".");
                        if (stemp.Contains("."))
                        {
                            var f = float.Parse(stemp);
                            l.Add(f);
                        }
                    }
                    catch (Exception exc) { }
                }
                Assert.True(l.Count > 0);
                Assert.Equal(146.62, l[3], 2); // Bug si espace dans le chiffre ex 1 032Ä, faire avec une regex

            }
        }
    }
}