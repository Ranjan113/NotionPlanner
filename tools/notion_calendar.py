from langchain.tools import tool
import requests
import os

@tool
def get_calendar_events(date:str) -> dict:
    """
    This tool will get calendar events for a specific date (YYYY-MM-DD) from Notion
    """
    api_key = os.getenv('NOTION_API_KEY')
    db_id = os.getenv('NOTION_CALENDAR_DB_ID')

    if not api_key or not db_id:
        return ("Error: Notion API key or DB id not set")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    url = f"https://api.notion.com/v1/databases/{db_id}/query"

    payload = {
        "filter" : {
            "property" : "Date",
            "date" : {
                "equals" : date
            }
        }
    }

    try:
        res = requests.post(url,headers=headers,json=payload)
        res.raise_for_status()
        data = res.json()
        print(data)

        events = []

        for page in data.get("results",[]):
            props = page.get("properties",[])

            #  Extract the Event name
            event_title_list = props.get("Event",{}).get("title",[])
            event_name = event_title_list[0].get("text",{}).get("content","") if event_title_list else "Untitled event"

            # Extract the time of the event
            time_list = props.get("Time",{}).get("rich_text",[])
            event_time = time_list[0].get("text",{}).get("content","") if time_list else "All day"

            events.append({
                "event":event_name,
                "time":event_time
            })
        return {"events":events, "date":date}
    
    except Exception as e:
        return f"Error: {str(e)}"
    

@tool
def add_calendar_events(date:str, time:str, event:str) -> str:
    """
    this tool will be used to add calendar events in notion
    You have to provide data (YYYY-MM-DD), time(HH:MM), event(description)
    """
    api_key = os.getenv('NOTION_API_KEY')
    db_id = os.getenv('NOTION_CALENDAR_DB_ID')

    if not api_key or not db_id:
        return ("Error: Notion API key or DB id not set")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    url = "https://api.notion.com/v1/pages"

    start_datetime = f"{date}T{time}:00" if time else date

    payload = {
        "parent": {"database_id":db_id},
        "properties": {
            "Event":{
                "title": [{"text":{"content":event}}]
            },
            "Date":{
                "date":{"start":start_datetime}
            }
        }
    }

    try:
        res = requests.post(url,headers=headers,json=payload)
        res.raise_for_status()
        return f"Added Event:{event} at {time} on {date} "
    
    except Exception as e:
        return f"Error: {str(e)}"
    