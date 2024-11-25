# TexTk

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

__version__ = "1.4.2"

#main window class

class TextEditor(tk.Tk):
    """Main app window."""
    def __init__(self):
        super().__init__()
        self.title("TexTk")
        self.geometry("600x500")
        self.option_add('*tearOff', False) # this is so stupid

        self.createGUI()

    def createGUI(self):
        """Creates main widgets."""
        self.textFont = font.Font(family="Helvetica", size=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.textSpace = tk.Text(
            self.frame, 
            font=self.textFont,
            wrap="char", # <--- change that
        ) 
        self.textSpace.pack(padx=10, pady=10, expand=True, fill="both")

        #TODO: this is so broken. decide to fix it or trash it
        #self.scrollbarX = tk.Scrollbar(self.frame, command=self.textSpace.xview)
        #self.scrollbarX.pack(side="bottom", fill="x")
        #self.textSpace.configure(xscrollcommand=self.scrollbarX.set)

        #~ Keybinds
        self.bind("<Control-s>", self.saveFile)
        self.bind("<Control-o>", self.openFile)

        #~ menu bar stuff
        self.menubar = tk.Menu(self)
        self["menu"] = self.menubar

        #~ File menu
        self.fileMenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.fileMenu, label="File")
        self.fileMenu.add_command(label="Open File", command=self.openFile)
        self.fileMenu.add_command(label="Save File", command=self.saveFile)

        #~ Themes menu
        self.themesMenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.themesMenu, label="Themes")

        self.themesMenu.add_command(label="Light", command=lambda: self.changeTheme("light"))
        self.themesMenu.add_command(label="Dark", command=lambda: self.changeTheme("dark"))
        self.themesMenu.add_command(label="Black", command=lambda: self.changeTheme("black"))
        self.themesMenu.add_command(label="Matrix", command=lambda: self.changeTheme("matrix"))
        self.themesMenu.add_command(label="Solarized Dark", command=lambda: self.changeTheme("solardark"))
        self.themesMenu.add_command(label="Solarized Dark 2", command=lambda: self.changeTheme("solardark2"))

        #~ Font Menu
        self.fontMenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.fontMenu, label="Font")

        # hey look i did a smart thing
        for i in range(8, 21, 2):
            self.fontMenu.add_command(label=f"{i}", command=lambda size=i: self.changeFontSize(size))

        #~ About menu
        self.aboutMenu = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.aboutMenu, label="About")
        self.aboutMenu.add_command(label="About", command=self.openAbout)

    def changeTheme(self, theme):
        if theme == "light":
            self.frame.configure(bg="lightgrey")
            self.textSpace.configure(bg="white", fg="black")

        elif theme == "dark":
            self.frame.configure(bg="#1a1a1a")
            self.textSpace.configure(bg="#1f1f1f", fg="white")

        elif theme == "black":
            self.frame.configure(bg="black")
            self.textSpace.configure(bg="black", fg="white")

        elif theme == "matrix":
            self.frame.configure(bg="black")
            self.textSpace.configure(bg="black", fg="lime") 

        elif theme == "solardark":
            self.frame.configure(bg="#002b36")
            self.textSpace.configure(bg="#073642", fg="white")

        elif theme == "solardark2":
            self.frame.configure(bg="#002b36")
            self.textSpace.configure(bg="#073642", fg="#859900")    

    def changeFontSize(self, size: int):
        self.textFont.configure(size=size)

    def openAbout(self):
        """Opens the about window."""
        self.about = AboutWindow()

    #~ file stuff
    def isBinaryFile(self, path):
        """Checks if the file is not a text file. Not 100% accurate because I'm lazy."""
        try:
            with open(path, "rb") as f:
                testArea = f.read(512)
                testArea.decode("utf-8")
                return False
        except UnicodeDecodeError:
            return True

    def openFile(self, event=None):
        """Opens a file."""
        self.filePath = filedialog.askopenfilename()
        #~ check if the file is a text file
        if self.isBinaryFile(self.filePath):
            messagebox.showerror(title="Error", message="Exception occured:\nFile contains binary data. This may be wrong.\n If so, remove any potentally odd characters.")
        else:
            with open(self.filePath, "r") as f:
                txtData = f.read()
                self.textSpace.delete("1.0", tk.END)
                self.textSpace.insert("1.0", txtData)
                messagebox.showinfo(title="Loaded", message=f"Loaded file {self.filePath}")

    def saveFile(self, event=None):
        """Saves the contents of the text space to a file."""
        try:
            self.fileName = filedialog.asksaveasfilename(defaultextension=".txt")
            with open(self.fileName, "w") as f:
                f.write(self.textSpace.get("1.0", tk.END))
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Exception occured: {e}")

class AboutWindow(tk.Toplevel):
    """The about window."""
    def __init__(self):
        super().__init__()
        self.title("About")
        self.geometry("300x200")
        self.resizable(False, False)

        self.createGUI()

    def createGUI(self):
        self.title = tk.Label(
            self,
            text="TexTk",
            font=("Helvetica", 22, "bold")
        ).pack(pady=10)
        
        self.dev = tk.Label(
            self,
            text="Developed by BlueJay",
            font=("Helvetica", 12)
        ).pack(pady=10)

        self.version = tk.Label(
            self,
            text=f"Version v{__version__}",
            font=("Helvetica", 12)
        ).pack(pady=10)

        self.tip = tk.Label(
            self,
            text="You can use Ctrl+O & Ctrl+S to open and save files!",
            font=("Helvetica", 9)
        ).pack(pady=10)


#~ actually run code
if __name__ == "__main__":
    app = TextEditor()
    app.mainloop()
