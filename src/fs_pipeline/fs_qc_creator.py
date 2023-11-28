#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 09:57:31 2017

@author: shahidm
"""

import os
import nipype.pipeline.engine as pe
import nipype.interfaces.utility as util
from nipype.interfaces.utility import IdentityInterface
from nipype.interfaces.io import FreeSurferSource    
from .screenshot import create_mri_screenshots


def get_path(subjectid, output_dir, filepattern):
    
    import os

    full_path=os.path.join(output_dir,subjectid, "mri", filepattern+".mgz")

    return full_path

    
def create_qc_wf(output_dir, subject_ids, work_dir, name="fs_qc_snapshot"):
   
    cwf = pe.Workflow(name=name)
    
    inputnode = pe.Node(interface=IdentityInterface(fields=['subject_ids']),
                        name='inputnode')
    inputnode.iterables = [('subject_ids', subject_ids)] 
    inputnode.inputs.subject_ids = subject_ids
    
    cwf.base_dir = os.path.abspath(work_dir)
            

    #qc snapshots
    qcsnapshots = pe.Node(interface=util.Function(input_names=['path_orig','path_aseg','out_dir','subject_id', 'num_slices','padd','spacing','image_extension'],
                                                  output_names=['dual_sagittal','dual_axial'],
                                                  function=create_mri_screenshots),name='create_qc_snapshots')

    qcsnapshots.inputs.out_dir=output_dir
    qcsnapshots.inputs.num_slices=60
    qcsnapshots.inputs.padd=4
    qcsnapshots.inputs.spacing=3
    qcsnapshots.inputs.image_extension='png'


    cwf.connect(inputnode, 'subject_ids', qcsnapshots, 'subject_id')

    cwf.connect(inputnode, ('subject_ids', get_path, output_dir,
                               "aseg"), qcsnapshots, 'path_aseg')

    cwf.connect(inputnode, ('subject_ids', get_path, output_dir,
                               "orig"), qcsnapshots, 'path_orig')

    
    return cwf
    
