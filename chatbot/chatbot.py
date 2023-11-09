
import os
import requests

#from langchain.embeddings.openai import OpenAIEmbeddings
#from langchain.chat_models import ChatOpenAI
#from langchain.llms import HuggingFaceHub
#from langchain.vectorstores import Pinecone
#from langchain.chains import LLMChain

#from langchain.prompts.chat import (
#    ChatPromptTemplate,
#    SystemMessagePromptTemplate,
#    HumanMessagePromptTemplate,
#)

#from getpass import getpass

from dotenv import find_dotenv, load_dotenv
import streamlit as st



class MaverickChatbot:
    
    def __init__(self):
        load_dotenv(find_dotenv())

    @st.cache_data(show_spinner=False)
    def get_response_from_query(_self, query):
        """
        Function that generates a response to a customer question using LLama and Vectara DB
        """
        try:

            # Get the values from environment variables
            #customer_id = os.getenv("CUSTOMER_ID")
            #x_api_key = os.getenv("VECTARA_API_KEY")
            #customerid = os.getenv("CUSTOMERID")
            #vectara_token = os.getenv("TOKEN")
            #corpusid = os.getenv("CORPUSID")

            customer_id = st.secrets("CUSTOMER_ID")
            x_api_key = st.secrets("VECTARA_API_KEY")
            customerid = st.secrets("CUSTOMERID")
            vectara_token = st.secrets("TOKEN")
            corpusid = st.secrets("CORPUSID")            
            
            url = 'https://api.vectara.io/v1/query'


            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'customer-id': customer_id,
                'x-api-key': x_api_key
            }


            data = {
                "query": [
                    {
                        "query": query,
                        "start": 0,
                        "numResults": 5,
                        "corpusKey": [
                            {
                                "customerId": customerid,
                                "corpusId": corpusid,
                                "semantics": "DEFAULT",
                                "dim": [
                                    {
                                        "name": "string",
                                        "weight": 0
                                    }
                                ],
                                "metadataFilter": "part.lang = 'eng'",
                                "lexicalInterpolationConfig": {
                                    "lambda": 0
                                }
                            }
                        ],
                        "rerankingConfig": {
                            "rerankerId": 272725717
                        },
                        "summary": [
                            {
                                "summarizerPromptName": "string",
                                "maxSummarizedResults": 0,
                                "responseLang": "string"
                            }
                        ]
                    }
                ]
            }
        
        
            #Perform API call - POST towards  VECTARA DB  
            response1 = requests.post(url, headers=headers, json=data)

            if response1.status_code == 200:
                response_json = response.json()

                # Check if results are available
                if "responseSet" in response_json and len(response_json["responseSet"]) > 0:
                    ##############################################################################################################################
                    # text = response narrow down from VectaraDB to a customer query that will be used later by Llama-2-70b-chat-hf as GUIDELINE
                    ##############################################################################################################################
                    for result in response_json["responseSet"][0]["response"]:
                        text = result.get("text", "")
                        #print("Extracted Text:")
                        #print(text)
                else:
                    return "1ST -- No results were found for the query."
                    #print("No results were found for the query.")
            else:
                return f"2ND -- Request failed with status code: {response1.status_code}"
                #print(f"Request failed with status code: {response.status_code}")


            s = requests.Session()

            #api_base = os.getenv("ANYSCALE_API_BASE")
            api_base = "https://api.endpoints.anyscale.com/v1"
            token = vectara_token 
            url = f"{api_base}/chat/completions"
            body = {
                    "model": "meta-llama/Llama-2-70b-chat-hf",
                    "messages": [{"role": "system", "content": "Your name is Kamal and you are a helpful and casual consultation doctor, you will extract and summarize factual information from {text} and give an accurate response(don't summarize links so write them as source), The is information from {text} is to prevent you from hallucination and guide you to provide factual information. Make sure you are conversational, use relevant emojis in some some cases. You understand how to handle compliment and greetings such as Hello, what's up, hey, Thank you etc. In a circumstance in which you don't have enough information just say 'I'm out of information, can say something different?' "}, 
                                 {"role": "user", "content": query}],
                                  "temperature": 0.7
                   }

            response = s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body)

            error_response = ""
            if response.status_code == 200:
                response_json = response.json()
                chatbot_response = response_json["choices"][0]["message"]["content"]
                #print("Chatbot Response:")
                error_response = chatbot_response
                return chatbot_response
            else:
                return f"4th -- Request failed with status code: {response.status_code}"
                #print(f"Request failed with status code: {response.status_code}")

            
        except:
            return f"EXCEPTION - No response available at this time response-code = {response.status_code}"
