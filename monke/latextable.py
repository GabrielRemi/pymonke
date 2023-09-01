import numpy as np
from functions import error_round

class Latextable():
    __instance = (list, np.ndarray)
    
    def __init__(self, caption: str="caption", label: str=None, error_mode: str= "plus-minus"):
        self.caption = caption
        self.label = label
        self.table_str = ""
        self.figure_str = ""
        self.fig_mode = "htbp"
        self.content_str = ""
        self.alignment = None
        self.header = ""
        self.error_mode = error_mode
        self.lines_before_header: list[str] = []
        self.lines_after_values: list[str] = []
        
    def set_caption(self, caption: str):
        self.caption = caption
    
    def set_label(self, label: str):
        self.label = label
        
    def set_error_mode(self, error_mode: str):
        self.error_mode = error_mode
        
    def set_fig_mode(self, fig_mode: str):
        self.fig_mode = fig_mode
        
    def set_alignment(self, alignment: str):
        self.alignment = alignment
        
    def add_header(self, *args):
        for text in args:
            self.header += f'{text} & '
        self.header = self.header[:-2]
        self.header += "\\\\ \n"
        
    def add_values(self, *args):
        self.length = len(args)
        self.array_lengths = []
        self.types = [type(arg) for arg in args]
        for value_array in args:
            if isinstance(value_array, self.__instance):
                self.array_lengths.append(len(value_array))
            elif isinstance(value_array, tuple):
                self.array_lengths.append(len(value_array[0]))
            else:
                exit(-1)
        
        self.max_length = np.max(self.array_lengths)
        
        for i in range(self.max_length):
            for j, array in enumerate(args):
                if i < self.array_lengths[j]:
                    if isinstance(array, self.__instance):
                        self.content_str += f'${array[i]}$'
                    if isinstance(array, tuple):
                        value = array[0][i]
                        error = array[1][i]
                        if self.error_mode == "plus-minus":
                            rounded_value_and_error = error_round(value, error)
                            self.content_str += f'${rounded_value_and_error[0]} \\pm {rounded_value_and_error[1]}$'
                        elif self.error_mode == "parenthesis":
                            round_value = error_round(value, error, error_mode=self.error_mode)
                            self.content_str += f'${round_value}$'
                        elif self.error_mode == "scientific":
                            round_value = error_round(value, error, "scientific")[0]
                            self.content_str += f'${round_value}$'
                else:
                    self.content_str += "  "
                    
                if j < self.length - 1:
                    self.content_str += " & "
                else:
                    self.content_str += " \\\\\n"
                    
        # Set alignment
        if not self.alignment:
            self.alignment = ""
            for _ in range(self.length):
                self.alignment += "c|"
            self.alignment = self.alignment[:-1]
            
        self._make_table()
                
    def add_line_before_header(self, *items: str, end: str="\\\\"):
        text = ""
        for item in items:
            text += f'{item} & '
        text = text[:-3]
        text += f"{end}\n"
        self.lines_before_header.append(text)
        
    def add_line_after_values(self, *items: str, end: str="\\\\"):
        """Füge eine weitere Zeile in die Tabelle nach den Messwerten ein"""
        text = ""
        for item in items:
            text += f'{item} & '
        text = text[:-3]
        text += f"{end}\n"
        self.lines_after_values.append(text)
        
    def add_hline(self, num=1):
        """Füge den Befehl \\hline in die Tabelle for dem header ein"""
        for _ in range(num):
            self.lines_before_header.append("\\hline")
            
    def end_with_hline(self, num=1):
        """Ende die Tabelle with num x \\hline Befehlen"""
        for _ in range(num):
            self.lines_after_values.append("\\hline")
                
    def _make_table(self):
        self.table_str = f"\\begin{{tabular}}{{{self.alignment}}}\n"
        for line in self.lines_before_header:
            self.table_str += f'{line}\n'
        self.table_str += f'{self.header}\hline\n'
        self.table_str += self.content_str
        for line in self.lines_after_values:
            self.table_str += f'{line}\n'
        self.table_str += f"\\end{{tabular}}\n\\caption{{{self.caption}}}\n"
        if self.label:
            self.table_str += f"\\label{{{self.label}}}\n"
    
    def make_figure(self, other=None) -> str:
        """Binde die Tabelle in eine figure Umgebung ein. Falls other!=none, dann füge
            self und other beide in die gleiche figure Umgebung, damit zwei Objekte im Dokument nebeneinander 
            angezeigt werden können. Benutze dafür den parbox Befehl"""
            
        figure_str = f"\\begin{{figure}}[{self.fig_mode}]\n   \\centering\n"
        if not other:
            figure_str += self.table_str
        elif isinstance(other, Latextable):
            figure_str += "\\parbox{0.45\\linewidth}{\\centering\n"
            figure_str += self.table_str
            figure_str += "}\\quad"
            figure_str += "\\parbox{0.45\\linewidth}{\\centering\n"
            figure_str += other.table_str
            figure_str += "}"
        else:
            exit(-1)
        figure_str += "\\end{figure}"
        return figure_str