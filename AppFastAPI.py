from fastapi import FastAPI
from pydantic import BaseModel
import json
import VRPTimeLimit

app = FastAPI()

class VRPModelInput(BaseModel):
    n_nodes: int
    n_vehicles: int
    depot: list
    time_matrix: list
    time_windows: list
    pickup_capacity: list
    delivery_capacity: list
    vehicle_capacity: int

@app.post('/vehicle_routes')
def vehicle_routes(data: VRPModelInput):
    
    n_nodes = data.n_nodes
    
    main(data.n_nodes, data.n_vehicles, data._decompose_class)
    

