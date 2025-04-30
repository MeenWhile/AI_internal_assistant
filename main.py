from fastapi import FastAPI
from pydantic import BaseModel
from src.deep_research_agent import DeepResearchAgent

app = FastAPI()

# Request body model
class QueryRequest(BaseModel):
    user_input: str

# API endpoint
@app.post("/query")
def query_agent(request: QueryRequest):
    
    # run the agent
    result = DeepResearchAgent.run_agent(request.user_input)

    return result
