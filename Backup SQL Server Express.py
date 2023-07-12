from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import subprocess, os
import smtplib

host = "127.0.0.1\\sqlInstanceHere"
backupPath = "C:\\backups\\"
daysToKeep = 7

databases = [] #Your database names here
fileSizes = []

def runQuery(query):
	return subprocess.getoutput(f'SQLCMD.EXE -S {host} -E -Q "{query}"')

def createFolder(folderName):
	folderPath = f"{backupPath}{folderName}"
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)

def deleteOlderLogs(database):
	try:
		filename = f"{backupPath}{database}\\{database}-{(datetime.now() - timedelta(days=limit)).strftime('%Y-%m-%d')}.bak"
		os.remove(filename)
		return True

	except Exception as error:
		return error

def sendMail(body):
	try:
		msg = MIMEMultipart()
		msg['Subject'] = "Backup alert"
		msg['From'] = 'from@from.com'
		msg['To'] = "to@to.com"

		msg.add_header('Content-Type','text/html')
		msg.attach(MIMEText(body, 'html'))

		mailserver = smtplib.SMTP('smtp.addr.here', 587)
		mailserver.connect('smtp.addr.here', 587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login('from@from.com', 'pass')
		mailserver.sendmail(msg['From'], [msg['To']], msg.as_string())
		mailserver.quit()		
		
		return True

	except Exception as error:
		return error

def getSize(path):
        size = os.path.getsize(path)
        if size < 1024:
            return f"{size} bytes"
        
        elif size < pow(1024,2):
            return f"{round(size/1024, 2)} KB"

        elif size < pow(1024,3):
            return f"{round(size/(pow(1024,2)), 2)} MB"

        elif size < pow(1024,4):
            return f"{round(size/(pow(1024,3)), 2)} GB"

try:
	for database in databases:
		filename = f"{backupPath}{database}\\{database}-{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.bak"
		createFolder(database)
		deleteOlderLogs(database)
		backupDatabaseCommand = runQuery(f"BACKUP DATABASE {database} TO DISK = '{filename}';")		
		if "BACKUP DATABASE successfully" not in backupDatabaseCommand or False:
			raise ValueError(f"An error ocurred when backing up the database {database}. <br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Message</b>: {backupDatabaseCommand}")
		
		else:
			fileSize = f"<b>{database}</b>: {getSize(filename)}.<br />"
			fileSizes.append(fileSize)
		
		continue

except Exception as error:	
	sendMail(f"""
		The backup routine did not run successfully. Check the following log for more details.<br /><i>
		<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{str(error)}
		</i>
	""")

else:
	sendMail(f"""
		The backup routine was executed successfully on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
		<br /> <br />Log files size:<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'.join(fileSizes)}
	""")