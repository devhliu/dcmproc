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
import shutil
import pydicom

import pandas as pd

from glob import glob

from dcmproc.uih.uih_dcmtags import *
from dcmproc.common.dcmtags import *

#------------------------------------------------------------------------------------------------------
#
class DUMP_UIHPCT_BUNDLES_2_ONE_ROW():
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
        self.PT_SourceIsotopeName = ''
        
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
    def update_bundles_by_petimage(self, bundles_root):
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
            if len(dcmfiles) == 0: 
                self.BUNDLES_Image = False
                return
            # identify right dicom file with PT information
            for dcmfile in dcmfiles:
                ds = pydicom.read_file(dcmfile, stop_before_pixels=True, force=True)
                if ds.Modality == 'PT' and ds.Manufacturer == 'UIH': PET_dcmfile = dcmfile
            if PET_dcmfile != '': 
                try:
                    ds = pydicom.read_file(PET_dcmfile, stop_before_pixels=True, force=True)
                    # update dcm tags
                    for key in self.__dict__.keys():
                        if key.startswith('PT') or key.startswith('BUNDLES'): continue
                        if ds.get_item(key) is None: continue
                        self.__dict__[key] = ds[key].value
                    # update if there is specific characterset used
                    if ds.get(TagSpecificEncoding) is not None:
                        _special_encoding = pydicom.charset.convert_encodings(ds[TagSpecificEncoding].value)[0]
                        # only apply for insitutename and patientname
                        self.InstitutionName = ds[TagInstitutionName].value.encode(_special_encoding).decode()
                        self.PatientName = ds[TagPatientName].value.encode(_special_encoding).decode()
                    # upate PET specific dcm tags
                    self.PT_SourceIsotopeName = str(ds[TagSourceIsotopeName].value).replace('-', '')
                    _radiopharm = ds[TagRadiopharmaceuticalInformationSequence].value[0]
                    self.PT_RadioPharmTracer = str(_radiopharm[TagRadiopharmaceutical].value)
                    self.PT_RadioPharmStartDateTime = str(_radiopharm[TagRadiopharmaceuticalStartDateTime].value)
                    self.PT_RadioPharmTotalDose = str(_radiopharm[TagRadionuclideTotalDose].value)
                    self.PT_RadioPharmHalfTime = str(_radiopharm[TagRadionuclideHalfLife].value)
                except: self.BUNDLES_Image = False
            else: self.BUNDLES_Image = False
        
        return
    #----------------------------------------------------------------------------------------------------
    #
    def update_bundles_by_petrawdata(self, bundles_root):
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
        
        # read dcm tags from dcm series under bundle_root/PET/RawData/SeriesName/DCMFile
        if self.BUNDLES_PET:
            dcmfiles = glob(os.path.join(os.path.join(subroot_PET, 'RawData', '*', '*.dcm')))
            if len(dcmfiles) == 0: 
                self.BUNDLES_PET = False
                return
            try: 
                PET_dcmfile = dcmfiles[0]
                ds = pydicom.read_file(PET_dcmfile, stop_before_pixels=True, force=True)
                # update dcm tags
                for key in self.__dict__.keys():
                    if key.startswith('PT') or key.startswith('BUNDLES'): continue
                    if ds.get_item(key) is None: continue
                    self.__dict__[key] = ds[key].value
                # update if there is specific characterset used
                if ds.get(TagSpecificEncoding) is not None:
                    _special_encoding = pydicom.charset.convert_encodings(ds[TagSpecificEncoding].value)[0]
                    # only apply for insitutename and patientname
                    self.InstitutionName = ds[TagInstitutionName].value.encode(_special_encoding).decode()
                    self.PatientName = ds[TagPatientName].value.encode(_special_encoding).decode()
                # upate PET specific dcm tags
                self.PT_SourceIsotopeName = str(ds[TagSourceIsotopeName].value).replace('-', '')
                self.PT_RadioPharmTracer = str(ds[TagRadiopharmaceutical].value).replace('-', '')
                self.PT_RadioPharmStartDateTime = str(ds[TagRadiopharmaceuticalStartDateTime].value)
                self.PT_RadioPharmTotalDose = str(ds[TagRadionuclideTotalDose].value)
                self.PT_RadioPharmHalfTime = str(ds[TagRadionuclideHalfLife].value)
            except:
                self.BUNDLES_PET = False
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
def dump_uihpct_bundles_2_xlsx(working_root, xlsx_file, save_per_rows=100):
    """_summary_

    Args:
        working_root (_type_): _description_
        xlsx_file (_type_): _description_
    Returns:
        _type_: _description_
    """
    if save_per_rows <= 0: save_per_rows = 1
    tags = []
    for sub_root, _, _ in os.walk(working_root):
        # check whether sub_root is valid UIH PCT Bundles root
        val_0 = os.path.isfile(os.path.join(sub_root, 'import.rawdata'))
        val_1 = os.path.isdir(os.path.join(sub_root, 'Image'))
        val_2 = os.path.isdir(os.path.join(sub_root, 'PET'))
        if not all([val_0, val_1, val_2]): continue
        # dump valid UIH PCT bundles into row of df
        col_tags = DUMP_UIHPCT_BUNDLES_2_ONE_ROW()
        col_tags.update_bundles_by_petrawdata(sub_root)
        tags.append(col_tags.get_dcmtags())
        
        # save per rows
        if len(tags) % save_per_rows != 0: continue
        if os.path.isfile(xlsx_file): 
            df_0 = pd.read_excel(xlsx_file)
            df_i = pd.DataFrame(tags)
            df_1 = pd.concat([df_0, df_i], axis=0)
            df_1.to_excel(xlsx_file)
        else: 
            df_0 = pd.DataFrame(tags)
            df_0.to_excel(xlsx_file)
        tags = []
    return

#------------------------------------------------------------------------------------------------------
#
#   UIH PCT Bundles Operation Utils with CSV supporting
#       datacenter data structure v1
#       storageroot/modality/institution/tracer/pid-pn-studydate/[Image, PET, import.rawdata]
#
#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
#
def dump_uihpct_bundles_2_xlsx_datacenter_v1(working_root, xlsx_file, save_per_cases=100, mode='splitted'):
    """_summary_
        dump uihpct PET bundles with additional tags:
            
    Args:
        working_root (_type_): _description_
        xlsx_file (_type_): _description_
        save_per_cases (_type_): _description_
        mode (_type_): _description_ ['continuous', 'splitted']
    Returns:
        _type_: _description_
    """
    if save_per_cases <= 0: save_per_cases = 1
    if mode not in ['continuous', 'splitted']: mode = 'splitted'
    tags = []
    i_splitted = 0
    for sub_root, _, _ in os.walk(working_root):
        # check whether sub_root is valid UIH PCT Bundles root
        val_0 = os.path.isfile(os.path.join(sub_root, 'import.rawdata'))
        val_1 = os.path.isdir(os.path.join(sub_root, 'Image'))
        val_2 = os.path.isdir(os.path.join(sub_root, 'PET'))
        if not all([val_0, val_1, val_2]): continue
        
        # dump valid UIH PCT bundles into row of df
        print('working on %s...'%(sub_root))
        col_tags = DUMP_UIHPCT_BUNDLES_2_ONE_ROW()
        col_tags.update_bundles_by_petrawdata(sub_root)
        col_tag = col_tags.get_dcmtags()
        col_tag['StorageRoot'] = ''
        col_tag['SubRoot0'] = str(col_tag['ManufacturerModelName']).upper().replace(' ', '-')
        col_tag['SubRoot1'] = re.sub(r'[^a-zA-Z0-9\s]', repl='', string=str(col_tag['InstitutionName'])).upper().replace(' ', '_')
        col_tag['SubRoot2'] = str(col_tag['PT_SourceIsotopeName']) + '-' + \
                              re.sub(r'[^a-zA-Z0-9\s]', repl='', string=str(col_tag['PT_RadioPharmTracer'])).upper().replace(' ', '')
        col_tag['SubRoot3'] = 'PID-' \
                              + re.sub(r'[^a-zA-Z0-9\s]', repl='', string=str(col_tag['PatientID'])).upper().replace(' ', '') \
                              + '-PN-' \
                              +  re.sub(r'[^a-zA-Z0-9\s]', repl='', string=str(col_tag['PatientName'])).upper().replace(' ', '') \
                              + '-' + str(col_tag['StudyDate']) + str(col_tag['StudyTime'])[:4]
        tags.append(col_tag)
        
        if len(tags) % save_per_cases != 0: continue
        if mode == 'continuous':
            if os.path.isfile(xlsx_file): 
                df_0 = pd.read_excel(xlsx_file)
                df_i = pd.DataFrame(tags)
                df_1 = pd.concat([df_0, df_i], axis=0)
                df_1.to_excel(xlsx_file)
            else: 
                df_0 = pd.DataFrame(tags)
                df_0.to_excel(xlsx_file)
        elif mode =='splitted':
            df_i = pd.DataFrame(tags)
            df_i.to_excel(xlsx_file[:-5] + '-{:06d}.xlsx'.format(i_splitted))
            i_splitted += 1
        tags = []
    
    # in the case of the len(tags) is not N x save_per_cases:
    if len(tags) % save_per_cases != 0:
        if mode == 'continuous':
            if os.path.isfile(xlsx_file): 
                df_0 = pd.read_excel(xlsx_file)
                df_i = pd.DataFrame(tags)
                df_1 = pd.concat([df_0, df_i], axis=0)
                df_1.to_excel(xlsx_file)
            else: 
                df_0 = pd.DataFrame(tags)
                df_0.to_excel(xlsx_file)
        elif mode =='splitted':
            df_i = pd.DataFrame(tags)
            df_i.to_excel(xlsx_file[:-5] + '-{:06d}.xlsx'.format(i_splitted))
    return

#------------------------------------------------------------------------------------------------------
#
def _copy_uihpct_bundles_tree_datacenter_v1(src_bundles_root, target_bundles_root):
    """_summary_

    Args:
        src_bundles_root (_type_): _description_
            Image
            PET
            CT (will be copied)
            import.rawdata
        target_bundles_root (_type_): _description_
    """
    if not os.path.exists(src_bundles_root): return
    if not os.path.exists(target_bundles_root): return
    
    # copy <import.rawdata>
    src_import_rawdata_file = os.path.join(src_bundles_root, 'import.rawdata')
    target_import_rawdata_file = os.path.join(target_bundles_root, 'import.rawdata')
    if os.path.isfile(src_import_rawdata_file):
        shutil.copyfile(src_import_rawdata_file, target_import_rawdata_file)
    
    # copy <PET> rawdata
    src_PET_rawdata_subroot = os.path.join(src_bundles_root, 'PET')
    if os.path.exists(src_PET_rawdata_subroot):
        target_PET_rawdata_subroot = os.path.join(target_bundles_root, 'PET')
        for src_subroot, src_subdirs, src_filenames in os.walk(src_PET_rawdata_subroot):
            target_subroot = src_subroot.replace(src_PET_rawdata_subroot, target_PET_rawdata_subroot)
            os.makedirs(target_subroot, exist_ok=True)
            for src_subdir in src_subdirs:
                if src_subdir not in ['.', '..']: os.makedirs(os.path.join(target_subroot, src_subdir), exist_ok=True)
            for src_filename in src_filenames:
                abs_src_file = os.path.join(src_subroot, src_filename)
                abs_target_file = os.path.join(target_subroot, src_filename)
                if not os.path.isfile(abs_target_file): shutil.copyfile(abs_src_file, abs_target_file)
                
    # copy <Image> dicoms
    src_dcm_subroot = os.path.join(src_bundles_root, 'Image')
    if os.path.exists(src_dcm_subroot):
        target_dcm_subroot = os.path.join(target_bundles_root, 'Image')
        for src_subroot, src_subdirs, src_filenames in os.walk(src_dcm_subroot):
            target_subroot = src_subroot.replace(src_dcm_subroot, target_dcm_subroot)
            os.makedirs(target_subroot, exist_ok=True)
            for src_subdir in src_subdirs:
                if src_subdir not in ['.', '..']: os.makedirs(os.path.join(target_subroot, src_subdir), exist_ok=True)
            for src_filename in src_filenames:
                # not to copy repeated dcms: xxxxxxxx_x.dcm and only copy xxxxxxxx.dcm
                if re.match('[0-9]*.dcm', src_filename) is None: continue
                abs_src_file = os.path.join(src_subroot, src_filename)
                abs_target_file = os.path.join(target_subroot, src_filename)
                if not os.path.isfile(abs_target_file): shutil.copyfile(abs_src_file, abs_target_file)
                
    # copy other dicoms under this src_bundles_root into target_bundles_root/Image
    # for speed reason, the dicoms in this group are not validated
    dcm_series_subdirs = os.listdir(src_bundles_root)
    dcm_series_subroots = []
    for dcm_series_subdir in dcm_series_subdirs:
        if dcm_series_subdir in ['.', '..', 'Image', 'PET', 'CT']: continue
        dcm_series_subroots.append(os.path.join(src_bundles_root, dcm_series_subdir))
    for src_dcm_series_subroot in dcm_series_subroots:
        dcm_files = glob(os.path.join(src_dcm_series_subroot, '*.dcm'))
        if len(dcm_files) == 0: continue
        target_dcm_series_subroot = os.path.join(target_bundles_root, 'Image', os.path.basename(src_dcm_series_subroot))
        os.makedirs(target_dcm_series_subroot, exist_ok=True)
        for dcm_file in dcm_files:
            dcm_filename = os.path.basename(dcm_file)
            # not to copy repeated dcms: xxxxxxxx_x.dcm and only copy xxxxxxxx.dcm
            if re.match('[0-9]*.dcm', dcm_filename) is None: continue
            target_dcm_file = os.path.join(target_dcm_series_subroot, dcm_filename)
            if not os.path.isfile(target_dcm_file): shutil.copyfile(dcm_file, target_dcm_file)
    return
        
#------------------------------------------------------------------------------------------------------
#
def xlsx_copy_uihpct_bundles_2_datacenter_v1(df):
    """_summary_
        copy uihpct PET bundles from src_root into target_root with naming organization defined in df
        paired with dump_uihpct_bundles_2_df_datacenter_v1
            
    Args:

        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    for idx, row in df.iterrows():
        target_root = row['StorageRoot']
        if target_root == '': continue
        if target_root == 'NOTRUN': continue
        if os.path.sep not in target_root: continue
        if not os.path.isdir(target_root): continue
        target_bundles_subroot = os.path.join(target_root, row['SubRoot0'], row['SubRoot1'], 
                                              row['SubRoot2'], row['SubRoot3'])
        os.makedirs(target_bundles_subroot, exist_ok=True)
        src_bundles_subroot = row['BUNDLES_ROOT']
        if not os.path.isdir(src_bundles_subroot): continue
        
        print('copying %s to %s...'%(idx, target_bundles_subroot))
        try:
            #shutil.copytree(src_bundles_subroot, target_bundles_subroot, dirs_exist_ok=True)
            _copy_uihpct_bundles_tree_datacenter_v1(src_bundles_subroot, target_bundles_subroot)
            print('<yyyyyy> successed in copying to %s: %s'%(idx, target_bundles_subroot))
        except:
            print('<xxxxxx> failed in copying to %s: %s'%(idx, target_bundles_subroot))
    return