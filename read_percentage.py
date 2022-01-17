from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import json

class IgnouPercentage:
    def __init__(self):
        #Disabling the browser window to open
        config = json.load(open("config.json"))
        option = Options()
        option.headless = bool(config["headless"])
        self.driver = webdriver.Firefox(options=option,executable_path=config["executable_path"])

        # Default siter url
        self.driver.get("https://gradecard.ignou.ac.in/gradecardM/Result.asp")
        self.__student_details = []
        self.__data_frame = {}
        self.__extracted_frame = {}
    
    def getStudent_RollNo_And_Program(self,roll_no,program):
        try:
            select = Select(self.driver.find_element_by_css_selector('body > form:nth-child(4) > select:nth-child(1)'))
            select.select_by_value(program)
            self.driver.execute_script("document.getElementsByName('eno')[0].value = '{}'".format(roll_no))
            self.driver.find_element_by_css_selector('body > form:nth-child(4) > input:nth-child(3)').click()
        except Exception as e:
            print(e)
            self.driver.close()
            return "IGNOU Server Down!!! Try again after some time...."
            

        student = self.driver.find_elements_by_xpath('/html/body/form/b')
        if not student:
            return "Invalid Enrollment Number !!!"
        else:
            for s in student:
                self.__student_details.append(s.get_attribute('textContent'))
            #extracting data from the grade card page
            self.__extractData()
            #move to home page and close the browser
            self.driver.back()
            self.driver.close()
            #calculating the results and grade based on the extracted data
            self.__calculateResult()
        
        return [self.__data_frame,self.__extracted_frame,self.__student_details]
    
    #Private Member function
    #extract and store student marks
    def __extractData(self):

        assignment = []
        courses = []
        lab = []
        viva = []
        term_end = []

        #course list
        for code in self.driver.find_elements_by_xpath('/html/body/form/p[1]/table/tbody/tr/td[1]/strong'):
            courses.append(code.get_attribute('textContent'))
                
        # assignment
        for x in self.driver.find_elements_by_xpath('/html/body/form/p[1]/table/tbody/tr/td[2]/strong'):
            mark = x.get_attribute("textContent")
            if mark == '-':
                assignment.append(0)
                continue
            assignment.append(int(mark))

        #lab
        for x in self.driver.find_elements_by_xpath('/html/body/form/p[1]/table/tbody/tr/td[3]/strong'):
            mark = x.get_attribute("textContent")
            if mark == '-':
                lab.append(0)
                continue
            lab.append(int(mark))
        
        #viva
        for x in self.driver.find_elements_by_xpath('/html/body/form/p[1]/table/tbody/tr/td[4]/strong'):
            mark = x.get_attribute("textContent")
            if mark == '-':
                viva.append(0)
                continue
            viva.append(int(mark))
        
        #term end
        for x in self.driver.find_elements_by_xpath('/html/body/form/p[1]/table/tbody/tr/td[7]/strong'):
            mark = x.get_attribute("textContent")
            if mark == '-':
                term_end.append(0)
                continue
            term_end.append(int(mark))

        
        #store the results in the list
        [
            self.__extracted_frame.setdefault(course,list((assignment[index],lab[index],viva[index],term_end[index]))) 
            for index,course in enumerate(courses)
        ]
         
    #calculate percentage and status of each course
    def __calculateResult(self):
        for key,val in json.load(open("course_dictionary.json")).items():
            dct = {}
            for k,v in val.items():
                try:
                    lst_data = self.__extracted_frame[k]
                except:
                    dct.setdefault(k,list((k,v['SUBJECT_NAME'],0.0,0.0,0.0,'NOT COMPLETED',v['CREDITS'])))
                    continue
                if k not in ['BCSP064']:
                    assignment_weight = lst_data[0]*0.3
                    term_end_weight = (lst_data[1]+lst_data[3])*0.7
                    total = assignment_weight + term_end_weight
                else:
                    total = ((lst_data[1]+lst_data[2])/200)*100
                if total > 40.0:
                    status='PASS'
                else:
                    status='FAIL/NOT COMPLETED'
                dct.setdefault(k,list((k,v['SUBJECT_NAME'],assignment_weight,term_end_weight,total,status,v['CREDITS'])))
            self.__data_frame[key] = dct            


