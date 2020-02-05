import sys, os, math, re, zipfile, time, shutil, subprocess, signal, random, glob, errno; 
from pyunpack import Archive
from random import shuffle

assignment_name = "Coursework4"
   
marks = [];

class StudentMark:
    
    def __init__(self, student_id, mark, capped, plag):
        
        self.student_id = student_id;
        
        self.mark = mark;
        
        self.capped = capped;
        
        self.plag = plag;
        
    @property
    def mark(self):
        return self._mark;
        
def copy_anything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def delete_folder_content(folder):
    
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception, e:
            print e
        
def find_marks(id):
    
    for root, dirs, files in os.walk("Assignments/Coursework4/Marks/"):
        
        path = root.split('/')
              
        for file in files:

            filename, file_extension = os.path.splitext(root + file);
        
            if ( file_extension != ".csv" ):
            
                continue;
            
            with open(root + "/" + file) as csvfile:
    
                lines = csvfile.readlines()
            
                for line in lines:
                
                    currentTup = [];
                
                    for item in line[:-1].split(","):
                    
                        if ( not item[0].isdigit() and not item == "-1" ):   
                            currentTup.append(item);
                            
                        else:
                         
                            if ( item == "-1" ):
                                currentTup.append(0);
                        
                            else: 
                                #print item + " --> " + str( (float(item) / maxMark)*maxPercentage );
                                currentTup.append(item);
                            
                            
                            if ( id in currentTup[0] ):
                                return currentTup;
                            
                            currentTup = []

def copy_submission(assignment_path, student_id):
    
    capped_info = "";
    
    plagiarism_info = "";
    
    with open("Assignments/" + assignment_name + "/capped.csv") as capped_submissions:
        
          capped_lines = capped_submissions.readlines()
          
          for line in capped_lines :
              
              if ( student_id in line):
                  
                  capped_info = " - capped";
                  
    with open("Assignments/" + assignment_name + "/plagiarism.csv") as plag_submissions:
        
          plag_lines = plag_submissions.readlines()
          
          for line in plag_lines :
              
              if ( student_id in line):
                  
                  plagiarism_info = " - *penalise for plagiarism*";
                  
    with open("Assignments/" + assignment_name + "/warning.csv") as warn_submissions:
        
          warn_lines = warn_submissions.readlines()
          
          for line in warn_lines :
              
              if ( student_id in line):
                  
                  plagiarism_info = " - warning about plagiarism";
    
    if ( capped_info == " - capped" and "plagiarism" in plagiarism_info ):
        marks.append(StudentMark(student_id, find_marks(student_id)[1], "YES", "YES" + plagiarism_info))
    elif ( capped_info == " - capped" and "plagiarism" not in plagiarism_info ):
        marks.append(StudentMark(student_id, find_marks(student_id)[1], "YES", "No"))
    elif ( capped_info != " - capped" and "plagiarism" in plagiarism_info ):
        marks.append(StudentMark(student_id, find_marks(student_id)[1], "No", "YES" + plagiarism_info))
    else:
        marks.append(StudentMark(student_id, find_marks(student_id)[1], "No", "No"))
    
    if ( os.path.isdir("Assignments/" + assignment_name + "/PartBs/" + student_id + " (" + str(find_marks(student_id)[1]) + capped_info + plagiarism_info + ")") ):
        shutil.rmtree("Assignments/" + assignment_name + "/PartBs/" + student_id + " (" + str(find_marks(student_id)[1]) + capped_info + plagiarism_info + ")")
    
    copy_anything(assignment_path, "Assignments/" + assignment_name + "/PartBs/" + student_id + " (" + str(find_marks(student_id)[1]) + capped_info + plagiarism_info + ")");
                    
def file_loop(assignment_path, files, root, student_id):
    
    for file in files:
        
        if ("DS" in file): continue;
        
        filename, file_extension = os.path.splitext(root + file);
        
        if ( not file_extension == ".java" or filename.startswith('.') or "#" in filename ): continue;
        
        if root.endswith(" "):
            root = root[:-1]
            
        with open(root + "/" + file) as opened_submission: 
            
            if "hacker" in file.lower() or "elliot" in file.lower() or "darlene" in file.lower() or "trenton" in file.lower() or "romero" in file.lower() or "mrrobot" in file.lower() or "mobley" in file.lower() or "cisco" in file.lower():
                #print "-" + student_id + " " + str(find_marks(student_id)[1]);
                copy_submission(assignment_path, student_id)
                return True
            
            assignment_lines = opened_submission.readlines()
            
            for line in assignment_lines :
                
                if ( "Math" in line ):
                    #print "!" + student_id + " " + str(find_marks(student_id)[1]);
                    copy_submission(assignment_path, student_id)
                    return True
                    
    return False;

for file in os.listdir("Assignments/" + assignment_name + "/Submissions/"):
    
    if ("DS" in file): continue;

    student_id = file;

    def unzip(source_filename, dest_dir):
        
        os.makedirs(dest_dir)
        
        Archive(source_filename).extractall(dest_dir);
      
    for root, dirs, files in os.walk("Assignments/" + assignment_name + "/Submissions/" + student_id + "/"):
        
        root = root.replace(" ", "\ ");
        
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
    
    for root, dirs, files in os.walk("Assignments/" + assignment_name + "/Submissions/" + student_id + "/"):
        
        #root = root.replace(" ", "\ ")
         
        path = root.split('/')
        
        if "__MACOSX" in path:
            
            continue;
        
        if ( len(dirs) > 0 and "Extracted" in dirs[0] ):
            
            isExtracted = True;
        
        if ( file_loop("Assignments/" + assignment_name + "/Submissions/" + student_id + "/", files, root, student_id) ):
            break;
        
marks.sort(key=lambda StudentMark: StudentMark.mark, reverse=False)

idsmap = {}

with open("Assignments/" + assignment_name + "/idsToNames.csv") as idstonames: 
    
    idstonames_lines = idstonames.readlines()
    
    for line in idstonames_lines :
        
        idsmap[line.split(",")[2]] = line.split(",")[1]

f = open("Assignments/" + assignment_name + "/PartBs/PartBMarks.csv",'w')

e = open("Assignments/" + assignment_name + "/PartBs/PartBIDs.csv",'w')

print "Marks: " + str(len(marks))
f.write("Student,Part A Mark (out of 28),Capped at this mark?,Potential plagiarism case?,Part B Mark (out of 12), Comments\n");
for mark in marks:
    f.write(mark.student_id + "," + str(mark.mark) + "," + mark.capped + "," + mark.plag + "\n");
    e.write(idsmap[mark.student_id] + "," + mark.student_id + "\n");

    