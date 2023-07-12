# SQL-Server-Express-Backup

This script will help you to create a fully automated backup for your SQL Server Express database.
It will work on any version of SQL server, but since the Express version doesn't support an SQL Server Agent, you can't create a routine using the SSMS, So you can use this script instead.


### How to

1. Download the `Backup SQL Server Express.py` file.
2. Change the required variables and data, those being:
   - host (Your SQL instance. Example: "127.0.0.1\\SQL1".
   - databases (Your databases name. You can change the script to automatically fetch all your databases if you wish).
   - backupPath (Your backup folder. The script will create a folder for every database in your databases list.
   - daysToKeep (The script will automatically delete any log file older than this value in days. The script does not look recursively for every day, it just deletes one file, be aware).
   - sendMail() function (This script sends an e-mail with the error message in case of error, and file sizes in case of success. But first you need to configure the SMTP login for it to work).
  
3. (Optional, but recommended): Compile your final code as an .exe file. It's pretty simple, just as follows:
  - Install nuitka using `pip install nuitka3`
  - Compile it using, for example, this command: `nuitka --show-progress --onefile "Backup SQL Server Express.py" --onefile --output-filename=Backup.exe --mingw64 --remove-output`

4. Create a recurrent task using Windows Task scheduler. You can read and tutorial [here](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10).

This script was made for my personal use-case, it might require some changes for your environment, but it's pretty simple and easy to do so.
