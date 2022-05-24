#-----------------------------------------------------------------------------------------------------
#
#   Project - dcmproc
#   Description:
#       A python processing package for various dicom operation
#   Author: hui.liu02@united-imaging.com
#   Created 2022-04-28
#-----------------------------------------------------------------------------------------------------

import os
import re
import pydicom
import pandas as pd

from glob import glob

from .dcmtags import *

#------------------------------------------------------------------------------------------------------
#
class DUMP_DCMSERIESTAGS_2_ONE_COL():
    def __init__(self):
        # General
        self.InstitutionName = ''
        self.Modality = ''
        self.Manufacturer = ''
        self.ManufacturerModelName = ''
        # Patient
        self.PatientName = ''
        self.PatientID = ''
        self.PatientSex = ''
        self.PatientWeight = ''
        self.PatientSize = ''
        self.PatientAge = ''
        # Study
        self.StudyInstanceUID = ''
        self.StudyDescription = ''
        self.StudyDate = ''
        self.StudyTime = ''
        # Series
        self.SeriesInstanceUID = ''
        self.SeriesNumber = ''
        self.SeriesDescription = ''
        self.SeriesDate = ''
        self.SeriesTime = ''
        self.AcquisitionDateTime = ''
        self.BodyPartExamined = ''
        self.SliceThickness = 0.0
        self.Rows = 0
        self.Columns = 0
        return
    #----------------------------------------------------------------------------------------------------
    #
    def update_dcmtags(self, ds):
        for key in self.__dict__.keys():
            if ds.get_item(key) is None: continue
            self.__dict__[key] = ds[key].value
        return
    #----------------------------------------------------------------------------------------------------
    #
    def get_dcmtags(self):
        _tags = {}
        for key in self.__dict__.keys():
            _tags[key] = self.__dict__[key]
        return _tags

#------------------------------------------------------------------------------------------------------
#
class DUMP_UIHPCT_DCMSERIESTAGS_2_ONE_COL(DUMP_DCMSERIESTAGS_2_ONE_COL):
    """ _summary_
        UIH PCT DICOM
    """
    def __init__(self):
        # init general DICOM tags
        super().__init__()
        
        # Series - CT specific
        self.CT_AverageKVP = 0
        self.CT_AveragemAs = 0
        
        # Study - PET specific
        self.PT_Units = ''
        self.PT_RadioPharmTracer = ''
        self.PT_RadioPharmStartDateTime = ''
        self.PT_RadioPharmTotalDose = ''
        self.PT_RadioPharmHalfTime = ''
        
        # Series - PET reconstruction
        self.PT_AcquisitionDuration = ''
        self.PT_ReconstructionAlgorithm = ''
        self.PT_ReconstructionFOV = ''
        self.PT_ReconstructionNumIterations = 0
        self.PT_ReconstructionNumSubsets = 0
                
        return
    #----------------------------------------------------------------------------------------------------
    def update_dcmtags(self, ds):
        super().update_dcmtags(ds)
        
        if self.Modality == 'CT' and self.Manufacturer == 'UIH':
            self.FILE_NumberofSlices = ds[0x0020, 0x1002].value
        if self.Modality == 'PT' and self.Manufacturer == 'UIH':
            self.FILE_NumberofSlices = ds[TagSeriesNbSlices].value
            self.PT_Units = ds['Units'].value

            _radiopharm = ds[TagRadiopharmaceuticalInformationSequence].value[0]
            self.PT_RadioPharmTracer = _radiopharm[TagRadiopharmaceutical].value
            self.PT_RadioPharmStartDateTime = _radiopharm[TagRadiopharmaceuticalStartDateTime].value
            self.PT_RadioPharmTotalDose = _radiopharm[TagRadionuclideTotalDose].value
            self.PT_RadioPharmHalfTime = _radiopharm[TagRadionuclideHalfLife].value

            _acq = ds[0x0067, 0x1021].value[0]
            self.PT_AcquisitionDuration = _acq[TagAcquisitionDuration].value
            _recon = _acq[0x0018, 0x9749].value[0]
            self.PT_ReconstructionAlgorithm = _recon[0x0018, 0x9315].value
            self.PT_ReconstructionFOV = _recon[0x0018, 0x9317].value[0]
            self.PT_ReconstructionNumIterations = _recon[0x0018, 0x9739].value
            self.PT_ReconstructionNumSubsets = _recon[0x0018, 0x9740].value
        return

#------------------------------------------------------------------------------------------------------
#
class DUMP_UIHPCT_BUNDLES_2_ONE_COL():
    """
        UIH PCT DATA including DCM and RAWDATA
            STUDY_ROOT
                CT
                    import.ctrawdata: None
                    CTRawDataFile: CT rawdata subfolder
                Image
                    various DCM series
                PET
                    import.petrawdata: None
                    RawData: PET rawdata subfolder
                    DBRecords: DBRecords.xml
                import.rawdata: StudyUID
    Returns:
        _type_: _description_
    """
    def __init__(self):
        # Col Names
        
        # General
        self.InstitutionName = ''
        self.Modality = ''
        self.Manufacturer = ''
        self.ManufacturerModelName = ''
        
        # Patient
        self.PatientName = ''
        self.PatientID = ''
        self.PatientSex = ''
        self.PatientWeight = ''
        self.PatientSize = ''
        self.PatientAge = ''
        
        # Study
        self.StudyInstanceUID = ''
        self.StudyDescription = ''
        self.StudyDate = ''
        self.StudyTime = ''
        
        # PET Specific Tags
        self.PT_RadioPharmTracer = ''
        self.PT_RadioPharmStartDateTime = ''
        self.PT_RadioPharmTotalDose = ''
        self.PT_RadioPharmHalfTime = ''
        
        # PKG information
        self.BUNDLES_ROOT = ''
        self.BUNDLES_import_rawdata = False
        self.BUNDLES_Image = False
        self.BUNDLES_CT = False
        self.BUNDLES_PET = False
        self.BUNDLES_PET_DBRecords = False
        return

    #----------------------------------------------------------------------------------------------------
    #
    def update_bundles(self, bundles_root):
        """
        
        Args:
            bundles_root (_type_): _description_

        Returns:
            _type_: _description_
        """
        subroot_Image = os.path.join(bundles_root, 'Image')
        subroot_PET = os.path.join(bundles_root, 'PET')
        subroot_CT = os.path.join(bundles_root, 'CT')
        
        self.BUNDLES_ROOT = bundles_root
        self.BUNDLES_import_rawdata = os.path.isfile(os.path.join(bundles_root, 'import.rawdata'))
        self.BUNDLES_CT = os.path.isdir(subroot_CT)
        self.BUNDLES_Image = os.path.isdir(subroot_Image)
        self.BUNDLES_PET = os.path.isdir(subroot_PET)
        self.BUNDLES_PET_DBRecords = os.path.isfile(os.path.join(subroot_PET, 'DBRecords', 'DBRecords.xml'))
        
        # read dcm tags from dcm series under bundle_root/Image/SeriesName/DCMFile
        PET_dcmfile = ''
        if self.BUNDLES_Image:
            dcmfiles = glob(os.path.join(os.path.join(subroot_Image, '*', '00000001.dcm')))
            for dcmfile in dcmfiles:
                ds = pydicom.read_file(dcmfile, stop_before_pixels=True, force=True)
                if ds.Modality == 'PT' and ds.Manufacturer == 'UIH': PET_dcmfile = dcmfile
            if PET_dcmfile != '': 
                ds = pydicom.read_file(PET_dcmfile, stop_before_pixels=True, force=True)
                # update dcm tags
                for key in self.__dict__.keys():
                    if key.startswith('PT') or key.startswith('BUNDLES'): continue
                    if ds.get_item(key) is None: continue
                    self.__dict__[key] = ds[key].value
                # upate PET specific dcm tags
                _radiopharm = ds[TagRadiopharmaceuticalInformationSequence].value[0]
                self.PT_RadioPharmTracer = _radiopharm[TagRadiopharmaceutical].value
                self.PT_RadioPharmStartDateTime = _radiopharm[TagRadiopharmaceuticalStartDateTime].value
                self.PT_RadioPharmTotalDose = _radiopharm[TagRadionuclideTotalDose].value
                self.PT_RadioPharmHalfTime = _radiopharm[TagRadionuclideHalfLife].value
        # read tags from records xml
        # PET_DBRecords_file = os.path.join(subroot_PET, 'DBRecords', 'DBRecords.xml')
        # if self.BUNDLES_PET_DBRecords:
        
        return
    #----------------------------------------------------------------------------------------------------
    #
    def get_dcmtags(self):
        _tags = {}
        for key in self.__dict__.keys():
            _tags[key] = self.__dict__[key]
        return _tags

#------------------------------------------------------------------------------------------------------
#
def dump_uihpct_bundles_2_df(working_root):
    """_summary_

    Args:
        working_root (_type_): _description_

    Returns:
        _type_: _description_
    """
    tags = []
    for sub_root, _, _ in os.walk(working_root):
        val_0 = os.path.isfile(os.path.join(sub_root, 'import.rawdata'))
        val_1 = os.path.isdir(os.path.join(sub_root, 'Image'))
        val_2 = os.path.isdir(os.path.join(sub_root, 'PET'))
        # val_3 = os.path.isdir(os.path.join(sub_root, 'CT'))
        if not all([val_0, val_1, val_2]): continue
        col_tags = DUMP_UIHPCT_BUNDLES_2_ONE_COL()
        col_tags.update_bundles(sub_root)
        tags.append(col_tags.get_dcmtags())
    return pd.DataFrame(tags)
#------------------------------------------------------------------------------------------------------
#
def dump_uihpct_bundles_2_df_datacenter_v1(working_root):
    """_summary_
        dump uihpct PET bundles with additional tags:
            
    Args:
        working_root (_type_): _description_

    Returns:
        _type_: _description_
    """
    tags = []
    for sub_root, _, _ in os.walk(working_root):
        val_0 = os.path.isfile(os.path.join(sub_root, 'import.rawdata'))
        val_1 = os.path.isdir(os.path.join(sub_root, 'Image'))
        val_2 = os.path.isdir(os.path.join(sub_root, 'PET'))
        # val_3 = os.path.isdir(os.path.join(sub_root, 'CT'))
        if not all([val_0, val_1, val_2]): continue
        
        print('working on %s...'%(sub_root))
        
        col_tags = DUMP_UIHPCT_BUNDLES_2_ONE_COL()
        col_tags.update_bundles(sub_root)
        col_tag = col_tags.get_dcmtags()
        
        # datacenter data structure v1
        col_tag['StorageRoot'] = ''
        col_tag['SubRoot0'] = col_tag['Manufacturer'].upper() + '-' + col_tag['ManufacturerModelName'].upper()
        col_tag['SubRoot1'] = re.sub(r'[^a-zA-Z0-9\s]', repl='', string=str(col_tag['InstitutionName'])).upper()
        col_tag['SubRoot2'] = re.sub(r'[^a-zA-Z0-9\s]', repl='', string=str(col_tag['PT_RadioPharmTracer'])).upper()
        col_tag['SubRoot3'] = 'PID-' \
                              + re.sub(r'[^a-zA-Z0-9\s]', repl='', string=str(col_tag['PatientID'])).upper() \
                              + 'PNAME-' \
                              +  re.sub(r'[^a-zA-Z0-9\s]', repl='', string=str(col_tag['PatientName'])).upper()
        col_tag['SubRoot4'] = str(col_tag['StudyDate']) + str(col_tag['StudyTime'])[:6]
        
        tags.append(col_tag)
        
    return pd.DataFrame(tags)
