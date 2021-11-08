"""
@author:    Amir Tosson
@license:   GNU General Public License v3 or higher
@copyright: Universität Siegen, Deutschland
@email:     tosson@physik.uni-siegen.de
"""

"""
summary:    this model contains the checker functions 
            for different parameters of the simulation 
            components (sample, detector, beam .. etc)

name:       SiegParaChecker

date:       08-11-2021

"""


class SiegParaChecker(object):
    def __init__(self):
        super().__init__

    def CheckSamplePara(self, include_physics=False, sample_para=[]):
        #print(len(sample_para))
        return True

    def CheckDetectorPara(self, include_physics=False, detector_para=[]):
        #print(len(detector_para))
        return True

    def CheckBeamPara(self, include_physics=False, beam_para=[]):
        #print(len(beam_para))
        return True

    def CheckSimPara(self, include_physics=False, sim_para=[]):
        #print(len(sim_para))
        return True
