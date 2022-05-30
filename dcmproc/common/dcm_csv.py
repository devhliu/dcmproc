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

from dcmproc.common.dcmtags import *

#------------------------------------------------------------------------------------------------------
#
class DUMP_DCMSERIESTAGS_2_ONE_ROW():
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