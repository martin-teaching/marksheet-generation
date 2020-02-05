import csv, os, sys

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

marks = [];

for root, dirs, files in os.walk("Assignments/Coursework1/Marks/"):
        
    path = root.split('/')
        
    #print (len(path) - 1) *'---' , os.path.basename(root)       
                    
    for file in files:

        filename, file_extension = os.path.splitext(root + file);
        
        if ( file_extension != ".csv" ):
            
            continue;
            
        with open(root + "/" + file) as csvfile:
    
            lines = csvfile.readlines()
            
            for line in lines:
                
                currentTup = [];
                
                #print line[:-1];
                
                for item in line[:-1].split(","):
                    
                    #print item;
                    #not hasNumbers(item) and
                    if (  "." in item ):
                        
                        currentTup.append(item);

                    else:
                         
                        maxMark = 10.00;
    
                        maxPercentage = 13.00;
                        
                        print item + " --> " + str( (float(item) / maxMark)*maxPercentage );
                        
                        currentTup.append((float(item) / maxMark)*maxPercentage);
                        print currentTup;
                        marks.append(currentTup);
                        currentTup = []
                
                #sys.exit(0)
#sys.exit(0);

#print marks   

f = open('lines.csv','w')

with open("GradesheetCoursework1.csv") as rawCSV:
    
    rawCSVLines = rawCSV.readlines();
    
    for line in rawCSVLines:
        
        foundMark = False;
        
        for storedMark in marks:
            
            #print "SM: " + str(storedMark)
            #print storedMark[1]
            if storedMark[0] in line:
                
                foundMark = True
                #print storedMark[1];
               
                f.write(line.replace(",-", "," + str(storedMark[1])))
                
        
        if ( not foundMark):
             print "!" + line;  
             f.write(line.replace(",-", "," + str(0.0)))             

f.close() # you can omit in most cases as the destructor will call it  