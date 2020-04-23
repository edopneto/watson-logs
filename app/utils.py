import os
from json       import dumps, dump, load
from pprint     import pprint
from uuid       import uuid4
from pathlib    import Path
from datetime   import datetime
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator



def get_assistant(
    apikey:str=None,
    version:str='2020-04-01',
    service_locale:str='https://api.eu-gb.assistant.watson.cloud.ibm.com',
    authenticator=IAMAuthenticator,
    assistant_class=AssistantV1,
    *args,
    **kwargs) -> AssistantV1:
    
    if not apikey: apikey = os.environ.get('WATSON_IAM_APIKEY', None)
    if not apikey: raise RuntimeError("Verifique o parâmetro 'apikey'.")
    
    assistant = assistant_class(
        version=version,
        authenticator=authenticator(apikey)
    )

    assistant.set_service_url(service_locale)

    return assistant


def get_logs(
    assistant:AssistantV1,
    workspace_id:str=None,
    cursor:str=None,
    processing_result=[],
    iteration:int=1,
    saving:bool=True,
    saving_destiny:str='processing',
    *args,
    **kwargs
    ):
    if not workspace_id: workspace_id = os.environ.get('WATSON_WORKSPACE_ID', None)
    if not workspace_id: raise RuntimeError("Verifique o parâmetro 'workspace_id'.")
    
    print("\n\nIteração {}".format(iteration))
    
    response = assistant.list_logs(
        workspace_id=workspace_id,
        cursor=cursor
        ).get_result()
    
    if not 'logs' in response or not response['logs']:
        return processing_result
     
    print("Adicionando {} interações!".format(len(response['logs'])))

    processing_result.extend(response['logs'])
    
    print("Total de {} interações!".format(len(processing_result)))

    """
    Verificando se podemos paginar os resultados:
    """
    if 'pagination' in response and 'next_cursor' in response['pagination'] and\
        response['pagination']['next_cursor'] != cursor:

        # Atribuindo novo valor ao cursor:
        cursor = response['pagination']['next_cursor']

        return get_logs(assistant, workspace_id, cursor=cursor, iteration=iteration+1)

    print("Finalizado!")
    
    if saving: 
        return save_data(processing_result, 'complete_result')
    
    return processing_result


def get_diff_conversations(
    file_path:str,
    *args,
    **kwargs):
    
    data = load_data(file_path)
    conversations = set()

    for element in data:
        try:
            conversations.add( element['response']['context']['conversation_id'] )
        except Exception as err:
            continue
      
    return list(conversations)


def get_logs_by_conversations(
    data,
    saving:bool=True,
    *args,
    **kwargs):
    
    if isinstance(data, str): data = load_data(data)

    conversations = {}

    for element in data:
        try:
            id = element['response']['context']['conversation_id'] 
            conversations[id] = element
        except Exception as err:
            continue
    
    if saving:
        return save_data(conversations, 'log_by_conversation')
    
    return conversations


def save_data(
    data,
    name=str(uuid4()), 
    tag=datetime.now,
    path='processing',
    *args,
    **kwargs):
    """
    Função para salvar os dados extraídos da API do Watson em um arquivo no File System.

    :data: dados a serem salvos
    
    :name: nome do arquivo

    """
    tag = tag() if callable(tag) else str(tag)

    if not isinstance(tag, str): tag = str(tag)
    
    path = '{}/{}'.format(path, tag)

    if not os.path.exists(path):    os.makedirs(path)
    if not name.endswith('.json'):  name = '{}.json'.format(name)

    file_path = str(Path('{}/{}'.format(path, name)))
            
    with open(file_path, 'w') as file:
        dump(data, file, ensure_ascii=False)
    
    return file_path


def load_data(file_path, *args, **kwargs):
    with open(file_path) as json_file:
        return load(json_file)
