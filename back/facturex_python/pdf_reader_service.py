from io import StringIO
from typing import Optional, List, Tuple, Dict
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import re
from PIL import Image
import pytesseract
from pdf2image import convert_from_path


class PdfReaderService:

    def __init__(self, path: str, vat_rate=0.2):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
        self.poppler_path = r'C:\Program Files (x86)\poppler-0.68.0\bin'
        self.path = path
        self.vat_rate = vat_rate
        self.content: Optional[str] = None
        self.regex = re.compile(r"([\w.\-]+ )?(\d+[.,]\d+)")
        self.numbers: List[Tuple[float, Optional[str], int]] = []
        self.nets: Dict[float, float] = {}
        self.wts: Dict[float, float] = {}
        self.taxes: Dict[float, float] = {}
        self.mode = "PDF"
        self.accounts: List[Tuple[str, str, str]] = [("552081317", "EDF.FR", "EDF"),
                                                     ("43841898000035", "CYRILVINCENT.COM", "CYRIL VINCENT CONSEIL")]

    def parse(self):
        extension = self.path[-3:].upper()
        if extension == "PDF":
            self.parse_pdf()
            if self.content.strip() == "":
                self.mode = "POPPLER"
                self.poppler()
        elif extension == "PNG" or extension == "JPG":
            self.mode = "PNG"
            self.parse_png()
        else:
            raise ValueError(f"Bad extension {extension}")


    def parse_pdf(self, nb_page=1):
        resource_manager = PDFResourceManager()
        with StringIO() as string_writer, open(self.path, 'rb') as pdf_file:
            la = LAParams() # Peut être modifié
            with TextConverter(resource_manager, string_writer, codec='utf-8', laparams=la) as device:
                interpreter = PDFPageInterpreter(resource_manager, device)
                for page in PDFPage.get_pages(pdf_file, maxpages=nb_page):
                    interpreter.process_page(page)
                self.content = string_writer.getvalue().upper()

    def parse_png(self):
        self.content = pytesseract.image_to_string(Image.open(self.path), lang='fra').upper()

    def poppler(self):
        pages = convert_from_path(self.path, 500, poppler_path=self.poppler_path)
        page = pages[0]
        page.save("docs/poppler.jpg", 'JPEG')
        self.content = str((pytesseract.image_to_string(Image.open("docs/poppler.jpg")))).upper()

    def match_regex(self, s) -> Optional[Tuple[float, Optional[str], int]]:
        m = self.regex.search(s)
        res = None
        if m is not None and m.lastindex == 2:
            pos = m.regs[0][1]
            res = m[2].replace(",", "."), m[1], pos
        return res

    def matches(self):
        s = self.content
        i = 0
        res = self.match_regex(s)
        while res is not None:
            prefix = res[1] if res[1] is not None else ""
            self.numbers.append((float(res[0]), prefix.strip().replace(".", "").upper(), res[2] + i))
            i += res[2]
            s = s[res[2] + 1:]
            res = self.match_regex(s)

    def get_net_strategy_1(self):
        for n in self.numbers:
            if "TTC" in n[1]:
                self.nets[n[0]] = 0.25

    def get_net_strategy_2(self):
        max = 0
        for n in self.numbers:
            if n[0] > max:
                max = n[0]
        if max not in self.nets:
            self.nets[max] = 0
        self.nets[max] += 0.5

    def get_net_strategy_3(self):
        n = self.numbers[-1][0]
        if n not in self.nets:
            self.nets[n] = 0
        self.nets[n] += 0.25

    def get_net(self):
        self.get_net_strategy_1()
        self.get_net_strategy_2()
        self.get_net_strategy_3()

    def get_wt_strategy_1(self):
        for n in self.numbers:
            if "HT" in n[1]:
                self.wts[n[0]] = 0.25

    def get_wt_strategy_2(self):
        max = 0
        before_max = 0
        for n in self.numbers:
            if n[0] > max:
                if before_max != max:
                    before_max = max
                max = n[0]
            elif n[0] > before_max and n[0] != max:
                before_max = n[0]
        if before_max not in self.wts:
            self.wts[before_max] = 0
        self.wts[before_max] += 0.3

    def get_wt_strategy_3(self):
        if len(self.numbers) > 1:
            n = self.numbers[-2][0]
            if n not in self.wts:
                self.wts[n] = 0
            self.wts[n] += 0.25

    def get_wt_strategy_4(self):
        for nnet in self.numbers:
            wt = round(nnet[0] / (1 + self.vat_rate), 2)
            for nwt in self.numbers:
                if nwt[0] == wt:
                    if nwt[0] not in self.wts:
                        self.wts[nwt[0]] = 0
                    if nnet[0] not in self.nets:
                        self.nets[nnet[0]] = 0
                    self.wts[nwt[0]] += 0.25
                    self.nets[nnet[0]] += 0.25

    def get_wt(self):
        self.get_wt_strategy_1()
        self.get_wt_strategy_2()
        self.get_wt_strategy_3()
        self.get_wt_strategy_4()

    def get_tax_strategy_1(self):
        for n in self.numbers:
            if "TVA" in n[1]:
                self.taxes[n[0]] = 0.5

    def get_tax(self):
        self.get_tax_strategy_1()

    def get_best(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        if len(self.numbers) > 0:
            self.get_net()
            self.get_wt()
            self.get_tax()
        best_net = 0
        best_net_score = 0
        best_wt = 0
        best_wt_score = 0
        for net in self.nets:
            if self.nets[net] > best_net_score:
                best_net_score = self.nets[net]
                best_net = net
        for tax in self.taxes:
            calculate = best_net - tax
            if calculate not in self.wts:
                self.wts[calculate] = 0
            self.wts[calculate] += 0.5
        for wt in self.wts:
            if wt != best_net and self.wts[wt] > best_wt_score:
                best_wt_score = self.wts[wt]
                best_wt = wt
        if best_wt == 0:
            for n in self.numbers:
                if n[0] < best_net:
                    best_wt = n[0]
        return (best_net, best_net_score), (best_wt, best_wt_score)

    def get_account(self):
        for a in self.accounts:
            if a[0] in self.content:
                return a, 1
        for a in self.accounts:
            if a[1] in self.content:
                return a, 0.9
        for a in self.accounts:
            if a[2] in self.content:
                return a, 0.5
        return "", "", "Unknown Account"


if __name__ == '__main__':
    # s = PdfReaderService("docs/FactureCVC875.pdf")
    # s = PdfReaderService("docs/poppler.jpg")
    s = PdfReaderService("docs/FactureEdf.pdf")
    # Mauvais order du texte, l'api itext7 de .NET gère mieux ce problèmes
    s.parse()
    print(s.mode)
    print(s.content.replace("\n", " "))
    s.matches()
    print(s.numbers)
    res = s.get_best()
    print(s.nets)
    print(s.wts)
    print(res)
    res = s.get_account()
    print(res[0])