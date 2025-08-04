import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

# --- SAS template ---
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
PopulationDatasource = "{population_source}";
Note1 = "";
Note2 = "";
Note3 = "";
CrossNotes = "";
MapTitlePrefix = "";
MapTitleSuffix = "";
MapInsert = "";
VarComments = "";
Tag = "{var_name}_{dataset}";
DefaultPopulationSource = "CHS";
output;
run;
"""

# --- Topic/Subtopic Dropdown Options ---
TOPIC_OPTIONS = {
    "Children and Youth": 5,
    "Community Characteristics": 6,
    "Diseases and Conditions": 1,
    "Healthy Living": 4,
    "Health Care Access and Use": 2,
    "Living and Environmental Conditions": 7,
    "Mental Health": 3,
    "Sleep": 33,
    "Smoking": 7,
    "Vaccinations": 29,
    "Violence": 1
}

SUBTOPIC_OPTIONS = {
    "Chronic Disease": 24,
    "Day Care and School": 34,
    "Drug and Alcohol Use": 10,
    "Economic Factors": 31,
    "Health Care Use": 17,
    "Housing": 14,
    "Household and Neighborhood": 16,
    "Mental Health": 3,
    "Mental Health Conditions": 20,
    "Mental Health Counseling and Treatment": 27,
    "Nutrition": 23,
    "Physical Activity": 35,
    "Population Characteristics": 11,
    "Safety": 4,
    "Screening": 19,
    "Sexual Behavior": 30,
    "Smoking": 7,
    "Social Factors": 13,
    "Vaccinations": 29,
    "Violence": 1
}

DATASET_NAMES = {
    "CHS": "NYC Community Health Survey",
    "YRBS": "NYC Youth Risk Behavior Survey"
}

# --- GUI Setup ---
root = tk.Tk()
root.title("SAS Code Generator")

# Set default style
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", font=("Segoe UI", 10), padding=5)
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
style.configure("TEntry", padding=5)
style.configure("TCombobox", padding=5)

main_frame = ttk.Frame(root, padding="15")
main_frame.grid(row=0, column=0)

fields = {}

# --- Input Fields ---
def add_label_entry(row, label, varname):
    ttk.Label(main_frame, text=label).grid(row=row, column=0, sticky="e")
    entry = ttk.Entry(main_frame, width=40)
    entry.grid(row=row, column=1, pady=2, sticky="w")
    fields[varname] = entry

add_label_entry(0, "Variable Code:", "var_code")
add_label_entry(1, "Variable Name:", "var_name")
add_label_entry(2, "Description:", "description")

# --- Topic Dropdown ---
ttk.Label(main_frame, text="Topic:").grid(row=3, column=0, sticky="e")
topic_var = tk.StringVar()
topic_dropdown = ttk.Combobox(main_frame, textvariable=topic_var, values=sorted(TOPIC_OPTIONS.keys()), width=38)
topic_dropdown.grid(row=3, column=1, sticky="w")
fields['topic'] = topic_dropdown

# --- Sub-Topic Dropdown ---
ttk.Label(main_frame, text="Sub-Topic:").grid(row=4, column=0, sticky="e")
subtopic_var = tk.StringVar()
subtopic_dropdown = ttk.Combobox(main_frame, textvariable=subtopic_var, values=sorted(SUBTOPIC_OPTIONS.keys()), width=38)
subtopic_dropdown.grid(row=4, column=1, sticky="w")
fields['sub_topic'] = subtopic_dropdown

# --- VarType Dropdown ---
ttk.Label(main_frame, text="Variable Type:").grid(row=5, column=0, sticky="e")
vartype_var = tk.StringVar()
vartype_dropdown = ttk.Combobox(main_frame, textvariable=vartype_var, values=sorted(["Indicator", "Demographic"]), width=38)
vartype_dropdown.grid(row=5, column=1, sticky="w")
fields['var_type'] = vartype_dropdown

# --- Dataset Dropdown ---
ttk.Label(main_frame, text="Dataset:").grid(row=6, column=0, sticky="e")
dataset_var = tk.StringVar()
dataset_dropdown = ttk.Combobox(main_frame, textvariable=dataset_var, values=sorted(DATASET_NAMES.keys()), width=38)
dataset_dropdown.grid(row=6, column=1, sticky="w")
fields['dataset'] = dataset_dropdown

# --- Output Box ---
output_box = tk.Text(root, width=100, height=25, wrap="word", font=("Courier New", 9))
output_box.grid(row=1, column=0, padx=15, pady=10)

# --- Generate SAS Code ---
def generate_sas():
    try:
        selected_dataset = fields['dataset'].get()
        if selected_dataset not in DATASET_NAMES:
            messagebox.showerror("Error", "Please select a valid dataset.")
            return

        dataset_full_name = DATASET_NAMES[selected_dataset]
        population_source = "Adult" if selected_dataset == "CHS" else "Youth"

        num_levels_str = simpledialog.askstring("Input", "How many levels for this variable (last # of variable code)?", parent=root)
        if not num_levels_str or not num_levels_str.isdigit():
            messagebox.showerror("Error", "Please enter a valid number of levels.")
            return
        num_levels = int(num_levels_str)

        var_values = []
        for i in range(1, num_levels + 1):
            val = simpledialog.askstring("Var Value", f"Enter Variable Value #{i}:", parent=root)
            if val:
                var_values.append(val)

        output_box.delete("1.0", tk.END)

        for i, val in enumerate(var_values):
            sas_code = SAS_TEMPLATE.format(
                varvalid=i + 1,
                topic=fields['topic'].get(),
                sub_topic=fields['sub_topic'].get(),
                topic_id=TOPIC_OPTIONS.get(fields['topic'].get(), 0),
                subtopic_id=SUBTOPIC_OPTIONS.get(fields['sub_topic'].get(), 0),
                var_code=fields['var_code'].get(),
                var_value=val,
                var_type=fields['var_type'].get(),
                var_name=fields['var_name'].get(),
                description=fields['description'].get(),
                dataset=selected_dataset,
                dataset_name=dataset_full_name,
                population_source=population_source
            )
            output_box.insert(tk.END, sas_code + "\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Generate Button ---
ttk.Button(main_frame, text="Generate SAS Code", command=generate_sas).grid(row=7, column=0, columnspan=2, pady=15)

root.mainloop()
