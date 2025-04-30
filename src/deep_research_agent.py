# region Setup

from smolagents import (
    CodeAgent,
    LiteLLMModel,
    Tool
)
from src.tool import TestBugReport, TestUserFeedback, IssueSummaryTool
from src.prompt import Prompt

# Select model
model = LiteLLMModel(model_id="openai/gpt-4o-mini", temperature=0)
# model = LiteLLMModel(model_id="bedrock/us.meta.llama3-3-70b-instruct-v1:0", temperature=0)

# Set import that agent can use
AUTHORIZED_IMPORTS = [
    "requests",
    "zipfile",
    "os",
    "pandas",
    "numpy",
    "json",
    "bs4",
    "io",
    "PyPDF2",
    "pptx",
    "datetime",
    "csv"
]

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# region Answer_internal_question_agent

class AnswerInternalQuestionsAgent(Tool):

    name = "answer_internal_question_agent"
    description = """This agent retrieves data from bug reports and user feedback to answer internal questions.
    **Use only** when the user's input suggests the need to search for specific information in the database."""
    inputs = {"user_input": {"type": "string", "description": "user input text"}}
    output_type = "string"

    def __init__(self):
        
        super().__init__()

    def forward(self, user_input: str) -> str:

        # Set tool
        TOOLS = [
            TestBugReport(5),
            TestUserFeedback(10)
        ]

        # Set sub agent
        agent = CodeAgent(tools=TOOLS, model=model, additional_authorized_imports=AUTHORIZED_IMPORTS)

        # Set prompt
        prompt = Prompt.prompt_answer_internal_question_agent(user_input)

        # Run agent
        result = agent.run(prompt, max_steps=20)

        return result
    
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# region Summarize_key_product_issues_agent

class SummarizeKeyProductIssuesAgent(Tool):

    name = "summarize_key_product_issues_agent"
    description = """This agent will extract key insights and summarize product-related issues from the provided user input.
Use this agent when the user input contains information related to product issues, but does not require searching for additional data."""
    inputs = {"user_input": {"type": "string", "description": "user input text"}}
    output_type = "string"

    def __init__(self):

        super().__init__()

    def forward(self, user_input: str) -> str:

        # Set tool
        TOOLS = [
            IssueSummaryTool()
        ]

        # Set sub agent
        agent = CodeAgent(tools=TOOLS, model=model, additional_authorized_imports=AUTHORIZED_IMPORTS)

        # Set prompt
        prompt = Prompt.prompt_summarize_key_product_issues_agent(user_input)

        # Run sub agent
        result = agent.run(prompt, max_steps=20)

        return result
    
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# region Manager_agent

class DeepResearchAgent:
    
    @staticmethod
    def run_agent(user_input):

        # Set sub agent
        AGENTS = [
            AnswerInternalQuestionsAgent(),
            SummarizeKeyProductIssuesAgent()
        ]

        # Set manager agent
        agent = CodeAgent(tools=AGENTS, model=model, additional_authorized_imports=AUTHORIZED_IMPORTS)

        # Set prompt
        prompt = Prompt.prompt_manager_agent(user_input)

        # Run agent
        result = agent.run(prompt, max_steps=20)

        return result

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


