# region Setup

import os
import json
from dotenv import load_dotenv
import numpy as np
import openai
import faiss
from smolagents import Tool

# Prevent library conflicts. 
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Set OpenAI API key for embedding model
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # แทนที่ด้วย API key ของคุณ

# set function for calling embedding model
def get_embeddings(texts):
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"  # หรือโมเดลที่คุณต้องการใช้
    )
    embeddings = [record.embedding for record in response.data]
    return np.array(embeddings)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# region Bug_report

class TestBugReport(Tool):

    name = "get_test_bug_report"
    description = """This tool searches the vector database to retrieve **bug_reports** based on the provided query."""
    inputs = {"query": {"type": "string", "description": "query text that you want to find"}}
    output_type = "string"

    def __init__(self, k):

        super().__init__()

        # Set number of returned data
        self.k = k

        # Set path for bug_report data
        self.loaded_index = faiss.read_index(os.path.join("dataset","dataset_test_bug_report.index"))
        with open(os.path.join("dataset","dataset_test_bug_report.json"), 'r') as f:
            self.bugs_data = json.load(f)

    def forward(self, query: str) -> str:

        # Embedding
        query_embedding = get_embeddings([query])

        # Vector search
        distances, indices = self.loaded_index.search(query_embedding, self.k)

        # Create result to send to agent
        text = ""
        for i, idx in enumerate(indices[0]):
            text += f"Matched Document: {self.bugs_data[idx]}\n"
            text += f"Score (Distance): {distances[0][i]:.4f}\n\n"

        text += f"You always get {self.k} matched document but the relevant result normally just some of document is really match the query"

        return text
    
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# region User_feedback

class TestUserFeedback(Tool):

    name = "get_test_user_feedback"
    description = """This tool searches the vector database to retrieve **user_feedback** based on the provided query."""
    inputs = {"query": {"type": "string", "description": "query text that you want to find"}}
    output_type = "string"

    def __init__(self, k):

        super().__init__()

        # Set number of returned data
        self.k = k

        # Set path for bug_report data
        self.loaded_index = faiss.read_index(os.path.join("dataset","dataset_test_user_feedback.index"))
        with open(os.path.join("dataset","dataset_test_user_feedback.json"), 'r') as f:
            self.bugs_data = json.load(f)

    def forward(self, query: str) -> str:

        # Embedding
        query_embedding = get_embeddings([query])

        # Vector search
        distances, indices = self.loaded_index.search(query_embedding, self.k)

        # Create result to send to agent
        text = ""
        for i, idx in enumerate(indices[0]):
            text += f"Matched Document: {self.bugs_data[idx]}\n"
            text += f"Score (Distance): {distances[0][i]:.4f}\n\n"

        text += f"You always get {self.k} matched document but the relevant result normally just some of document is really match the query"

        return text
       
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# region Issue_summary

class IssueSummaryTool(Tool):

    name = "issue_summary_tool"
    description = """This tool summarizes an issue by extracting the following key details:
- Reported issues
- Affected features/components
- Severity (with possible values: Low, Medium, High)
"""
    inputs = {"reported_issues": {"type": "string", "description": "Reported issues that you think"},
              "affect_feature": {"type": "array", "description": "Affected features/components that you think"},
              "severity": {"type": "string", "description": "Have only Low, Medium, High"}}
    output_type = "string"

    def __init__(self):
        super().__init__()

    def forward(self, reported_issues: str, affect_feature: list, severity: str) -> str:

        # Create result structure
        output = {
            "reported_issues": reported_issues,
            "affect_feature": affect_feature,
            "severity": severity
        }

        return str(output)
    
       
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
