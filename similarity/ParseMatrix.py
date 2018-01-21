from TextSimilar import cosine_sim
from numpy import argmax
import csv

testList = []

similarityMatrix = cosine_sim(*testList).tolist()
topicsList = []
masterList = []
delCount = 0

for simList in similarityMatrix:
  topic = []
  selfIndex = simList.index(max(simList))
  topic.append(selfIndex)
  for simIndex in range(selfIndex + 1, len(simList)):
    if (simList[simIndex] < 0.95 and simList[simIndex] > 0.15 and simIndex not in masterList): #refine later
      topic.append(simIndex)
      delCount = sum(num < simIndex for num in masterList)
      del similarityMatrix[simIndex - delCount]
      masterList.append(simIndex)
  topicsList.append(topic)

print(topicsList)