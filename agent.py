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
    'request_timeout': 120,
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
                   "examples where possible.",
)


def readfile(filename):
    with open(filename, 'r') as file:
        title = file.readline()
        content = file.read()

    task = f'''Topic is: {title}'''

    return content, task


def explain(filename):
    content, task = readfile(filename)
    user_proxy = autogen.UserProxyAgent(
        name='user_proxy',
        human_input_mode='ALWAYS',
        system_message=''' ''',
        is_termination_msg=lambda x: x.get('content', '').rstrip().endswith('TERMINATE'),
        code_execution_config={'workdir': 'web'},
        llm_config=llm_config,
    )

    user_proxy.initiate_chat(
        Explainer,
        message=task,
    )


def main():
    file = 'summary.txt'
    explain(filename=file)


if __name__ == '__main__':
    main()
