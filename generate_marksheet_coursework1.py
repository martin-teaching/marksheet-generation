#Similarity Check

#Check for keywords

#Generate marksheet

import sys, os, math, re, zipfile, time, shutil, subprocess, signal; 
from pyunpack import Archive
from random import shuffle

assignment_name = "Coursework1"

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
      
      self.options = [];
      
      self.capped = False;
      
      self.matched = False
      
      self.capped_reason = ""
   
   def addOptionWithValue(self, option_name, value):
     
      self.options.append((option_name, value));
      
      self.matched = True;

   def setCapped(self, capped_reason):
      self.capped = True;
      self.capped_reason = capped_reason
      
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
        
def Question2( student_submission ):

    mustContainCorrectProperties = [ "Firstname", "Surname" ];
    
    correctPropertiesToContain = mustContainCorrectProperties;

    with open("Assignments/" + assignment_name + "/Overview/overview.csv") as overview:
        
        overviewLines = overview.readlines()
    
        for line in overviewLines:
        
            splitLine = line.split(",");
            
            #print student_id;
            #print splitLine[0] + " " + student_id[:-5];
            
            #print splitLine[0] + " " + student_submission.student_id
            
            question = Question("Question2", "How competently can the student compile and run their program in order to print their name to the screen?");
            
            #if ( splitLine[0] != student_id[:-5] ): continue;
            if ( splitLine[0] != student_submission.student_id ): continue;
            
            lastData = "";
            
            for data in splitLine:
            
                if ( lastData in mustContainCorrectProperties ):
                    
                    correctPropertiesToContain.append(data);
             
                lastData = data;
            
            numberOfCorrectPropertiesFound = 0;
            
            testCompile = False;
            
            if ( testCompile): 
            
                proc = subprocess.Popen(['javac', student_submission.submission_file_name],stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            
                while True:
                  line = proc.stderr.readline()
                  if line != '':
                    print "Compiler : " + line;
                
                    #the real code does filtering here
                    if "error" in line:
                    
                        #os.killpg(proc.pid, signal.SIGTERM)
                        question.addOptionWithValue("0", 0);
                        question.addOptionWithValue("1", 2);
        
                        question.setCapped("- Code did not compile.");
        
                        student_submission.addQuestion(question);
                
                        return "Question2";
                  else:
                    break
            
            #print "================="
            for line in student_submission.assignment_lines:
                
                for aProperty in correctPropertiesToContain:
                    
                    #print aProperty.replace("-", "") + " " + line.replace("-", "");
                    
                    if ( string_found(aProperty.replace("-", ""), line.replace("-", "")) ): 
            
                        numberOfCorrectPropertiesFound += 1;
            
            #print "================="
            #print numberOfCorrectPropertiesFound;
            
            if ( numberOfCorrectPropertiesFound > 0 & ( numberOfCorrectPropertiesFound == len(correctPropertiesToContain) ) ):
                
                checkHello = True;
              
                #print "================="
                for line in student_submission.assignment_lines:
                
                    #print ( "hello world in " + line.lower() + str("hello world" in line.lower()))
                    #print ( "helloworld in " + line.lower() + str("helloworld" in line.lower()))
                
                    if ( checkHello and "hello world" in line.lower() or "helloworld" in line.lower() ): 
                    
                        question.addOptionWithValue("0", 0);
                        question.addOptionWithValue("1", 2);
                        question.addOptionWithValue("2", 5);
    
                        question.setCapped("- Student reused Hello World.");
    
                        student_submission.addQuestion(question);
            
                        return "Question2";
                        
                question.addOptionWithValue("0", 0);
                question.addOptionWithValue("1", 2);
                question.addOptionWithValue("2", 5);
                question.addOptionWithValue("3", 8);
                
                student_submission.addQuestion(question);
                
                #IDtoResulttoClass.append((submissionID[:-5], "OK", ""));
    
            else:
    
                question.addOptionWithValue("0", 0);
                question.addOptionWithValue("1", 2);
                
                question.setCapped("- Did not supply firstname and surname as indicated.");
                
                student_submission.addQuestion(question);
                
                #IDtoResulttoClass.append((submissionID[:-5], "Does not match question specification.", ""));
            
            return "Question2";
        
        question.addOptionWithValue("0", 0);
        question.addOptionWithValue("1", 2);
        
        question.setCapped("- Did not download coursework as instructed.");
        
        student_submission.addQuestion(question);
        
            
def Question1( student_submission ):
    
    foundHello = False;
    
    isHelloWorldFile = False;
    
    for line in student_submission.assignment_lines:
        
        if ( ( "publicclassHelloWorld" in line.replace(" ", "") ) and ( "HelloWorld.java" == os.path.basename(student_submission.submission_file_name) ) or
             ( "publicclassHelloworld" in line.replace(" ", "") ) and ( "Helloworld.java" == os.path.basename(student_submission.submission_file_name) ) ):
            
            foundHello = True;
    
        if ( 'system.out.println("hello' in line.replace(" ", "").lower() ):
            
            isHelloWorldFile = True;
            
    question = Question("Question1", "Can the student explain what was wrong with the 'HelloWorld.java' program?");
    
    if ( not foundHello and isHelloWorldFile ):
        
        question.addOptionWithValue("No", 0);
        
        question.setCapped("- Student did not complete question requirement.");
        
        student_submission.addQuestion(question);
    
    elif ( isHelloWorldFile ):
        
        question.addOptionWithValue("Yes", 2);
    
        question.addOptionWithValue("No", 0);
        
        student_submission.addQuestion(question);
    
    if ( isHelloWorldFile ):
         return "Question1";
    
criteria = []

criteria.append(Question1)
criteria.append(Question2)

for file in os.listdir("Assignments/" + assignment_name + "/Submissions/"):
    
    #print "=====";
    
    if ("DS" in file): continue;
    
    student_id = file;
    
    student = Student(student_id);
    
    #print student_id;
    
    students.append(student);
    
    located_questions = [];
    
    #print "----- STUDENT ID: " + student_id + "-----------";
    
    #for submission in next(os.walk("Assignments/" + assignment_name + "/Submissions/"))[1]:
        
        #if submission_folder == student_id:
            
    #for submission in os.listdir(student_id):
       
        #with open("Assignments/" + assignment_name + "/Submissions/" + submission) as assignment:
    
    def unzip(source_filename, dest_dir):
        os.makedirs(dest_dir)
        Archive(source_filename).extractall(dest_dir);
        
        #with zipfile.ZipFile(source_filename) as zf:
        #    for member in zf.infolist():
                # Path traversal defense copied from
                # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
        #        words = member.filename.split('/')
        #        path = dest_dir
        #        for word in words[:-1]:
        #            drive, word = os.path.splitdrive(word)
        #            head, word = os.path.split(word)
        #            if word in (os.curdir, os.pardir, ''): continue
        #            path = os.path.join(path, word)
        #        zf.extract(member, path)
    
    for root, dirs, files in os.walk("Assignments/" + assignment_name + "/Submissions/" + student_id + "/"):
        
        path = root.split('/')
        
        #print (len(path) - 1) *'---' , os.path.basename(root)       
        
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
        
        path = root.split('/')
        
        #print (len(path) - 1) *'---' , os.path.basename(root)       
        
        #print dirs;
        
        if "__MACOSX" in path:
            
            continue;
        
        if ( len(dirs) > 0 and "Extracted" in dirs[0] ):
            
            isExtracted = True;
            
        for file in files:
            
            file_count = file_count + 1;
            
            filename, file_extension = os.path.splitext(root + file);
            
            if ("DS" in file): continue;
            
            #print len(path)*'---', file
            
            #Question1 = False;
            
            #Question2 = False;
            
            filename, file_extension = os.path.splitext(root + file);
            
            #if ( filename.startswith('.') or file_extension == "" or file_extension == ".iml" or file_extension == ".ini" or file_extension == ".zip" or file_extension == ".class" or file_extension == ".rtf" or file_extension == ".rar" or file_extension == ".png" or file_extension == ".gz" or file_extension == ".tar.gz" or file_extension == ".xml"):
            
            if ( not file_extension == ".java" or filename.startswith('.') or "#" in filename ):   
                continue;
            
            #print file
            #with open("Assignments/" + assignment_name + "/Submissions/" + student_id + "/" + file) as opened_submission: 
            with open(root + "/" + file) as opened_submission: 
                
                #print opened_submission.name;
                
                file_question_number = "";
                
                assignment_lines = opened_submission.readlines()
                
                #assignment_lines.append(); #Add assignment name to make accessible to passed function
                
                student_submission = StudentSubmission(student_id, assignment_name, opened_submission.name, assignment_lines);
                
                #print criteria;
                
                for function in criteria:
                    
                    response = function(student_submission);
                    
                    #print str(function);
                    
                    #print response;
                    
                    if ( response == "Question1" ):
                        
                        #Question1 = True;
                        
                        file_question_number = "Question1";
                        
                        located_questions.append(file_question_number);
                        
                    elif ( response == "Question2" ):
                        
                        #Question2 = True;
                        
                        file_question_number = "Question2";
                        
                        located_questions.append(file_question_number);
                        
                student.addSubmission(student_submission);
                
    if ( not isExtracted ): 
        
        print student.student_id;
    
    if ( file_count == 0 ):
        
        print student.student_id;
    
    find_student = "";
    
    if ( not find_student == "" ):
        
        if ( student.student_id == find_student):
        
            for submission in student.submissions :
            
                for question in submission.questions :
                
                    print question.question + question.capped_reason;
                
            sys.exit(0);
    
    #sys.exit(0);
    
    #print located_questions;
       
    if ( "Question1" not in located_questions and len(student.submissions) < 2 ):
        
        question = Question("Question1", "Can the student explain what was wrong with the 'HelloWorld.java' program?");
        
        question.addOptionWithValue("0", 0);
        
        question.setCapped("- Could not locate submitted question.")
        
        student_submission = StudentSubmission(student_id, assignment_name, "", "");
        
        student_submission.addQuestion(question);
        
        student_submission.notSubmitted();
        
        student.addSubmission(student_submission);
        
    if ( "Question2" not in located_questions and len(student.submissions) < 2 ):
        
        question = Question("Question2", "How competently can the student compile and run their program in order to print their name to the screen?");
        
        question.addOptionWithValue("0", 0);
        
        question.setCapped("- Could not locate submitted question.")
        
        student_submission = StudentSubmission(student_id, assignment_name, "", "");

        student_submission.addQuestion(question);
        
        student_submission.notSubmitted();
    
        student.addSubmission(student_submission);
        
    #mustContainText = ["HelloWorld"];

    #correctPropertiesToContain = [];

    #print student.student_id
    
    #print student.submissions[0].questions[0].capped_reason;
    
    #print student.submissions[0].questions[1].capped_reason;
    
    #print student.submissions[1].questions[0].capped_reason;
    
    #print student.submissions[1].questions[1].capped_reason;

#sys.exit(0);
  
for file in os.listdir("Groups/"):

    classList = file;
    
    if ("DS" in file): continue;
    
    with open("Groups/" + classList) as classFile:
    
        lines = classFile.readlines()
    
        for line in lines:
            
            if ("StudentName" in line): continue;
            
            splitLine = line.split(",");
            
            #print splitLine[1];
            
            #print IDtoResulttoClass;
            
            #print len([item for item in IDtoResulttoClass if splitLine[1].strip() in item])
            
            for student in students :
                    
                if ( student.student_id == splitLine[1].strip() ):
                    
                    student.addClassList(lines);
                    
                    student.addClass(classList);
                    
                    #print "Adding class list for" + student.student_id + " " + classList;
            
            if not any(student.student_id == splitLine[1].strip() for student in students) and len(splitLine[1].strip()) > 0:
                
                no_student = Student(splitLine[1].strip());
                
                no_student.addClassList(lines);
                
                no_student.addClass(classList);
                
                students.append(no_student);
                
            #if ( len([item for item in IDtoResulttoClass if splitLine[1].strip() in item]) > 0 ):
            
                #index = [y[0] for y in IDtoResulttoClass].index(splitLine[1].strip())
                
                #IDtoResulttoClass[index] = (IDtoResulttoClass[index][0], IDtoResulttoClass[index][1], classList, splitLine[0])
            
          

# To sort the list in place...
students.sort(key=lambda Student: Student.classname, reverse=False)

#IDtoResulttoClass.sort(key=lambda tup: tup[2])
         
#print IDtoResulttoClass;

#List of submissions per lab group
groupList = [];

#sys.exit(0);

i = 0;

while i < len(students):
    
    entry = students[i]; #IDtoResulttoClass[i];
    
    #print "entry: " + str(entry);
    
    #print len(IDtoResulttoClass);
    
    #print i;
    
    if ( student.student_id == "" ):
    
        print "========="
        
        print student.student_id + " " + student.classname;
    
        print "========="
    
    end = False;
    
    #
    
    if ( entry.classname == "" ):
        
        print entry.student_id;
        
        i = i + 1;
        continue;
    
    if ( len(students) == i + 1 ): 
        
        groupList.append(entry)
    
        end = True;
    
    if ( end or ( len(groupList) > 0 and ( entry.classname != groupList[len(groupList) -1].classname) ) ):
        
        #print "groupList: " + str(len(groupList));
        
        markerLines = []
        
        #print groupList[len(groupList) -1].student_id;
        #print groupList[len(groupList) -1].classname;
        
        #print groupList[len(groupList) -1].classname == ""
        
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
                
                    #print "========="
    
                    #print student.student_id;
    
                    #print "========="
                    
                    #print student.classname;
                    
                    outputFile.write("<div style='height: 50px;'></div>");
                    
                    outputFile.write("<hr />");

                    #outputFile.write(student.student_id + "Submitted " + str(len(student.submissions)) + " files" + "\n");
                    
                    outputFile.write(student.student_id + "\n");
                    
                    outputFile.write("<hr />");
                    
                    student_questions = [];
                    
                    ## Questions
                    
                    #print len(student.submissions);
                    
                    #print str(len(student.submissions))
                    
                    # Work out which the 'best submission' is for each question, workaround for having different submission listed under different questions
                    for submission in student.submissions :
                        
                        #print submission.submission_file_name
                        #print submission
                        
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
                    
                    #for question in student_questions :
                        
                         #print question.question + " " + str(question.matched) + " " + str(question.capped) + " " + str(question.capped_reason);
                    #print "No submission: " + str (student.nosubmission);
                    
                    #for submission in student.submissions :  
                    
                        #print "Submitted: " + str(submission.submitted);
                        
                        #for question in submission.questions:
                    
                            #print question.question + " " + str(question.matched) + " " + str(question.capped);
                        
                    #print "========="
                    
                    outputFile.write('<div class="question" id="' + student.student_id + '">');
                    
                    if ( student.nosubmission ):
                        
                        outputFile.write('No work submitted - if submitted late, will be marked separately.')
                        
                        outputFile.write('</div>')
                        
                        print question.question_number + " " + student.student_id;
                        
                        continue;
                        
                    for question in student_questions :
                    
                        outputFile.write('<fieldset>');
                        outputFile.write('<legend>' + question.question + '</legend>');
                        
                        for option in question.options :
                            
                            outputFile.write('<input type="radio" id="' + student.student_id + str(question.question_number) + str(option[1]) + '" name="' + student.student_id + str(question.question_number) + '" value="' + str(option[1]) + '"><label for="' + student.student_id + str(question.question_number) + str(option[1]) + '">' + str(option[0]) + '</label> ');
                        
                        outputFile.write(question.capped_reason);
                        
                        if ( question.capped_reason != "" ):
                            
                            print question.question_number + " " + student.student_id + " " + question.capped_reason;
                            
                    	#<label> <input type="radio" name="Question1" value="2"> Yes </label>
                    	#<label> <input type="radio" name="Question1" value="0"> No </label>
                        
                        outputFile.write('</fieldset>');

                    outputFile.write('<p class="total"></p>');

                    outputFile.write('</div>');
                    
                    #with open("Assignments/" + assignment_name + "/HTMLQuestions/questions.html") as questions:
    
                        #questionLines = questions.readlines()
                        
                        #justOneOption = False;
                        
                        #for line in questionLines:
                        
                            #line = line.replace("id=''", "id='" + student[0] + "'")
                            
                            #line = line.replace("Question", student[0] + "Question")
                        
                            #if ( student[1] == "Not Submitted" ):
                                
                                 #outputFile.write("<div class='question' id='" + student[0] + "'>");
	                             
                                 #outputFile.write("No work submitted. If submitted late, they will be marked in a different session.");
                                 
                                 #outputFile.write("<p class='total'>" + student[0] + ",0</p>");

                                 #outputFile.write("</div>");
                                 
                                 #break;
                                
                            #elif ( student[1] == "Does not match question specification." ):
                                
                                #if "input" in line:
                                    
                                    #if ( "Limit" in line ):
                                        
                                        #if ( justOneOption ): 
                                    
                                            #continue;
                                    
                                        #else:
                                        
                                            #justOneOption = True;
                                        
                                            #outputFile.write(line + " (Mark automatically capped -- student did not complete question correctly)." "\n");
                                    #else:
                                         
                                         #outputFile.write(line + "\n");
                                           
                                #else:       
                                    
                                    #justOneOption = False;
                                    
                                    #outputFile.write(line + "\n");
                                
                            #else:
                                
                                #outputFile.write(line + "\n");
                    
                    ##
                    
                    #outputFile.write("<hr />");
                    
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

         
                