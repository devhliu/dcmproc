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

from dcmproc.uih.uihpct_xlsx import dump_uihpct_bundles_2_xlsx_datacenter_v1 as dump_2_xlsx
from dcmproc.uih.uihpct_xlsx import xlsx_copy_uihpct_bundles_2_datacenter_v1 as copy_using_xlsx

#-----------------------------------------------------------------------------------------------------
#
#
#
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # dump
    working_root = '\\\\dataserver03\\mi\\MI_RECON\\3.0'
    xlsx_file = 'M:\\code\\dataserver03_mi_MI_RECON_3.0_dumped.xlsx'
    dump_2_xlsx(working_root, xlsx_file, save_per_cases=100, mode='splitted')
    
    # xcopy
    #xlsx_file = 'M:\\code\\xijingclinicaldata_xcopy_working.xlsx'
    #copy_using_xlsx(xlsx_file)