#Similarity Check

#Check for keywords

#Generate marksheet

import sys, os, math, re, zipfile, time, shutil, subprocess, signal; 
from pyunpack import Archive
from random import shuffle

assignment_name = "Coursework3"

submissionPaths = []
    
for file in os.listdir("Assignments/" + assignment_name + "/Submissions/"):
    
    if ("DS" in file): continue;

    student_id = file;
    
    def unzip(source_filename, dest_dir):
        os.makedirs(dest_dir)
        Archive(source_filename).extractall(dest_dir);
        
    for root, dirs, files in os.walk("Assignments/" + assignment_name + "/Submissions/" + student_id + "/"):
        
        path = root.split('/')
        
        for dir in dirs:
            
            if ( "Extracted" in dir ):
                
                fullpath = root + dir
                
                shutil.rmtree(fullpath);
                
        for file in files:
            
            filename, file_extension = os.path.splitext(root + file);
            
            if ( file_extension == ".zip" or file_extension == ".gz" or file_extension == ".rar" ):
                
                try:
                    unzip(root + file, root + "Extracted" + str(time.time()));
                except zipfile.BadZipfile as e:
                    print "Bad zip " + root + file
    
    file_count = 0;
    
    for root, dirs, files in os.walk("Assignments/" + assignment_name + "/Submissions/" + student_id + "/"):
        
        path = root.split('/')
        
        if "__MACOSX" in path:
            
            continue;
            
        for file in files:
            
            filename, file_extension = os.path.splitext(root + file);
            
            if ("DS" in file): continue;
            
            if ( not file_extension == ".java" or filename.startswith('.') or "#" in filename ):   
                continue;
           
            filepathA = root + "/" + file
                    
            submissionPaths.append(filepathA)
               
for filepathA in submissionPaths:
    
    for filepathB in submissionPaths:
    
        #print "Comparing " + filepathA.replace(" ", "\ ") + " " + filepathB.replace(" ", "\ ")
        
        if filepathA == filepathB:
            continue;
                  
        cmd = "diff " + filepathA.replace(" ", "\ ").replace("'", "\\'")  + " " + filepathB.replace(" ", "\ ").replace("'", "\\'")
                    
        proc = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                    
        lines = 0;
        
        while True:
            
            line = proc.stdout.readline()
            #print "line: " + line;
            if line != '':
                lines = lines + 1;
            else:
                break
            
        if ( lines == 0 ):
            print cmd;
            #print lines;
                        
            
