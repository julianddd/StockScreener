import csv


def writeCSV(array, filePath='C:\\Users\\Julian\\Development\\StockScreener\\scratchPad\\', fileName='temp.csv'):
    writer = csv.writer(open(filePath + fileName, 'w'), delimiter=',', lineterminator='\n')
    for x in array:
        writer.writerow([x])

def readCSV(filePath='C:\\Users\\Julian\\Development\\StockScreener\\scratchPad\\', fileName='temp.csv'):
    array = []
    reader = csv.reader(open(filePath + fileName))
    for x in reader:
        array.append(x)
    return array

if __name__ == '__main__':
#    writeCSV(['this, is, a, test', 'this, is, a, test'])
    print(readCSV())
