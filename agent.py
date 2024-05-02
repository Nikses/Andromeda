# agent that explains the latest bill
import autogen
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('CHATGPT_API_KEY')
config_list = [
    {
        'model': 'gpt-3.5-turbo-16k',
        'api_key': api_key,
    }
]

llm_config = {
    'timeout': 120,
    'seed': 43,
    'config_list': config_list,
    'temperature': 0.9,
}


Explainer = autogen.AssistantAgent(
    name='Explainer',
    llm_config=llm_config,
    system_message="Given the full text of a bill, your task "
                   "is to analyze and summarize the bill in simple terms. Provide a brief overview of the key "
                   "provisions of the bill, and explain their potential real-life implications for the general public. "
                   "Focus on making your explanation accessible and relatable, using layman's terms and concrete "
                   "examples where possible. Add corresponding emojis in the beginning of each paragraph. ",
)


def readfile(filename):
    """Read the file and get it's content and title"""
    with open(filename, 'r') as file:
        title = file.readline()
        content = file.read()

    file.close()

    task = f'''Topic is: {title}'''

    return content, task


def explain(filename):
    """Use the agent to explain and write in new file"""
    content, task = readfile(filename)
    user_proxy = autogen.UserProxyAgent(
        name='user_proxy',
        human_input_mode='ALWAYS',
        system_message='''Say TERMINATE once finished. ''',
        is_termination_msg=lambda x: x.get('content', '').rstrip().endswith('TERMINATE'),
        code_execution_config={'use_docker': False},
        llm_config=llm_config,
    )

    chat_result = user_proxy.initiate_chat(
        Explainer,
        message=task,
    )

    with open('explained_logs/' + filename[13:-4] + '.txt', 'w') as file:
        file.write(str(chat_result))

    file.close()
