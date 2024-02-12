from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from flask import Flask, render_template, request
import asyncio
import os
from dotenv import load_dotenv


if 'FUNCTIONS_EXTENSION_VERSION' not in os.environ:
        print("Loading environment variables for .env file")
        load_dotenv('./.env')

app = Flask(__name__)

async def run(user_gender,user_first,user_last):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=os.environ["EVENT_HUB_CONNECTION_STR"],
        eventhub_name=os.environ["EVENT_HUB_NAME"] 
    )
    async with producer:
        # Create a batch.
        #await asyncio.sleep(1)
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        user = {"results":
                    [
                        {
                        "gender": user_gender,
                        "name":
                            {
                                "first" :   user_first,
                                "last"  :   user_last
                            }
                        }
                    ]
                }
        event_data_batch.add(EventData(str(user)))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the data from the form
        user_gender = request.form['user_gender']
        user_first = request.form['user_first']
        user_last = request.form['user_last']


        asyncio.run(run(user_gender,user_first,user_last))
        # Display the data on the webpage
        return render_template('result.html', user_gender=user_gender,
                               user_first=user_first,
                               user_last=user_last)
    # Render the form on the webpage
    
    return render_template('form.html')



if __name__ == "__main__":
    app.run()


