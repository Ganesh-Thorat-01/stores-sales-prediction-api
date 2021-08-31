import uvicorn
from fastapi import FastAPI
from BigMart import Bigmart
import pickle
from datetime import date

app=FastAPI()

with open("rf_model.pkl","rb") as model_file:
    model=pickle.load(model_file)

@app.get("/")
def index():
    return {"message":"Hello,stranger",
            "Parameters":[{
    "Item_Weight":"float | Weight of product",
    "Item_Fat_Content" :  "string | Whether the product is Low Fat/Non-Edible/Normal", 
    "Item_Visibility"   :  "float | The percent of total display area of all products in a store allocated to the particular product",
    "Item_Type"  :  "string | The category to which the product belongs Food/Drinks/Non-Consumable" ,
    "Item_MRP"   : "float | Maximum Retail Price (list price) of the product",
    "Outlet_Establishment_Year": "float | The year in which store was established",  
    "Outlet_Size"  : "string | The size of the store in terms of ground area covered High/Medium/Small" ,
    "Outlet_Location_Type" :  "string | The type of city in which the store is located Tier 1/Tier 2/Tier 3", 
    "Outlet_Type"  : "string | Whether the outlet is just a grocery store or some sort of supermarket Glocery Store/Supermarket Type1/Supermarket Type2/Supermarket Type3"}],
    "URL of API Call":"https://stores-sales-api.herokuapp.com/predict",
    "To Test API please visit":"https://stores-sale-prediction.herokuapp.com",
     "© Copyright":"2021 Ganesh Thorat" }

@app.post("/predict")
async def predict_sales(input_data:Bigmart):
    data=input_data.dict() 
    Item_Weight=data["Item_Weight"]
    Item_Fat_Content = data["Item_Fat_Content"] 
    Item_Visibility = data["Item_Visibility"]
    Item_Type_Combined = data["Item_Type"] 
    Item_MRP  =data["Item_MRP"]
    Outlet_Establishment_Year= data["Outlet_Establishment_Year"]  
    Outlet_Size = data["Outlet_Size"] 
    Outlet_Location_Type=data["Outlet_Location_Type"] 
    Outlet_Type =data["Outlet_Type"]

    #Outlet years
    todays_date = date.today()
    Outlet_Years=todays_date.year-Outlet_Establishment_Year
    Item_Visibility_MeanRatio=1.061884


    if Item_Fat_Content=="Low Fat":
        Item_Fat_Content_0=1
        Item_Fat_Content_1=0
        Item_Fat_Content_2=0  
    elif Item_Fat_Content=="Non-Edible":
        Item_Fat_Content_0=0
        Item_Fat_Content_1=1
        Item_Fat_Content_2=0   
    else:
        Item_Fat_Content_0=0
        Item_Fat_Content_1=0
        Item_Fat_Content_2=1  

    if Outlet_Size=="High":
        Outlet_Size_0 = 1       
        Outlet_Size_1 = 0               
        Outlet_Size_2 = 0
    elif Outlet_Size=="Medium":
        Outlet_Size_0 = 0       
        Outlet_Size_1 = 1              
        Outlet_Size_2 = 0
    else:
        Outlet_Size_0 = 0       
        Outlet_Size_1 = 0               
        Outlet_Size_2 = 1

    #Outlet Location Type
    if Outlet_Location_Type=="Tier 1":
        Outlet_Location_Type_0 = 1   
        Outlet_Location_Type_1 = 0       
        Outlet_Location_Type_2 = 0
    elif Outlet_Location_Type=="Tier 2":
        Outlet_Location_Type_0 = 0   
        Outlet_Location_Type_1 = 1       
        Outlet_Location_Type_2 = 0
    else:
        Outlet_Location_Type_0 = 0   
        Outlet_Location_Type_1 = 0       
        Outlet_Location_Type_2 = 1

    #Outlet Type
    if Outlet_Type=="Glocery Store":
        Outlet_Type_0 = 1             
        Outlet_Type_1 = 0             
        Outlet_Type_2 = 0            
        Outlet_Type_3 = 0
    elif Outlet_Type=="Supermarket Type1":
        Outlet_Type_0 = 0             
        Outlet_Type_1 = 1            
        Outlet_Type_2 = 0            
        Outlet_Type_3 = 0
    elif Outlet_Type=="Supermarket Type2":
        Outlet_Type_0 = 0             
        Outlet_Type_1 = 0             
        Outlet_Type_2 = 1            
        Outlet_Type_3 = 0
    else:
        Outlet_Type_0 = 0             
        Outlet_Type_1 = 0             
        Outlet_Type_2 = 0            
        Outlet_Type_3 = 1
    #Item Type  
    if Item_Type_Combined=="Drinks":
        Item_Type_Combined_0 = 1     
        Item_Type_Combined_1 = 0       
        Item_Type_Combined_2 = 0
    elif Item_Type_Combined=="Food":
        Item_Type_Combined_0 = 0     
        Item_Type_Combined_1 = 1       
        Item_Type_Combined_2 = 0
    else:
        Item_Type_Combined_0 = 0     
        Item_Type_Combined_1 = 0       
        Item_Type_Combined_2 = 1

    features=[Item_Weight,Item_Visibility,Item_MRP,Outlet_Years,Item_Visibility_MeanRatio,
        Item_Fat_Content_0,Item_Fat_Content_1,
        Item_Fat_Content_2,Outlet_Size_0,Outlet_Size_1,Outlet_Size_2,
        Outlet_Location_Type_0,Outlet_Location_Type_1,Outlet_Location_Type_2,
        Outlet_Type_0,Outlet_Type_1,Outlet_Type_2,Outlet_Type_3,Item_Type_Combined_0,
        Item_Type_Combined_1,Item_Type_Combined_2]

    try:
        #Predicting Sales
        result=model.predict([features])
        return {"Predicted sales":result[0]}
    except:
        return {"message":"Internal server error"}

if __name__=="__main__":
    uvicorn.run(app)
