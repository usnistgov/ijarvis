
import glob,fileinput
for file in glob.glob("jvaspdata2.js"):
        for line in fileinput.input(file, inplace=True):
                   print (line.rstrip().replace(' nan', '"--"'))

