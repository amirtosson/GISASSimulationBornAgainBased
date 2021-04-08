# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 11:12:24 2021

@author: Tosson
"""

import multiprocessing





import numpy as np
import timeit
import bornagain as ba
from bornagain import deg, nm
from random import randint



def InitBeam():
    direction = ba.Direction(0.64*deg, 0.0*deg)
    beam = ba.Beam(1e+16*0.3/80, 0.14073*nm, direction) 
    return beam

def InitDetector():
    detector = ba.RectangularDetector(128, 60, 128, 60)
    detector.setResolutionFunction(ba.ResolutionFunction2DGaussian(0.02, 0.02))
    detector.setPerpendicularToReflectedBeam(1277.0, 0.75, 20.65)
    return detector

def InitSim(_sample, _beam, _detector):
    sim = ba.GISASSimulation(_beam, _sample, _detector)
    sim.getOptions().setUseAvgMaterials(True)
    sim.getOptions().setIncludeSpecular(False)
    background = ba.ConstantBackground(5e+01)
    sim.setBackground(background)
    return sim

def InitSample():
    dis1=(1+0.2*randint(0,10))*1e-05
    dis2=(2+0.2*randint(0,10))*1e-05
    dis3=(1+0.2*randint(0,10))*1e-05
    dis4=(2+0.2*randint(0,10))*1e-05
    dis5=(1+0.2*randint(0,10))*1e-05
    dis6=(2+0.2*randint(0,10))*1e-05
    dis7=(1+0.2*randint(0,10))*1e-05
    dis8=(2+0.2*randint(0,10))*1e-05
    dis9=(1+0.2*randint(0,10))*1e-05
    dis10=(2+0.2*randint(0,10))*1e-05
    dis11=(1+0.2*randint(0,10))*1e-05
    dis12=(2+0.2*randint(0,10))*1e-05
    thi1=(1+0.4*randint(0,10))
    thi2=(1+0.4*randint(0,10))
    thi3=(6+0.6*randint(0,10))
    thi4=(1+0.4*randint(0,10))
    thi5=(6+0.6*randint(0,10))
    thi6=(1+0.4*randint(0,10))
    thi7=(6+0.6*randint(0,10))
    thi8=(1+0.4*randint(0,10))
    thi9=(6+0.6*randint(0,10))
    thi10=(1+0.4*randint(0,10))
    thi11=(6+0.6*randint(0,10))
    thi12=(1+0.4*randint(0,10))

    material_1 = ba.HomogeneousMaterial("Air", 0.0, 0.0)
    material_2 = ba.HomogeneousMaterial("TaO", dis1, 3.3e-7)
    material_3 = ba.HomogeneousMaterial("Ta1", dis2, 2.34e-06)
    material_4 = ba.HomogeneousMaterial("Cu3N1",dis3, 3.65e-07)
    material_5 = ba.HomogeneousMaterial("Ta2", dis4, 2.34e-06)
    material_6 = ba.HomogeneousMaterial("Cu3N2", dis5, 3.65e-07)
    material_7 = ba.HomogeneousMaterial("Ta3", dis6, 2.34e-06)
    material_8 = ba.HomogeneousMaterial("Cu3N3", dis7, 3.65e-07)
    material_9 = ba.HomogeneousMaterial("Ta4", dis8, 2.34e-06)
    material_10 = ba.HomogeneousMaterial("Cu3N4", dis9, 3.65e-07)
    material_11 = ba.HomogeneousMaterial("Ta5", dis10, 2.34e-06)
    material_12 = ba.HomogeneousMaterial("Cu3N5", dis11, 3.65e-07)
    material_13 = ba.HomogeneousMaterial("Ta6", dis12, 2.34e-06)
    material_14 = ba.HomogeneousMaterial("SiO2", 5.93e-06, 7.42e-08)
    material_15 = ba.HomogeneousMaterial("Substrate", 6.31e-06, 1.21e-07)


    # Defining Layers
    layer_1 = ba.Layer(material_1)
    layer_2 = ba.Layer(material_2,thi1)
    layer_3 = ba.Layer(material_3,thi2)
    layer_4 = ba.Layer(material_4, thi3)
    layer_5 = ba.Layer(material_5, thi4)
    layer_6 = ba.Layer(material_6, thi5)
    layer_7 = ba.Layer(material_7, thi6)
    layer_8 = ba.Layer(material_8, thi7)
    layer_9 = ba.Layer(material_9, thi8)
    layer_10 = ba.Layer(material_10, thi9)
    layer_11 = ba.Layer(material_11, thi10)
    layer_12 = ba.Layer(material_12, thi11)
    layer_13 = ba.Layer(material_13, thi12)
    layer_14 = ba.Layer(material_14, 100)
    layer_15 = ba.Layer(material_15)


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
    #print(multiprocessing.cpu_count())
    
    multiLayer_1 = ba.MultiLayer()
    multiLayer_1.setCrossCorrLength(2000)
    multiLayer_1.addLayer(layer_1)
    multiLayer_1.addLayerWithTopRoughness(layer_2, layerRoughness_1)
    multiLayer_1.addLayerWithTopRoughness(layer_3, layerRoughness_2)
    multiLayer_1.addLayerWithTopRoughness(layer_4, layerRoughness_3)
    multiLayer_1.addLayerWithTopRoughness(layer_5, layerRoughness_4)
    multiLayer_1.addLayerWithTopRoughness(layer_6, layerRoughness_5)
    multiLayer_1.addLayerWithTopRoughness(layer_7, layerRoughness_6)
    multiLayer_1.addLayerWithTopRoughness(layer_8, layerRoughness_7)
    multiLayer_1.addLayerWithTopRoughness(layer_9, layerRoughness_8)
    multiLayer_1.addLayerWithTopRoughness(layer_10, layerRoughness_9)
    multiLayer_1.addLayerWithTopRoughness(layer_11, layerRoughness_10)
    multiLayer_1.addLayerWithTopRoughness(layer_12, layerRoughness_11)
    multiLayer_1.addLayerWithTopRoughness(layer_13, layerRoughness_12)
    multiLayer_1.addLayerWithTopRoughness(layer_14, layerRoughness_13)
    multiLayer_1.addLayerWithTopRoughness(layer_15, layerRoughness_14)
    return multiLayer_1


def DetectorSetup():
    detector = ba.RectangularDetector(30, 1.5, 1024, 51.2)
    detector.setPerpendicularToReflectedBeam(1277.0, 0.75, 20.65)
    return detector




#sample initialization    
sample = InitSample()
print("Sample is set")

#dector initialization 
detector = InitDetector()
print("Detector is set")

#beam initialization 
beam = InitBeam()
print("Beam is set")

#simulation initialization
simulation = InitSim(sample, beam, detector)






















