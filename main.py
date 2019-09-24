import pandas as pd
import os
import regex as re
import Parser as p
import numpy as np
import math
import experiment as exp
from CVRP import CVRPInfo as CVRP
from CuckooSearchCVRP import CuckooSearch

experimentData = []
instanceData = []

#region Load Datasets
DataSetAPath = 'data/A-VRP/'
DataSetBPath = 'data/B-VRP/'
DataSetPPath = 'data/P-VRP/'

DataSetA = os.listdir(DataSetAPath) # list of file names of benchmark instances from Set A
DataSetB = os.listdir(DataSetBPath) # list of file names of benchmark instances from Set B
DataSetP = os.listdir(DataSetPPath) # list of file names of benchmark instances from Set P
#end region


ResultsSetAPath = 'results/A-VRP/'
ResultsSetBPath = 'results/B-VRP/'
ResultsSetPPath = 'results/P-VRP/'

FinalResultsSetAPath = 'finalresults/A-VRP/'
FinalResultsSetBPath = 'finalresults/B-VRP/'
FinalResultsSetPPath = 'finalresults/P-VRP/'

#region Initialize Parameters
#Initialize Cuckoo SearchParameters
numNests = 15
Pa = 0.25 # Fraction of worse solutions to be replaced
Pc = 0.6 # Fraction of cuckoos performing Levy Flights
maxGenerations = 1000# maximum number of iterations
stopCriterion = maxGenerations # attempt limit of successive iterations

print('Parameters: numNests = ' + str(numNests) + ' Pa = ' + str(Pa) + ' Pc = ' + str(Pc) +
' maxGenerations: ' + str(maxGenerations) + ' stopCriterion = ' + str(stopCriterion))

#region iterate once
fileNameSuffix = 'twoOpt_exchange_5050_levy6_savingsInitial'
data = []
data = exp.initializeInstanceData()
for dataset in DataSetA:
        CVRPInstance = CVRP(DataSetAPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        exp.appendRowToInstanceDf(data, solver.readData())
exp.saveResultsToCsv(data, ResultsSetAPath, fileNameSuffix)

data = exp.initializeInstanceData()
for dataset in DataSetB:
        CVRPInstance = CVRP(DataSetBPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        exp.appendRowToInstanceDf(data, solver.readData())
exp.saveResultsToCsv(data, ResultsSetBPath, fileNameSuffix)

data = exp.initializeInstanceData()
for dataset in DataSetP:
        CVRPInstance = CVRP(DataSetPPath + dataset) #pass data to CVRP       
        solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
        solver.solveInstance()
        exp.appendRowToInstanceDf(data, solver.readData())
exp.saveResultsToCsv(data, ResultsSetPPath, fileNameSuffix)
#endregion
#region iterate 30 times
numIter = 10

experimentData = exp.initializeExperimentData()
instanceData = exp.initializeInstanceData()
for dataset in DataSetA:
        instanceData = exp.initializeInstanceData()
        for i in range(numIter):
                CVRPInstance = CVRP(DataSetAPath + dataset) #pass data to CVRP       
                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
                solver.solveInstance()
                exp.appendRowToInstanceDf(instanceData, solver.readData())
        row = exp.calculateInstanceResults(instanceData)
        exp.appendRowToExperimentDf(experimentData, row)
exp.saveResultsToCsv(experimentData, FinalResultsSetAPath, type='finalresults')

experimentData = exp.initializeExperimentData()
instanceData = exp.initializeInstanceData()
for dataset in DataSetB:
        instanceData = exp.initializeInstanceData()
        for i in range(numIter):
                CVRPInstance = CVRP(DataSetBPath + dataset) #pass data to CVRP       
                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
                solver.solveInstance()
                exp.appendRowToInstanceDf(instanceData, solver.readData())
        row = exp.calculateInstanceResults(instanceData)
        exp.appendRowToExperimentDf(experimentData, row)
exp.saveResultsToCsv(experimentData, FinalResultsSetBPath, type='finalresults')


experimentData = exp.initializeExperimentData()
instanceData = exp.initializeInstanceData()
for dataset in DataSetP:
        instanceData = exp.initializeInstanceData()
        for i in range(numIter):
                CVRPInstance = CVRP(DataSetPPath + dataset) #pass data to CVRP       
                solver = CuckooSearch(CVRPInstance = CVRPInstance, numCuckoos = numNests, Pa = Pa, Pc = Pc, generations = maxGenerations)
                solver.solveInstance()
                exp.appendRowToInstanceDf(instanceData, solver.readData())
        row = exp.calculateInstanceResults(instanceData)
        exp.appendRowToExperimentDf(experimentData, row)
exp.saveResultsToCsv(experimentData, FinalResultsSetPPath, type='finalresults')


#endregion



