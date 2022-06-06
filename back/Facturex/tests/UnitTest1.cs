using iText.Kernel.Pdf;
using iText.Kernel.Pdf.Canvas.Parser;
using iText.Kernel.Pdf.Canvas.Parser.Listener;
using System;
using System.Text;
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
                ITextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
                string content = PdfTextExtractor.GetTextFromPage(page, strategy);
                Console.WriteLine(content);
                Assert.Equal(document.GetNumberOfPages(), 1);
                Assert.Equal(document.GetPdfVersion().ToString(), "PDF-1.7");
                Assert.Null(document.GetXmpMetadata());
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
                Assert.Equal(document.GetNumberOfPages(), 4);
                Assert.Equal(document.GetPdfVersion().ToString(), "PDF-1.7");
                byte[] xmp = document.GetXmpMetadata();
                string s = Encoding.ASCII.GetString(xmp);
                Assert.NotNull(s);

            }
        }

        [Fact]
        public void Itext7PdfOcrTest()
        {
            using (PdfReader reader = new PdfReader("docs/Madelin.pdf"))
            {
                PdfDocument document = new PdfDocument(reader);
                PdfPage page = document.GetPage(1);
                ITextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
                string content = PdfTextExtractor.GetTextFromPage(page, strategy);
                Console.WriteLine(content);
                Assert.Equal(document.GetNumberOfPages(), 1);
                Assert.Equal(document.GetPdfVersion().ToString(), "PDF-1.4");

            }
        }
    }
}