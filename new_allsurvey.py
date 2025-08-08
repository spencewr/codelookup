import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

# --- Topic/Subtopic/ID/Color Data ---
TOPICS = {
    "Birth and Death": {
        "id": 8,
        "color": "#FDD9FF",  # rose
        "subtopics": {
            "Birth": 38,
            "Infant Mortality": 51,
            "Leading Cause of Death": 52,
            "Mortality and Premature Mortality": 49,
        },
    },
    "Children and Youth": {
        "id": 5,
        "color": "#FFD9E8",  # pink
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
    "Community Characteristics": {
        "id": 6,
        "color": "#D9E8FF",  # blue
        "subtopics": {
            "Day Care and School": 34,
            "Economic Factors": 31,
            "Population Characteristics": 11,
            "Social Factors": 13,
        },
    },
    "Diseases and Conditions": {
        "id": 1,
        "color": "#FFE6CC",  # peach
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
        "color": "#CCFFF5",  # aqua
        "subtopics": {
            "Health Care Use": 17,
            "Health Insurance": 15,
            "Mental Health Counseling and Treatment": 27,
            "Screening": 19,
            "Vaccinations": 29,
        },
    },
    "Healthy Living": {
        "id": 4,
        "color": "#D9FFD9",  # mint
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
    "Living and Environmental Conditions": {
        "id": 7,
        "color": "#FFF5CC",  # yellow
        "subtopics": {
            "Built Environment": 28,
            "Housing": 14,
        },
    },
    "Mental Health": {
        "id": 3,
        "color": "#E6D9FF",  # lavender
        "subtopics": {
            "Drug and Alcohol Use": 10,
            "Mental Health Conditions": 20,
            "Mental Health Counseling and Treatment": 27,
        },
    },
}

# --- Survey Info ---
SURVEYS = {
    "YRBS": {
        "full_name": "NYC Youth Risk Behavior Survey",
        "population": "Youth",
        "tag_suffix": "_YRBS",
        "theme": "superhero",
    },
    "CHS": {
        "full_name": "NYC Community Health Survey",
        "population": "Adult",
        "tag_suffix": "_CHS",
        "theme": "flatly",
    },
    "HANES": {
        "full_name": "NYC Health and Nutrition Examination Survey",
        "population": "Adult",
        "tag_suffix": "_HANES",
        "theme": "cosmo",
    },
    "CCHS": {
        "full_name": "NYC Child Health Data",
        "population": "Youth",
        "tag_suffix": "_CCHS",
        "theme": "minty",
    },
}

# --- SAS Template ---
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
Tag = "{var_name}{tag_suffix}";
DefaultPopulationSource = "{population}";
output;
run;
"""

def alphabetize_dict(d):
    return dict(sorted(d.items(), key=lambda item: item[0].lower()))

TOPICS = alphabetize_dict(TOPICS)
for topic in TOPICS:
    TOPICS[topic]["subtopics"] = alphabetize_dict(TOPICS[topic]["subtopics"])

class SASGeneratorApp(tb.Window):
    def __init__(self):
        super().__init__(title="SAS Code Generator", size=(900, 650))
        self.geometry("900x650")

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

    def on_survey_change(self, event=None):
        key = self.dataset_var.get()
        if not key:
            return
        self.current_survey_key = key
        survey_info = SURVEYS[key]

        try:
            self.style.theme_use(survey_info["theme"])
        except Exception:
            pass

        self.population = survey_info["population"]

        # Reset topic and subtopic
        self.topic_var.set("")
        self.subtopic_var.set("")
        self.output_box.delete("1.0", "end")
        self.levels_var.set("")

        # Reset topic dropdown bg color
        self.update_topic_dropdown_bg(None)

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
