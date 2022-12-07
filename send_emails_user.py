import smtplib
import pandas as pd
from string import Template
import email.message as message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendEmailList:
    def __init__(self,users_path, msg_path):
        self.users_df = pd.read_csv(users_path)
        
        self.host_email = self.users_df['email'][0]
        self.username = self.users_df['user'][0]
        password = 'kzmurvjaixvjswgn'

        self.users_df.drop(self.users_df.index[0], inplace=True)
        print(self.users_df)
        
        print(self.host_email)

        with open(msg_path, 'r', encoding='utf-8') as f:
            self.content = Template(f.read())

        self.server = smtplib.SMTP('smtp.gmail.com: 587')
        self.server.starttls()
        self.server.login(self.host_email, password)

    def send(self):
        # to = self.users_df['email'][0]
        for i, row in self.users_df.iterrows():
            print(f'Enviando email para {row["user"]}')
            
            content = self.content.substitute(PERSON_NAME=row['user'])
            msg = message.Message()
            msg['Subject'] = '[DULCINÉIA]EMAIL DE VERIFICAÇÃO DE CONTA'
            msg['From'] = self.host_email
            msg['To'] = row['email']
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(content)
            
            self.server.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            print('email enviado')


if __name__ == '__main__':
    users_path = 'data/users.csv'
    msg_path = 'message.txt'
    sendEmailList = SendEmailList(users_path, msg_path)
    sendEmailList.send()
    