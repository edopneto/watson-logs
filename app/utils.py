import os
from json       import dumps, dump, load
from pprint     import pprint
from uuid       import uuid4
from pathlib    import Path
from datetime   import datetime
from ibm_watson import AssistantV2, AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator, BasicAuthenticator



def get_assistant(
    apikey:str=None,
    version:str='2020-04-01',
    service_locale:str='https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/0ba07a41-559b-4434-b0c8-d1cfffdd4ba5',
    authenticator=IAMAuthenticator,
    assistant_class=AssistantV1,
    *args,
    **kwargs) -> AssistantV1:
    
    if not apikey: apikey = os.environ.get('WATSON_IAM_APIKEY', None)
    if not apikey: raise RuntimeError("Verifique o parâmetro 'apikey'.")
        
    authenticator = authenticator(apikey)

    assistant = assistant_class(
        version=version,
        authenticator=authenticator,
    )

    assistant.set_service_url(service_locale)

    return assistant


def get_logs(
    assistant,
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
    
    if cursor:
        response = assistant.list_logs(
            workspace_id=workspace_id,
            cursor=cursor
            ).get_result()
    
    else:
        response = assistant.list_logs(workspace_id=workspace_id).get_result()

    if not 'logs' in response or not response['logs']:
        input("...")
        return processing_result
    
    response['logs'] = list(filter(lambda element: element['workspace_id'] == workspace_id, \
        response['logs'] ))
    
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
    batch_size=50,
    *args,
    **kwargs):
    
    if isinstance(data, str): data = load_data(data)

    conversations = {}

    for element in data:
        id = element['response']['context']['conversation_id'] 

        if not id in conversations: conversations[id] = []

        conversations[id].append(element)

    if saving:
        tag = datetime.now()
        # Quebrando em vários arquivos:
        indexes = list(conversations.keys())

        while len(indexes):
            until = batch_size if batch_size < len(indexes) else batch_size - len(indexes)
            
            save_data(
                    data={key: conversations[key] for key in indexes[:until]},
                    name=str(uuid4()),
                    tag=tag
                    )
            indexes = indexes[until:]

        return True
    
    return conversations


def filter_keys_log(element:dict, *args, **kwargs):
    #element['request'] = {'input':}
    pass


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
