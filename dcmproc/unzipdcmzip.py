#-----------------------------------------------------------------------------------------------------
#
#   Project - dlaais-data
#   Description:
#       A python processing package for　data preparation for dlaais project
#   Author: huiliu.liu@gmail.com
#   Created 2021-01-30
#-----------------------------------------------------------------------------------------------------

import os
import zipfile

#-----------------------------------------------------------------------------------------------------
#
def batch_unzip_zipfile(zip_root, unzip_root):
    """
    """
    if not os.path.exists(unzip_root): os.makedirs(unzip_root)

    for subroot, _, files in os.walk(zip_root):
        if len(files) < 0: continue
        for file in files:
            if not file.endswith('.zip'): continue
            zip_file = os.path.join(subroot, file)
            try:
                series_root = subroot.replace(zip_root, unzip_root)
                print('unziping %s ...'%(zip_file))
                with zipfile.ZipFile(zip_file, 'r') as zipobj: zipobj.extractall(series_root)
            except: print('failed to unzip %s.'%(zip_file))
    return True

#-----------------------------------------------------------------------------------------------------
#
# test entry
#
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    zip_root = '/data/public/data'
    unzip_root = '/data/public/data'
    batch_unzip_zipfile(zip_root, unzip_root)