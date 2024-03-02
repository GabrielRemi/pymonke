import unittest

import pandas as pd

from src.pymonke.latex.tex_table import TexTable
from monke.latex.tex_tabular import TexTabular

# TODO table_test.py not up to date

class MyTestCase(unittest.TestCase):
    def test_empty(self):
        table = TexTable(tabular=[TexTabular(alignment="c")], widths=[0.3, 0.3])
        str(table)
        table = TexTable(tabular=[TexTabular(alignment="c"), TexTabular(alignment="c")], widths=[0.3, 0.3])
        str(table)

    def test_base_table(self):
        string = r"""\begin{table}[htbp]
    \centering
    \caption{Tabelle}
    \label{tab:tabelle}
    \begin{tabular}{c|c}
        \toprule
        Zahl1 & Zahl2 \\
        \midrule
        1.0 & 1.0 \\
        2.0 & 2.0 \\
        3.0 &   \\
        \bottomrule
    \end{tabular}
\end{table}"""
        data = pd.DataFrame(data={
            "Zahl1": [1, 2, 3],
            "Zahl2": [1, 2, None],
        })
        table = TexTable(tabular=[TexTabular(data=data, alignment="c|c", caption="Tabelle", label="tab:tabelle",
                                             h_lines=[0, 1, 4], filler=" ", booktabs=True)])
        self.assertEqual(string, str(table))

    def errors(self):

        with self.assertRaises(ValueError):
            table = TexTable(tabular=[TexTabular(), TexTabular()], widths=[0.34])
            print(table)


if __name__ == '__main__':
    unittest.main()
