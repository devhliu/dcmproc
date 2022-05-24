#-----------------------------------------------------------------------------------------------------
#
#   Project - dlaais-data.dcmproc.utils
#   Description:
#       A python processing package for data preparation for dlaais project
#   Author: huiliu.liu@gmail.com
#   Created 2021-08-19
#-----------------------------------------------------------------------------------------------------

import os
import shutil
import pydicom

from pydicom.misc import is_dicom

#-----------------------------------------------------------------------------------------------------
#
def copy_and_reformat_dcms(src_dcm_root, target_dcm_root, check_dcm=False):
    """
    """
    for sub_root, _, filenames in os.walk(src_dcm_root):
        if len(filenames) <= 0: continue
        for filename in filenames:
            _dcm_file = os.path.join(sub_root, filename)
            if not os.path.isfile(_dcm_file): continue
            if check_dcm: 
                if not is_dicom(_dcm_file): 
                    print(_dcm_file)
                    continue
            else:           
                try:
                    ds = pydicom.read_file(_dcm_file, stop_before_pixels=True, force=True)
                    sub_root_1 = os.path.join(target_dcm_root, ds.StudyInstanceUID, ds.SeriesInstanceUID)
                    os.makedirs(sub_root_1, exist_ok=True)
                    file_1 = os.path.join(sub_root_1, ds.SOPInstanceUID + '.dcm')
                    shutil.copyfile(_dcm_file, file_1)
                except:
                    print(_dcm_file)
    