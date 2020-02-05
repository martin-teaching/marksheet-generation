import sys, os, math, re, zipfile, time, shutil, subprocess, signal, random, glob; 
from pyunpack import Archive
from random import shuffle

assignment_name = "Coursework2"

required_submissions = 2

students = [];

def string_found(string1, string2):

   string1 = string1.replace("\n", "");
   
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return "True";
 
   return "False"

class Question:
   'Common base class for all questions'
   
   def __init__(self, question_number = None, question = None):
      
      self.question_number = question_number;
      
      self.question = question;
      
      self.answer = ""
      
      self.options = [];
      
      self.capped = False;
      
      self.matched = False
      
      self.capped_reason = ""
   
   def addOptionWithValue(self, option_name, value):
     
      self.options.append((option_name, value));
      
      self.matched = True;
      
      self.question_type = "options";

   def setCapped(self, capped_reason):
       
      self.capped = True;
      
      self.capped_reason = capped_reason
     
   def addMaxScore(self, max_score):
       
       self.max_score = max_score;

       self.question_type = "text";
       
   @property
   def answer(self):
       return self._answer       
       
   @property
   def capped(self):
       return self._capped
       
   @property
   def capped_reason(self):
       return self._capped_reason
       
   @property
   def options(self):
       return self._options
       
   @property
   def question(self):
       return self.question
       
   @property
   def matched(self):
       return self.matched

   @property
   def question_number(self):
       return self.question_number
       
   @property
   def question_type(self):
       return self.question_type
       
class StudentSubmission():

    def __init__(self, student_id, assignment_name, submission_file_name, assignment_lines):
        
        self.student_id = student_id;
        
        self.assignment_name = assignment_name;
        
        self.submission_file_name = submission_file_name;
        
        self.assignment_lines = assignment_lines;
        
        self.questions = [];
        
        self.submitted = True;
    
    def notSubmitted(self):
        self.submitted = False;
        
    @property
    def student_id(self):
        return self._student_id
        
    @property
    def assignment_name(self):
        return self._assignment_name
        
    @property
    def submission_file_name(self):
        return self._submission_file_name
        
    @property
    def submission_folder(self):
        return self._submission_folder
    
    @property
    def submitted(self):
        return self._submitted;
            
    @property
    def assignment_lines(self):
        return self._assignment_lines
        
    @property
    def questions(self):
        return self._questions
        
    def addQuestion(self, question):
        self.questions.append(question);
        
    def addFolder(self, submission_folder):
        self.submission_folder = submission_folder;
        

class Student:
    
    def __init__(self, student_id):
        
        self.student_id = student_id;
        
        self.submissions = []
        
        self.nosubmission = True;
        
        self.classname = "";
        
    def addSubmission(self, submission):
        
        self.submissions.append(submission);
        
        self.nosubmission = False;
        
    def addClassList(self, class_list):
        
        self.class_list = class_list;
        
    def addClass(self, classname):
        
        self.classname = classname;
    
    @property
    def nosubmission(self):
        return self._nosubmissions;
        
    @property
    def submissions(self):
        return self._submissions;
            
    @property
    def classname(self):
        return self._classname;
            
    @property
    def class_list(self):
        return self._class_list;
            
def Question1( student_submission ):
    
    mustContainCorrectProperties = [ "HeroOne", "HeroTwo", "Strength" ];
    
    correctPropertiesToContain = []#= mustContainCorrectProperties;

    with open("Assignments/" + assignment_name + "/Overview/overview.csv") as overview:
        
        overviewLines = overview.readlines()
    
        for line in overviewLines:
        
            splitLine = line.split(",");
            
            if ( splitLine[0] != student_submission.student_id ): continue;
            
            lastData = "";
            
            for data in splitLine:
            
                if ( lastData in mustContainCorrectProperties ):
                    
                    correctPropertiesToContain.append(data);
             
                lastData = data;
            
            numberOfCorrectPropertiesFound = 0;
            
            testCompile = True;
            
            if ( testCompile): 
                
                #files = glob.glob(student_submission.submission_folder + "/*.java")
                
                #for file in files :
                
                folder = student_submission.submission_folder;
                
                cmd = "javac " + folder.replace(" ", "\ ") + "/*.java"
                
                #print cmd;
                
                proc = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        
                while True:
                  line = proc.stderr.readline()
                  if line != '':
                    print "Compiler : " + line;
            
                    if "error" in line:
                
                        #os.killpg(proc.pid, signal.SIGTERM)
                        question = Question("Question1", "Ask the student to download their code from KEATS. Give the student a mark out of 8 (code did not compile), based upon the Marking Guidelines.");

                        question.addMaxScore(8);
            
                        question.setCapped("Code did not compile");

                        student_submission.addQuestion(question);
                    
                        return "Question1";
                
                  else:
                    break
            
            for line in student_submission.assignment_lines:
                
                for aProperty in correctPropertiesToContain:
                    
                    if ( string_found(aProperty.replace("-", ""), line.replace("-", "")) == "True" ): 
            
                        numberOfCorrectPropertiesFound += 1;
            
            if ( numberOfCorrectPropertiesFound > 0 & ( numberOfCorrectPropertiesFound >= len(mustContainCorrectProperties) ) ):
                
                question = Question("Question1", "Ask the student to download their code from KEATS. Give the student a mark out of 20, based upon the Marking Guidelines.");
    
                question.addMaxScore(20);
    
                student_submission.addQuestion(question);
                
            else:
                
                question = Question("Question1", "Ask the student to download their code from KEATS. Give the student a mark out of 10 (did not reference correct superhero or strength), based upon the Marking Guidelines.");
    
                question.addMaxScore(10);
                
                question.setCapped("Did not reference correct superhero");
    
                student_submission.addQuestion(question);
    
                #print "Does not contain: " + student_submission.student_id;
                
                #sys.exit(0)
                
            return "Question1";
    
    #question.addOptionWithValue("0", 0);
    #question.addOptionWithValue("1", 2);
    
    print "DID NOT DOWNLOAD!";
    
    #question.setCapped("- Did not download coursework as instructed.");
    
    #student_submission.addQuestion(question);
    
def Question2( student_submission ):
    
    potential_questions = ['they make two superheros fight', 'they determine the winner when two superhero fights', 'they powerup a superhero', 'they have made every superhero have a name', 'they have made a superhero\'s strength optional', 'they have extracted a superhero\'s name from a class', 'they have created two different superheros']
    
    question = Question("Question2", "Ask the student to describe how " + random.choice(potential_questions) + ". How confident and clear are they?");
    
    question.addOptionWithValue("0", 0);
    
    question.addOptionWithValue("1", 1);
    
    question.addOptionWithValue("2", 2);
    
    question.addOptionWithValue("3", 3);
    
    question.addOptionWithValue("4", 4);
    
    question.addOptionWithValue("5", 5);
    
    question.addOptionWithValue("6", 6);
    
    question.addOptionWithValue("7", 7);
    
    question.addOptionWithValue("8", 8);
    
    question.addOptionWithValue("9", 9);
    
    question.addOptionWithValue("10", 10);
    
    student_submission.addQuestion(question);
    
    return "Question2"
    
criteria = []

criteria.append(Question1)

#criteria.append(Question2)

for file in os.listdir("Assignments/" + assignment_name + "/Submissions/"):
    
    if ("DS" in file): continue;
    
    student_id = file;
    
    student = Student(student_id);
    
    students.append(student);
    
    located_questions = [];

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
                
                unzip(root + file, root + "Extracted" + str(time.time()));
    
    file_count = 0;
    
    for root, dirs, files in os.walk("Assignments/" + assignment_name + "/Submissions/" + student_id + "/"):
        
        #root = root.replace(" ", "\ ")
         
        path = root.split('/')
        
        if "__MACOSX" in path:
            
            continue;
        
        if ( len(dirs) > 0 and "Extracted" in dirs[0] ):
            
            isExtracted = True;
            
        for file in files:
            
            file_count = file_count + 1;
            
            if ("DS" in file): continue;
            
            filename, file_extension = os.path.splitext(root + file);
            
            if ( not file_extension == ".java" or filename.startswith('.') or "#" in filename ): continue;
            
            with open(root + "/" + file) as opened_submission: 
                
                file_question_number = "";
                
                assignment_lines = opened_submission.readlines()
                
                student_submission = StudentSubmission(student_id, assignment_name, opened_submission.name, assignment_lines);
                
                student_submission.addFolder(root);
                
                for function in criteria:
                    
                    response = function(student_submission);
                    
                    if ( response == "Question1" ):
                        
                        file_question_number = "Question1";
                        
                        located_questions.append(file_question_number);
                        
                student.addSubmission(student_submission);
    
    #if ( "Question1" not in located_questions ):
    
    Question2(student_submission);
    
    #sys.exit(0)
    
for file in os.listdir("Groups/"):

    classList = file;
    
    if ("DS" in file): continue;
    
    with open("Groups/" + classList) as classFile:
    
        lines = classFile.readlines()
    
        for line in lines:
            
            if ("StudentName" in line): continue;
            
            splitLine = line.split(",");
            
            for student in students :
                    
                if ( student.student_id == splitLine[1].strip() ):
                    
                    student.addClassList(lines);
                    
                    student.addClass(classList);
                    
            if not any(student.student_id == splitLine[1].strip() for student in students) and len(splitLine[1].strip()) > 0:
                
                no_student = Student(splitLine[1].strip());
                
                no_student.addClassList(lines);
                
                no_student.addClass(classList);
                
                students.append(no_student);
               
# To sort the list in place...
students.sort(key=lambda Student: Student.classname, reverse=False)

groupList = [];

i = 0;

while i < len(students):
    
    entry = students[i];
    
    if ( student.student_id == "" ):
    
        print "========="
        
        print student.student_id + " " + student.classname;
    
        print "========="
    
    end = False;
    
    if ( entry.classname == "" ):
        
        print entry.student_id;
        
        i = i + 1;
        continue;
    
    if ( len(students) == i + 1 ): 
        
        groupList.append(entry)
    
        end = True;
    
    if ( end or ( len(groupList) > 0 and ( entry.classname != groupList[len(groupList) -1].classname) ) ):
        
        markerLines = []
        
        #i = i + 1;
        #continue;
        
        while (len(groupList) > 0 and groupList[len(groupList) -1].classname == ""):
            
            print groupList[len(groupList) -1].student_id;
            print groupList[len(groupList) -1].classname;
            
            del groupList[len(groupList) -1];
        
        if ( len(groupList) == 0 ):
            
            break;
        
        with open("Markers/" + groupList[len(groupList) -1].classname) as markersFile:
            
            lines = markersFile.readlines()
            
            for line in lines:
                
                markerLines.append(line)
                
            del markerLines[0];
            
            interval = int(math.ceil(len(groupList) / float(len(markerLines))))
            
            #print ("interval " + str(interval));
            
            def chunks(l, n):
                n = max(1, n)
                return [l[i:i + n] for i in range(0, len(l), n)]
                
            def group(lst, div):
                lst = [ lst[i:i + len(lst)/div] for i in range(0, len(lst), len(lst)/div) ] #Subdivide list.
                #print "Len LST: " + str(len(lst));
                if len(lst) > div: # If it is an uneven list.
                    lst[div-1].extend(sum(lst[div:],[])) # Take the last part of the list and append it to the last equal division.
                return lst[:div] #Return the list up to that point.
                
            def slice_list(input, size):
                input_size = len(input)
                slice_size = input_size / size
                remain = input_size % size
                result = []
                iterator = iter(input)
                for i in range(size):
                    result.append([])
                    for j in range(slice_size):
                        result[i].append(iterator.next())
                    if remain:
                        result[i].append(iterator.next())
                        remain -= 1
                return result
            
            shuffle(groupList)
             
            for marker in markerLines:
                
                outputFileName = "Assignments/" + assignment_name + "/Marksheets/" + marker.replace("\n", "") + "-" + groupList[len(groupList) -1].classname + ".html"
                
                open(outputFileName, 'w').close()  
                
                outputFile = open(outputFileName, 'a');
                
                students_names = [];
                
                ## Write preamble
                
                with open("HTML/preamble.html") as preamble:
    
                    preambleLines = preamble.readlines()
    
                    for line in preambleLines:
                        
                        outputFile.write(line + "\n");
                
                ##
                
                outputFile.write("<heading>" + marker + " " + groupList[len(groupList) -1].classname + "</heading>");
                 
                outputFile.write("<form id='form'>");
                
                #print marker;
                
                if ( len(markerLines) > 1 ):
                    
                    students_names = slice_list(groupList, len(markerLines))[markerLines.index(marker)] #group(groupList, interval)[markerLines.index(marker)]
                    
                    students_names.sort(key=lambda Student: Student.student_id, reverse=False)
                    
                else:
                    
                    students_names = groupList;
                
                for student in students_names:
                
                    outputFile.write("<div style='height: 50px;'></div>");
                    
                    outputFile.write("<hr />");

                    outputFile.write(student.student_id + "\n");
                    
                    outputFile.write("<hr />");
                    
                    student_questions = [];
                    
                    # Work out which the 'best submission' is for each question, workaround for having different submission listed under different questions
                    for submission in student.submissions :
                        
                        for question in submission.questions :
                            
                            if ( len(student_questions) == 0 ):
                                
                                student_questions.append(question);
                                
                                #break;
                                
                            #for student_question in student_questions :
                            if any(student_question.question_number == question.question_number for student_question in student_questions):
                                
                                for stored in student_questions :
                                    
                                    if ( stored.question_number == question.question_number):
                                    
                                        #If existing is capped, but new is not (assume that this is the correct file for this question) and replace
                                        if ( stored.capped == True and question.capped == False or stored.capped == True and question.capped == True ):
                                        
                                            student_questions[student_questions.index(stored)] = question;
                                
                            else:
                                    
                                student_questions.append(question);
                    
                    student_questions.sort(key=lambda Question: Question.question_number, reverse=False)
                    
                    outputFile.write('<div class="question" id="' + student.student_id + '">')
                    
                    if ( student.nosubmission ):
                        
                        outputFile.write('No work submitted - if submitted late, will be marked separately.')
                        
                        outputFile.write('<p class="total"></p>');
                        
                        outputFile.write('</div>')
                        
                        print "No submission: " + question.question_number + " " + student.student_id;
                        
                        continue;
                    
                    outputFile.write('<input type="radio" id="' + student.student_id + 'Present0" name="' + student.student_id + 'Present" checked="checked" value="0">')
                    outputFile.write('<label for="' + student.student_id + 'Present0">Assessed</label>')
                    outputFile.write('<input type="radio" class="absent" id="' + student.student_id + 'Present-1" name="' + student.student_id + 'Present" value="-1">')
                    outputFile.write('<label for="' + student.student_id + 'Present-1">Not Assessed</label>')
                    
                    outputFile.write('<hr />')
                    
                    for question in student_questions :
                    
                        outputFile.write('<fieldset>');
                        outputFile.write('<legend>' + question.question + '</legend>');
                        
                        print "QT: " + question.question_type;
                        
                        if ( question.question_type == "text"):
                            
                            outputFile.write('<input type="text" id="' + student.student_id + 'Question' + str(question.question_number) + '" name="' + student.student_id + 'Question' + str(question.question_number) + '" maxlength="' + str(question.max_score) + '">')
                            
                        elif ( question.question_type == "options" ):
                            
                            for option in question.options :
                            
                                outputFile.write('<input type="radio" id="' + student.student_id + str(question.question_number) + str(option[1]) + '" name="' + student.student_id + str(question.question_number) + '" value="' + str(option[1]) + '"><label for="' + student.student_id + str(question.question_number) + str(option[1]) + '">' + str(option[0]) + '</label> ');
                        
                            outputFile.write(question.capped_reason);
                        
                        if ( question.capped_reason != "" ):
                            
                            print "Capped: " + question.question_number + " " + student.student_id + " " + question.capped_reason;
                            
                        outputFile.write('</fieldset>');

                    outputFile.write('<p class="total"></p>');

                    outputFile.write('</div>');
                    
                ## Write postamble
                
                outputFile.write("</form>");
                
                with open("HTML/postamble.html") as postamble:
    
                    postambleLines = postamble.readlines()
    
                    for line in postambleLines:
                        
                        outputFile.write(line + "\n");
                
                ##
            
            groupList = []
        
            #sys.exit(0);
            
            if ( end != True ): i-=1;
            
    else:
        
        groupList.append(entry);
    
    i+=1;
     
#Order pairs by group

#Loop through and find when current element is not in the same group, adding to a new list as you go

#Order this list alphabetically

#Split list based upon number of of tutors

#Print for each

         
                