import imaplib
import os
import email, getpass
import sys
import json
import pandas as pd

class GmailFinin():
    def helloWorld(self):
        print("\nHello I'm here to help you")

    def initializeVariables(self):
        self.usr = ""
        self.pwd = ""
        self.mail = object
        self.mailbox = ""
        self.mailCount = 0
        self.destFolder = ""
        self.data = []
        self.ids = []
        self.idsList = []

    def getLogin(self):
        print("\nPlease enter your Gmail login details below.")
        self.usr = input("Email: ")
        # self.pwd = input("Password: ")
        self.pwd = getpass.getpass("Enter your password --> ")

    def attemptLogin(self):
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        if self.mail.login(self.usr, self.pwd):
            print("\nLogon SUCCESSFUL")
            return True
        else:
            print("\nLogon FAILED")
            return False

    def checkIfUsersWantsToContinue(self):
        print("\nWe have found "+str(self.mailCount)+" emails in the mailbox "+self.mailbox+".")
        return True if input("Do you wish to continue extracting all the emails into "+self.destFolder+"? (y/N) ").lower().strip()[:1] == "y" else False       
        
    def selectMailbox(self):
        # self.mailbox = input("\nPlease type the name of the mailbox you want to extract, e.g. Inbox: ")
        self.mailbox = "Inbox"
        bin_count = self.mail.select(self.mailbox)[1]
        self.mailCount = int(bin_count[0].decode("utf-8"))
        return True if self.mailCount > 0 else False

    def searchThroughMailbox(self):
        type, self.data = self.mail.search(None, "ALL")
        self.ids = self.data[0]
        self.idsList = self.ids.split()

    def parseEmails(self):
        jsonOutput = {}
        for anEmail in self.data[0].split():
            type, self.data = self.mail.fetch(anEmail, '(UID RFC822)')
            raw = self.data[0][1]
            try:
                raw_str = raw.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    raw_str = raw.decode("ISO-8859-1") # ANSI support
                except UnicodeDecodeError:
                    try:
                        raw_str = raw.decode("ascii") # ASCII ?
                    except UnicodeDecodeError:
                        pass
                        
            msg = email.message_from_string(raw_str)

            jsonOutput['subject'] = msg['subject']
            jsonOutput['from'] = msg['from']
            jsonOutput['date'] = msg['date']
            raw = self.data[0][0]
            raw_str = raw.decode("utf-8")


            uid = raw_str.split()[2]
            # Body #
            try:
                if msg.is_multipart():
                    for part in msg.walk():
                        partType = part.get_content_type()
                        ## Get Body ##
                        if partType == "text/plain" and "attachment" not in part:
                            jsonOutput['body'] = part.get_payload()
                            key,companyemail='Payment ID','support@instamojo.com'
                            values=['ID' ,'Email','number']
                            lst=[]
                            if (key and companyemail) in jsonOutput['body']:
                                for i in range(len(jsonOutput['body'].split())):
                                    if jsonOutput['body'].split()[i] in values:
                                        lst.append(jsonOutput['body'].split()[i+1])
                            print(lst)
                            # file=pd.read_csv('data.csv')
                            if lst:
                                df=pd.DataFrame([lst])
                                print(df)
                                try:
                                    if not lst[0] in pd.read_csv('data.csv').ID:
                                        df.to_csv('data.csv',index=False,header=['ID','Email','number'])
                                except:
                                    df.to_csv('data.csv',index=False,header=['ID','Email','number'])

                        ## Get Attachments ##
                        # if part.get('Content-Disposition') is not None:
                        #     attchName = part.get_filename()
                        #     print(attchName)
                        #     if bool(attchName):
                        #         attchFilePath = str(self.destFolder)+str(uid)+str("/")+str(attchName)
                        #         print(attchFilePath)
                        #         os.makedirs(os.path.dirname(attchFilePath), exist_ok=True)
                        #         with open(attchFilePath, "wb") as f:
                        #             f.write(part.get_payload(decode=True))
                else:
                    jsonOutput['body'] = msg.get_payload(decode=True).decode("utf-8") # Non-multipart email, perhaps no attachments or just text.
                    jsonOutput['body'] = msg.get_payload()


                #outputDump = json.dumps(jsonOutput)
                #emailInfoFilePath = str(self.destFolder)+str(uid)+str("/")+str(uid)+str(".json")
                #os.makedirs(os.path.dirname(emailInfoFilePath), exist_ok=True)
                #print(emailInfoFilePath)
                #with open(emailInfoFilePath, "w") as f:
                    #f.write(outputDump)
            except:
                pass

    def __init__(self):
        self.initializeVariables()
        self.helloWorld()
        self.getLogin()
        if self.attemptLogin():
            not self.selectMailbox() and sys.exit()
        else:
            sys.exit()
        not self.checkIfUsersWantsToContinue() and sys.exit()
        self.searchThroughMailbox()
        self.parseEmails()

if __name__ == "__main__":
    run = GmailFinin()