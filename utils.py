import dotenv
import os
import google.generativeai as genai
import models
import json
import pandas as pd

def readDataFromEnv(keyVar:str):
    dotenv.load_dotenv()
    apiKeys=os.getenv(keyVar)
    apiKeys=apiKeys.split(',')
    return apiKeys
 
def getGeminiResponse(input_text, api_key):
        try:
            genai.configure(api_key=api_key) 
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(input_text)
            return response.text
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
         
         
def getSturturedQuery(input_text, api_key):
#    promptText=f"""Fields: Medical Record#,    Patient Name,    Specimen ID,    Age/Gender,    Account #,    Requesting Physicians,    Absolute Neutrophil Count,    W.B.C.(White Blood Count),    NE# (Neutrophilis),    LY# (Lymphocytes),    MO# (Monocytes),    EO# (Eosinophilis),    BA# (Basophilis),    R.B.C (Red Blood Count),    H.G.B (Haemoglobin),    H.C.T (Haematrocit),    M.C.V (mean corpuscular volume),    M.C.H (mean corpuscular hemoglobin),    M.C.H.C (Mean corpuscular hemoglobin concentration), R.D.W (red cell distribution width), P.L.T (Platelet Count)
# Give me the output in strutred format for the following :{input_text}

# Use this JSON schema:
# Filter = [
# {'{'}"field": str, "operator":str, "value": str or float or int{'}'}
# Return: list[Filter]
#    """
   promptText=f"""Fields: Medical Record#,    Patient Name,    Specimen ID,    Age/Gender,    Account #,    Requesting Physicians,    Absolute Neutrophil Count,    W.B.C.(White Blood Count),    NE# (Neutrophilis),    LY# (Lymphocytes),    MO# (Monocytes),    EO# (Eosinophilis),    BA# (Basophilis),    R.B.C (Red Blood Count),    H.G.B (Haemoglobin),    H.C.T (Haematrocit),    M.C.V (mean corpuscular volume),    M.C.H (mean corpuscular hemoglobin),    M.C.H.C (Mean corpuscular hemoglobin concentration), R.D.W (red cell distribution width), P.L.T (Platelet Count)
Give me the output in strutured format and use complete field names for the following :{input_text}"""
   try:
      genai.configure(api_key=api_key) 
      model = genai.GenerativeModel('gemini-1.5-flash-latest')
      response = model.generate_content(promptText,generation_config=genai.GenerationConfig(response_mime_type="application/json", response_schema=list[models.Filter]))
      return response.text
   except Exception as e:
      print(f"An error occurred: {e}")
      return None
   
   
def matchFieldNames(filters):
   for filt in filters:
      field=filt["field"]
      for report in availableFields:
         for availableField in availableFields[report]:
               if (availableField.find(field)!=-1):
                  
                  filt["field"] = availableField
   return filters
 
def setFilterType(df, filters):
    """
    Dynamically set the filter value type based on the column's type in the DataFrame.

    Parameters:
    - df (pandas.DataFrame): The dataset.
    - filters (list of dict): Filters with fields, operators, and values.

    Returns:
    - Updated filters with the correct types.
    """
    for filt in filters:
        field = filt["field"]
        if field in df.columns:
            fieldType = df[field].dtype
            # Convert the filter value to the same type as the column
            if pd.api.types.is_string_dtype(fieldType):
                filt["value"] = str(filt["value"])
            elif pd.api.types.is_integer_dtype(fieldType):
                filt["value"] = int(filt["value"])
            elif pd.api.types.is_float_dtype(fieldType):
                filt["value"] = float(filt["value"])
    return filters
 
def applyFiltersToCSV(df:pd.DataFrame, filters):
   filtered_df = df.copy()
   filters=matchFieldNames(filters)
   filters=setFilterType(df,filters)
   # print(filtered_df.count())
   # print(f'filters: {json.loads(filter)}')
   print(f'Init:{len(json.loads(filtered_df.to_json(orient='records')))}')
   for filt in filters:
      field = filt["field"]
      operator = filt["operator"]
      value = filt["value"]
      print(f'Field: {field}, Operator: {operator},Value: {value}')
      
      # value = float(filt["value"])  # Convert value to a numeric type if necessary

      # Apply filter dynamically
      if operator == ">":
         filtered_df = filtered_df[filtered_df[field] > value]
      elif operator == "<":
         filtered_df = filtered_df[filtered_df[field] < value]
      elif operator == "=":
         filtered_df = filtered_df[filtered_df[field] == value]
      elif operator == ">=":
         filtered_df = filtered_df[filtered_df[field] >= value]
      elif operator == "<=":
         filtered_df = filtered_df[filtered_df[field] <= value]
      print(f'Iter:{len(json.loads(filtered_df.to_json(orient='records')))}')

   return filtered_df
   
   
availableFields={"CBC":["Medical Record#", "Patient Name", "Specimen ID", "Age/Gender", "Account #", "Requesting Physicians", "Absolute Neutrophil Count", "W.B.C.(White Blood Count)", "NE# (Neutrophilis)", "LY# (Lymphocytes)", "MO# (Monocytes)", "EO# (Eosinophilis)", "BA# (Basophilis)", "R.B.C (Red Blood Count)", "H.G.B (Haemoglobin)", "H.C.T (Haematrocit)", "M.C.V (mean corpuscular volume)", "M.C.H (mean corpuscular hemoglobin)", "M.C.H.C (Mean corpuscular hemoglobin concentration)", "R.D.W (red cell distribution width)", "P.L.T (Platelet Count)"]}