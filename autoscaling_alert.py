import boto3
import logging
import datetime
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
import json

#setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main(event, context):
        try:
                details=event['Records'][0]['Sns']['Message']
                detail=json.loads(details)
                header=['Item','Details']
                data = [('Description',detail["Description"]),('AccountId',detail["AccountId"]),('Event',detail["Event"]),('Cause',detail["Cause"])]
                sub='Event: '+detail["Event"]
                content = table_formation(header,data)
                mailer(content,sub)
        except Exception, e:
                mailer(e,"Error in autoscalling alert")
        return 0

def table_formation(header,data,opt="center"):
        html_str=''
        bg='white'
        if data:
                if header:
                        html_str+='<table border=1 cellspacing=0><tr bgcolor="009900">'
                        for value in header:
                                html_str+='<th align="'+opt+'">'+str(value)+'</th>'
                        html_str+='</tr>\n'

                for rows in data:
                        html_str+='\n<tr>'
                        for value in rows:
                           html_str+='<td align="'+opt+'" bgcolor="'+bg+'">'+str(value)+'</td>'
                        html_str+='</tr>'
                html_str+='</table>'
        else:
                html_str=''
        return html_str

def mailer(html,sub):
        today = datetime.date.today()
        msg = MIMEMultipart()
        msg['From'] = '<FROM ADDRESS>'
        msg['To'] = '<TO ADDRESS>'
        msg['Subject'] = sub
        #message = "<h> Hi,<br><br> <h> Please find AWS autoscaled event . <br> <br>"+html+"<h> <br> Best Regards, <br> YOUR NAME"
        message = str(html)
        msg.attach(MIMEText(message,'html'))
        #msg.attach(MIMEText(message))
        mailserver = smtplib.SMTP("smtp.gmail.com", 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login("<FROM ADDRESS>","<PASSWORD>")
        mailserver.sendmail('<FROM ADDRESS>','<TO ADDRESS>',msg.as_string())
        mailserver.quit()
