from dataclasses import dataclass
from typing import List


@dataclass(init=False)
class Transaction:

    dt_posted: str
    dt_user: str
    trn_amt: float
    fit_id: str
    name: str


class OFXParser:

    def __init__(self):
        self.transacs = []

    def get_value(self, row):
        l = row.split(">")
        return l[1].strip()

    def parse(self, path):
        print(f"Load {path}")
        with open(path, "r") as f:
            for row in f:
                row = row.strip()
                if row == "<STMTTRN>":
                    t = Transaction()
                elif "DTPOSTED" in row:  # 0
                    t.dt_posted = self.get_value(row)
                elif "DTUSER" in row:  # 1
                    t.dt_user = self.get_value(row)
                elif "TRNAMT" in row:  # 2
                    t.trn_amt = float(self.get_value(row))
                elif "FITID" in row:  # 3
                    t.fit_id = self.get_value(row)
                elif "MEMO" in row or "NAME" in row:  # 4
                    t.name = self.get_value(row)
                elif row == "</STMTTRN>":
                    self.transacs.append(t)

class Transacs2CSVWriter:

    def __init__(self, transacs):
        self.transacs: List[Transaction] = transacs

    def write(self, path):
        with open(path, "w") as f:
            f.write("Date;Date valeur;Operation;Debit;Credit\n")
            for t in p.transacs:
                f.write(t.dt_posted + ";")
                f.write(t.dt_user + ";")
                f.write(t.name + ";")
                if t.trn_amt < 0:
                    f.write(f"{t.trn_amt};\n")
                else:
                    f.write(f";{t.trn_amt}\n")
        print(f"{path} generated")


if __name__ == '__main__':
    print("OFX to CSV by Cyril Vincent")
    print("===========================")
    p = OFXParser()
    p.parse("docs/comptes_annuel.ofx")
    print(p.transacs)
    w = Transacs2CSVWriter(p.transacs)
    w.write("docs/comptes.csv")