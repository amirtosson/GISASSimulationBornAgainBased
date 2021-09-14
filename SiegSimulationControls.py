# -*- coding: utf-8 -*-
"""
@author:    Amir Tosson
@license:   GNU General Public License v3 or higher
@copyright: Universität Siegen, Deutschland
@email:     tosson@physik.uni-siegen.de   
"""

"""
summary:    this model contains the controls and APIs of the 
            BornAgain-based simulation  

name:       SiegMainWindow

date:       01-04-2021
     
"""
import bornagain as ba
from bornagain import deg, nm
from random import randint
import matplotlib.pyplot as plt
import sys
import timeit as process_time
from random import randint
import multiprocessing
from numba import cuda
import numpy as np
import threading
import concurrent.futures
import SiegSample as _siegSample
import  SiegDetector as _siegDetector
import csv


t1_start=0
t1_stop=0



class SiegSimulationControls():
    resultAll = []
    def __init__(self, sample = _siegSample.SiegSample(1), detector = _siegDetector.SiegDetector(0), userData = []):
        super().__init__
        self.Sample = sample
        self.Detector = detector
        self.UserData = userData


    @property
    def Sample(self):
        return self._sample
    
    @Sample.setter
    def Sample(self, sample):
        self._sample = sample

    @property
    def Detector(self):
        return self._detector

    @Detector.setter
    def Detector(self, detector):
        self._detector = detector

    @property
    def UserData(self):
        return self._userData

    @UserData.setter
    def UserData(self, userData):
        self._userData = userData
    
    def InitBeam(self):
        direction = ba.Direction(0.64*deg, 0.0*deg)
        beam = ba.Beam(1e+16*0.3/80, 0.14073*nm, direction) 
        return beam
        
    def InitDetector(self):
        detector = ba.RectangularDetector(1024, 51.2, 1024, 51.2)
        detector.setResolutionFunction(ba.ResolutionFunction2DGaussian(0.02, 0.02))
        detector.setPerpendicularToReflectedBeam(1277.0, 10.75, 20.65)
        return detector
    
    def InitSim(self,_sample, _beam, _detector):
        sim = ba.GISASSimulation(_beam, _sample, _detector)
        sim.getOptions().setUseAvgMaterials(True)
        sim.getOptions().setIncludeSpecular(True)
        background = ba.ConstantBackground(5e+01)
        sim.setBackground(background)
        return sim


    def InitSample(self,numLayers=1, ThiDataUser=0, DisDataUser=0, AbsorUserData=0):
        # Defining constant materials
        materialAir = ba.HomogeneousMaterial("Air", 0.0, 0.0)
        materialSiO2 = ba.HomogeneousMaterial("SiO2", 5.93e-06, 7.42e-08)
        materialSubstrate = ba.HomogeneousMaterial("Substrate", 6.31e-06, 1.21e-07)
        # Defining constant Layers
        layerAir = ba.Layer(materialAir)
        layerSiO2 = ba.Layer(materialSiO2, 100* nm)
        layerSubstrate = ba.Layer(materialSubstrate, 500* nm)

        # Defining Roughness of constant layers
        layerRoughnessSiO2 = ba.LayerRoughness(0.54* nm, 0.6* nm, 30.0 * nm)
        layerRoughnessSubstrate = ba.LayerRoughness(0.54* nm, 0.6* nm, 30.0 * nm)
        # Defining layers roughness
        layersRoughness = [ba.LayerRoughness(0.46* nm, 0.6* nm, 30.0 * nm), ba.LayerRoughness(0.39* nm, 0.6* nm, 30.0 * nm),
                           ba.LayerRoughness(0.57* nm, 0.6* nm, 30.0 * nm)]

        # Defining layers names
        layersNames = ["TaO", "Ta", "Cu3N"]
        multiLayer = ba.MultiLayer()
        multiLayer.setCrossCorrLength(2000)

        # Adding the Air layer
        multiLayer.addLayer(layerAir)
        for i in range(numLayers):
            material = ba.HomogeneousMaterial(self.UserData[i][0], self.UserData[i][2] *1e-06, self.UserData[i][3] *1e-08)
            layer = ba.Layer(material, self.UserData[i][1]* nm)
            layerRoughness = ba.LayerRoughness(self.UserData[i][4]* nm, 0.6* nm, 30.0 * nm)
            multiLayer.addLayerWithTopRoughness(layer, layerRoughness)

        # Adding the SiO2 layer
        multiLayer.addLayerWithTopRoughness(layerSiO2, layerRoughnessSiO2)

        # Adding the Substrate layer
        multiLayer.addLayerWithTopRoughness(layerSubstrate, layerRoughnessSubstrate)
        return multiLayer

    def InitSampleLegacy(self, onlyLayers=False, ThiDataUser=0, DisDataUser=0):
        if onlyLayers == False:
            disData = [0] * 20
            thickData = [0] * 20
            for i in range(20):
                x = 1
                y = 1
                if i % 2 == 0:
                    x = 2
                    y = 6
                dis_h = (x + 0.2 * randint(0, 10)) * 1e-05
                thi_h = (y + (y/x) * 0.2 * randint(0, 10))
                disData[i] = dis_h
                thickData[i] = thi_h
        else:
            disData = DisDataUser
            thickData = ThiDataUser
        material_1 = ba.HomogeneousMaterial("Air", 0.0, 0.0)
        material_2 = ba.HomogeneousMaterial("TaO", disData[0], 3.3e-7)
        material_3 = ba.HomogeneousMaterial("Ta1", disData[2], 2.34e-06)
        material_4 = ba.HomogeneousMaterial("Cu3N1", disData[3], 3.65e-07)
        material_5 = ba.HomogeneousMaterial("Ta2", disData[4], 2.34e-06)
        material_6 = ba.HomogeneousMaterial("Cu3N2", disData[5], 3.65e-07)
        material_7 = ba.HomogeneousMaterial("Ta3", disData[6], 2.34e-06)
        material_8 = ba.HomogeneousMaterial("Cu3N3", disData[7], 3.65e-07)
        material_9 = ba.HomogeneousMaterial("Ta4", disData[8], 2.34e-06)
        material_10 = ba.HomogeneousMaterial("Cu3N4", disData[9], 3.65e-07)
        material_11 = ba.HomogeneousMaterial("Ta5", disData[10], 2.34e-06)
        material_12 = ba.HomogeneousMaterial("Cu3N5", disData[11], 3.65e-07)
        material_13 = ba.HomogeneousMaterial("Ta6", disData[12], 2.34e-06)
        material_14 = ba.HomogeneousMaterial("SiO2", 5.93e-06, 7.42e-08)
        material_15 = ba.HomogeneousMaterial("Substrate", 6.31e-06, 1.21e-07)

        # Defining Layers
        layer_1 = ba.Layer(material_1)
        layer_2 = ba.Layer(material_2, thickData[0])
        layer_3 = ba.Layer(material_3, thickData[1])
        layer_4 = ba.Layer(material_4, thickData[2])
        layer_5 = ba.Layer(material_5, thickData[3])
        layer_6 = ba.Layer(material_6, thickData[4])
        layer_7 = ba.Layer(material_7, thickData[5])
        layer_8 = ba.Layer(material_8, thickData[6])
        layer_9 = ba.Layer(material_9, thickData[7])
        layer_10 = ba.Layer(material_10, thickData[8])
        layer_11 = ba.Layer(material_11, thickData[9])
        layer_12 = ba.Layer(material_12, thickData[10])
        layer_13 = ba.Layer(material_13, thickData[11])
        layer_14 = ba.Layer(material_14, 100)
        layer_15 = ba.Layer(material_15, 500)

        # Defining Roughness Parameters
        layerRoughness_1 = ba.LayerRoughness(0.46,0.6, 30.0*nm)
        layerRoughness_2 = ba.LayerRoughness(0.46, 0.6, 30.0*nm)
        layerRoughness_3 = ba.LayerRoughness(0.39, 0.6, 30.0*nm)
        layerRoughness_4 = ba.LayerRoughness(0.57, 0.6, 30.0*nm)
        layerRoughness_5 = ba.LayerRoughness(0.39, 0.6, 30.0*nm)
        layerRoughness_6 = ba.LayerRoughness(0.57, 0.6, 30.0*nm)
        layerRoughness_7 = ba.LayerRoughness(0.39, 0.6, 30.0*nm)
        layerRoughness_8 = ba.LayerRoughness(0.57, 0.6, 30.0*nm)
        layerRoughness_9 = ba.LayerRoughness(0.39, 0.6, 30.0*nm)
        layerRoughness_10 = ba.LayerRoughness(0.57, 0.6, 30.0*nm)
        layerRoughness_11 = ba.LayerRoughness(0.39, 0.6, 30.0*nm)
        layerRoughness_12 = ba.LayerRoughness(0.57, 0.6, 30.0*nm)
        layerRoughness_13 = ba.LayerRoughness(0.54, 0.6, 30.0*nm)
        layerRoughness_14 = ba.LayerRoughness(0.54, 0.6, 30.0*nm)

        f = np.random.randint(10, size=1) + 1
        with open('dataNumLayer.csv', 'a', encoding='UTF8', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow(f)
        fd.close()



        multiLayer_1 = ba.MultiLayer()
        multiLayer_1.setCrossCorrLength(2000)
        multiLayer_1.addLayer(layer_1)
        multiLayer_1.addLayerWithTopRoughness(layer_2, layerRoughness_1)
        f = f-1
        if f> 0:
            multiLayer_1.addLayerWithTopRoughness(layer_3, layerRoughness_2)
        f = f - 1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_4, layerRoughness_3)
        f = f-1
        if f> 0:
            multiLayer_1.addLayerWithTopRoughness(layer_5, layerRoughness_4)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_6, layerRoughness_5)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_7, layerRoughness_6)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_8, layerRoughness_7)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_9, layerRoughness_8)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_10, layerRoughness_9)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_11, layerRoughness_10)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_12, layerRoughness_11)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_13, layerRoughness_12)
        f = f-1
        if f > 0:
            multiLayer_1.addLayerWithTopRoughness(layer_14, layerRoughness_13)

        multiLayer_1.addLayerWithTopRoughness(layer_15, layerRoughness_14)
        return multiLayer_1



    def InitSampleSingle(self):
        multiLayer_1 = ba.MultiLayer()
        multiLayer_1.setCrossCorrLength(2000) 
        
        material_1 = ba.HomogeneousMaterial("Air", 0.0, 0.0)
        layer_1 = ba.Layer(material_1)
        multiLayer_1.addLayer(layer_1)
        for i in range(len(self.Sample.layersData)):
            multiLayer_1.addLayerWithTopRoughness(ba.Layer( ba.HomogeneousMaterial("TaO"+str(i), 0.2*self.Sample.layersData[i][0]*1e-05, 3.3e-7), self.Sample.layersData[i][1]), ba.LayerRoughness(0.46,0.6, 30.0*nm))        
        return multiLayer_1


    
    
    def RunSim(self,_simulation):
        #import ba_plot
        #t1_start = process_time.default_timer()
        #_simulation.getOptions().setNumberOfBatches(10)
        #_simulation.getOptions().setNumberOfThreads(6)  
        #print(_simulation.numberOfSimulationElements())  
        _simulation.getOptions().setUseAvgMaterials(True)
        _simulation.getOptions().setIncludeSpecular(False)
        #_simulation.getOptions().setMonteCarloIntegration(False)
    
        background = ba.ConstantBackground(5e+01)
        _simulation.setBackground(background)
        #ba_plot.run_and_plot(_simulation)
        _simulation.runSimulation()  
        result = _simulation.result()   
        hist = result.histogram2d(ba.Axes.DEGREES)
        resultarr = hist.array()
        #resultAll.append(resultarr)
        #t1_stop = process_time.default_timer()
        #print("Sim_ " ,t1_stop-t1_start)
        return resultarr
    
    
    
    def StartSim(self, numOfLayer=1, ThiDataUser=0, DisDataUser=0, AbsorUserData=0):
        #print("\n ThreadStart " ,thrId)
        #self.RunSim(self.InitSim(self.InitSample(), self.InitBeam(), self.InitDetector()))
        #print("\n ThreadEnd " ,thrId)
        #return ("DONE ")
        #fig = plt.figure(figsize=(6, 3.2))

        zpoints, slds = ba.materialProfile(self.InitSample(numOfLayer,ThiDataUser,DisDataUser,AbsorUserData))
        return self.RunSim(self.InitSim(self.InitSample(numOfLayer,ThiDataUser,DisDataUser,AbsorUserData), self.InitBeam(), self.InitDetector())),zpoints, slds

        #return ("DONE ")
       # ax = fig.add_subplot()
       # ax.set_title('colorMap')
        #plt.imshow(resArr)
        
    
    
    def Test(self):
        t1_start = process_time.default_timer()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(self.StartSim) for x in range(4)]
        for f in concurrent.futures.as_completed(results):
            print(f.result())            
        t1_stop = process_time.default_timer()
        print("\n ThreadingT " ,t1_stop-t1_start)
        
    def TestNormal(self):
        #print( len(resultAll))
        t1_start = process_time.default_timer()
        for index in range(4):
             print(self.StartSim())
        t1_stop = process_time.default_timer()
        print("\n NOThreading " ,t1_stop-t1_start)
      
    def GenerateRefData(self, numOfLayer=1, ThiDataUser=0, DisDataUser=0, AbsorUserData=0):
        return self.StartSim(numOfLayer, ThiDataUser, DisDataUser, AbsorUserData)


    def TestVar(self):
        print(self.UserData[0][0])





    
    
    
    
    
    
    