from pycamunda.processinst import StartInstance, Variable
import requests

# URL to your Camunda engine
url = 'http://localhost:8080/engine-rest'

# Define variables that would be sent to the process
variables = {
    'sender_account_number': Variable(value='123456', type='String'),
    'receiver_account_number': Variable(value='654321', type='String'),
    'amount': Variable(value=100.50, type='Double')
}

# Start a process instance
start_instance = StartInstance(
    url=url,
    key='Process_1',  # BPMN Process ID
    variables=variables
)

# Execute the process
response = start_instance()

# Check if the process was started successfully
if response:
    print(f'Process instance started with ID: {response.id}')
else:
    print('Failed to start the process instance.')
