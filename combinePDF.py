import sys, os, math, send2trash
from PyPDF2 import PdfFileMerger, PdfFileReader

home = '/Users/jasminder88/'

rawFiles = os.listdir(home + 'Pictures')

pdfFiles = list(filter(lambda x: x[-3:]=='pdf', rawFiles))
filePath = list(map(lambda x : home + 'Pictures/'+x, pdfFiles))

rawPDF = PdfFileMerger()

for pdf in filePath:
    rawPDF.append(PdfFileReader(open(pdf,'rb')))
    send2trash.send2trash(pdf)

os.makedirs(home + sys.argv[1] + '/ASSN' + sys.argv[3])

rawPDF.write(home + sys.argv[1] + '/ASSN'+sys.argv[3] + '/' +
             sys.argv[2]+str(sys.argv[3])+'-ASSN-'+str(sys.argv[3])+'.pdf')


print('FINISHED')

















