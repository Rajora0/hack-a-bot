import re
import os
import json
import openai

model_engine = "gpt-3.5-turbo-0301"
openai.api_key = os.environ["OPENAI_API_KEY"]

prompt = '''

Problema cliente, palavras-chave, soluções, comunicação clara, eficiência, sentimento final e um template dentro dos disponiveis.
Retorne somente um JSON no seguinte no formato:

{ 
"resume": "text",
"problem_identification": "text",
"sentiment_analysis": "negative" / "positive" / "mixed" / "neutral",
"relevant_topics": ["unique words with max 3"],
"solution_suggestion": ["short phrases with max 2"],
"template_response": ["Contatos de suporte" | "Problemas com financeiro" | "Problemas especificos" | "Não identificado"]
}

'''

def validate_json_format(json_data):
    """
    Validates if a JSON dictionary has the required keys and values.

    Parameters:
    json_data (dict): the JSON dictionary to be validated

    Returns:
    bool: True if the dictionary is validated or False if it is not.

    Example:
    >>> validate_json_format({"resume": "text", "problem_identification": "text", "sentiment_analysis": "negative", "relevant_topics": ["unique words with max 3"], "solution_suggestion": ["short phrases with max 2"]})
    True
    """
    required_keys = [
        "resume",
        "problem_identification",
        "sentiment_analysis",
        "relevant_topics",
        "solution_suggestion",
        "template_response"
    ]

    if not all(key in json_data for key in required_keys):
        return False

    if not isinstance(json_data["sentiment_analysis"], str):
        return False

    sentiments = {"negative", "positive", "mixed", "neutral"}
    if json_data["sentiment_analysis"] not in sentiments:
        return False

    if not isinstance(json_data["relevant_topics"], list):
        return False

    if not isinstance(json_data["solution_suggestion"], list):
        return False


    return True

def extract_json_from_text(text):
    """
    Extracts a JSON dictionary from a string using regular expressions.

    Parameters:
    text (str): the string containing the JSON dictionary

    Returns:
    dict: the extracted JSON dictionary

    Example:
    >>> extract_json_from_text("{ "resume": "text", "problem_identification": "text", "sentiment_analysis": "negative", "relevant_topics": ["unique words with max 3"], "solution_suggestion": ["short phrases with max 2"]}")
    {"resume": "text", "problem_identification": "text", "sentiment_analysis": "negative", "relevant_topics": ["unique words with max 3"], "solution_suggestion": ["short phrases with max 2"]}
    """
    
    pattern = re.compile(r'\{.*?\}')
    json_str = pattern.search(str(text).replace('\n', '')).group(0)
    dicionario_response = json.loads(json_str)
    return dicionario_response

def text_suporte(text):
    """
    Sends a request to the OpenAI Chat API and returns the response in JSON format.

    Parameters:
    text (str): the text message to be sent to the API

    Returns:
    dict: the JSON response from the API containing the resume, problem identification, sentiment analysis, relevant topics, and solution suggestion.

    Example:
    >>> chatgpt("Customer problem, keywords, solutions, clear communication, efficiency.")
    {"resume": "text", "problem_identification": "text", "sentiment_analysis": "negative" / "positive" / "mixed" / "neutral", "relevant_topics": ["unique words with max 3"], "solution_suggestion": ["short phrases with max 2"]}
    """
    success = False
    assistant_response = None
    contador = 0

    while not success:
        try:
            messages = [{"role": "system", "content": prompt}, {"role": "user", "content": text}]
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            assistant_response = dict(response["choices"][0])["message"]["content"]

            
            if contador >= 5:
                print("Sorry, but you have exceeded the limit of attempts... Reformulate the text and try again.")
                return { 
                        "resume": "Sorry, but you have exceeded the limit of attempts... Reformulate the text and try again. Could not extract from text: " + text,
                        "problem_identification": "Could not identify",
                        "sentiment_analysis": "neutral",
                        "relevant_topics": ["Could not identify"],
                        "solution_suggestion": ["Could not identify"],
                        "template_response":["Could not identify"]
                        }

            contador = contador + 1
            
            
            json_data = extract_json_from_text(assistant_response)

            if validate_json_format(json_data):
                success = True
            else:
                print("O JSON não está no formato esperado. Tentando novamente...")
                
            

        except Exception as e:
            print(f"Erro ao chamar a API: {e}")
            print("Tentando novamente...")

    return json_data


