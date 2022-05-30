#-----------------------------------------------------------------------------------------------------
#
#   Project - dcmproc
#   Description:
#       A python processing package for various dicom operation
#   Author: huiliu.liu@gmail.com
#   Created 2022-04-28
#-----------------------------------------------------------------------------------------------------

import os
import sys
import subprocess

from dcmproc.common.dcmtags import create_pid_pname_from_onecol

#-----------------------------------------------------------------------------------------------------
#
def get_dcm2niix_bin():
    """
    :return:
    """
    dcm2niix_bin = 'dcm2niix'
    if sys.platform == 'win32': dcm2niix_bin = 'dcm2niix.exe'
    elif sys.platform == 'linux': dcm2niix_bin = 'dcm2niix'
    return dcm2niix_bin
#-----------------------------------------------------------------------------------------------------
#
def conv_dcmseries2nii(dcm_series_root, nii_rootname, nii_filename, zipped=True):
    """
    :param dcm_series_root:
    :param nii_rootname:
    :param nii_filename:
    :param zipped:
    :return:
    """
    dcm2niix_bin = get_dcm2niix_bin()
    if dcm2niix_bin == '': raise ValueError('there is no dcm2niix exist.')
    zip_y = 'y' if zipped else 'n'

    devnull = open(os.devnull, 'w')
    subprocess.call([dcm2niix_bin, '-b', 'y', '-z', zip_y,
                     '-f', nii_filename,
                     '-o', nii_rootname,
                     '-w', '1',
                     dcm_series_root],
                    stdout=devnull, stderr=subprocess.STDOUT)
    return
#-----------------------------------------------------------------------------------------------------
#
def batch_dcm2niix(df_dcm_info, niix_root):
    """
    :param df_dcm_info:
    :param niix_root:
    :return:
    """
    os.makedirs(niix_root, exist_ok=True)
    
    # read tags from df_dcm_info
    patient_names = df_dcm_info['PatientName'].values
    patient_ids = df_dcm_info['PatientID'].values
    study_dates = df_dcm_info['StudyDate'].values
    modalities = df_dcm_info['Modality'].values

    # tags for niix converting
    dcm_s_roots = df_dcm_info['GL_SeriesRoot'].values
    dcm_s_akas = df_dcm_info['GL_SeriesAKA'].values
    dcm_c_oks = df_dcm_info['GL_SeriesConvertNiix'].values
    
    # converting dicom series into niix
    for pname, pid, sdate, sroot, saka, cok, m in zip(patient_names, patient_ids, study_dates,
                                                      dcm_s_roots, dcm_s_akas, dcm_c_oks, modalities):
        if cok == False and saka != 'nan': continue
        if cok == False and pname != 'nan': continue
        pname_subroot = create_pid_pname_from_onecol(pid, pname)
        _sdate = str(sdate).split('.')[0]
        print('working on converting %s - %s dicom into niix.'%(pname, _sdate))
        series_niix_root = os.path.join(niix_root, pname_subroot, _sdate)
        os.makedirs(series_niix_root, exist_ok=True)

        if os.path.exists(os.path.join(series_niix_root, saka + '.nii.gz')): continue
        conv_dcmseries2nii(sroot, series_niix_root, saka)
        
        if m == 'PT': print('PET part is not finished yet.')
        
    return