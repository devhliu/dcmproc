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
    # dump
    #df = dump_uihpct_bundles_2_df_datacenter_v1('\\\\dataserver03\\mi\\P4.0\\02_Data\\XiJingCinicaldata_notdelete')
    #df.to_csv('M:\\code\\xijingclinicaldata_dumped.csv')
    # xcopy
    df = pd.read_csv('M:\\code\\xijingclinicaldata_xcopy_working.csv')
    cvs_copy_uihpct_bundles_2_datacenter_v1(df)