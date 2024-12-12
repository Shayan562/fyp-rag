import json
import math
import google.generativeai as genai
import time
import dotenv
import os

from numpy import record
import utils
import models
import pandas as pd


fileToRead='./modified_records.csv' #temp
def writeOutput(prompt:str, df:pd.DataFrame):
    numChunks=math.ceil(len(df)/15)
    if (numChunks==0):
        print("\n\nNo Patients Found")
    data=[]
    for i in range(numChunks):
        chunk_df = df.iloc[i * 15:(i + 1) * 15]  # Select the chunk of 15 records
        json_data = chunk_df.to_json(orient='records')
        json_data = json.loads(json_data)
        json_data=convertFormat(prompt,json_data)
        data.append(json_data)
            
    with open(f'./myfile array{i}.json','w') as f:
        # f.writelines(data)
        f.write(json.dumps({"Prompts":data}))
def convertFormat(prompt:str, data:json): #temp
    length=len(data)
    formattedData=prompt + '\n\nData:'
    dataToCombine=[]
    for report in data:
        tempStr=f''
    print(len(data))
    #    output = "Provide MR num with P.L.T (Platelet Count) > 70\n\nData:\n"
    formattedData += "\n".join(
        f"Medical Record#: {patient['Medical Record#']}\n"
        f"Patient Name: {patient['Patient Name']}\n"
        f"Specimen ID: {patient['Specimen ID']}\n"
        f"Age/Gender: {patient['Age/Gender']}\n"
        f"Account #: {patient['Account #']}\n"
        f"Requesting Physicians: {patient['Requesting Physicians']}\n"
        f"Absolute Neutrophil Count: {patient['Absolute Neutrophil Count']}\n"
        f"W.B.C.(White Blood Count): {patient['W.B.C.(White Blood Count)']}\n"
        f"NE# (Neutrophilis): {patient['NE# (Neutrophilis)']}\n"
        f"LY# (Lymphocytes): {patient['LY# (Lymphocytes)']}\n"
        f"MO# (Monocytes): {patient['MO# (Monocytes)']}\n"
        f"EO# (Eosinophilis): {patient['EO# (Eosinophilis)']}\n"
        f"BA# (Basophilis): {patient['BA# (Basophilis)']}\n"
        f"R.B.C (Red Blood Count): {patient['R.B.C (Red Blood Count)']}\n"
        f"H.G.B (Haemoglobin): {patient['H.G.B (Haemoglobin)']}\n"
        f"H.C.T (Haematrocit): {patient['H.C.T (Haematrocit)']}\n"
        f"M.C.V (mean corpuscular volume): {patient['M.C.V (mean corpuscular volume)']}\n"
        f"M.C.H (mean corpuscular hemoglobin): {patient['M.C.H (mean corpuscular hemoglobin)']}\n"
        f"M.C.H.C (Mean corpuscular hemoglobin concentration): {patient['M.C.H.C (Mean corpuscular hemoglobin concentration)']}\n"
        f"R.D.W (red cell distribution width): {patient['R.D.W (red cell distribution width)']}\n"
        f"P.L.T (Platelet Count): {patient['P.L.T (Platelet Count)']}\n"
        for patient in data
    )

    # json_obj={'Prompt':formattedData}
    # json_obj=json.dumps(json_obj)
    return formattedData 
    temp=[formattedData]
    with open(f'./myfile New.json','w') as f:
        f.write(json.dumps(json_obj))
        

if __name__=='__main__':
    #load data
    df=pd.read_csv(fileToRead)
    # dataInJson=json.loads(df.to_json(orient='records'))
    # print(dataInJson[3])
    
    geminiKeys=models.ApiKeyManagement(utils.readDataFromEnv('GEMINI_KEYS'))
    while True:
        userQuery=str(input("Entery your query: "))
        output=utils.getSturturedQuery(userQuery,geminiKeys.getKey())
        if(output==None):
            print("Something went wrong. Please try again")
            geminiKeys.nextKey()
            continue
        else:
            print(output)
            filteredCSV=utils.applyFiltersToCSV(df,json.loads(output))
            temp=filteredCSV.to_json(orient='records')
            writeOutput(userQuery,filteredCSV)
            # with open('Output.json','w') as f:
            #     f.write(f'')
            #    for line in temp:
            #        f.write(line)
            temp=json.loads(temp)
            # convertFormat(userQuery,temp)
            # min=999
            # max=-1
            # for val in temp:
            #     if (val["W.B.C.(White Blood Count)"]<min):
            #         min=val["W.B.C.(White Blood Count)"]
            #     if (val["W.B.C.(White Blood Count)"]>max):
            #         max=val["W.B.C.(White Blood Count)"]
            # print(f'min{min}, max{max}')
            # print(json.loads(temp))
    # genai.configure(api_key=geminiKeys.getKey())
    
   