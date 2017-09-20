import csv
import operator
import numpy as np
import os

#define your path
Global = 'C:/Users/xiong/Desktop/TestFile/'
#test.csv is the file name you input
GlobalPathInput = Global + 'test.csv'
GlobalStepPath1 = Global + 'Step1Result.csv'
GlobalStepPath2 = Global + 'Step2Result.csv'
GlobalStepPath3 = Global + 'Step3Result.csv'
GlobalStepPath3_1 = Global + 'Step3_1Result.csv'
GlobalStepPath4 = Global + 'Step4Result.csv'
GlobalStepPath5 = Global + 'Step5Result.csv'
GlobalStepPath6 = Global + 'Result.csv'

with open(GlobalPathInput, 'r') as csvinput:
    with open(GlobalStepPath1, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('Time_Label')
        all.append(row)

        for row in reader:
            #remove colon in time eg: 16:50:20 -> 165020
            row7 = row[7]
            no_colon = []
            for i in row7:
                if i.isdigit():
                    no_colon.append(i)
            numRow7 = ''.join(no_colon)
            row5 = row[5]
            row6 = row[6]

            if len(row5) != 2:
                row5 = '0' + row5
            if len(row6) != 2:
                row6 = '0' + row6
            value = row[4] + row5 + row6 + numRow7
            row.append(value)
            all.append(row)
        writer.writerows(all)

with open(GlobalStepPath1, 'r') as csvinput:
    with open(GlobalStepPath2, 'w', newline='') as csvoutput:
        reader = csv.reader(csvinput)
        writer = csv.writer(csvoutput)
        header = next(reader, None)
        if header:
            writer.writerow(header)
        sortedlist = sorted(reader, key=operator.itemgetter(15))
        writer.writerows(sortedlist)

with open(GlobalStepPath2, 'r') as csvinput:
    with open(GlobalStepPath3, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)
        DataList = list(reader)
        length = len(DataList)
        TimeArray = []
        LineArray = []

        for x in range(1, length):
            if DataList[x] == None:
                continue
            LineList = list(DataList[x])
            Speed = LineList[8]
            Year = str(''.join(LineList[4]))
            Month = str(''.join(LineList[5]))
            Day = str(''.join(LineList[6]))
            Label = str(''.join(LineList[14]))
            Lon = float(str(''.join(LineList[2])))
            Lat = float(str(''.join(LineList[3])))
            Sec = 0
            maxSec = int(str(''.join(LineList[13])))
            minSec = int(str(''.join(LineList[13])))
            if Speed != '0':
                continue

            for y in range(x + 1, length):
                print(y)
                if DataList[y] == None:
                    continue
                yLineList = list(DataList[y])
                ySpeed = yLineList[8]
                yYear = str(''.join(yLineList[4]))
                yMonth = str(''.join(yLineList[5]))
                yDay = str(''.join(yLineList[6]))
                yLabel = str(''.join(yLineList[14]))
                yLon = float(str(''.join(yLineList[2])))
                yLat = float(str(''.join(yLineList[3])))
                ySec = int(str(''.join(yLineList[13])))
                if ySpeed != '0':
                    if yYear != Year or yMonth != Month or yDay != Day or yLabel != Label:
                        break
                    else:
                        continue
                if yYear != Year or yMonth != Month or yDay != Day or yLabel != Label:
                    break
                if yLon == Lon and yLat == Lat:
                    if ySec > maxSec:
                        maxSec = ySec
                    if ySec < minSec:
                        minSec = ySec
                    #remove duplicated line and get the max Time_V0
                    DataList[y] = None
                    Sec = maxSec - minSec
                    TimeArray.append(Sec)
                    LineArray.append(x)

        #print(TimeArray)
        #print(LineArray)

        #MinStep2  Multiple Time_V0 value in one line, pick the max one
        maxTimeArray = []
        globalVal = 0
        maxTimeVal = 0

        for x in range(0, len(LineArray)):
            x = globalVal
            maxTimeVal = TimeArray[x]
            for y in range(x + 1, len(LineArray)):
                if LineArray[x] != LineArray[y]:
                    maxTimeArray.append(maxTimeVal)
                    globalVal = y
                    break
                if TimeArray[y] > maxTimeVal:
                    maxTimeVal = TimeArray[y]
        maxTimeArray.append(maxTimeVal)
        #print(maxTimeArray)

        seqLineArray = []
        for i in LineArray:
            if i not in seqLineArray:
                seqLineArray.append(i)
        #print(seqLineArray)

        #MinStep3 write Time_V0 value in column
        DataList[0].append("Time_V0")
        for x in range(0, len(seqLineArray)):
            line = seqLineArray[x]
            time = maxTimeArray[x]
            DataList[line].append(time)

        #MinStep4 if speed > 0, Time_V0 = 0
        for x in range(1, length):
            if DataList[x] == None:
                continue
            else:
                LineList = list(DataList[x])
                Speed = LineList[8]
                floatSpeed = float(str(''.join(Speed)))
                if floatSpeed > 0:
                    DataList[x].append('0')


        #MinStep5 remove all empty(None) value in list, this empty value is because we delete( DataList[y] = None ) the duplicated line
        result = []
        result.append(DataList[0])
        for x in range(1, len(DataList)):
            if DataList[x] is not None:
                result.append(DataList[x])


        resultList = np.array(result).tolist()

        writer.writerows(resultList)

with open(GlobalStepPath3, 'r') as csvinput:
    with open(GlobalStepPath3_1, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)
        DataList = list(reader)
        length = len(DataList)
        LineList = list(DataList[0])
        #print(len(LineList))
        #print(LineList)
        for x in range(1, length):
           LineList = list(DataList[x])
           if len(LineList) != 17:
               DataList[x].append('0')

        writer.writerows(DataList)

with open(GlobalStepPath3_1, 'r') as csvinput:
    with open(GlobalStepPath4, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)
        DataList = list(reader)
        DataList[0].append('State')

        for x in range(1, len(DataList)):
            LineList = list(DataList[x])
            Speed = LineList[16]
            FloatSpeed = float(str(''.join(Speed)))
            if FloatSpeed >= 120:
                DataList[x].append('Stop')
            else:
                DataList[x].append('Move')

        writer.writerows(DataList)

with open(GlobalStepPath4, 'r') as csvinput:
    with open(GlobalStepPath5, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)
        DataList = list(reader)
        DataList[0].append('State_Label')
        MoveCount = 0
        StopCount = 0
        for x in range(1, len(DataList)):
            LineList = list(DataList[x])
            State = LineList[17]
            StrState = str(''.join(State))
            if StrState == 'Move':
                MoveCount += 1
                DataList[x].append('Move' + str(MoveCount))
            else:
                StopCount += 1
                DataList[x].append('Stop' + str(StopCount))

        writer.writerows(DataList)

with open(GlobalStepPath5, 'r') as csvinput:
    with open(GlobalStepPath6, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)
        DataList = list(reader)
        DataList[0].append('Connection')
        SLabel1 = list(DataList[1])[18]
        SLabel2 = list(DataList[2])[18]
        DataList[1].append(str(' ') + str('-') + str(''.join(SLabel1)) + str('-') + str(''.join(SLabel2)))

        SecondLastState = list(DataList[len(DataList) - 2])[18]
        LastState = list(DataList[len(DataList) - 1])[18]
        DataList[len(DataList) - 1].append(str(''.join(SecondLastState)) + str('-') + str(''.join(LastState)) + str('-') + str(' '))

        for x in range(2, len(DataList) - 1):
            SLabelPre = list(DataList[x - 1])[18]
            SLabel = list(DataList[x])[18]
            SLabelAft = list(DataList[x + 1])[18]
            connection = str(''.join(SLabelPre)) + str('-') + str(''.join(SLabel)) + str('-') + str(''.join(SLabelAft))
            DataList[x].append(connection)

        writer.writerows(DataList)

os.remove(GlobalStepPath5)
os.remove(GlobalStepPath4)
os.remove(GlobalStepPath3_1)
os.remove(GlobalStepPath3)
os.remove(GlobalStepPath2)
os.remove(GlobalStepPath1)