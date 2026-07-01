from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from src.services.selectQuerys.SelectTransactionByDate import selectTransaction
from src.services.selectQuerys.ChargebackPercent import selectChargebackPercent
from src.services.selectQuerys.SelectAVGValue import getAVGValue
import os, dotenv

dotenv.load_dotenv()    
def create_caronte_agent(prompt : str, responseType):
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"))

    tools =[getAVGValue,selectChargebackPercent,selectTransaction]

    agent = create_agent(model=model,
                        system_prompt=prompt,
                        tools=tools,
                        response_format= responseType)
    return agent