from ibm_cloud_sdk_core.authenticators import BasicAuthenticator, IAMAuthenticator
from ibm_watson import AssistantV1
from pprint import pprint
from app import get_logs_by_conversations

#authenticator = IAMAuthenticator('D8fltBQ-OaVqdm9ByQ23LTIij8r34JczuEpCbiFc8RTb')
#assistant = AssistantV1(version='2020-04-01', authenticator=authenticator)
#assistant.set_service_url('https://api.eu-gb.assistant.watson.cloud.ibm.com')

#pprint(assistant.list_logs(workspace_id='c9c587b1-88a8-4a1f-b61c-77edc06d89d5').get_result())
#print(assistant.list_workspaces())

log_by_conversation = get_logs_by_conversations('processing/2020-04-23 20:48:19.666694/complete_result.json')

