from langchain.chat_models import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.config import settings
import requests


def evaluate_codes(codes):
    prompt = """
    You are a medical coding validation assistant.
    You have knowledge of ICD 10 AM and CPT codes.
    Your task is to evaluate the relevance of multiple CPT codes against multiple ICD-10 codes.
    you must not be chatty, just give the output in the format specified below.
    Follow the instructions carefully:

    1. You will receive input as {codes}.
    2. Evaluate the relevance of each CPT code against each ICD-10 code by using summary of each code.
    3. Relevance is determined as:
        - If a CPT code is not relevant to each ICD-10 codes, it should be considered as irrelevant.
        - If a CPT code is relevant to even a single ICD-10 code, it should be considered as relevant
    4. If all CPT codes are relevant, then give output strictly in this format:
    - All CPT codes are relevant to ICD codes
    5. If there are irrelevant CPT codes, then give output strictly in this format in the form of bullet points listing only irrelevant CPT codes:
    - 99201
    - 45380
    6. The input format for ICD-10 code is that it consists of a letter, followed by numbers, a decimal point, and additional characters for further specification of the condition (Example: A01.0).
    7. The input format for CPT code is that it consists of a 5-digit numeric code used to represent medical, surgical, and diagnostic procedures or services (Example: 99213).
    8. If the input is malformed or does not follow the above formats, return:
    Invalid input

    Input {codes}
    """
    content_prompt = ChatPromptTemplate.from_template(prompt)
    model = ChatOpenAI(
            model='gpt-4',
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
    parser = StrOutputParser()
    chain = content_prompt | model | parser
    response = chain.invoke({"codes": codes})
    return response if response else None



def get_code_description(codes):
    url = f"https://medical-codes-542808340038.us-central1.run.app/get_icd_descriptions?codes={codes}"

    payload = {'codes': codes}

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Error: Received status code {response.status_code}"
    
    except Exception as e:
        return f"Error: {str(e)}"
    

# Add these helper functions at the top with other functions
def get_relevant_codes(cpt_codes, irrelevant_codes):
    """Get list of relevant CPT codes by excluding irrelevant ones"""
    irrelevant_set = set(code.strip() for code in irrelevant_codes)
    return [code for code in cpt_codes if code not in irrelevant_set]