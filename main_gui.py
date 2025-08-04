import tkinter as tk
from tkinter import ttk, scrolledtext

# Topic and Subtopic ID mappings
TOPIC_IDS = {
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

SUBTOPIC_IDS = {
    "Drug and Alcohol Use": 10,
    "Household and Neighborhood": 16,
    "Mental Health": 3,
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
    "Mental Health Conditions": 20,
    "Mental Health Counseling and Treatment": 27,
    "Chronic Disease": 24,
    "Health Care Use": 17,
    "Screening": 19,
    "Vaccinations": 29
}

def generate_sas_code():
    topic = topic_var.get()
    sub_topic = subtopic_var.get()
    varcode = varcode_entry.get()
    varvalue = varvalue_entry.get()
    vartype = vartype_entry.get()
    varname = varname_entry.get()
    description = description_entry.get()

    topic_id = TOPIC_IDS.get(topic, "")
    subtopic_id = SUBTOPIC_IDS.get(sub_topic, "")
    tag = f")_YRBS {varname}"

    sas_code = f"""
data new_varxx;
    YearNum = 2023;
    VarValID = 1;
    Topic_ID = {topic_id};
    SubTopic_ID = {subtopic_id};
    ExcludeInclude = 1;
    SortOrder = 1;
    Topic_SortOrder = 1;
    SubTopic_SortOrder = 1;
    Topic_DefaultID = 1;
    DefaultID = 1;
    Indicator_SortOrder = .;
    YearDate = "2023-01-01";
    Dataset = "YRBS";
    Dataset_Name = "NYC Youth Risk Behavior Survey";
    Dataset_Type = "Health Surveys";
    VarCode = "{varcode}";
    VarValue = "{varvalue}";
    VarType = "{vartype}";
    VarName = "{varname}";
    Description = "{description}";
    Topic = "{topic}";
    Sub_Topic = "{sub_topic}";
    PopulationDatasource = "Youth";
    Note1 = "  ";
    Note2 = "  ";
    Note3 = "  ";
    CrossNotes = "  ";
    MapTitlePrefix = "  ";
    MapTitleSuffix = "  ";
    MapInsert = "  ";
    VarComments = "  ";
    Tag = "{tag}";
    DefaultPopulationSource = "CHS";
    output;
    /*output 1 record*/
run;
""".strip()

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, sas_code)

# GUI setup
root = tk.Tk()
root.title("SAS Code Generator")

# Fields
tk.Label(root, text="Topic:").grid(row=0, column=0, sticky="e")
topic_var = tk.StringVar()
topic_dropdown = ttk.Combobox(root, textvariable=topic_var, values=list(TOPIC_IDS.keys()), width=40)
topic_dropdown.grid(row=0, column=1)

tk.Label(root, text="Sub_Topic:").grid(row=1, column=0, sticky="e")
subtopic_var = tk.StringVar()
subtopic_dropdown = ttk.Combobox(root, textvariable=subtopic_var, values=list(SUBTOPIC_IDS.keys()), width=40)
subtopic_dropdown.grid(row=1, column=1)

def add_text_field(label, row):
    tk.Label(root, text=f"{label}:").grid(row=row, column=0, sticky="e")
    entry = tk.Entry(root, width=50)
    entry.grid(row=row, column=1)
    return entry

varcode_entry = add_text_field("VarCode", 2)
varvalue_entry = add_text_field("VarValue", 3)
vartype_entry = add_text_field("VarType", 4)
varname_entry = add_text_field("VarName", 5)
description_entry = add_text_field("Description", 6)

# Generate button
generate_button = tk.Button(root, text="Generate SAS Code", command=generate_sas_code)
generate_button.grid(row=7, column=0, columnspan=2, pady=10)

# Output box
output_box = scrolledtext.ScrolledText(root, width=100, height=20)
output_box.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
