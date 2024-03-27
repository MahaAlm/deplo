from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
import pandas as pd
from io import StringIO
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import openai
import io
import time
import os
import openai
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_api_key = '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'


def chat_with_csv(df,prompt):
    print(openai_api_key)
    llm = OpenAI(api_token=openai_api_key)
    df = SmartDataframe(df, config={"llm": llm})
    result = df.chat(prompt)
    print(result)
    return result

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Automatically accept incoming connection
        
        await self.accept()
        # Get session key from the scope's cookies (Assuming sessionid is the key)
        self.session_key = self.scope['cookies'].get('sessionid')

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']
        csv_data = text_data_json.get('csvData', '')

        
        # Convert CSV data from string back into DataFrame
        if csv_data:
            client = openai.OpenAI(api_key=openai_api_key)

            ids = []
            print('openai_api_key: ', openai_api_key)

            for csv in csv_data:
                csv_binary = io.BytesIO((csv).encode('utf-8'))
                file = client.files.create(
                    file=csv_binary,
                    purpose='assistants'
                )
                
                
                ids.append(file.id)
            
            print(ids)
            # Step 1: Create an Assistant
            assistant = client.beta.assistants.create(
                name="Data Analyst Assistant",
                instructions="You are a personal Data Analyst Assistant",
                model="gpt-4-1106-preview",
                tools=[{"type": "code_interpreter"}],
                file_ids=ids
            )
            thread = client.beta.threads.create()
            
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content= msg
            )
            
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )

            while True:
                # Wait for 5 seconds
                time.sleep(5)

                # Retrieve the run status
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

                # If run is completed, get messages
                if run_status.status == 'completed':
                    messages = client.beta.threads.messages.list(
                        thread_id=thread.id
                    )

                    last_content = messages.data[0].content[0].text.value
                    print(last_content)
                    break
                else:
                    print("Waiting for the Assistant to process...")
                    time.sleep(5)

            response = f"{last_content}"
        else:
            response = "No CSV data provided."

        await self.send(text_data=json.dumps({'message': response}))
        

class EchoGraphsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Automatically accept incoming connection
        
        await self.accept()
        # Get session key from the scope's cookies (Assuming sessionid is the key)
        self.session_key = self.scope['cookies'].get('sessionid')

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']
        csv_data = text_data_json.get('csvData', '')
        


        
        # Convert CSV data from string back into DataFrame
        if csv_data:
            print('in channel')
            print('openai_api_key: ', openai_api_key)

            df = pd.read_csv(StringIO(csv_data))
            
            response = chat_with_csv(df, msg)
        await self.send(text_data=json.dumps({'message': response}))
        
def truncate_strings(df, max_length=20):
    """
    Truncate strings in a DataFrame if they are longer than max_length.
    """
    for col in df:
        df[col] = df[col].apply(lambda x: x if not isinstance(x, str) else (x[:max_length] + '...') if len(x) > max_length else x)
    return df

class EchoModifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Automatically accept incoming connection
        
        await self.accept()
        # Get session key from the scope's cookies (Assuming sessionid is the key)
        self.session_key = self.scope['cookies'].get('sessionid')

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']
        csv_data = text_data_json.get('csvData', '')
        dataset_name = text_data_json['dataset_name']


        
        # Convert CSV data from string back into DataFrame
        if csv_data:
            print('in channel')
            print('openai_api_key: ', openai_api_key)

            df = pd.read_csv(StringIO(csv_data))
            
            response = chat_with_csv(df, msg)
            
            response_df = response.head(3) # Placeholder for actual DataFrame processing
            response_df_truncated = truncate_strings(response_df.copy())

            # Convert truncated first 3 rows to HTML
            preview_html = response_df_truncated.to_html(index=False, border=0, classes='preview_table')

            # Convert entire DataFrame to CSV
            response_csv = response.to_csv(index=False)
            
            # Send back the HTML and CSV as JSON
            await self.send(text_data=json.dumps({
                'preview': preview_html,
                'csv': response_csv,
                'dataset_name': dataset_name
            }))
        

