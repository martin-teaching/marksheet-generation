#Similarity Check

#Check for keywords

#Generate marksheet

import sys, os, math, re;

assignment_name = "Sample"

required_submissions = 2

students = [];

def string_found(string1, string2):
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return True
   return False

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
            
            #if ( splitLine[0] != student_id[:-5] ): continue;
            if ( splitLine[0] != student_submission.student_id ): continue;
            
            lastData = "";
            
            for data in splitLine:
            
                if ( lastData in mustContainCorrectProperties ):
                    
                    correctPropertiesToContain.append(data);
             
                lastData = data;
            
            numberOfCorrectPropertiesFound = 0;
    
            for line in student_submission.assignment_lines:
                
                if ( "hello world" in line.lower() or "helloworld" in line.lower() ): 
                    
                    return False;
                
                for aProperty in correctPropertiesToContain:
                    
                    if ( string_found(aProperty, line) ): 
            
                        numberOfCorrectPropertiesFound += 1;
            
            #print numberOfCorrectPropertiesFound;
            
            question = Question("Question2", "How competently can the student compile and run their program, and print their name to the screen?");
    
            if ( numberOfCorrectPropertiesFound > 0 & ( numberOfCorrectPropertiesFound == len(correctPropertiesToContain) ) ):
                
                question.addOptionWithValue("1", 2);
                question.addOptionWithValue("2", 5);
                question.addOptionWithValue("3", 8);
                
                student_submission.addQuestion(question);
                
                #IDtoResulttoClass.append((submissionID[:-5], "OK", ""));
    
            else:
    
                question.addOptionWithValue("1", 2);
                
                question.setCapped("Did not supply firstname and surname as indicated.");
                
                student_submission.addQuestion(question);
                
                #IDtoResulttoClass.append((submissionID[:-5], "Does not match question specification.", ""));
            
            return "Question2";
            
def Question1( student_submission ):
    
    foundHello = False;
    
    for line in student_submission.assignment_lines:
        
        if ( ( "public class Helloworld" in line and "Helloworld" in student_submission.submission_file_name ) or ( "public class HelloWorld" in line and "HelloWorld" in student_submission.submission_file_name ) ):
            
            foundHello = True;
        
    question = Question("Question1", "Can the student explain what was wrong the 'HelloWorld.java' program?");
    
    if ( not foundHello ):
        
        question.addOptionWithValue("No", 0);
        
        question.setCapped("Student did not complete question requirements.");
        
        student_submission.addQuestion(question);
    
    else:
        
        question.addOptionWithValue("Yes", 2);
    
        question.addOptionWithValue("No", 0);
        
        student_submission.addQuestion(question);
    
    return "Question1";
    
criteria = []

criteria.append(Question1)
criteria.append(Question2)

for file in os.listdir("Assignments/" + assignment_name + "/Submissions/"):
    
    if ("DS" in file): continue;
    
    student_id = file;
    
    student = Student(student_id);
    
    students.append(student);
    
    located_questions = [];
    
    print "----- STUDENT ID: " + student_id + "-----------";
    
    #for submission in next(os.walk("Assignments/" + assignment_name + "/Submissions/"))[1]:
        
        #if submission_folder == student_id:
            
    #for submission in os.listdir(student_id):
       
        #with open("Assignments/" + assignment_name + "/Submissions/" + submission) as assignment:
    
    for root, dirs, files in os.walk("Assignments/" + assignment_name + "/Submissions/" + student_id + "/"):
        
        path = root.split('/')
        
        print (len(path) - 1) *'---' , os.path.basename(root)       
        
        for file in files:
            
            if ("DS" in file): continue;
            
            print "File: " + file;
            
            #print len(path)*'---', file
            
            #Question1 = False;
            
            #Question2 = False;
            
            with open("Assignments/" + assignment_name + "/Submissions/" + student_id + "/" + file) as opened_submission: 
            
                file_question_number = "";
                
                assignment_lines = opened_submission.readlines()
                
                #assignment_lines.append(); #Add assignment name to make accessible to passed function
                
                student_submission = StudentSubmission(student_id, assignment_name, opened_submission.name, assignment_lines);
                
                for function in criteria:
                    
                    response = function(student_submission);
                    
                    print str(function);
                    
                    print response;
                    
                    if ( response == "Question1" ):
                        
                        #Question1 = True;
                        
                        file_question_number = "Question1";
                        
                        located_questions.append(file_question_number);
                        
                    elif ( response == "Question2" ):
                        
                        #Question2 = True;
                        
                        file_question_number = "Question2";
                        
                        located_questions.append(file_question_number);
                        
                student.addSubmission(student_submission);
                        
    if ( "Question1" not in located_questions and len(student.submissions) < 2 ):
        
        question = Question("Question1", "Can the student explain what was wrong the 'HelloWorld.java' program?");
        
        student_submission = StudentSubmission(student_id, assignment_name, "", "");
        
        student_submission.addQuestion(question);
        
        student_submission.notSubmitted();
        
        student.addSubmission(student_submission);
        
    if ( "Question2" not in located_questions and len(student.submissions) < 2 ):
        
        print ":()"
        question = Question("Question2", "How competently can the student compile and run their program, to print their name to the screen?");
        
        student_submission = StudentSubmission(student_id, assignment_name, "", "");

        student_submission.addQuestion(question);
        
        student_submission.notSubmitted();
    
        student.addSubmission(student_submission);
        
    #mustContainText = ["HelloWorld"];

    #correctPropertiesToContain = [];

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
                    
                    print "Adding class list for" + student.student_id + " " + classList;
            
            if not any(student.student_id == splitLine[1].strip() for student in students):
                
                no_student = Student(splitLine[1].strip());
                
                no_student.addClassList(lines);
                
                no_student.addClass(classList);
                
                students.append(no_student);
                
            #if ( len([item for item in IDtoResulttoClass if splitLine[1].strip() in item]) > 0 ):
            
                #index = [y[0] for y in IDtoResulttoClass].index(splitLine[1].strip())
                
                #IDtoResulttoClass[index] = (IDtoResulttoClass[index][0], IDtoResulttoClass[index][1], classList, splitLine[0])
            
          

# To sort the list in place...
students.sort(key=lambda Student: Student.student_id, reverse=False)

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
    
    end = False;
    
    if ( len(students) == i + 1 ): 
        
        groupList.append(entry)
    
        end = True;
        
    if ( end or ( len(groupList) > 0 and ( entry.classname != groupList[len(groupList) -1].classname) ) ):
        
        markerLines = []
        
        with open("Markers/" + groupList[len(groupList) -1].classname) as markersFile:
            
            lines = markersFile.readlines()
    
            for line in lines:
                
                markerLines.append(line)
                
            del markerLines[0];
            
            interval = int(math.ceil(len(groupList) / float(len(markerLines))))
    
            def group(lst, div):
                lst = [ lst[i:i + len(lst)/div] for i in range(0, len(lst), len(lst)/div) ] #Subdivide list.
                if len(lst) > div: # If it is an uneven list.
                    lst[div-1].extend(sum(lst[div:],[])) # Take the last part of the list and append it to the last equal division.
                return lst[:div] #Return the list up to that point.
        
            for marker in markerLines:
                
                outputFileName = "Assignments/" + assignment_name + "/Marksheets/" + marker.replace("\n", "") + ".html"
                
                open(outputFileName, 'w').close()  
                
                outputFile = open(outputFileName, 'a');
                
                students_names = [];
                
                ## Write preamble
                
                with open("HTML/preamble.html") as preamble:
    
                    preambleLines = preamble.readlines()
    
                    for line in preambleLines:
                        
                        outputFile.write(line + "\n");
                
                ##
                
                outputFile.write("<heading>" + marker + "</heading>");
                 
                if ( len(markerLines) > 1 ):
                    
                    students_names = group(groupList, interval)[markerLines.index(marker)]
                    
                else:
                    
                    students_names = groupList;
                
                for student in students_names:
                
                    print "========="
                    
                    print student.student_id;
                    
                    print "========="
                    
                    outputFile.write("<div style='height: 50px;'></div>");
                    
                    outputFile.write("<hr />");

                    #outputFile.write(student.student_id + "Submitted " + str(len(student.submissions)) + " files" + "\n");
                    
                    outputFile.write(student.student_id + "\n");
                    
                    outputFile.write("<hr />");
                    
                    student_questions = [];
                    
                    ## Questions
                    
                    print len(student.submissions);
                    
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
                                        if ( stored.capped == True and question.capped == False ):
                                        
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
                        
                        outputFile.write('No work submitted.')
                        
                        outputFile.write('</div>')
                        
                    for question in student_questions :
                    
                        outputFile.write('<fieldset>');
                        outputFile.write('<legend>' + question.question + '</legend>');
                        
                        for option in question.options :
                            
                            outputFile.write('<label> <input type="radio" name="' + str(question.question_number) + '" value="' + str(option[1]) + '">' + str(option[0]) + '</label> ' + question.capped_reason);
                             
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
                
                with open("HTML/postamble.html") as postamble:
    
                    postambleLines = postamble.readlines()
    
                    for line in postambleLines:
                        
                        outputFile.write(line + "\n");
                
                ##
            
            groupList = []
        
            if ( end != True ): i-=1;
            
    else:
        
        groupList.append(entry);
    
    i+=1;
     
#Order pairs by group

#Loop through and find when current element is not in the same group, adding to a new list as you go

#Order this list alphabetically

#Split list based upon number of of tutors

#Print for each

         
                