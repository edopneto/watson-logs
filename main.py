

if __name__ == "__main__":
    from app import *
    
    assistant           = get_assistant()
    complete_log        = get_logs(assistant)
    log_by_conversation = get_logs_by_conversations(complete_log)
