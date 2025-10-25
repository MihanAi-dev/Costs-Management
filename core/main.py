from fastapi import FastAPI
app = FastAPI()
costs_dict = {}

counter = 1


@app.post("/costs")
def add_costs(desc: str, cost: float):
    global counter
    costs_dict[counter] = {"description": desc, "cost": cost}
    counter += 1
    return (costs_dict)


@app.get("/costs")
def retrieve_costs():
    return (costs_dict)


@app.get("/costs/{cost_id}")
def find_costs(cost_id: int = 0):
    return [cost_value for cost_key, cost_value in costs_dict.items()
            if cost_key == cost_id]


@app.put("/costs/{cost_key}")
def update_costs(cost_key: int = 0, cost_desc: str = "",
                 cost_amount: float = 0.0):
    for key in costs_dict:
        if (key == cost_key):
            costs_dict[cost_key] = {"description": cost_desc,
                                    "cost": cost_amount}
            return (costs_dict)


@app.delete("/costs")
def delete_costs(cost_key: int = 0):
    for keys in costs_dict:
        if (keys == cost_key):
            costs_dict.pop(cost_key)
            return (costs_dict)
