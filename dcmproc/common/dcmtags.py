#-----------------------------------------------------------------------------------------------------
#
#   Project - dcmproc
#   Description:
#       A python processing package for various dicom operation
#   Author: hui.liu02@united-imaging.com
#   Created 2022-04-28
#-----------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
#

# specific characterset encoding
TagSpecificEncoding            = [0x0008, 0x0005]

# institution
TagInstitutionName              = [0x0008, 0x0080]

# general tags - patient
TagPatientName                 = [0x0010, 0x0010]
TagPatientID                   = [0x0010, 0x0020]
TagPatientAge                  = [0x0010, 0x1010]
TagPatientSex                  = [0x0010, 0x0040]
TagPatientWeight               = [0x0010, 0x1030]

# general tags - study, series
TagStudyDate                   = [0x0008, 0x0020]
TagStudyTime                   = [0x0008, 0x0030]
TagSeriesNumber                = [0x0020, 0x0014]
TagSeriesDescription           = [0x0008, 0x103e]

# general tags - acquisition timing
TagAcquisitionDateTime         = [0x0008, 0x002a]
TagAcquisitionDuration         = [0x0018, 0x9073]

# general tags - modality
TagModality                    = [0x0008, 0x0060]
TagManufacturer                = [0x0008, 0x0070]

# general tags - matrix
TagRows                        = [0x0028, 0x0010]
TagColumns                     = [0x0028, 0x0011]
TagSeriesNbSlices              = [0x0054, 0x0081]
TagNbTimeSlices                = [0x0054, 0x0101]

# MR specific tags
TagMRAcquisitionType           = [0x0018, 0x0023]
TagSequenceName                = [0x0018, 0x0024]
TagTR                          = [0x0018, 0x0080]
TagTE                          = [0x0018, 0x0081]
TagFunc                        = [0x0065, 0x102b]

# PET specific tags
TagAxialDetectorDimension      = [0x0018, 0x9727]

TagActualFrameDuration         = [0x0018, 0x1242]
TagSourceIsotopeName           = [0x300a, 0x0226]
TagUnit                        = [0x0054, 0x1001]

TagRadiopharmaceuticalInformationSequence = [0x0054, 0x0016]
TagRadiopharmaceutical                    = [0x0018, 0x0031]
TagRadiopharmaceuticalStartDateTime       = [0x0018, 0x1078]
TagRadionuclideHalfLife                   = [0x0018, 0x1075]
TagRadionuclideTotalDose                  = [0x0018, 0x1074]

TagCorrectedImage              = [0x0028, 0x0051]
TagDecayCorrection             = [0x0054, 0x1102]

TagFrameReferenceTime          = [0x0054, 0x1300]
TagDecayFactor                 = [0x0054, 0x1321]
TagDoseCalibrationFactor       = [0x0054, 0x1322]
TagScatterFractionFactor       = [0x0054, 0x1323]

TagSeriesType                  = [0x0054, 0x1000]
TagImageIndex                  = [0x0054, 0x1330]

TagPerFrameFunctionalGroupsSequence     = [0x5200, 0x9230]


# CT specific tags


# UIH private tags - multi subseries
TagSubSeriesID                 = [0x0065, 0x102c]
