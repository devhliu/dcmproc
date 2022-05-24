#-----------------------------------------------------------------------------------------------------
#
#   Project - zip dcm - reading and writing
#   Description:
#       A python processing package for　bids convert
#   Author: hui.liu02@united-imaging.com
#   Created 2021-01-30
#-----------------------------------------------------------------------------------------------------

import os
import zipfile
import pydicom
import shutil

from pydicom.misc import is_dicom

from dlaaisdata.dcmproc.dcmtags import create_pid_pname_from_dcm
from dlaaisdata.dcmproc.dcm2niix import conv_series2nii


#----------------------------------------------------------------------------------------------------
#
def compress_dcmroot_2_zipfile(dcmroot, zip_file):
    """
    :param dcmroot:
    :param zip_file:
    :return:
    """
    print('zipping %s to %s'%(dcmroot, zip_file))
    ziping_file = zipfile.ZipFile(zip_file, 'w')
    with ziping_file:
        for _subroot, _, files in os.walk(dcmroot):
            for filename in files:
                file_path = os.path.join(_subroot, filename)
                if is_dicom(file_path): ziping_file.write(file_path)
    return
#----------------------------------------------------------------------------------------------------
#
def compress_patient_dcmroot_2_ziproot(patient_dcmroot, zip_root):
    """
    :param patient_dcmroot:     assume that there is only one patient dcm data in this dcmroot
    :param patient_dcmzip_file:
    :return:
    organized by pid-pname/studydate-study_uid/series_uid
    """
    # find the first dcm
    dcm_file = ''
    for subroot, _, files in os.walk(patient_dcmroot):
        if len(files) == 0: continue
        for file in files:
            if is_dicom(os.path.join(subroot, file)):
                dcm_file = os.path.join(subroot, file)
                break
    if not os.path.exists(dcm_file):
        print('there is no valid dcm in %s.'%(patient_dcmroot))
        return

    # read the first dcm
    ds = pydicom.read_file(dcm_file, stop_before_pixels=True)
    patient_uid = create_pid_pname_from_dcm(ds)

    zip_file = os.path.join(zip_root, patient_uid + '.zip')
    if os.path.exists(zip_file): return

    # zipping the dcm files on the single patient level
    print('zipping %s into %s'%(patient_dcmroot, zip_file))
    ziping_file = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_BZIP2)
    with ziping_file:
        for _subroot, _, files in os.walk(patient_dcmroot):
            for filename in files:
                _dcmfile = os.path.join(_subroot, filename)
                if not is_dicom(_dcmfile): continue
                _ds = pydicom.read_file(_dcmfile, stop_before_pixels=True)
                _studydate = str(_ds.get('StudyDate'))
                _seriesuid = str(_ds.get('SeriesInstanceUID'))
                ziping_file.write(_dcmfile,
                                  os.path.join(patient_uid, _studydate, _seriesuid, filename),
                                  compresslevel=9)
    return
#----------------------------------------------------------------------------------------------------
#
def convert_patient_dcmzip_2_niifile(patient_dcm_zipfile, patient_niifile):
    """
    :param patient_dcm_zipfile:
    :param patient_niifile:
    :return:
    """
    if not os.path.exists(patient_dcm_zipfile): return False

    # create patient_niix_root if not exist
    patient_niix_root = os.path.join(os.path.dirname(patient_niifile))
    os.makedirs(patient_niix_root, exist_ok=True)

    dcm_zipfilename = os.path.basename(patient_dcm_zipfile)[:-4]
    _dcm_root = os.path.join(patient_niix_root, dcm_zipfilename)
    if os.path.exists(_dcm_root): shutil.rmtree(_dcm_root)
    os.makedirs(_dcm_root, exist_ok=True)

    with zipfile.ZipFile(patient_dcm_zipfile, 'r') as zipobj: zipobj.extractall(_dcm_root)
    dcm_file = None
    for subroot, _, files in os.walk(_dcm_root):
        if len(files) > 0:
            dcm_file = os.path.join(subroot, files[0])
            break
    if dcm_file is None: return False
    conv_series2nii(_dcm_root, patient_niix_root, dcm_zipfilename)
    if os.path.exists(_dcm_root): shutil.rmtree(_dcm_root)

    return True