from pydantic import BaseModel

class Bigmart(BaseModel):
    Item_Identifier:str 
    Item_Weight:float
    Item_Fat_Content :  str 
    Item_Visibility   :  float
    Item_Type  :  str 
    Item_MRP   : float
    Outlet_Identifier : str 
    Outlet_Establishment_Year: int  
    Outlet_Size  : str 
    Outlet_Location_Type :  str 
    Outlet_Type  : str