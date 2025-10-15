from fastapi import FastAPI
import random 
app =FastAPI()

costs_dict ={}

@app.post("/costs")
def add_costs(desc:str, cost:float):
    id = random.randint(1,100)
    costs_dict[id] = {
        "id" : id,
        "description" : desc,
        "cost" : cost
    } 
    print(costs_dict)
    
