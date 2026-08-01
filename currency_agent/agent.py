import requests
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

GROQ_API_KEY= os.getenv("GROQ_API_KEY")

def get_currency_rates(from_currency:str, to_currency:str)->dict:
    
    """
    Fetch the currency exchange rates based on the provided parameter i.e. from_currency & to_currency.
    Use this tool whenever user asks about currency exchange rates.

    Arguments:
    from_currency: the base country currency symbol(for example: NPR, AUD, USD).ISO currency code
    to_currency: the quotes country currency symbol.
    
    Return the result in dictionary containing currency exchange rate.
    """
    try:
        url=f"https://api.frankfurter.dev/v2/rates?base={from_currency}&quotes={to_currency}"
        response=requests.get(url)
        
        print(response.status_code)

        
        data=response.json()
        print(data)
        rate= data[0]["rate"]
        return rate
    
    except Exception as e:
        return ({"message": "An error occurred while fetching weather data", "error": str(e)})


SYSTEM_PROMPT = """
You are a currency exchange assistant.

Whenever the user asks for an exchange rate or currency conversion,
always use the get_currency_rates tool.

Never make up exchange rates from memory.
"""

root_agent= Agent(
    name="currency_agent",
    model=LiteLlm(model="groq/llama-3.1-8b-instant"),
    instruction=SYSTEM_PROMPT,
    description="Answer user query related to currency exchange rates",
    tools=[get_currency_rates]
)
