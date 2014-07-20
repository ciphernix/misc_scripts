#!/usr/bin/env python2.6

import sys
import cmd

class cmd_test(cmd.Cmd):
    '''Cmd example'''

    prompt = ">>"
    #intro = "Simple cmd example"
    #misc_header = 'misc_header'
    #undoc_header = 'undoc_header'

    ruler = '='

    doc_header = "Supported commands  (type help <command>):"

    def do_add(self,s):
        l = s.split()
        if len(l)!=2:
            print "*** invalid number of arguments"
            return
        try:
            l = [int(i) for i in l]
        except ValueError:
            print "*** arguments should be numbers"
            return
        print l[0]+l[1]

    def do_exit(self,line):
        sys.exit(0)

    do_quit = do_exit

    def do_EOF(self,line):
        return True

    def help_add(self):
        print 'add two integral numbers'

    def help_exit(slef):
        print "Exit"

    help_quit = help_exit

    def help_EOF(self):
        print "EOF char can be use to exit"

    def help_introduction(self):
        print 'introduction'
        print 'a good place for a tutorial'

    help_help = help_introduction


if __name__ == '__main__':
    try:
        cmd_test().cmdloop()
    except KeyboardInterrupt,SystemExit:
        print
        sys.exit(0)

