#-----------------------------------------------------------------------------------------------------
#
#   Project - dcmproc
#   Description:
#       A python processing package for various dicom operation
#   Author: hui.liu02@united-imaging.com
#   Created 2022-05-24
#-----------------------------------------------------------------------------------------------------

import os
import argparse

import pandas as pd

from dcmproc.uih.uihpct_csv import dump_uihpct_bundles_2_df_datacenter_v1
from dcmproc.uih.uihpct_csv import cvs_copy_uihpct_bundles_2_datacenter_v1

#-----------------------------------------------------------------------------------------------------
#
#
#
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # add arguments
    parser.add_argument('-m', '--mode', help='working mode: dump or copy', action="store_true")
    parser.add_argument('-f', '--csvfile', help='csv file: csv file will be overrided in dump mode and used \
                        as copy rules in copy mode', action="store_true")
    parser.add_argument('-w', '--workingroot', help='working root for coping from', action="store_true")
    # parse argments
    args = parser.parse_args()
    
    # dump mode
    if args.mode == 'dump':
        run_dump = True
        if args.workingroot == None or args.csvfile == None:
            print('the workingroot / csvfile should be specified.')
            run_dump = False
        if not os.path.isdir(args.workingroot):
            print('the workingroot does not existed.')
            run_dump = False
        if os.path.isfile(args.csvfile):
            print('csvfile: %s is existed, please use new one.'%(args.csvfile))
            run_dump = False
        if run_dump:
            df = dump_uihpct_bundles_2_df_datacenter_v1(working_root=args.workingroot)
            df.to_csv(args.csvfile)
    
    # copy mode
    if args.mode == 'copy':
        run_copy = True
        if not os.path.isfile(args.csvfile):
            print('csvfile: %s is not existed, please use dump to create a new one and then \
                  edit it before copy.'%(args.csvfile))
            run_copy = False
        if run_copy:
            df = pd.read_csv(args.csvfile)
            cvs_copy_uihpct_bundles_2_datacenter_v1(df)