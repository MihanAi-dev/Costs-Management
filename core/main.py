from fastapi import FastAPI,HTTPException,status, Path
from fastapi.responses import JSONResponse
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from typing import Dict

app = FastAPI(title= "Cost Management", version="1.1.0")
DESC_PATTERN = r"^[\w\s\u0600-\u06FF\.\-_,()\/]{3,100}$"

class CostItem(BaseModel):
    desc : str = Field(...,pattern=DESC_PATTERN, description="تعداد 3 تا 100 کاراکتر فارسی یا لاتین مجاز است.")
    cost : Decimal = Field(...,gt=0, description="مبلغ باید عدد مثبت باشد.")
    @field_validator ("cost")
    @classmethod
    def normalize_cost(cls, v: Decimal) -> Decimal:
        return v.quantize(Decimal("0.01"))
    
costs_dict : Dict[int, CostItem] = {}
counter = 1


@app.get("/costs", status_code=status.HTTP_200_OK)
def retrieve_costs():
    if not costs_dict:
         raise HTTPException(status_code= 404, detail = "No costs found")
    return (costs_dict)


@app.post("/costs", status_code=status.HTTP_201_CREATED)
def add_cost(payload: CostItem):
    global counter
    costs_dict[counter] = payload
    response = {
        "detail": "object created successfully",
        "id": counter,
        "data": payload
    }
    counter += 1
    return response


@app.get("/costs/{cost_id}", status_code=status.HTTP_200_OK)
def find_cost(cost_id: int = Path(...,ge =1)):
    if cost_id not in costs_dict:
         raise HTTPException(status_code= 404, detail="Cost not found") 
    return costs_dict[cost_id]


@app.put("/costs/{cost_id}" , status_code=status.HTTP_200_OK)
def update_cost(cost_id: int, payload: CostItem):
    if(cost_id not in costs_dict):
        raise HTTPException(status_code= 404, detail= "object not found")
    costs_dict[cost_id] = payload
    return {"detail": "object updated successfully", "updated_item": payload}


@app.delete("/costs/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost(cost_id: int):
    if (cost_id in costs_dict):
        del costs_dict[cost_id]
        return JSONResponse(content={"detail": "object remove successfully"},status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="object not found")
    
