#!/usr/bin/env python
'''Script to monitor disk usage.'''

import subprocess
import smtplib
import socket
import sys
import os
import optparse
import string


def sendEmail(filesystem,percetange,toEmail,mailhost):
    '''Sends an e-mail, specifiy the file system, utilizatio percentage and e-mail address to send e-mail to.'''
        
    hostname = socket.gethostname()
    subjet = "%s : FS %s has %s utilization" %(hostname, filesystem,percetange)
    fromEmail = "root@" + hostname
    text = "File system %s has %s percent utilization. Please clear some space" % (filesystem,percetange)
    body = string.join((
        "From: %s" %fromEmail, 
        "To: %s" % toEmail,
        "Subject: %s" % subjet,
        "",
        text
        ), "\r\n" )
    server = smtplib.SMTP(mailhost)
    server.sendmail(fromEmail,[toEmail], body)
    server.quit()

def checkSpaceUtilization(filesystem):

        df = subprocess.Popen(["df","-h",filesystem], stdout=subprocess.PIPE)
        output = df.communicate()[0]
        if len(output.split("\n")[1].split() ) < 6:
            device = output.split("\n")[1]
            size, used, available, percent, mountpoint = output.split("\n")[2].split()
        else:
            device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
        return [device,size,used,available,percent, mountpoint]

def main():
        opts = optparse.OptionParser(usage="usage: %prog [options] <host or FILE with hosts>",
                                        version="%prog 0.01" )
        opts.add_option("--fs", "-f", type="string", help="filesystem to check", dest="filesystem", default="/var/log")
        opts.add_option("--email", "-e", type="string", help="E-mail address to send warning to", dest="toEmail", default="email@example.com")
        opts.add_option("--mailhost", "-m", type="string", help="smtp server to use, defaults to mailhost.odc", dest="mailhost", default="relay.example.com")
        opts.add_option("--treshold", "-t", type="int", help="utilization percetange treshold", dest="treshold", default=90)
        options,arguments = opts.parse_args()
        
        if not os.path.exists(options.filesystem):
                print "%s not a valid file system" % options.filesystem
                sys.exit(-1)
        percent  = int(checkSpaceUtilization(options.filesystem)[4].strip("%"))
        print "Files system is %s %% full" %percent
        if percent >= options.treshold:
                sendEmail(options.filesystem,percent,options.toEmail,options.mailhost)

if __name__ == "__main__":
        main()
