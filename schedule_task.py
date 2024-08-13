import subprocess

task_name = "RunNewsPodcast"
task_time = "12:35"

# Path to the batch file created in step 1
batch_file_path = r"aipodcast\news_pipeline\run_news_podcast.bat"

# Command to create a scheduled task
create_task_command = (
    f"schtasks /create /tn {task_name} /tr {batch_file_path} /sc daily /st {task_time} /f"
)

try:
    subprocess.run(create_task_command, check=True, shell=True)
    print(f"Scheduled task '{task_name}' created successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to create scheduled task '{task_name}': {e}")

# To delete the task, use the following command
# delete_task_command = f"schtasks /delete /tn {task_name} /f"
# subprocess.run(delete_task_command, check=True, shell=True)
