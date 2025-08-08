import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

# ... [topics, surveys, SAS_TEMPLATE same as before] ...

SURVEY_STYLES = {
    "YRBS": {
        "bg": "#FFF0F5",
        "entry_bg": "#FFF8F9",
        "entry_fg": "#800000",
        "btn_bootstyle": "danger-outline",
        "text_bg": "#FFF8F9",
        "text_fg": "#800000",
        "dropdown_bg": "#FFD9E8",
    },
    "CHS": {
        "bg": "#D0F0F0",
        "entry_bg": "#E0F7F7",
        "entry_fg": "#004d40",
        "btn_bootstyle": "success-outline",
        "text_bg": "#E0F7F7",
        "text_fg": "#004d40",
        "dropdown_bg": "#B2DFDB",
    },
    "HANES": {
        "bg": "#FFEDD5",
        "entry_bg": "#FFF3E0",
        "entry_fg": "#E65100",
        "btn_bootstyle": "warning-outline",
        "text_bg": "#FFF3E0",
        "text_fg": "#E65100",
        "dropdown_bg": "#FFCC80",
    },
    "CCHS": {
        "bg": "#DFFFE0",
        "entry_bg": "#E8FFF1",
        "entry_fg": "#2E7D32",
        "btn_bootstyle": "info-outline",
        "text_bg": "#E8FFF1",
        "text_fg": "#2E7D32",
        "dropdown_bg": "#A5D6A7",
    },
}

class SASGeneratorApp(tb.Window):
    def __init__(self):
        super().__init__(title="SAS Code Generator", size=(900, 650))
        self.geometry("900x650")

        # Variables
        self.current_survey_key = None

        # Dataset Dropdown
        self.label_dataset = tb.Label(self, text="Select Survey Dataset:")
        self.label_dataset.pack(pady=(15, 3), anchor="w", padx=15)
        self.dataset_var = tb.StringVar()
        self.dataset_dropdown = tb.Combobox(
            self, textvariable=self.dataset_var, bootstyle="info", state="readonly"
        )
        self.dataset_dropdown["values"] = sorted(SURVEYS.keys())
        self.dataset_dropdown.pack(fill="x", padx=15)
        self.dataset_dropdown.bind("<<ComboboxSelected>>", self.on_survey_change)

        # Variable Code
        self.label_var_code = tb.Label(self, text="Variable Code:")
        self.label_var_code.pack(pady=(15, 3), anchor="w", padx=15)
        self.var_code_entry = tb.Entry(self)
        self.var_code_entry.pack(fill="x", padx=15)

        # Variable Name
        self.label_var_name = tb.Label(self, text="Variable Name:")
        self.label_var_name.pack(pady=(15, 3), anchor="w", padx=15)
        self.var_name_entry = tb.Entry(self)
        self.var_name_entry.pack(fill="x", padx=15)

        # Description
        self.label_description = tb.Label(self, text="Description:")
        self.label_description.pack(pady=(15, 3), anchor="w", padx=15)
        self.description_entry = tb.Entry(self)
        self.description_entry.pack(fill="x", padx=15)

        # Variable Type Dropdown (moved before Topic)
        self.label_var_type = tb.Label(self, text="Variable Type:")
        self.label_var_type.pack(pady=(15, 3), anchor="w", padx=15)
        self.var_type_var = tb.StringVar()
        self.var_type_dropdown = tb.Combobox(
            self,
            textvariable=self.var_type_var,
            values=["Indicator", "Demographic"],
            state="readonly",
        )
        self.var_type_dropdown.pack(fill="x", padx=15)
        self.var_type_dropdown.bind("<<ComboboxSelected>>", self.on_vartype_change)

        # Topic Dropdown
        self.label_topic = tb.Label(self, text="Topic:")
        self.label_topic.pack(pady=(15, 3), anchor="w", padx=15)
        self.topic_var = tb.StringVar()
        self.topic_dropdown = tb.Combobox(
            self, textvariable=self.topic_var, state="readonly"
        )
        self.topic_dropdown["values"] = list(TOPICS.keys())
        self.topic_dropdown.pack(fill="x", padx=15)
        self.topic_dropdown.bind("<<ComboboxSelected>>", self.on_topic_change)

        # Subtopic Dropdown
        self.label_subtopic = tb.Label(self, text="Sub-Topic:")
        self.label_subtopic.pack(pady=(15, 3), anchor="w", padx=15)
        self.subtopic_var = tb.StringVar()
        self.subtopic_dropdown = tb.Combobox(
            self, textvariable=self.subtopic_var, state="readonly"
        )
        self.subtopic_dropdown.pack(fill="x", padx=15)

        # Levels Input
        self.label_levels = tb.Label(
            self,
            text="Number of Levels (for variable values):",
        )
        self.label_levels.pack(pady=(15, 3), anchor="w", padx=15)
        self.levels_var = tb.StringVar()
        self.levels_entry = tb.Entry(self, textvariable=self.levels_var)
        self.levels_entry.pack(fill="x", padx=15)

        # Generate Button
        self.generate_btn = tb.Button(
            self, text="Generate SAS Code", bootstyle="success-outline"
        )
        self.generate_btn.pack(pady=20)
        self.generate_btn.configure(command=self.generate_sas)

        # Output SAS Code Preview
        self.output_box = tb.Text(
            self,
            height=15,
            wrap="word",
            font=("Consolas", 11),
            borderwidth=1,
            relief="sunken",
        )
        self.output_box.pack(fill="both", padx=15, pady=(0, 15), expand=True)

        # Set default survey and variable type
        self.dataset_dropdown.current(0)
        self.var_type_dropdown.current(0)
        self.on_survey_change()
        self.on_vartype_change()

    def apply_style_for_survey(self, survey_key):
        style_info = SURVEY_STYLES.get(survey_key, None)
        if not style_info:
            return

        # Window background
        self.configure(background=style_info["bg"])

        # Labels foreground to dark color (black or survey color)
        fg_color = style_info["entry_fg"]
        bg_color = style_info["bg"]

        for widget in self.winfo_children():
            # Set background for Labels
            if isinstance(widget, tb.Label):
                widget.configure(background=bg_color, foreground=fg_color)
            # Set Entry fields
            elif isinstance(widget, tb.Entry):
                widget.configure(background=style_info["entry_bg"], foreground=style_info["entry_fg"])
            # Set Comboboxes background (requires style)
            elif isinstance(widget, tb.Combobox):
                widget.configure(bootstyle="info")
                # We will set a style with custom bg later if needed
            # Buttons style
            elif isinstance(widget, tb.Button):
                widget.configure(bootstyle=style_info["btn_bootstyle"])

        # Output box colors
        self.output_box.configure(
            background=style_info["text_bg"], foreground=style_info["text_fg"]
        )

    def on_survey_change(self, event=None):
        key = self.dataset_var.get()
        if not key:
            return
        self.current_survey_key = key

        # Use ttkbootstrap theme if available
        survey_theme = SURVEYS[key].get("theme", None)
        if survey_theme:
            try:
                self.style.theme_use(survey_theme)
            except Exception:
                pass

        self.population = SURVEYS[key]["population"]

        # Clear Topic and Subtopic selections and values
        self.topic_var.set("")
        self.subtopic_var.set("")
        self.output_box.delete("1.0", "end")
        self.levels_var.set("")

        # Update Topic dropdown bg color reset
        self.update_topic_dropdown_bg(None)

        # Apply dramatic style changes
        self.apply_style_for_survey(key)

    def on_vartype_change(self, event=None):
        vt = self.var_type_var.get()
        if vt == "Demographic":
            # Disable topic and subtopic
            self.topic_dropdown.configure(state="disabled")
            self.subtopic_dropdown.configure(state="disabled")
            # Clear selections
            self.topic_var.set("")
            self.subtopic_var.set("")
            self.update_topic_dropdown_bg(None)
        else:
            # Enable topic and subtopic
            self.topic_dropdown.configure(state="readonly")
            self.subtopic_dropdown.configure(state="readonly")

    def on_topic_change(self, event=None):
        topic = self.topic_var.get()
        if not topic:
            self.subtopic_dropdown["values"] = []
            self.subtopic_var.set("")
            self.update_topic_dropdown_bg(None)
            return
        subtopics = list(TOPICS[topic]["subtopics"].keys())
        self.subtopic_dropdown["values"] = subtopics
        self.subtopic_var.set("")
        self.update_topic_dropdown_bg(TOPICS[topic]["color"])

    def update_topic_dropdown_bg(self, color):
        style_name = "Custom.TCombobox"
        if color:
            self.style.configure(style_name, fieldbackground=color)
        else:
            self.style.configure(style_name, fieldbackground="white")
        self.topic_dropdown.configure(style=style_name)

    def generate_sas(self):
        var_code = self.var_code_entry.get().strip()
        var_name = self.var_name_entry.get().strip()
        description = self.description_entry.get().strip()
        var_type = self.var_type_var.get()
        levels = self.levels_var.get()
        topic = self.topic_var.get()
        subtopic = self.subtopic_var.get()

        # Validation
        if not (var_code and var_name and description and var_type and levels):
            messagebox.showerror(
                "Missing input", "Please fill in all required fields before generating."
            )
            return
        if var_type == "Indicator" and (not topic or not subtopic):
            messagebox.showerror(
                "Missing input", "Please select both Topic and Sub-Topic for Indicators."
            )
            return

        try:
            num_levels = int(levels)
            if num_levels < 1:
                raise ValueError()
        except Exception:
            messagebox.showerror(
                "Invalid input", "Please enter a valid positive integer for number of levels."
            )
            return

        self.output_box.delete("1.0", "end")

        survey_info = SURVEYS[self.current_survey_key]
        dataset_name = survey_info["full_name"]
        population = survey_info["population"]
        tag_suffix = survey_info["tag_suffix"]

        topic_id = TOPICS[topic]["id"] if topic in TOPICS else 0
        subtopic_id = TOPICS[topic]["subtopics"][subtopic] if var_type == "Indicator" and subtopic in TOPICS.get(topic, {}).get("subtopics", {}) else 0

        import tkinter.simpledialog as simpledialog

        var_values = []
        for i in range(1, num_levels + 1):
            val = simpledialog.askstring(
                "Variable Value Input",
                f"Enter Variable Value #{i}:",
                parent=self,
            )
            if val is None or val.strip() == "":
                messagebox.showerror(
                    "Invalid input",
                    "Variable Value cannot be empty. SAS code generation cancelled.",
                )
                return
            var_values.append(val.strip())

        for idx, val in enumerate(var_values, 1):
            sas_code = SAS_TEMPLATE.format(
                varvalid=idx,
                topic_id=topic_id,
                subtopic_id=subtopic_id,
                dataset=self.current_survey_key,
                dataset_name=dataset_name,
                var_code=var_code,
                var_value=val,
                var_type=var_type,
                var_name=var_name,
                description=description,
                topic=topic if var_type == "Indicator" else "",
                sub_topic=subtopic if var_type == "Indicator" else "",
                population=population,
                tag_suffix=tag_suffix,
            )
            self.output_box.insert("end", sas_code + "\n\n")


if __name__ == "__main__":
    app = SASGeneratorApp()
    app.mainloop()
