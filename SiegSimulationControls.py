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
t1_start=0
t1_stop=0



class SiegSimulationControls():
    resultAll = []
    def __init__(self, sample = _siegSample.SiegSample(1)):
        super().__init__
        self.Sample = sample


    @property
    def Sample(self):
        return self._sample
    
    @Sample.setter
    def Sample(self, sample):
        self._sample = sample
    
    def InitBeam(self):
        direction = ba.Direction(0.64*deg, 0.0*deg)
        beam = ba.Beam(1e+16*0.3/80, 0.14073*nm, direction) 
        return beam
        
    def InitDetector(self):
        detector = ba.RectangularDetector(1024, 15, 1024, 51.2)
        detector.setResolutionFunction(ba.ResolutionFunction2DGaussian(0.02, 0.02))
        detector.setPerpendicularToReflectedBeam(1277.0, 0.75, 20.65)
        return detector
    
    def InitSim(self,_sample, _beam, _detector):
        sim = ba.GISASSimulation(_beam, _sample, _detector)
        sim.getOptions().setUseAvgMaterials(True)
        sim.getOptions().setIncludeSpecular(False)
        background = ba.ConstantBackground(5e+01)
        sim.setBackground(background)
        return sim
    
    def InitSample(self):
        t1_start = process_time.default_timer()
        #print("starting")
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
        thi1=(1+0.6*randint(0,10))
        thi2=(1+0.6*randint(0,10))
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
        #print("a")
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
    
        #print("b")
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
    
        #print("c")
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
        #print("d")
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
        t1_stop = process_time.default_timer()
        #print("Sample_ " ,t1_stop-t1_start)
        return multiLayer_1



    def InitSampleSingle(self):
        multiLayer_1 = ba.MultiLayer()
        multiLayer_1.setCrossCorrLength(2000)    
        for i in range(len(self.Sample.layersData)):
            print(self.Sample.layersData[i][0])
            multiLayer_1.addLayerWithTopRoughness(ba.Layer( ba.HomogeneousMaterial("TaO"+str(i), 0.2*self.Sample.layersData[i][0]*1e-05, 3.3e-7), self.Sample.layersData[i][1]), ba.LayerRoughness(0.46,0.6, 30.0*nm))        
        return multiLayer_1


    
    
    def RunSim(self,_simulation):
        import ba_plot
        #t1_start = process_time.default_timer()
        #_simulation.getOptions().setNumberOfBatches(10)
        #_simulation.getOptions().setNumberOfThreads(6)  
        #print(_simulation.numberOfSimulationElements())  
        _simulation.getOptions().setUseAvgMaterials(True)
        _simulation.getOptions().setIncludeSpecular(False)
        #_simulation.getOptions().setMonteCarloIntegration(False)
    
        background = ba.ConstantBackground(5e+01)
        _simulation.setBackground(background)
        ba_plot.run_and_plot(_simulation)
        #_simulation.runSimulation()  
        #result = _simulation.result()   
        #hist = result.histogram2d(ba.Axes.QSPACE)
        #resultarr = hist.array()
        #resultAll.append(resultarr)
        #t1_stop = process_time.default_timer()
        #print("Sim_ " ,t1_stop-t1_start)
        #return resultarr
    
    
    
    def StartSim(self):
        #print("\n ThreadStart " ,thrId)
        #self.RunSim(self.InitSim(self.InitSample(), self.InitBeam(), self.InitDetector()))
        #print("\n ThreadEnd " ,thrId)
        #return ("DONE ")
        #fig = plt.figure(figsize=(6, 3.2))
        self.RunSim(self.InitSim(self.InitSample(), self.InitBeam(), self.InitDetector()))
        return ("DONE ")
       # ax = fig.add_subplot()
       # ax.set_title('colorMap')
        #plt.imshow(resArr)
        
    
    
    def Test(self):
        # print(threading.activeCount())
        t1_start = process_time.default_timer()
        with concurrent.futures.ProcessPoolExecutor() as executer:
            results = [executer.submit(self.StartSim) for x in range(4)]
        for f in concurrent.futures.as_completed(results):
            print(f.result())
        
        
        
        
        #threads = list()
        #main_thread = threading.currentThread()
        # for index in range(threading.activeCount()):
        #     x = threading.Thread(target=StartSim, args=(index,))
        #     threads.append(x)
        #     #x.start()
        # for j in threads:
        #     j.start()
    
        # # Ensure all of the processes have finished
        # for j in threads:
        #     j.join()    
            
        t1_stop = process_time.default_timer()
        print("\n ThreadingT " ,t1_stop-t1_start)
        self.TestNormal()
        
        
        
    def TestNormal(self):
        #print( len(resultAll))
        t1_start = process_time.default_timer()
        for index in range(4):
             print(self.StartSim())
        t1_stop = process_time.default_timer()
        print("\n NOThreading " ,t1_stop-t1_start)
    
    
    
    def GenerateRefData(self):
        return self.StartSim()
    





















#     driver.init()
#     ngpus = driver.Device.count()
#     for i in range(ngpus):
#         t = gpuThread(i)
#         t.start()
#         t.join()

# # Print the result
#     print("data.count()")
    
    
# @cuda.jit
# def my_kernel(io_array):
#     # Thread id in a 1D block
#     tx = cuda.threadIdx.x
#     # Block id in a 1D grid
#     ty = cuda.blockIdx.x
#     # Block width, i.e. number of threads per block
#     bw = cuda.blockDim.x
#     # Compute flattened index inside the array
#     pos = tx + ty * bw
#     if pos < io_array.size:  # Check array boundaries
#         io_array[pos] *= 2 # do the computation    
    
    
    
# @cuda.jit
# def SamplePrepParallel(io_array):    
#     dis1=(1+0.2)*1e-05
#     thi1=(1+0.6)
#     tx = cuda.threadIdx.x
#     io_array[tx] = thi1

#     #layer_1 = ba.Layer(material_1)
#     #multiLayer_1 = ba.MultiLayer()
#     #multiLayer_1.setCrossCorrLength(2000)
#     #multiLayer_1.addLayer(layer_1)
    



    
    
    
    
    
    
    