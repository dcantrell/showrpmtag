#!/usr/bin/python3
#
# showrpmtag.py
# Given an RPM or SRPM file and a list of header tag symbolic names, try
# to read them and dump them to the terminal.
#
# by: David Cantrell <dcantrell@redhat.com>
# SPDX-License-Identifier: GPL-2.0-or-later
#

import os
import sys
import rpm

def usage(progname):
    print("Usage: %s [.rpm or .srpm] RPMTAG ...\n" % progname)
    print("The second argument is a path to an RPM or SRPM package.  The second")
    print("and following arguments are the RPM header tag values you want to see")
    print("the values of.\n")
    print("The list of tags can be found in /usr/include/rpm/rpmtag.h\n")
    print("The tag values should not carry the RPMTAG_ prefix.")
    return

def get_tag_val(tag):
    for v, n in rpm.tagnames.items():
        if tag == n:
            return v

    return -1

if __name__ == "__main__":
    progname = os.path.basename(sys.argv[0])

    if len(sys.argv) < 3:
        usage(progname)
        sys.exit(1)

    pkg = os.path.realpath(sys.argv[1])
    i = 2

    ts = rpm.TransactionSet()
    fdno = os.open(pkg, os.O_RDONLY)
    hdr = ts.hdrFromFdno(fdno)
    os.close(fdno)

    while i < len(sys.argv):
        if not sys.argv[i].isupper():
            sys.stderr.write("*** invalid tag `%s', tags must be all uppercase" % sys.argv[i])
            i += 1
            continue

        if sys.argv[i].startswith("RPMTAG_"):
            tag = sys.argv[i][7:]
        else:
            tag = sys.argv[i]

        val = get_tag_val(tag)

        if val == -1:
            print("%s: unknown tag name" % sys.argv[i])
            i += 1
            continue
        else:
            print("%s: |%s|" % (sys.argv[i], hdr[val]))

        i += 1
