#!/usr/bin/env python2
'''Script to clean up directories/path'''

import optparse
import tarfile
import time
import os
import subprocess
import sys

def tar_files(tar_list,tarname=None,path="/tmp",keep_path=False,recursive=False):
    '''Tar and compress files in tar_list'''
    
    if not tarname:
        tarname = os.path.join(path,"backup-" + time.strftime("%Y%m%d%M") + ".tgz")
    tar = tarfile.open(tarname, mode='w:gz')
    try:
        for name in tar_list:
            if keep_path:
                tar.add(name,recursive=recursive)
            else:
                file_name = os.path.split(name)[1]
                tar.add(name,arcname=file_name,recursive=recursive)
            print "{0}: {1} archived".format(tarname,file_name)
    except Exception, why:
        print why
    finally:
        tar.close()

def find_files(path,days=60,recursive=False):
    '''Finds files that are n days old. Returns a list with path and file name.'''

    current_time = time.time()
    delta = 3600*24*days
    file_list = []
    
    if recursive:
        for dirpath,dirs,files, in os.walk(path):
            for name in files:
                fpath = os.path.join(dirpath,name)
                if (current_time - os.path.getctime(fpath) >= delta):
                    file_list.append(fpath)
    else:
        for item in os.listdir(path):
            f = os.path.join(path,item)
            if os.path.isfile(f):
                if (current_time - os.path.getctime(f) >= delta):
                     file_list.append(f)

    return file_list

def remove_files(remove_list):
    '''Remove  files in remove_list.'''

    try:
        for name in remove_list:
            os.remove(name)
            print "{0} removed".format(name)
    except Exception,why:
        print why

def main():
    parser = optparse.OptionParser()
    parser.add_option("-a", "--age", type="int", dest="age", help="age of files (in days)to keep, older than age will be \
            compressed/removed",default=60,metavar="<1-9999>")
    parser.add_option("-n", "--name", dest="fname", help="file name pattern to compress and remove, this will match *filename and \
            filename*",metavar="<file pattern>")
    parser.add_option("-p", "--path", dest="path", help="path to clean up",default="/bb/websec/config_repo/",metavar="</path/to/clean/")
    parser.add_option("-r", "--recursive", dest="recursive", action="store_true", help="recusively clean up files under path")
    parser.add_option("-k", "--keep", dest="keep", action="store_true", help="keep full path when taring files")
    parser.add_option("-D", "--Delete", dest="Delete", action="store_true", help="Delete files only, do not backup and compress")

    options,args = parser.parse_args()

    age = options.age
    recursive = False
    delete = False
    keep=False
    cleanup_list = []

    if options.fname:
        fname = options.fname
    else:
        print "Need -n/--name option"
        parser.print_help()
        sys.exit(-1)

    if options.path:
        path = options.path
    else:
        print "Need -p/--path option"
        parser.print_help()

    if options.recursive:
        recursive = True
    if options.Delete:
        delete = True
    if options.keep:
        keep=True

    file_list = find_files(path,days=age,recursive=recursive)
    for file_ in file_list:
        if fname in file_:
            cleanup_list.append(file_)
    if delete:
        remove_files(cleanup_list)
    else:
        tar_files(cleanup_list,path=path,keep_path=keep)
        remove_files(cleanup_list)



if __name__=="__main__":
    main()

