import yaml, sys, os

import email
import imaplib
import re

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

imap_host = cfg['email']['imap_server']
imap_user = cfg['email']['imap_user']
imap_pass = cfg['email']['imap_password']
imap_folder = cfg['email']['imap_folder']

class FetchEmail():
    def __init__(self,
        mail_server=imap_host,
        username=imap_user,
        password=imap_pass,
        downloadfolder=imap_folder):

        self.error = None
        self.connection = None
        self.mail_server = mail_server
        self.username = username
        self.password = password
        self.folder = downloadfolder
        self.connection = imaplib.IMAP4(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False) # so we can mark mails as readread

    def close_connection(self):
            self.connection.close()

    def save_attachment(self, msg):
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename is not None:
                if re.match("LEEDS STOCK.*\.xlsx", filename):
                    filename = "FPS_LEEDS.xlsx"
                elif re.match("KILEN.*\.csv", filename):
                    filename = "kilen.csv"
                elif re.match(".*.png", filename):
                    continue
                print("Downloading:", filename)
                att_path = os.path.join(self.folder, filename)

                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
        return att_path

    def fetch_unread_messages(self):
        emails = []
        (result, messages) = self.connection.search(None, 'UnSeen')
        if result == "OK":
            for message in messages[0].decode().split(' '):
                try:
                    ret, data = self.connection.fetch(message,'(RFC822)')
                except:
                    print("No new emails to read.")
                    # self.close_connection()
                    return None
                msg = email.message_from_bytes(data[0][1])
                if isinstance(msg, str) == False:
                    emails.append(msg)
                # response, data = self.connection.store(message, '+FLAGS','\\Seen')
            return emails

        self.error = "Failed to retreive emails."
        return emails

def download():
    fe = FetchEmail()
    print("Collecting unread messages")
    unread = fe.fetch_unread_messages()
    if unread:
        print("Collecting attachments")
        for email in unread:
            fe.save_attachment(email)
    fe.close_connection()
