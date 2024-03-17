from customtkinter import CTkLabel


class InfoLabel(CTkLabel):
    def __init__(self, **kwargs):
        CTkLabel.__init__(self, **kwargs)

    def show_info(self, text: str):
        self.configure(text=text, text_color="green")

    def show_error(self, text: str):
        self.configure(text=text, text_color="red")
