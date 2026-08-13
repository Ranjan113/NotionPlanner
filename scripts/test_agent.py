from dotenv import load_dotenv
from agent.bot import create_react_agent_custom

def main():
    load_dotenv()
    agent = create_react_agent_custom()

    query = "Tell me the weather of delhi"

    res = agent.invoke({"messages":[("user",query)]})

    print("\n Agent Response")
    print(res['messages'][-1].content)

if __name__ == "__main__":
    main()