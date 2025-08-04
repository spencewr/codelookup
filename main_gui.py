from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, Text, END

# Define mappings
topic_map = {
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

subtopic_map = {
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

def generate_code():
    varname = varname_entry.get()
    vartype = vartype_var.get()
    varcode = varcode_entry.get()
    varvalue = varvalue_entry.get()
    topic = topic_var.get()
    subtopic = subtopic_var.get()
    description = description_var.get()

    topic_id = topic_map.get(topic, "")
    subtopic_id = subtopic_map.get(subtopic, "")
    
    tag = f"{varname}_YRBS" 

    code = f"""data new_varxx;
YearNum =2023 ;
VarValID =1 ;
Topic_ID ={topic_id} ;
SubTopic_ID ={subtopic_id} ;
ExcludeInclude =1 ;
SortOrder =1 ;
Topic_SortOrder =1 ;
SubTopic_SortOrder =1 ;
Topic_DefaultID =1 ;
DefaultID =1 ;
Indicator_SortOrder =;
YearDate ="2023-01-01 ";
Dataset ="YRBS ";
Dataset_Name ="NYC Youth Risk Behavior Survey ";
Dataset_Type ="Health Surveys ";
VarCode ="{varcode}" ;
VarValue ="{varvalue}" ;
VarType ="{vartype}" ;
VarName ="{varname}" ;
Description ="{description}" ;
Topic ="{topic}" ;
Sub_Topic ="{subtopic}" ;
PopulationDatasource ="Youth ";
Note1 ="  ";
Note2 ="  ";
Note3 ="  ";
CrossNotes ="  ";
MapTitlePrefix ="  ";
MapTitleSuffix ="  ";
MapInsert ="  ";
VarComments ="  ";
Tag ="{tag}";
DefaultPopulationSource ="CHS ";
output;
run;"""

    output_text.delete("1.0", END)
    output_text.insert(END, code)

# GUI setup
root = Tk()
root.title("SAS Code Generator")

# Input rows
Label(root, text="Variable Name (ex. Felt sad (last 30 days))").grid(row=0, column=0, sticky="e")
varname_entry = Entry(root, width=30)
varname_entry.grid(row=0, column=1)

Label(root, text="Variable Code (ex. sadsad4, boroug5)").grid(row=1, column=0, sticky="e")
varcode_entry = Entry(root, width=30)
varcode_entry.grid(row=1, column=1)

Label(root, text="Variable Value (ex. Felt sad, Did not feel sad)").grid(row=2, column=0, sticky="e")
varvalue_entry = Entry(root, width=30)
varvalue_entry.grid(row=2, column=1)

Label(root, text="Description (ex. Students that felt sad or hopeless over past 30 days)").grid(row=3, column=0, sticky="e")
description_entry = Entry(root, width=30)
description_entry.grid(row=2, column=1)

Label(root, text="Variable Type").grid(row=4, column=0, sticky="e")
vartype_var = StringVar(root)
vartype_var.set("Indicator")
OptionMenu(root, vartype_var, "Indicator", "Demographic").grid(row=3, column=1, sticky="w")

Label(root, text="Topic").grid(row=5, column=0, sticky="e")
topic_var = StringVar(root)
topic_var.set(next(iter(topic_map)))
OptionMenu(root, topic_var, *topic_map).grid(row=4, column=1, sticky="w")

Label(root, text="Subtopic").grid(row=6, column=0, sticky="e")
subtopic_var = StringVar(root)
subtopic_var.set(next(iter(subtopic_map)))
OptionMenu(root, subtopic_var, *subtopic_map).grid(row=5, column=1, sticky="w")

# Generate button
Button(root, text="Generate SAS Code", command=generate_code).grid(row=6, columnspan=2, pady=10)

# Output SAS code area
output_text = Text(root, height=25, width=90)
output_text.grid(row=7, columnspan=2, padx=10, pady=10)

root.mainloop()
