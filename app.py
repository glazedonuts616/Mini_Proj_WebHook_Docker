import os

# Ensure the directory exists
os.makedirs('/opt/mini_proj', exist_ok=True)

# Create the log file if it doesn't exist
log_path = '/opt/mini_proj/log.txt'
if not os.path.exists(log_path):
    with open(log_path, 'w') as f:
        f.write("Log file created.\n")

# Create the Flask app
from flask import Flask, request, render_template
import json

app = Flask(__name__)

request_counter = 0
def read_log_file():
    if os.path.exists('/opt/mini_proj/log.txt'):
        with open('/opt/mini_proj/log.txt', 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Return empty list if file is empty or corrupted
    return []


def read_yoni_file():
       if os.path.exists("C:/Users/admin/Documents/DevOps/Mini_Project_Webhook/log2.txt"):
        with open("C:/Users/admin/Documents/DevOps/Mini_Project_Webhook/log2.txt", 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  # Return empty list if file is empty or corrupted
       return []

@app.route('/')
def hello_world():
    global request_counter
    request_counter += 1
    hostname = request.headers.get('Host')
    return f'Hello, World! my server is: {hostname} and request count is: {request_counter}'

@app.route('/webhook', methods=['POST'])
def webhook():
    print(f"Received webhook data", flush=True)
    webhook_data = request.get_json()

    if webhook_data:
        repository_name = webhook_data.get('repository', {}).get('name', 'Unknown repository')
        pusher_name = webhook_data.get('pusher', {}).get('name', 'Unknown pusher')
        
        # Safely access the first commit if it exists
        commits = webhook_data.get('commits', [])
        if commits:
            first_commit = commits[0]
            commit_id = first_commit.get('id', 'Unknown Commit ID')
            added_files = first_commit.get('added', 'No Added Files')
            modified_files = first_commit.get('modified', 'No Modified Files')
            removed_files = first_commit.get('removed', 'No Removed Files')
        else:
            commit_id = 'Unknown Commit ID'
            added_files = 'No Added Files'
            modified_files = 'No Modified Files'
            removed_files = 'No Removed Files'

        # Create a filtered data dictionary
        filtered_data = {
            'repository_name': repository_name,
            'pusher_name': pusher_name,
            'commit_id': commit_id,
            'changes_to_files': [
                {
                    "added_files": added_files,
                    "modified_files": modified_files,
                    "removed_files": removed_files
                }
            ]
        }

        log_file_path = '/opt/mini_proj/log.txt'

        # Step 1: Load existing data or initialize as an empty list if file does not exist or is empty
        try:
            with open(log_file_path, 'r') as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        # Step 2: Append the new data
        existing_data.append(filtered_data)
        app.webhook_display_data = existing_data

        # Step 3: Write the updated list back to the file
        with open(log_file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)
            f.write('\n')

    # if webhook_data:
    #     repository_name = webhook_data.get('repository', {}).get('name', 'Unknown repository')
    #     pusher_name = webhook_data.get('pusher', {}).get('name', 'Unknown pusher')
    #     commit_id = webhook_data.get('commits'[0], {}).get('id', 'Unknown Commit ID')
    #     added_files= webhook_data.get('commits'[0], {}).get('added', 'No Added Files')
    #     modified_files= webhook_data.get('commits'[0], {}).get('modified', 'No Modified Files')
    #     removed_files= webhook_data.get('commits'[0], {}).get('removed', 'No Removed Files')
    # if webhook_data:
    #     repository_name = webhook_data.get('repository', {}).get('name', 'Unknown repository')
    #     pusher_name = webhook_data.get('pusher', {}).get('name', 'Unknown pusher')
    
    # # Safely access the first commit if it exists
    #     commits = webhook_data.get('commits', [])
    #     if commits:  # Check if there is at least one commit
    #         first_commit = commits[0]
    #         commit_id = first_commit.get('id', 'Unknown Commit ID')
    #         added_files = first_commit.get('added', 'No Added Files')
    #         modified_files = first_commit.get('modified', 'No Modified Files')
    #         removed_files = first_commit.get('removed', 'No Removed Files')
    #     else:
    #         # Handle the case where there are no commits
    #         commit_id = 'Unknown Commit ID'
    #         added_files = 'No Added Files'
    #         modified_files = 'No Modified Files'
    #         removed_files = 'No Removed Files'

        # filtered_data = {
        #     'repository_name': repository_name,
        #     'pusher_name': pusher_name,
        #     'commit_id': commit_id,
        #     'changes_to_files': [
        #         {
        #             "added_files": added_files,
        #             "modified_files": modified_files,
        #             "removed_files": removed_files
        #         }
        #     ]
        # }

        
    # # try:
    # #     with open('/opt/mini_proj/log.txt', 'r') as f:
    # #         existing_data = json.load(f)  # Load existing data
    # # except (FileNotFoundError, json.JSONDecodeError):
    # #     existing_data = []  # Start with an empty list if the file doesn't exist or is invalid

    # # existing_data.append(filtered_data)  # Append new data

    # # with open('/opt/mini_proj/log.txt', 'w') as f:
    # #     json.dump(existing_data, f, indent=4)  # Write back as a JSON array
    #     # Save the filtered data to a JSON file
    #     with open('/opt/mini_proj/log.txt', 'a') as f:
    #         json.dump(filtered_data, f, indent=4)
    #         f.write('\n')

        return 'Webhook received and filtered data saved', 200

    return 'Webhook received but no data', 200

@app.route('/webhooks')
def show_webhooks():
    if os.path.exists('/opt/mini_proj/log.txt'):
        with open('/opt/mini_proj/log.txt', 'r') as f:
            webhook_data = json.load(f)
            if webhook_data:
                webhook_data = json.dumps(webhook_data, indent=4)
    else:
        webhook_data = 'No webhook data received yet'
    return webhook_data 

@app.route('/webhooks_data', methods=['GET'])
def display_webhooks_data():
# #     # data = app.webhook_display_data if hasattr(app, 'webhook_display_data') else {}
# #     # return render_template('webhook_data.html', **data)
# #     # Pass existing_data as part of a dictionary
# #     # Read all existing data from log.txt and pass it to the template
# #     # data = read_log_file()
#     # Safely retrieve changes_to_files or use an empty list as a fallback
    changes_to_files = app.webhook_display_data if hasattr(app, 'webhook_display_data') else []
    data=changes_to_files
    data
    print("Changes to files:", changes_to_files)  # For debugging
    return render_template('webhook_data.html', changes_to_files=changes_to_files)
# def display_webhooks_data():
    # Check if webhook_display_data is set; if not, use an empty list
    # data = app.webhook_display_data if hasattr(app, 'webhook_display_data') else []
    
    # Initialize a list to hold commit information
    # commits_info = []

    # Iterate over each commit in the data (assuming it's a list of commits)
    # for commit in data:
    #     # Safely retrieve the fields for each commit or set to default values
    #     changes_to_files = commit.get('changes_to_files', [])
    #     repository_name = commit.get('repository_name', 'Unknown repository')
    #     pusher_name = commit.get('pusher_name', 'Unknown pusher')
    #     commit_id = commit.get('commit_id', 'Unknown Commit ID')
        
    #     # Append the information as a dictionary to the commits_info list
    #     commits_info.append({
    #         'changes_to_files': changes_to_files,
    #         'repository_name': repository_name,
    #         'pusher_name': pusher_name,
    #         'commit_id': commit_id
    #     })

    # return render_template('webhook_data.html', commits=commits_info)

#     # data = read_yoni_file()
#     # return render_template('webhook_data.html', webhooks=data)
#     @app.route('/webhooks_data', methods=['GET'])
# def display_webhooks_data():
#     data = app.webhook_display_data if hasattr(app, 'webhook_display_data') else {}
    
#     # Safely retrieve the fields or set to a default
#     changes_to_files = data.get('changes_to_files', [])
#     repository_name = data.get('repository_name', 'Unknown repository')
#     pusher_name = data.get('pusher_name', 'Unknown pusher')
#     commit_id = data.get('commit_id', 'Unknown Commit ID')

#     return render_template('webhook_data.html', changes_to_files=changes_to_files, repository_name=repository_name, pusher_name=pusher_name, commit_id=commit_id)
# def display_webhooks_data():
#     log_file_path = '/opt/mini_proj/log.txt'
#     if os.path.exists(log_file_path):
#         with open(log_file_path, 'r') as f:
#             existing_data = json.load(f)
#     else:
#         existing_data = []

#     return render_template('webhook_data.html', commits=existing_data)




@app.route('/log')
def show_log():
    log_file_path = '/opt/simpleFlask/app.log'
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            log_data = f.read()
        return f"<pre>{log_data}</pre>"
    return 'No log data available'

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
