from random import choice
from agents import Agent, Runner, ModelSettings,FileSearchTool,set_default_openai_key
from dotenv import load_dotenv
import os
import asyncio
from openai import vector_stores
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    set_default_openai_key(api_key)
vector_id = os.environ.get("VECTOR_STORE_ID")
_vector_ids = [vector_id] if vector_id else []
ppc_agent=Agent(
    name="LegalAId",
    instructions="""you are a helpful Legal advisor agent and you have to always use the tool to answer the querry
    and according to the PPC and only according to Pakistan law
    you have to meantion the sort of act related to that crime
    they should be like related to crime 
    related act :: punishment""",
    tools=[FileSearchTool(
        max_num_results=4,
        vector_store_ids=_vector_ids,
    )],
    model_settings=ModelSettings(tool_choice="required"),
    model="gpt-5.4-nano"
)
simple_agent=Agent(
    name="Simp",
    instructions="""you are a helpful assisstant and you have to answer his querries
    but if he asks about any sort of crime you have to handsoff to the PPC_agent for any queeries related to pakistan penal code
    """,
    model="gpt-5.4-nano",
    handoffs=[ppc_agent]
)
async def get_response(userQ:str):
    print("\n---- Agent is Thinking ----")
    result=await Runner.run(simple_agent,userQ)
    answer=result.final_output
    ag_name=result.last_agent.name
    return answer,ag_name
        

