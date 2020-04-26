

if __name__ == "__main__":
    from app import *
    from pprint import pprint
    
    assistant           = get_assistant('D8fltBQ-OaVqdm9ByQ23LTIij8r34JczuEpCbiFc8RTb')

    complete_log        = get_logs(assistant, 'c9c587b1-88a8-4a1f-b61c-77edc06d89d5')
    log_by_conversation = get_logs_by_conversations(complete_log)
