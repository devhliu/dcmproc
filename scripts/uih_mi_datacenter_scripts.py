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

from glob import glob

from dcmproc.uih.uihpct_xlsx import dump_uihpct_bundles_2_xlsx_datacenter_v1 as dump_2_xlsx
from dcmproc.uih.uihpct_xlsx import xlsx_copy_uihpct_bundles_2_datacenter_v1 as copy_using_xlsx
from dcmproc.uih.uihpct_xlsx import xlsx_dump_uihpct_bundles_size_datacenter_v1 as get_bundles_info_2_xlsx
from dcmproc.uih.uihpct_xlsx import check_copy_uihpct_buldles_datacenter_v1 as check_copy_results
#-----------------------------------------------------------------------------------------------------
#
#
#
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # dump
    #working_root = '/mnt/d/umic/datax'
    #xlsx_file = '/mnt/d/umic/dataserver03_mi_MI_RECON_3.0_dumped.xlsx'
    #dump_2_xlsx(working_root, xlsx_file, save_per_cases=100, mode='splitted')
    
    # xcopy
    #xlsx_file = 'M:\\code\\xijingclinicaldata_xcopy_working.xlsx'
    #copy_using_xlsx(xlsx_file)

    #storage_root = '/mnt/d/umic/datay/UMI-PANORAMA-35S/XIJING_HOSPITAL'
    #pct_bundles_roots = glob(os.path.join(storage_root, '*', 'PID-*'))
    #xlsx_file = os.path.join(storage_root, 'PCT_BUNDLES_INFO.xlsx')
    #get_bundles_info_2_xlsx(pct_bundles_roots, xlsx_file)