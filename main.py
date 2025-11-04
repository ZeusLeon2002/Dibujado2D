import customtkinter as ctk
from Drawing2D import Draw

if __name__ == "__main__":
    root = ctk.CTk()
    app = Draw(root)
    root.mainloop()