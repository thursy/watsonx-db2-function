#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import json
import os, ibm_db, ibm_db_dbi as dbi, pandas as pd
import requests

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams


###=======================Main function====================================
def main(params):
    user_query = params['user_query']
    
    db2_dsn = 'DATABASE={};HOSTNAME={};PORT={};PROTOCOL=TCPIP;UID={uid};PWD={pwd};SECURITY=SSL'.format(
        'bludb',
        'XXXX.databases.appdomain.cloud',   #host
        'XXXX',         #Port
        uid='XXXX',     #username
        pwd='XXXX'      #password
    )
    
    db2_connection = dbi.connect(db2_dsn)
    
    ## FIRST QUERY - Turn the user input to SQL query using prompting
    example_query = """user question: what is the average modal price for banana
    JSON output: {"query": "SELECT AVG(MODAL_PRICE) as AVG_MODAL_PRICE FROM HXK89399.INVENTORY WHERE COMMODITY = 'Banana'"}

    user question: what is the average modal price for all commodities
    JSON output: 
    {"query": "SELECT AVG(MODAL_PRICE) as AVG_MODAL_PRICE FROM HXK89399.INVENTORY"}

    user question: what is the maximum price for potato in Gujarat
    JSON output: 
    {"query": "SELECT MAX(MAX_PRICE) as MAX_PRICE FROM HXK89399.INVENTORY WHERE STATE = 'Gujarat' AND COMMODITY = 'Potato'"}

    user question:  which comodity is the most expensive?
    JSON ouput: 
    {"query": "SELECT COMMODITY, MAX(MAX_PRICE) as MAX_PRICE FROM HXK89399.INVENTORY GROUP BY COMMODITY ORDER BY MAX_PRICE DESC LIMIT 1"}"""

    prompt_query = f"""Generate an SQL query If we have table with this information 
    table: "agri"."inventory"
    columns: STATE, DISTRICT, MARKET, COMMODITY, VARIETY, ARRIVAL_DATE, MIN_PRICE, MAX_PRICE, MODAL_PRICE
    Provide the query in JSON format.

    example: {example_query}

    user question: {user_query}
    JSON output:
    """
    response = send_to_watsonxai(prompts=[prompt_query])
    response = json.loads(response.strip())

    
    ##QUERY to DB2
    query = response["query"]
    answer_df = pd.read_sql_query(query, con=db2_connection)
    answer = answer_df.to_dict(orient="records")
    #answer = [{"MAX_PRICE":"24000"}]

    ## SECOND QUERY
    output_format = "{answer:}"

    prompt_answering=f"""
    user question: {user_query}
    query result: {answer}

    Generate the answer in engaging style, if the user question and query result is given above. 
    create output in this format {output_format}

    Json output:
    """
    response = send_to_watsonxai(prompts=[prompt_answering])
    response = json.loads(response.strip())
    
    return response
    

###=========================HELPER FUNCTION=============================================    
def send_to_watsonxai(prompts,
                    model_name='meta-llama/llama-2-70b-chat',
                    decoding_method="greedy",
                    max_new_tokens=100,
                    min_new_tokens=1,
                    temperature=1.0,
                    repetition_penalty=1.0,
                    stop_sequences=["\n\n"]
                    
                    ):
    '''
   helper function for sending prompts and params to Watsonx.ai
    
    Args:  
        prompts:list list of text prompts
        decoding:str Watsonx.ai parameter "sample" or "greedy"
        max_new_tok:int Watsonx.ai parameter for max new tokens/response returned
        temperature:float Watsonx.ai parameter for temperature (range 0>2)
        repetition_penalty:float Watsonx.ai parameter for repetition penalty (range 1.0 to 2.0)

    Returns: None
        prints response
    '''

    assert not any(map(lambda prompt: len(prompt) < 1, prompts)), "make sure none of the prompts in the inputs prompts are empty"

    # Instantiate parameters for text generation
    model_params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: temperature,
        GenParams.REPETITION_PENALTY: repetition_penalty,
        GenParams.STOP_SEQUENCES: stop_sequences
    }

    api_key =  "XXXX"   #IBM Cloud API Key
    ibm_cloud_url = "https://us-south.ml.cloud.ibm.com"
    project_id = "XXXX" #Project ID watsox.ai

    creds = {
        "url": ibm_cloud_url,
        "apikey": api_key 
    }

    # Instantiate a model proxy object to send your requests
    model = Model(
        model_id=model_name,
        params=model_params,
        credentials=creds,
        project_id=project_id)


    for prompt in prompts:
        output = model.generate_text(prompt)

    return output
