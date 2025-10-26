from fastapi import FastAPI,HTTPException,status
from fastapi.responses import JSONResponse

app = FastAPI()
costs_dict = {}
counter = 1


@app.get("/costs", status_code=status.HTTP_200_OK)
def retrieve_costs():
    if not costs_dict:
         raise HTTPException(status_code= 404, detail = "No costs found")
    return (costs_dict)


@app.post("/costs", status_code=status.HTTP_201_CREATED)
def add_cost(desc: str, cost: float):
    global counter
    costs_dict[counter] = {"description": desc, "cost": float(cost)}
    counter += 1
    return {"detail": "object created successfully", "id":counter -1, "data": costs_dict[counter - 1]}


@app.get("/costs/{cost_id}", status_code=status.HTTP_200_OK)
def find_cost(cost_id: int):
    if cost_id not in costs_dict:
         raise HTTPException(status_code= 404, detail="Cost not found") 
    return costs_dict[cost_id]


@app.put("/costs/{cost_id}" , status_code=status.HTTP_200_OK)
def update_cost(cost_id: int, cost_desc: str = "", cost_amount: float = 0.0):
    if(cost_id not in costs_dict):
        raise HTTPException(status_code= 404, detail= "object not found")
    costs_dict[cost_id] = {
        "description": cost_desc,
        "cost": float(cost_amount)
        }
    return {"detail": "object updated successfully", "updated_item": costs_dict[cost_id]}


@app.delete("/costs/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cost(cost_id: int = 0):
    if (cost_id in costs_dict):
        del costs_dict[cost_id]
        return JSONResponse(content={"detail": "object remove successfully"},status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="object not found")