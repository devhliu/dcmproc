#-----------------------------------------------------------------------------------------------------
#
#   Project - dcmproc
#   Description:
#       A python processing package for various dicom operation
#   Author: hui.liu02@united-imaging.com
#   Created 2022-05-24
#-----------------------------------------------------------------------------------------------------

from setuptools import setup, find_packages

required_packages = ['pydicom', 'pandas']

setup(name='dcmproc',
      version='0.0.1',
      description='A python processing package for various dicom operation',
      author='UIH-MI-RECON',
      author_email='hui.liu02@united-imaging.com',
      packages=find_packages(),
      install_requires=required_packages,
      include_package_data=True
      )