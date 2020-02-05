import csv, os, sys, string

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

marks = [];

for root, dirs, files in os.walk("Assignments/Coursework3/Marks/"):
        
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
                    
                    #print "item: " + item;
                    #not hasNumbers(item) and
                    #if (  "." in item ):
                    if ( not item[0].isdigit() and not item == "-1" ):   
                        currentTup.append(item);
                        
                        print "name: " + item;

                    else:
                         
                        maxMark = 30.00;
    
                        maxPercentage = 33.00;
                        
                        if ( item == "-1" ):
                            currentTup.append(0);
                            marks.append(currentTup);
                        
                        else: 
                            #print item + " --> " + str( (float(item) / maxMark)*maxPercentage );
                            currentTup.append(round((float(item) / maxMark)*maxPercentage, 2));
                            #print currentTup;
                            marks.append(currentTup);
                        
                        currentTup = []
                    
                #sys.exit(0)
#sys.exit(0);

#print marks   

f = open('lines.csv','w')

with open("GradesheetCoursework3.csv") as rawCSV:
    
    rawCSVLines = rawCSV.readlines();
    
    for line in rawCSVLines:
        
        foundMark = False;
        
        for storedMark in marks:
            
            #print storedMark[0]
            if storedMark[0] in line:
                
                foundMark = True
                #print storedMark[1];
               
                f.write(line.replace(",-", "," + str(storedMark[1])))
                
        if ( not foundMark):
             print "!" + line;  
 
             f.write(line.replace(",-", "," + str(0.0)))             

f.close() 