#-----------------------------------------------------------------------------------------------------
#
#   Project - dcmproc
#   Description:
#       A python processing package for various dicom operation
#   Author: hui.liu02@united-imaging.com
#   Created 2022-04-28
#-----------------------------------------------------------------------------------------------------

import os
import shutil

#------------------------------------------------------------------------------------------------------
#
def cvs_copy_uihpct_bundles_datacenter_v1(df):
    """_summary_
        copy uihpct PET bundles from src_root into target_root with naming organization defined in df
        paired with dump_uihpct_bundles_2_df_datacenter_v1
            
    Args:

        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    for row in df.rows:
        target_root = row['StorageRoot']
        if target_root == '': continue
        if not os.path.isdir(target_root): continue
        target_bundles_subroot = os.path.join(target_root, row['SubRoot0'], row['SubRoot1'], 
                                              row['SubRoot2'], row['SubRoot3'], row['SubRoot4'])
        os.makedirs(target_bundles_subroot, exist_ok=True)
        src_bundles_subroot = row['BUNDLES_ROOT']
        if not os.path.isdir(src_bundles_subroot): continue
        
        print('working on copying %s to %s...'%(src_bundles_subroot, target_bundles_subroot))
        shutil.copytree(src_bundles_subroot, target_bundles_subroot, dirs_exist_ok=True)
        
    return
