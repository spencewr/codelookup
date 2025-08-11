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

TOPICS = {
    "Children and Youth": {
        "id": 5,
        "subtopics": {
            "Child Development and Disabilities": 26,
            "Day Care and School": 34,
            "Drug and Alcohol Use": 10,
            "Health Care Use": 17,
            "Health Insurance": 15,
            "Household and Neighborhood": 16,
            "Health Status": 18,
            "Mental Health": 3,
            "Nutrition": 23,
            "Physical Activity": 35,
            "Physical Health Conditions": 12,
            "Population Characteristics": 11,
            "Safety": 4,
            "Sleep": 33,
            "Sexual Behavior": 30,
            "Smoking": 7,
            "Violence": 1,
        },
    },
    "Healthy Living": {
        "id": 4,
        "subtopics": {
            "Vaccinations": 29,
            "Drug and Alcohol Use": 10,
            "Health Status": 18,
            "Nutrition": 23,
            "Physical Activity": 35,
            "Safety": 4,
            "Screening": 19,
            "Sexual Behavior": 30,
        },
    },
    "Sleep": {"id": 33, "subtopics": {}},
    "Smoking": {"id": 7, "subtopics": {}},
    "Vaccinations": {"id": 29, "subtopics": {}},
    "Violence": {"id": 1, "subtopics": {}},
    "Community Characteristics": {
        "id": 6,
        "subtopics": {
            "Day Care and School": 34,
            "Economic Factors": 31,
            "Population Characteristics": 11,
            "Social Factors": 13,
        },
    },
    "Living and Environmental Conditions": {
        "id": 7,
        "subtopics": {
            "Built Environment": 28,
            "Housing": 14,
        },
    },
    "Safety": {"id": 4, "subtopics": {}},
    "Social Factors": {"id": 13, "subtopics": {}},
    "Mental Health": {
        "id": 3,
        "subtopics": {
            "Drug and Alcohol Use": 10,
            "Mental Health Conditions": 20,
            "Mental Health Counseling and Treatment": 27,
        },
    },
    "Diseases and Conditions": {
        "id": 1,
        "subtopics": {
            "Child Development and Disabilities": 26,
            "Chronic Diseases": 24,
            "Dental Health": 21,
            "Foodborne or Waterborne Infections": 43,
            "HIV-AIDS": 8,
            "Hearing and Vision Health": 36,
            "Hepatitis Infections": 48,
            "Invasive Bacterial Infections": 45,
            "Mosquitoborne Infections": 37,
            "Other and Rare Diseases": 46,
            "Person-to-Person Infections": 44,
            "Respiratory Infections": 41,
            "Sexually Transmitted Infections": 5,
            "Syndromic Surveillance": 39,
            "Tickborne Infections": 42,
            "Tuberculosis": 53,
            "Vaccine-Preventable Diseases": 47,
            "Zoonotic Infections": 40,
        },
    },
    "Health Care Access and Use": {
        "id": 2,
        "subtopics": {
            "Health Care Use": 17,
            "Health Insurance": 15,
            "Mental Health Counseling and Treatment": 27,
            "Screening": 19,
            "Vaccinations": 29,
        },
    },
    "Birth and Death": {
        "id": 8,
        "subtopics": {
            "Birth": 38,
            "Infant Mortality": 51,
            "Leading Cause of Death": 52,
            "Mortality and Premature Mortality": 49,
        },
    },
}

SURVEYS = {
    "YRBS": {
        "full_name": "NYC Youth Risk Behavior Survey",
        "population": "Youth",
        "tag_suffix": "YRBS",
    },
    "CHS": {
        "full_name": "Community Health Survey",
        "population": "Adult",
        "tag_suffix": "CHS",
    },
    "HANES": {
        "full_name": "NYC Health and Nutrition Examination Survey",
        "population": "Adult",
        "tag_suffix": "HANES",
    },
    "CCHS": {
        "full_name": "NYC Child Health Data",
        "population": "Youth",
        "tag_suffix": "CCHS",
    },
}


class SASGeneratorApp(tb.Window):
    def __init__(self):
        super().__init__(title="SAS Code Generator", size=(900, 750))

        self.variables = []  # List to store multiple variables info
        self.current_var_index = -1

        # === Dataset selection ===
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

        # Variable Type (Indicator/Demographic)
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

        # Number of Levels dropdown (2-6)
        tb.Label(self, text="Number of Levels:").pack(pady=(15, 3), anchor="w", padx=15)
        self.levels_var = tb.StringVar()
        self.levels_dropdown = tb.Combobox(self, textvariable=self.levels_var, state="readonly")
        self.levels_dropdown["values"] = [str(i) for i in range(2, 7)]
        self.levels_dropdown.pack(fill="x", padx=15)
        self.levels_dropdown.bind("<<ComboboxSelected>>", self.on_levels_change)

        # Frame to hold level name entry fields
        self.level_names_frame = tb.Frame(self)
        self.level_names_frame.pack(fill="x", padx=15, pady=(5, 15))
        self.level_name_entries = []

        # Navigation Frame with Previous / Next variable and Add Variable buttons
        nav_frame = tb.Frame(self)
        nav_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.prev_btn = tb.Button(nav_frame, text="← Previous Variable", command=self.prev_variable)
        self.prev_btn.pack(side="left")

        self.next_btn = tb.Button(nav_frame, text="Next Variable →", command=self.next_variable)
        self.next_btn.pack(side="left", padx=10)

        self.add_var_btn = tb.Button(
            nav_frame, text="Add Another Variable", bootstyle="primary", command=self.add_variable
        )
        self.add_var_btn.pack(side="right")

        self.delete_var_btn = tb.Button(
            nav_frame, text="Delete Current Variable", bootstyle="danger", command=self.delete_variable
        )
        self.delete_var_btn.pack(side="right", padx=(0, 10))

        # Generate SAS Code button (green)
        self.generate_btn = tb.Button(
            self, text="Generate SAS Code", bootstyle="success", command=self.generate_sas_code
        )
        self.generate_btn.pack(pady=(0, 15))

        # Footer label
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
        self.load_variable(0)
        self.update_nav_buttons()

    # === Event Handlers ===

    def on_survey_change(self, event=None):
        self.topic_var.set("")
        self.subtopic_var.set("")

    def on_vartype_change(self, event=None):
        vt = self.var_type_var.get()
        if vt == "Demographic":
            self.topic_dropdown.configure(state="disabled")
            self.subtopic_dropdown.configure(state="disabled")
            self.topic_var.set("")
            self.subtopic_var.set("")
        else:
            self.topic_dropdown.configure(state="readonly")
            self.subtopic_dropdown.configure(state="readonly")

    def on_topic_change(self, event=None):
        topic = self.topic_var.get()
        if not topic:
            self.subtopic_dropdown["values"] = []
            self.subtopic_var.set("")
            return
        subtopics = sorted(TOPICS[topic]["subtopics"].keys())
        self.subtopic_dropdown["values"] = subtopics
        self.subtopic_var.set("")

    def on_levels_change(self, event=None):
        for widget in self.level_names_frame.winfo_children():
            widget.destroy()
        self.level_name_entries.clear()

        try:
            n_levels = int(self.levels_var.get())
        except Exception:
            return

        for i in range(n_levels):
            label = tb.Label(self.level_names_frame, text=f"Level {i+1} Name:")
            label.grid(row=i, column=0, sticky="w", pady=2, padx=5)
            entry = tb.Entry(self.level_names_frame)
            entry.grid(row=i, column=1, sticky="ew", pady=2, padx=5)
            self.level_name_entries.append(entry)

        self.level_names_frame.columnconfigure(1, weight=1)

    # === Variable Data Management ===

    def save_current_variable(self):
        if not self.dataset_var.get():
            messagebox.showerror("Error", "Please select a Survey Dataset.")
            return False
        if not self.var_code_entry.get().strip():
            messagebox.showerror("Error", "Please enter Variable Code.")
            return False
        if not self.var_name_entry.get().strip():
            messagebox.showerror("Error", "Please enter Variable Name.")
            return False
        if not self.description_entry.get().strip():
            messagebox.showerror("Error", "Please enter Description.")
            return False
        if not self.var_type_var.get():
            messagebox.showerror("Error", "Please select Variable Type.")
            return False
        if self.var_type_var.get() == "Indicator":
            if not self.topic_var.get() or not self.subtopic_var.get():
                messagebox.showerror("Error", "Please select Topic and Sub-Topic for Indicators.")
                return False
        if not self.levels_var.get():
            messagebox.showerror("Error", "Please select Number of Levels.")
            return False
        for idx, entry in enumerate(self.level_name_entries, start=1):
            if not entry.get().strip():
                messagebox.showerror("Error", f"Please enter a name for Level {idx}.")
                return False

        data = {
            "dataset": self.dataset_var.get(),
            "dataset_name": SURVEYS[self.dataset_var.get()]["full_name"],
            "population": SURVEYS[self.dataset_var.get()]["population"],
            "tag_suffix": SURVEYS[self.dataset_var.get()]["tag_suffix"],
            "var_code": self.var_code_entry.get().strip(),
            "var_name": self.var_name_entry.get().strip(),
            "description": self.description_entry.get().strip(),
            "var_type": self.var_type_var.get(),
            "topic": self.topic_var.get() if self.var_type_var.get() == "Indicator" else "",
            "sub_topic": self.subtopic_var.get() if self.var_type_var.get() == "Indicator" else "",
            "topic_id": TOPICS[self.topic_var.get()]["id"] if self.topic_var.get() in TOPICS else 0,
            "subtopic_id": (
                TOPICS[self.topic_var.get()]["subtopics"][self.subtopic_var.get()]
                if self.var_type_var.get() == "Indicator"
                and self.subtopic_var.get() in TOPICS.get(self.topic_var.get(), {}).get("subtopics", {})
                else 0
            ),
            "levels": [entry.get().strip() for entry in self.level_name_entries],
        }

        if 0 <= self.current_var_index < len(self.variables):
            self.variables[self.current_var_index] = data
        else:
            self.variables.append(data)
            self.current_var_index = len(self.variables) - 1

        return True

    def load_variable(self, index):
        if not self.variables or index < 0 or index >= len(self.variables):
            # Clear form if out of range
            self.clear_form()
            self.current_var_index = -1
            self.update_nav_buttons()
            return

        self.current_var_index = index
        var_data = self.variables[index]

        self.dataset_var.set(var_data["dataset"])
        self.var_code_entry.delete(0, "end")
        self.var_code_entry.insert(0, var_data["var_code"])

        self.var_name_entry.delete(0, "end")
        self.var_name_entry.insert(0, var_data["var_name"])

        self.description_entry.delete(0, "end")
        self.description_entry.insert(0, var_data["description"])

        self.var_type_var.set(var_data["var_type"])
        self.on_vartype_change()

        self.topic_var.set(var_data["topic"])
        self.on_topic_change()

        self.subtopic_var.set(var_data["sub_topic"])

        self.levels_var.set(str(len(var_data["levels"])))
        self.on_levels_change()

        for entry, val in zip(self.level_name_entries, var_data["levels"]):
            entry.delete(0, "end")
            entry.insert(0, val)

        self.update_nav_buttons()

    def clear_form(self):
        self.dataset_var.set("")
        self.var_code_entry.delete(0, "end")
        self.var_name_entry.delete(0, "end")
        self.description_entry.delete(0, "end")
        self.var_type_var.set("")
        self.topic_var.set("")
        self.subtopic_var.set("")
        self.subtopic_dropdown["values"] = []
        self.levels_var.set("")
        self.on_levels_change()
        self.update_nav_buttons()

    # === Navigation ===

    def prev_variable(self):
        if self.current_var_index > 0:
            if not self.save_current_variable():
                return
            self.load_variable(self.current_var_index - 1)

    def next_variable(self):
        if self.current_var_index < len(self.variables) - 1:
            if not self.save_current_variable():
                return
            self.load_variable(self.current_var_index + 1)

    def add_variable(self):
        if not self.save_current_variable():
            return
        # Clear form for new variable input
        self.current_var_index = len(self.variables)
        self.clear_form()
        # Enable delete if at least one variable already exists
        if self.variables:
            self.delete_var_btn.configure(state="normal")

    def update_nav_buttons(self):
        self.prev_btn.configure(state="normal" if self.current_var_index > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.current_var_index < len(self.variables) - 1 else "disabled")
        # Allow delete if we have any saved variables OR we're currently editing a variable
        self.delete_var_btn.configure(
            state="normal" if self.variables or self.current_var_index >= 0 else "disabled"
        )

    def delete_variable(self):
        # Case 1: No saved variables yet — just clear the form
        if not self.variables:
            if (
                self.var_code_entry.get().strip()
                or self.var_name_entry.get().strip()
                or self.description_entry.get().strip()
            ):
                result = messagebox.askyesno(
                    "Clear Form",
                    "No variables saved yet.\nClear the current form?"
                )
                if not result:
                    return
            self.clear_form()
            self.current_var_index = -1
            self.update_nav_buttons()
            return

        # Case 2: We have saved variables, but index is invalid
        if self.current_var_index < 0 or self.current_var_index >= len(self.variables):
            messagebox.showwarning("Warning", "No current variable selected to delete.")
            return

        # Normal delete process
        var_name = self.variables[self.current_var_index].get("var_name", "Unknown")
        result = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete variable '{var_name}'?\n\nThis action cannot be undone."
        )
        if not result:
            return

        del self.variables[self.current_var_index]

        if not self.variables:
            self.current_var_index = -1
            self.clear_form()
        elif self.current_var_index >= len(self.variables):
            self.current_var_index = len(self.variables) - 1
            self.load_variable(self.current_var_index)
        else:
            self.load_variable(self.current_var_index)

        self.update_nav_buttons()
        messagebox.showinfo("Success", f"Variable '{var_name}' has been deleted.")

    # === Generate SAS code ===

    def generate_sas_code(self):
        if not self.save_current_variable():
            return
        if not self.variables:
            messagebox.showerror("Error", "No variables to generate SAS code.")
            return

        sas_code_parts = []

        for var_data in self.variables:
            for idx, val in enumerate(var_data["levels"], start=1):
                sas_code_parts.append(
                    SAS_TEMPLATE.format(
                        varvalid=idx,
                        topic_id=var_data["topic_id"],
                        subtopic_id=var_data["subtopic_id"],
                        dataset=var_data["dataset"],
                        dataset_name=var_data["dataset_name"],
                        var_code=var_data["var_code"],
                        var_value=val,
                        var_type=var_data["var_type"],
                        var_name=var_data["var_name"],
                        description=var_data["description"],
                        topic=var_data["topic"],
                        sub_topic=var_data["sub_topic"],
                        population=var_data["population"],
                        tag_suffix=var_data["tag_suffix"],
                    )
                )
                sas_code_parts.append("")  # blank line between entries

        full_code = "\n".join(sas_code_parts)
        self.show_output_popup(full_code)

    # === Popup for SAS output ===

    def show_output_popup(self, sas_code):
        popup = tk.Toplevel(self)
        popup.title("Generated SAS Code")
        popup.geometry("850x650")

        text = tk.Text(popup, wrap="word", font=("Consolas", 11))
        text.insert("1.0", sas_code)
        text.configure(state="disabled")  # read-only
        text.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(popup, command=text.yview)
        scrollbar.pack(side="right", fill="y")
        text.config(yscrollcommand=scrollbar.set)


if __name__ == "__main__":
    app = SASGeneratorApp()
    app.mainloop()
