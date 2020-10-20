# todoist-discord
This repo transforms your Todoist tasks into a text task list (especially useful for Discord)

### What you need:
* Todoist premium
* Python interpreter 2.7
* Bash shell (optional but if you do not have it, you have to do the work manually)

### What you will obtain:
A text task list for the tasks of the current date, ordered by priority and start time (midnight if not declared). The tasks will be divided between normal tasks and recurring tasks.

### How it works:
The shell script will be executed first, it will erase txt files from the previous days (only the files needed for this system) and will create a fresh one for the current date (the file name will be formatted as YYYYMMDD.txt), then a python script will be launched. It will retrieve data from your account, will save the IDs of the tasks of the day (so that it can keep track of migrated tasks) into the txt file and will check the status of each tasks. Next, it will sort them as mentioned above and finally it will put together a long string with all your tasks that will be copied to your clipboard

### What you need to do:
* Insert the shell script in your default working directory (just for simplicity)
* Paste the directory where you store the txt files in the shell script and in the python script
* Paste your Todoist token in the python script
* Tweak the scripts to your liking
