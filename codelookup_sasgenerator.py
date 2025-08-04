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
Dataset = "YRBS";
Dataset_Name = "NYC Youth Risk Behavior Survey";
Dataset_Type = "Health Surveys";
VarCode = "{var_code}";
VarValue = "{var_value}";
VarType = "{var_type}";
VarName = "{var_name}";
Description = "{description}";
Topic = "{topic}";
Sub_Topic = "{sub_topic}";
PopulationDatasource = "Youth";
Note1 = "";
Note2 = "";
Note3 = "";
CrossNotes = "";
MapTitlePrefix = "";
MapTitleSuffix = "";
MapInsert = "";
VarComments = "";
Tag = "{var_name}_YRBS";
DefaultPopulationSource = "CHS";
output;
run;
"""

# --- Topic/Subtopic Dropdown Options ---
TOPIC_OPTIONS = {
    "Children and Youth": 5,
    "Healthy Living": 4,
    "Sleep": 33,
    "Smoking": 7,
    "Vaccinations": 29,
    "Violence": 1,
    "Community Characteristics": 6,
    "Living and Environmental Conditions": 7,
    "Mental Health": 3,
    "Diseases and Conditions": 1,
    "Health Care Access and Use": 2
}

SUBTOPIC_OPTIONS = {
    "Drug and Alcohol Use": 10,
    "Household and Neighborhood": 16,
    "Mental Health": 3,
    "Mental Health Conditions": 20,
    "Mental Health Counseling and Treatment": 27,
    "Nutrition": 23,
    "Physical Activity": 35,
    "Population Characteristics": 11,
    "Safety": 4,
    "Sexual Behavior": 30,
    "Smoking": 7,
    "Violence": 1,
    "Day Care and School": 34,
    "Economic Factors": 31,
    "Social Factors": 13,
    "Housing": 14,
    "Chronic Disease": 24,
    "Health Care Use": 17,
    "Screening": 19,
    "Vaccinations": 29
}

# --- GUI Setup ---
root = tk.Tk()
root.title("SAS Code Generator")

fields = {}

# --- Input Fields ---
def add_label_entry(row, label, varname):
    tk.Label(root, text=label).grid(row=row, column=0, sticky="e")
    entry = tk.Entry(root, width=40)
    entry.grid(row=row, column=1, pady=2, sticky="w")
    fields[varname] = entry

add_label_entry(0, "Variable Code:", "var_code")
add_label_entry(1, "Variable Name:", "var_name")
add_label_entry(2, "Description:", "description")

# --- dropdowns ---
tk.Label(root, text="Topic:").grid(row=3, column=0, sticky="e")
topic_var = tk.StringVar()
topic_dropdown = ttk.Combobox(root, textvariable=topic_var, values=list(TOPIC_OPTIONS.keys()))
topic_dropdown.grid(row=3, column=1, sticky="w")
fields['topic'] = topic_dropdown

tk.Label(root, text="Sub-Topic:").grid(row=4, column=0, sticky="e")
subtopic_var = tk.StringVar()
subtopic_dropdown = ttk.Combobox(root, textvariable=subtopic_var, values=list(SUBTOPIC_OPTIONS.keys()))
subtopic_dropdown.grid(row=4, column=1, sticky="w")
fields['sub_topic'] = subtopic_dropdown

# --- VarType Dropdown ---
tk.Label(root, text="Variable Type:").grid(row=5, column=0, sticky="e")
vartype_var = tk.StringVar()
vartype_dropdown = ttk.Combobox(root, textvariable=vartype_var, values=["Indicator", "Demographic"])
vartype_dropdown.grid(row=5, column=1, sticky="w")
fields['var_type'] = vartype_dropdown

# --- Output Box ---
output_box = tk.Text(root, width=90, height=25, wrap="word")
output_box.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# --- Generate SAS Code ---
def generate_sas():
    try:
        num_levels = int(simpledialog.askstring("Input", "How many levels for this variable (last # of variable code)?", parent=root))
        var_values = []
        for i in range(1, num_levels + 1):
            val = simpledialog.askstring("Var Value", f"Enter Variable Value #{i}:", parent=root)
            var_values.append(val)

        # Clear the output box
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
                description=fields['description'].get()
            )
            output_box.insert(tk.END, sas_code + "\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Button ---
tk.Button(root, text="Generate SAS Code", command=generate_sas).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
