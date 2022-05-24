#-----------------------------------------------------------------------------------------------------
#
#   Project - dcmproc
#   Description:
#       A python processing package for various dicom operation
#   Author: huiliu.liu@gmail.com
#   Created 2022-04-29
#-----------------------------------------------------------------------------------------------------

import os
import difflib
import pydicom
import shutil
import subprocess

import numpy as np
import nibabel as nib

from glob import glob
from pydicom import Dataset, DataElement
from pydicom.dataset import FileMetaDataset

#-----------------------------------------------------------------------------------------------------
#
def diffdcm(dcm_file_0, dcm_file_1, out_diff_txt_file):
    """_summary_

    Args:
        dcm_file_0 (_type_): _description_
        dcm_file_1 (_type_): _description_
        out_diff_txt_file (_type_): _description_
    """
    datasets = tuple([pydicom.dcmread(filename, force=True)
                  for filename in (dcm_file_0, dcm_file_1)])

    # difflib compare functions require a list of lines, each terminated with
    # newline character massage the string representation of each dicom dataset
    # into this form:
    rep = []
    for dataset in datasets:
        lines = str(dataset).split("\n")
        lines = [line + "\n" for line in lines]  # add the newline to end
        rep.append(lines)

    with open(out_diff_txt_file, 'w') as fojb:
        diff = difflib.Differ()
        for line in diff.compare(rep[0], rep[1]):
            if line[0] != "?":
                #print(line)
                fojb.write(line)
    
    return
#-----------------------------------------------------------------------------------------------------
#
def convert_3ddcm_to_3dnii(in_3ddcm_file, out_3dnii_file):
    """_summary_

    Args:
        in_3ddcm_file (_type_): _description_
        out_3dnii_file (_type_): _description_
    """
    _workroot = in_3ddcm_file[:-4]
    shutil.rmtree(_workroot, ignore_errors=True)
    os.makedirs(_workroot, exist_ok=True)
    
    working_in_3ddcm_file = os.path.join(_workroot, os.path.basename(in_3ddcm_file))
    
    shutil.copyfile(in_3ddcm_file, working_in_3ddcm_file)
    devnull = open(os.devnull, 'w')
    subprocess.call(['dcm2niix', '-b', 'y', '-z', 'y',
                     '-f', os.path.basename(in_3ddcm_file)[:-4],
                     '-o', _workroot,
                     '-w', '1',
                     _workroot],
                    stdout=devnull, stderr=subprocess.STDOUT)
    working_out_3dniix_file = os.path.join(_workroot, os.path.basename(in_3ddcm_file)[:-4] + '.nii.gz')
    if os.path.exists(working_out_3dniix_file): shutil.copyfile(working_out_3dniix_file, out_3dnii_file)
    
    shutil.rmtree(_workroot)
    return
#-----------------------------------------------------------------------------------------------------
#
def convert_3ddcmtags_to_2ddcmtags(ds_3dtags, slice):
    """_summary_

    Args:
        ds_3dtags (_type_): _description_
        ds_2dtags (_type_): _description_
    """
    ds_2dtags = Dataset()
    ds_2dtags.file_meta = ds_3dtags.file_meta
    for key in ds_3dtags.keys(): ds_2dtags[key] = ds_3dtags[key]
    
    # SOP UID
    sop_uids = ds_3dtags.get([0x0008, 0x1115]).value[0].get([0x0008, 0x114a]).value[slice-1]
    ds_2dtags.file_meta[0x0002, 0x0002].value = '1.2.840.10008.5.1.4.1.1.128'
    ds_2dtags.file_meta[0x0002, 0x0003].value = sop_uids[0x0008, 0x1155].value
    ds_2dtags[0x0008, 0x0016].value = '1.2.840.10008.5.1.4.1.1.128'
    ds_2dtags[0x0008, 0x0018].value = sop_uids[0x0008, 0x1155].value
    del ds_2dtags[0x0008, 0x1115]
    
    # (5200, 9229)  Shared Functional Groups Sequence
    functiongroup = ds_3dtags.get([0x5200, 0x9229]).value[0]
    for key in functiongroup.keys(): ds_2dtags[key] = functiongroup[key]
    del ds_2dtags[0x5200, 0x9229]
    
    # (5200, 9230)  Per-frame Functional Groups Sequence
    framegroup = ds_3dtags.get([0x5200, 0x9230]).value[slice-1]
    for key in framegroup.keys():
        if framegroup.get(key).value.__class__ is pydicom.sequence.Sequence:
            if len(framegroup.get(key).value) == 0: continue
            first_level_group = framegroup.get(key).value[0]
            for first_level_key in  first_level_group.keys(): 
                if first_level_group.get(first_level_key).value.__class__ is pydicom.sequence.Sequence:
                    if len(first_level_group.get(first_level_key).value) == 0: continue
                    second_level_group = first_level_group.get(first_level_key).value[0]
                    for second_level_key in  second_level_group.keys(): 
                        ds_2dtags[second_level_key] = second_level_group[second_level_key]
                ds_2dtags[first_level_key] = first_level_group[first_level_key]     
    del ds_2dtags[0x5200, 0x9230]
    
    # del nonuseful stuff from 3D stacks
    del ds_2dtags[0x0008, 0x0100]
    del ds_2dtags[0x0008, 0x0102]
    del ds_2dtags[0x0008, 0x0104]
    del ds_2dtags[0x0008, 0x1140]
    del ds_2dtags[0x0008, 0x9124]
    del ds_2dtags[0x0020, 0x9057]
    del ds_2dtags[0x0020, 0x9116]
    del ds_2dtags[0x0020, 0x9071]
    del ds_2dtags[0x0020, 0x9056]
    del ds_2dtags[0x0020, 0x9221]
    del ds_2dtags[0x0020, 0x930f]
    
    # instance and acquisition number
    ds_2dtags[0x0054, 0x1330] = DataElement([0x0054, 0x1330], 'US', slice)
    ds_2dtags[0x0020, 0x0013].value = slice
    ds_2dtags[0x0020, 0x0012].value = 1
    ds_2dtags[0x0028, 0x0008].value = 1
    
    # slice position setting
    # slice location
    ds_2dtags[0x0020, 0x1041] = DataElement([0x0020, 0x1041], 'DS', ds_2dtags[0x0020, 0x0032].value[-1])
    px = ds_2dtags[0x0028, 0x9110].value[0]
    # pixel spacing
    ds_2dtags[0x0028, 0x0030] = DataElement([0x0028, 0x0030], 'DS', px[0x0028, 0x0030].value)
    # slice thickness
    ds_2dtags[0x0018, 0x0050] = DataElement([0x0018, 0x0050], 'DS', px[0x0018, 0x0050].value)
    
    # study/series information
    ds_2dtags[0x0008, 0x1030] = DataElement([0x0008, 0x1030], 'LO', 'StudyDescription')
    ds_2dtags[0x0008, 0x103e] = DataElement([0x0008, 0x103e], 'LO', 'SeriesDescription')
    
    return ds_2dtags   

#-----------------------------------------------------------------------------------------------------
#
def convert_3ddcm_to_2ddcm(in_3ddcm_file, in_3dnii_file, out_2ddcm_root):
    """_summary_

    Args:
        in_3ddcm_file (_type_): _description_
        out_2ddcm_root (_type_): _description_
    """
    ds_3ddcm = pydicom.read_file(in_3ddcm_file, stop_before_pixels=True, force=True)
    
    rescale_intercept = ds_3ddcm.get([0x5200, 0x9229])[0].get([0x0028, 0x9145])[0].get([0x0028, 0x1052]).value
    rescale_slope = ds_3ddcm.get([0x5200, 0x9229])[0].get([0x0028, 0x9145])[0].get([0x0028, 0x1053]).value
    np_3dimg = nib.load(in_3dnii_file).get_fdata()
    np_3dimg = (np_3dimg - rescale_intercept) / rescale_slope
    np_3darray = np_3dimg.astype(np.uint16)
    np_3darray = np_3darray[:, :, ::-1]
    np_3darray = np.transpose(np_3darray, [1, 0, 2])
    np_3darray = np_3darray[::-1, :, :]
    # 
    for s in range(np_3darray.shape[-1], 0, -1):
        np_2darray = np_3darray[:, :, s-1]
        ds_2dtags_s = convert_3ddcmtags_to_2ddcmtags(ds_3ddcm, s)
        ds_2dtags_s.PixelData = np_2darray.tobytes()
        del ds_2dtags_s.file_meta
        ds_2dtags_s.file_meta = FileMetaDataset()
        ds_2dtags_s.is_little_endian = True
        ds_2dtags_s.is_implicit_VR = True
        
        pydicom.dcmwrite(os.path.join(out_2ddcm_root, '{:06d}.dcm'.format(s)), ds_2dtags_s, write_like_original=False)
    return
#-----------------------------------------------------------------------------------------------------
#
# test entry
#
#-----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    
    series_root = '/home/kube/workspace/data/p2000dcm/Anonymous_ANO_20220407_1757354_163608/SeriesDescription_311'
    out_root = '/home/kube/workspace/data/p2000dcm/Anonymous_ANO_20220407_1757354_163608/DynamicSeries_411'
    dcm_files = glob(os.path.join(series_root, '*.dcm'))
    nii_files = [dcm_file[:-4]+'.nii.gz' for dcm_file in dcm_files]
    for dcm_file, nii_file in zip(dcm_files, nii_files):
        print(dcm_file)
        convert_3ddcm_to_3dnii(dcm_file, nii_file)
        out_2dseries_root = os.path.join(out_root, os.path.basename(dcm_file)[:-4])
        os.makedirs(out_2dseries_root, exist_ok=True)
        convert_3ddcm_to_2ddcm(dcm_file, nii_file, out_2dseries_root)
    
    #dcm_0 = '/home/kube/workspace/data/p2000dcm/Anonymous_ANO_20220407_1757354_163608/DynamicSeries_411/00000064/000001.dcm'
    #dcm_1 = '/home/kube/workspace/data/p2000dcm/Anonymous_ANO_20220407_1757354_163608/DynamicSeries_411/00000064/000389.dcm'
    #diffdcm(dcm_0, dcm_1, '/home/kube/workspace/data/p2000dcm/Anonymous_ANO_20220407_1757354_163608/compare-01-01-md-re.txt')