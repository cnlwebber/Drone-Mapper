import customtkinter as customtk
import tkinter as tk
import converter as cv
import trackconverter as tcv

from tkinter import filedialog
from tkinter.messagebox import askyesno

"""
Functionality: input a CSV file, then save to KML

Possible additions: have a default header that uses the red spots, and if disabled,
lets user fill out "<name>Mapped Drone</name>", scale, style, and etc.

"""

DEFAULT_STRING = "Default Header and Default Formatting Selected"
X_PADDING = 20
Y_PADDING = 20
GREEN = "#605B43"


# Centers window (grabbed from customtkinter GitHub)
def centerwindowtodisplay(screen: customtk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


class GUI(customtk.CTk):

    def __init__(self):
        super().__init__()

        # declare general fields
        self.track_header = "Default"
        self.track_format = "Default"
        self.csv_file_path = None

        # configure window
        self.title("CSV Converter")
        self.geometry(centerwindowtodisplay(self, 700, 400, self._get_window_scaling()))
        self.resizable(False, False)
        customtk.set_appearance_mode("dark")
        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # -------- Labels  --------
        # label for the text box
        box_label_var = tk.StringVar(value="Customize gx:Track KML Below:")
        self.text_label = customtk.CTkLabel(master=self, textvariable=box_label_var,
                                            width=425, height=25, padx=X_PADDING,
                                            fg_color="transparent")
        self.text_label.grid(row=0, column=1)

        # label for user feedback
        self.feedback_label_var = tk.StringVar(value=DEFAULT_STRING)
        self.feedback_label = customtk.CTkLabel(master=self, textvariable=self.feedback_label_var,
                                                width=450, height=25, padx=X_PADDING,
                                                fg_color="#793324")
        self.feedback_label.grid(row=10, column=1)

        # -------- TextBox --------
        # create a scrolled text window to input formatting
        self.text_box = customtk.CTkTextbox(master=self, state="normal", width=425, height=300,
                                            wrap="none", font=("Times New Roman", 14))
        self.text_box.grid(row=1, rowspan=8, column=1, sticky="wens", padx=X_PADDING)

        # -------- Buttons --------
        # button for opening a csv file
        self.open_button = customtk.CTkButton(master=self, text="Open CSV...", command=self.open_callback)
        self.open_button.grid(row=0, column=0, rowspan=2, sticky="ens", padx=X_PADDING, pady=Y_PADDING)
        # button for creating placemark kml file
        self.placemark_button = customtk.CTkButton(master=self, text="Save as Marker KML...",
                                                   command=self.placemark_callback,
                                                   state="disabled")
        self.placemark_button.grid(row=2, column=0, rowspan=2, sticky="ens", padx=X_PADDING, pady=Y_PADDING)
        # button for creating track kml file
        self.track_button = customtk.CTkButton(master=self, text="Save as Track KML...", command=self.track_callback,
                                               state="disabled", fg_color=GREEN)
        self.track_button.grid(row=8, column=0, rowspan=2, sticky="ens", padx=X_PADDING, pady=Y_PADDING)

        # button for setting the kml header
        self.header_button = customtk.CTkButton(master=self, text="Set Track Header", command=self.header_callback,
                                                state="normal", fg_color=GREEN)
        self.header_button.grid(row=4, column=0, rowspan=2, sticky="ens", padx=X_PADDING, pady=Y_PADDING)

        # button for setting the gx:track formatting
        self.format_button = customtk.CTkButton(master=self, text="Set Track Format", command=self.format_callback,
                                                state="normal", fg_color=GREEN)
        self.format_button.grid(row=6, column=0, rowspan=2, sticky="ens", padx=X_PADDING, pady=Y_PADDING)

        # button to clear input
        self.clear_button = customtk.CTkButton(master=self, text="Clear Input", command=self.clear_callback,
                                               state="disabled", fg_color=GREEN)
        self.clear_button.grid(row=10, column=0, rowspan=2, sticky="ens", padx=X_PADDING, pady=Y_PADDING)

    def clear_callback(self):
        self.feedback_label_var.set(DEFAULT_STRING)
        self.track_header = "Default"
        self.track_format = "Default"
        self.clear_button.configure(state="disabled")
        self.format_button.configure(state='normal')
        self.header_button.configure(state='normal')

    def format_callback(self):
        temp_format = self.text_box.get(1.0, tk.END).strip()
        if temp_format != "":
            self.track_format = temp_format
            self.text_box.delete(1.0, tk.END)
            self.clear_button.configure(state='normal')
            self.format_button.configure(state='disabled')
            if self.feedback_label_var.get() == DEFAULT_STRING:
                self.feedback_label_var.set("Default Header and Custom Formatting Selected")
            else:
                self.feedback_label_var.set("Custom Header and Custom Formatting Selected")

    def header_callback(self):
        temp_header = self.text_box.get(1.0, tk.END).strip()
        if temp_header != "":
            self.track_header = self.text_box.get(1.0, tk.END)
            self.text_box.delete(1.0, tk.END)
            self.clear_button.configure(state='normal')
            self.header_button.configure(state="disabled")
            if self.feedback_label_var.get() == DEFAULT_STRING:
                self.feedback_label_var.set("Custom Header and Default Formatting Selected")
            else:
                self.feedback_label_var.set("Custom Header and Custom Formatting Selected")

    # callback for csv file open button
    def open_callback(self):
        self.csv_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.csv_file_path:
            self.placemark_button.configure(state='normal')
            self.track_button.configure(state='normal')

    # callback for placemark kml file button, uses converter.py
    def placemark_callback(self):
        output_file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
        if output_file_path:
            converter = cv.Converter(self.csv_file_path)
            converter.convert(output_file_path)

    def track_callback(self):
        if self.track_header == "Default" or self.track_format == "Default":
            answer = askyesno(title="Use Defaults?",
                              message="Are you sure you want to use the default header or gx:Track formatting?")
            if answer:
                output_file_path = filedialog.asksaveasfilename(defaultextension=".kml",
                                                                filetypes=[("KML files", "*.kml")])
                if output_file_path:
                    tconverter = tcv.TrackConverter(self.csv_file_path)
                    tconverter.convert(output_file_path, self.track_header, self.track_format)
        else:
            output_file_path = filedialog.asksaveasfilename(defaultextension=".kml",
                                                            filetypes=[("KML files", "*.kml")])
            if output_file_path:
                tconverter = tcv.TrackConverter(self.csv_file_path)
                tconverter.convert(output_file_path, self.track_header, self.track_format)


gui = GUI()
gui.mainloop()
