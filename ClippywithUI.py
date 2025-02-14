from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import chainlit as cl
import asyncio
import requests
import urllib.parse
import json
import configparser
from datetime import date
from langchain_community.tools.tavily_search import TavilySearchResults
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from configparser import SectionProxy
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, MessagesState, StateGraph
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_openai import OpenAI
from langchain_core.runnables import ConfigurableField
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ChatMessageHistory
from dotenv import load_dotenv, find_dotenv
from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from langgraph.types import interrupt
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from typing import Literal
from langgraph.prebuilt import ToolNode
from langchain.schema.runnable.config import RunnableConfig
from langgraph.errors import GraphRecursionError
from langgraph.checkpoint.memory import MemorySaver
#MSAL Auth
import msal
import jwt
import json
import sys
import requests
from datetime import datetime as dt
from datetime import date
from msal_extensions import *


#load the environment
load_dotenv(override=True)


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
TENANT_GRAPH_ACCESS_TOKEN = os.getenv("TENANT_GRAPH_ACCESS_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
USERNAME = os.getenv("USERNAME")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")



#MSAL Auth
graphURI = 'https://graph.microsoft.com'
tenantID = TENANT_ID
authority = 'https://login.microsoftonline.com/' + tenantID
clientID = CLIENT_ID
scope = ["User.Read","Calendars.Read","Calendars.ReadBasic", "Calendars.Read", "Calendars.ReadWrite"]
username = USERNAME
result = None
tokenExpiry = None

def msal_persistence(location, fallback_to_plaintext=False):
    """Build a suitable persistence instance based your current OS"""
    if sys.platform.startswith('win'):
        return FilePersistenceWithDataProtection(location)
    if sys.platform.startswith('darwin'):
        return KeychainPersistence(location, "my_service_name", "my_account_name")
    return FilePersistence(location)

def msal_cache_accounts(clientID, authority):
    # Accounts
    persistence = msal_persistence("token_cache.bin")
    #print("Is this MSAL persistence cache encrypted?", persistence.is_encrypted)
    cache = PersistedTokenCache(persistence)
    
    app = msal.PublicClientApplication(
        client_id=clientID, authority=authority, token_cache=cache)
    accounts = app.get_accounts()
    #print(accounts)
    return accounts

def msal_delegated_refresh(clientID, scope, authority, account):
    persistence = msal_persistence("token_cache.bin")
    cache = PersistedTokenCache(persistence)
    
    app = msal.PublicClientApplication(
        client_id=clientID, authority=authority, token_cache=cache)
    result = app.acquire_token_silent_with_error(
        scopes=scope, account=account)
    return result

def msal_delegated_refresh_force(clientID, scope, authority, account):
    persistence = msal_persistence("token_cache.bin")
    cache = PersistedTokenCache(persistence)
    
    app = msal.PublicClientApplication(
        client_id=clientID, authority=authority, token_cache=cache)
    result = app.acquire_token_silent_with_error(
        scopes=scope, account=account, force_refresh=True)
    return result

def msal_delegated_device_flow(clientID, scope, authority):
    #print("Initiate Device Code Flow to get an AAD Access Token.")
    #print("Open a browser window and paste in the URL below and then enter the Code. CTRL+C to cancel.")
    persistence = msal_persistence("token_cache.bin")
    cache = PersistedTokenCache(persistence)
    app = msal.PublicClientApplication(client_id=clientID, authority=authority, token_cache=cache)
    flow = app.initiate_device_flow(scopes=scope)
    if "user_code" not in flow:
        raise ValueError("Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))
    print(flow["message"])
    sys.stdout.flush()
    result = app.acquire_token_by_device_flow(flow)
    return result

def msal_jwt_expiry(accessToken):
    decodedAccessToken = jwt.decode(accessToken, verify=False)
    accessTokenFormatted = json.dumps(decodedAccessToken, indent=2)
    # Token Expiry
    tokenExpiry = dt.fromtimestamp(int(decodedAccessToken['exp']))
    #print("Token Expires at: " + str(tokenExpiry))
    return tokenExpiry


def msgraph_request(resource, requestHeaders):
    # Request
    results = requests.get(resource, headers=requestHeaders).json()
    return results

accounts = msal_cache_accounts(clientID, authority)
if accounts:
    for account in accounts:
        if account['username'] == username:
            myAccount = account
            #print("Found account in MSAL Cache: " + account['username'])
            #print("Obtaining a new Access Token using the Refresh Token")
            result = msal_delegated_refresh(clientID, scope, authority, myAccount)

            if result is None:
                # Get a new Access Token using the Device Code Flow
                result = msal_delegated_device_flow(clientID, scope, authority)
            else:
                if result["access_token"]:
                    msal_jwt_expiry(result["access_token"])                    
else:
    # Get a new Access Token using the Device Code Flow
    result = msal_delegated_device_flow(clientID, scope, authority)

    if result["access_token"]:
        msal_jwt_expiry(result["access_token"])

GRAPH_ACCESS_TOKEN =result["access_token"] 
# End of authentication code

@tool
async def getevents():
    """Get a list of my events from my calendar and display them with the meeting name, subject of the meeting, start dateTime, end dateTime, organizers, participants, date and time."""
    # To initialize your graph_client, see https://learn.microsoft.com/en-us/graph/sdks/create-client?from=snippets&tabs=python
    print("using getevents tool")
    requestHeaders = {'Authorization': 'Bearer ' + result["access_token"],'Content-Type': 'application/json'}
    queryResults = msgraph_request(graphURI + "/v1.0/me/events",requestHeaders)
    #print(json.dumps(queryResults, indent=2))
    return queryResults
    

@tool
async def getcontacts():
    """Get a list of my contacts and display with their full name, office location, email id, company name"""
    print("using getevents tool")
    requestHeaders = {'Authorization': 'Bearer ' + result["access_token"],'Content-Type': 'application/json'}
    queryResults = msgraph_request(graphURI + "/v1.0/me/contacts",requestHeaders)
    #print(json.dumps(queryResults, indent=2))
    return queryResults


@tool
def sendmail(subject: str, body: str, email: str) -> str:
    """Send a mail to the email address provided with the Subject provided in the subject and Body provided in the body as the user.Send an empty body if there is no body in the user query. Do not sign the mail."""
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers = {
        "Authorization": f"Bearer {GRAPH_ACCESS_TOKEN}"}
    data = {
            "message": {
                "subject": f"{subject}",
                "body": {
                    "contentType": "Text",
                    "content": f"{body}"
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": f"{email}"
                        }
                    }
                ]
            }
        }
    response = requests.post(url, headers=headers, json=data)
    #response = requests.post(url, json=data)
    print("Status Code", response.status_code)
    #print("JSON Response ", response.json())
    return response

llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", "you're a helpful admin assistant who can send emails on behalf of the user. Your name is Clippy. Please answer all questions knowing that today's date is"+ date.today().strftime('%m/%d/%Y') +"Whenever someone wants to see their events, use the tool getevents and identify the right start dateTime from the results you get from getEvents tool and answer the user prompt about their availability correctly. Please format the tool responses you get into much more readable format. You can fetch their contacts. You can search the web for anything else you don't understand. You can get their calendar events. You can also give information to users about the holidays in their regions. Their DTO policies. Their timeoff policies. Anything they want to know about their employee benefits. The access_tokens are available in the tools so don't ask the users again."), 
    ("human", "{input}"), 
    ("placeholder", "{agent_scratchpad}"),
])

search = TavilySearchResults(max_results=2)

# all the tools I have access to
tools = [getcontacts, getevents, sendmail, search]

model = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_retries=2)


llm = ChatOpenAI(model="gpt-4o")

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
async def call_model(state: MessagesState):
    prompt = prompt.invoke(state)
    response = model.ainvoke(prompt)
    return {"messages": response}

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = ChatMessageHistory(session_id="test-session")
app = workflow.compile(checkpointer=memory)

agent = create_tool_calling_agent(model, tools, prompt)
langgraph_agent_executor = agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, trim_intermediate_steps=True)
agent_with_chat_history = RunnableWithMessageHistory(
    langgraph_agent_executor,
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

config = {"configurable": {"thread_id": "def234"}}

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Hello! I am your personal companion, Clippy! Ask me about your meetings. Or the weather. I can answer most things about the world!").send()
    cl.user_session.set("langgraph_agent_executor", langgraph_agent_executor)

@cl.on_message
async def handle_message(message: cl.Message):
    langgraph_agent_executor = cl.user_session.get("langgraph_agent_executor")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "you're a helpful admin assistant who can send mails on behalf of users. You can answer simple questions like country capitals without using any tools. You can search the web. Your name is Clippy. Please answer all questions knowing that today's date is "+ date.today().strftime('%m/%d/%Y') +". Whenever someone wants to see their events, use the tool getevents and identify the right start dateTime from the results you get from getEvents tool and answer the user prompt about their availability correctly. Please format the tool responses you get into much more readable format. You can fetch their contacts. You can search the web for anything else you don't understand. You can get their calendar events. You can also give information to users about the holidays in their regions. Their DTO policies. Their timeoff policies. Anything they want to know about their employee benefits. The access_tokens are available in the tools so don't ask the users again."), 
        ("human", message.content), 
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(model, tools, prompt)
    langgraph_agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, trim_intermediate_steps=True)
    agent_with_chat_history = RunnableWithMessageHistory(
        langgraph_agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    
    
    # Invoke the LangGraph agent executor
    config = {"configurable": {"session_id": "def234"}}
    
    async for chunk in agent_with_chat_history.astream(
        {"messages": [HumanMessage(content=message.content)]}, config
    ):
        print(chunk)
        if 'output' in chunk:
            # Do something if the object has the 'my_field' attribute
            print("Object has the attribute")
            await cl.Message(chunk['output']).send()
        else:
            cl.Message("Processing step:","\n")
            await cl.Message(chunk).send()
        print("----")