import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

SAS_TEMPLATE = """
/* {var_value} */
data new_varxx;
YearNum = 2023;
VarValID = {varvalid};
Topic_ID = {topic_id};
SubTopic_ID = {subtopic_id};
ExcludeInclude = 1;
SortOrder = 1;
Topic_SortOrder = 1;
SubTopic_SortOrder = 1;
Topic_DefaultID = 1;
DefaultID = 1;
Indicator_SortOrder = ;
YearDate = "2023-01-01";
Dataset = "{dataset}";
Dataset_Name = "{dataset_name}";
Dataset_Type = "Health Surveys";
VarCode = "{var_code}";
VarValue = "{var_value}";
VarType = "{var_type}";
VarName = "{var_name}";
Description = "{description}";
Topic = "{topic}";
Sub_Topic = "{sub_topic}";
PopulationDatasource = "{population}";
Note1 = "";
Note2 = "";
Note3 = "";
CrossNotes = "";
MapTitlePrefix = "";
MapTitleSuffix = "";
MapInsert = "";
VarComments = "";
Tag = "{var_name}_{tag_suffix}";
DefaultPopulationSource = "{population}";
output;
run;
"""

# Your TOPICS and SURVEYS dictionaries here (unchanged)...

class SASGeneratorApp(tb.Window):
    def __init__(self):
        super().__init__(title="SAS Code Generator", size=(900, 700))

        self.current_survey_key = None
        self.variables_data = []  # list of dicts for each variable
        self.current_index = 0

        # Dataset selection
        tb.Label(self, text="Select Survey Dataset:").pack(pady=(15, 3), anchor="w", padx=15)
        self.dataset_var = tb.StringVar()
        self.dataset_dropdown = tb.Combobox(self, textvariable=self.dataset_var, state="readonly")
        self.dataset_dropdown["values"] = sorted(SURVEYS.keys())
        self.dataset_dropdown.pack(fill="x", padx=15)
        self.dataset_dropdown.bind("<<ComboboxSelected>>", self.on_survey_change)

        # Variable Code
        tb.Label(self, text="Variable Code:").pack(pady=(15, 3), anchor="w", padx=15)
        self.var_code_entry = tb.Entry(self)
        self.var_code_entry.pack(fill="x", padx=15)

        # Variable Name
        tb.Label(self, text="Variable Name:").pack(pady=(15, 3), anchor="w", padx=15)
        self.var_name_entry = tb.Entry(self)
        self.var_name_entry.pack(fill="x", padx=15)

        # Description
        tb.Label(self, text="Description:").pack(pady=(15, 3), anchor="w", padx=15)
        self.description_entry = tb.Entry(self)
        self.description_entry.pack(fill="x", padx=15)

        # Variable Type
        tb.Label(self, text="Variable Type:").pack(pady=(15, 3), anchor="w", padx=15)
        self.var_type_var = tb.StringVar()
        self.var_type_dropdown = tb.Combobox(
            self, textvariable=self.var_type_var, values=["Indicator", "Demographic"], state="readonly"
        )
        self.var_type_dropdown.pack(fill="x", padx=15)
        self.var_type_dropdown.bind("<<ComboboxSelected>>", self.on_vartype_change)

        # Topic dropdown
        tb.Label(self, text="Topic:").pack(pady=(15, 3), anchor="w", padx=15)
        self.topic_var = tb.StringVar()
        self.topic_dropdown = tb.Combobox(
            self, textvariable=self.topic_var, values=sorted(TOPICS.keys()), state="readonly"
        )
        self.topic_dropdown.pack(fill="x", padx=15)
        self.topic_dropdown.bind("<<ComboboxSelected>>", self.on_topic_change)

        # Subtopic dropdown
        tb.Label(self, text="Sub-Topic:").pack(pady=(15, 3), anchor="w", padx=15)
        self.subtopic_var = tb.StringVar()
        self.subtopic_dropdown = tb.Combobox(self, textvariable=self.subtopic_var, state="readonly")
        self.subtopic_dropdown.pack(fill="x", padx=15)

        # Number of levels dropdown
        tb.Label(self, text="Number of Levels:").pack(pady=(15, 3), anchor="w", padx=15)
        self.levels_var = tb.StringVar()
        self.levels_dropdown = tb.Combobox(
            self, textvariable=self.levels_var, values=[str(i) for i in range(2, 7)], state="readonly"
        )
        self.levels_dropdown.pack(fill="x", padx=15)
        self.levels_dropdown.bind("<<ComboboxSelected>>", self.populate_level_entries)

        # Frame for dynamic level entries
        self.levels_frame = tb.Frame(self)
        self.levels_frame.pack(fill="x", padx=15, pady=5)

        # Navigation + Buttons Frame
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=10, fill="x")

        self.prev_btn = tb.Button(btn_frame, text="← Previous", command=self.prev_variable, bootstyle="secondary")
        self.prev_btn.pack(side="left", padx=5)

        self.add_btn = tb.Button(btn_frame, text="Add Another Variable", command=self.add_variable, bootstyle="primary")
        self.add_btn.pack(side="left", padx=5)

        self.next_btn = tb.Button(btn_frame, text="Next →", command=self.next_variable, bootstyle="secondary")
        self.next_btn.pack(side="left", padx=5)

        self.generate_btn = tb.Button(btn_frame, text="Generate SAS Code", command=self.generate_all_sas, bootstyle="success")
        self.generate_btn.pack(side="right", padx=5)

        # Footer
        self.footer_label = tb.Label(
            self,
            text="Made by Spencer Riddell, August 2025",
            font=("Segoe UI", 8),
            foreground="#666666",
        )
        self.footer_label.pack(side="bottom", pady=5)

        # Initialize defaults
        self.dataset_dropdown.current(0)
        self.var_type_dropdown.current(0)
        self.on_survey_change()
        self.on_vartype_change()
        self.new_variable_form()

    def on_survey_change(self, event=None):
        self.current_survey_key = self.dataset_var.get()
        self.topic_var.set("")
        self.subtopic_var.set("")

    def on_vartype_change(self, event=None):
        if self.var_type_var.get() == "Demographic":
            self.topic_dropdown.configure(state="disabled")
            self.subtopic_dropdown.configure(state="disabled")
            self.topic_var.set("")
            self.subtopic_var.set("")
        else:
            self.topic_dropdown.configure(state="readonly")
            self.subtopic_dropdown.configure(state="readonly")

    def on_topic_change(self, event=None):
        topic = self.topic_var.get()
        subtopics = sorted(TOPICS.get(topic, {}).get("subtopics", {}).keys())
        self.subtopic_dropdown["values"] = subtopics
        self.subtopic_var.set("")

    def populate_level_entries(self, event=None):
        for widget in self.levels_frame.winfo_children():
            widget.destroy()
        try:
            count = int(self.levels_var.get())
        except:
            return
        self.level_entries = []
        for i in range(1, count + 1):
            lbl = tb.Label(self.levels_frame, text=f"Variable Value #{i}:")
            lbl.pack(anchor="w")
            entry = tb.Entry(self.levels_frame)
            entry.pack(fill="x", pady=2)
            self.level_entries.append(entry)

    def save_current_variable(self):
        """Save current form data to variables_data"""
        if len(self.variables_data) <= self.current_index:
            self.variables_data.append({})
        var_data = {
            "dataset": self.current_survey_key,
            "var_code": self.var_code_entry.get().strip(),
            "var_name": self.var_name_entry.get().strip(),
            "description": self.description_entry.get().strip(),
            "var_type": self.var_type_var.get(),
            "topic": self.topic_var.get(),
            "subtopic": self.subtopic_var.get(),
            "levels": [e.get().strip() for e in getattr(self, "level_entries", [])],
        }
        self.variables_data[self.current_index] = var_data

    def load_variable_form(self, index):
        """Load data from variables_data[index] into form"""
        var_data = self.variables_data[index]
        self.dataset_var.set(var_data.get("dataset", ""))
        self.on_survey_change()
        self.var_code_entry.delete(0, "end")
        self.var_code_entry.insert(0, var_data.get("var_code", ""))
        self.var_name_entry.delete(0, "end")
        self.var_name_entry.insert(0, var_data.get("var_name", ""))
        self.description_entry.delete(0, "end")
        self.description_entry.insert(0, var_data.get("description", ""))
        self.var_type_var.set(var_data.get("var_type", "Indicator"))
        self.on_vartype_change()
        self.topic_var.set(var_data.get("topic", ""))
        self.on_topic_change()
        self.subtopic_var.set(var_data.get("subtopic", ""))
        self.levels_var.set(str(len(var_data.get("levels", []))) if var_data.get("levels") else "")
        self.populate_level_entries()
        for entry, value in zip(getattr(self, "level_entries", []), var_data.get("levels", [])):
            entry.delete(0, "end")
            entry.insert(0, value)

    def new_variable_form(self):
        self.var_code_entry.delete(0, "end")
        self.var_name_entry.delete(0, "end")
        self.description_entry.delete(0, "end")
        self.var_type_var.set("Indicator")
        self.on_vartype_change()
        self.topic_var.set("")
        self.subtopic_var.set("")
        self.levels_var.set("")
        self.populate_level_entries()

    def add_variable(self):
        self.save_current_variable()
        self.current_index = len(self.variables_data)
        self.new_variable_form()

    def prev_variable(self):
        if self.current_index > 0:
            self.save_current_variable()
            self.current_index -= 1
            self.load_variable_form(self.current_index)

    def next_variable(self):
        if self.current_index < len(self.variables_data) - 1:
            self.save_current_variable()
            self.current_index += 1
            self.load_variable_form(self.current_index)

    def generate_all_sas(self):
        self.save_current_variable()
        sas_code_str = ""
        for var in self.variables_data:
            if not var.get("var_code") or not var.get("var_name") or not var.get("description") or not var.get("levels"):
                continue
            survey_info = SURVEYS.get(var["dataset"], {})
            topic_id = TOPICS[var["topic"]]["id"] if var["topic"] in TOPICS else 0
            subtopic_id = (
                TOPICS[var["topic"]]["subtopics"].get(var["subtopic"], 0)
                if var["var_type"] == "Indicator" else 0
            )
            for idx, val in enumerate(var["levels"], 1):
                sas_code_str += SAS_TEMPLATE.format(
                    varvalid=idx,
                    topic_id=topic_id,
                    subtopic_id=subtopic_id,
                    dataset=var["dataset"],
                    dataset_name=survey_info.get("full_name", ""),
                    var_code=var["var_code"],
                    var_value=val,
                    var_type=var["var_type"],
                    var_name=var["var_name"],
                    description=var["description"],
                    topic=var["topic"] if var["var_type"] == "Indicator" else "",
                    sub_topic=var["subtopic"] if var["var_type"] == "Indicator" else "",
                    population=survey_info.get("population", ""),
                    tag_suffix=survey_info.get("tag_suffix", ""),
                ) + "\n\n"
        self.show_output_popup(sas_code_str)

    def show_output_popup(self, sas_code):
        popup = tk.Toplevel(self)
        popup.title("Generated SAS Code")
        popup.geometry("800x600")
        text = tk.Text(popup, wrap="word", font=("Consolas", 11))
        text.insert("1.0", sas_code)
        text.configure(state="disabled")
        text.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(popup, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)


if __name__ == "__main__":
    app = SASGeneratorApp()
    app.mainloop()
