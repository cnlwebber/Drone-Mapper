import customtkinter as customtk
from tkinter import filedialog
import converter as cv

"""
Functionality: input a CSV file, then save to KML

Possible additions: have a default header that uses the red spots, and if disabled,
lets user fill out "<name>Mapped Drone</name>", scale, style, and etc.

"""
class GUI(customtk.CTk):

    def __init__ (self):
        super().__init__()

        self.title("CSV Converter")
        self.geometry("500x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.csv_file_path = None

        self.open_button = customtk.CTkButton(self, text="Open CSV", command=self.open_callback)
        self.open_button.grid(row=0,column=0,padx=20,pady=20, sticky="ew", columnspan=2)

        self.save_button = customtk.CTkButton(self, text="Save as KML", command=self.save_callback,state="disabled")
        self.save_button.grid(row=1,column=0,padx=20,pady=20, sticky="ew", columnspan=2)

    def open_callback(self):
        self.csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.csv_file_path:
            self.save_button.configure(state='normal')

    def save_callback(self):
        output_file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
        if output_file_path:
            converter = cv.Converter(self.csv_file_path)
            converter.convert(output_file_path)


gui = GUI()
gui.mainloop()


