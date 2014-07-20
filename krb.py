#!/usr/bin/env python2.6
'''Script to create and delete kerberos keytab using kinit on CENTOS'''

import os
import tempfile

def kinit():
    KRB5CC = tempfile.NamedTemporaryFile(prefix="krb5cc_", delete=False)
        if (os.stat(KRB5CC.name).st_size == 0):
                keytab = os.path.join(os.path.dirname(__file__), "../etc/auth.keytab")
                os.system("KRB5CCNAME=%s /usr/bin/kinit -k -t %s user@DOMAIN.COM" % (KRB5CC.name, keytab))
        return KRB5CC.name

def kdestroy(krbTicket):
        os.system("KRB5CCNAME=%s kdestroy" % krbTicket)


if __name__ == "__main__":
        kinit()
