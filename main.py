import PyQt5.QtWidgets as qtw
import requests
import json
from bs4 import BeautifulSoup

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        #Title
        self.setWindowTitle("RS61 Class Schedule")
        #form layout
        form_layout=qtw.QFormLayout()
        self.setLayout(form_layout)

        #Add Widgets
        label_1=qtw.QLabel("Enter your USIS email and Password")
        email=qtw.QLineEdit(self,placeholderText='example@abc.com')
        password=qtw.QLineEdit(self)
        password.setEchoMode(qtw.QLineEdit.Password)

        #down print
        down_print=qtw.QLabel("")

        #Button
        my_button=qtw.QPushButton("Login",clicked=lambda: press_it())

        #add rows to app
        form_layout.addRow(label_1)
        form_layout.addRow("Email: ",email)
        form_layout.addRow("Password: ",password)
        form_layout.addRow(my_button)
        
        #Show
        self.show()

        #functions
        def press_it():
            #login
            s = requests.Session()
            s.get("https://usis.bracu.ac.bd/academia/j_spring_security_check")
            s.post("https://usis.bracu.ac.bd/academia/j_spring_security_check", data={'j_username': email.text(), 'j_password': password.text()})

            form_layout.removeRow(label_1)
            form_layout.removeRow(email)
            form_layout.removeRow(password)
            form_layout.removeRow(my_button)

            #name print
            name=s.get('https://usis.bracu.ac.bd/academia/dashBoard/show')
            soup = BeautifulSoup( name.content , 'html.parser')
            spans = soup.find_all('span', attrs={'class':'text'})
            name=str(spans[0])
            name=name[name.find('Welcome')+8:name.find('|')-2:]
            printer(f'Hello <b style=" color:yellow; ">{name}</b>')

            #courses
            course=s.get('https://usis.bracu.ac.bd/academia/studentCourse/advisedCourse?738&7380.08575964058052254&738')
            soup = BeautifulSoup( course.content , 'html.parser')
            spans = soup.find_all('tr')
            course_dict=dict()
            for i in range(1,len(spans),1):
                spans_t = spans[i].find_all('td')
                dct=dict()
                dct['Course']=str(spans_t[0])[str(spans_t[0]).find('>')+1:str(spans_t[0]).find('</'):]
                dct['Course_name']=str(spans_t[1])[str(spans_t[1]).find('>')+1:str(spans_t[1]).find('</'):]
                dct['Section']=str(spans_t[2])[str(spans_t[2]).find('>')+1:str(spans_t[2]).find('</'):]
                dct['Faculty']=str(spans_t[3])[str(spans_t[3]).find('>')+1:str(spans_t[3]).find('</'):]
                course_dict[i]=dct
            printer(f'You took <b style = "color:#fc031c;">{len(course_dict)}</b> courses this semester!')
            
            #combo add
            my_combo=qtw.QComboBox(self, editable=False,insertPolicy=qtw.QComboBox.InsertAtBottom)
            for v in course_dict.values():
                my_combo.addItem(f'{v["Course"]} - {v["Course_name"]}')

            #File Download
            soup = s.get(f'https://usis.bracu.ac.bd/academia/studentCourse/showClassScheduleInTabularFormatInGrid?query=&academiaSession=627119&_search=falsend=1663435687760&rows=-1&page=1&sidx=course_code&sord=asc').text, 'html.parser'
            dct=json.loads(str(soup[0]))
            lst=dct['rows']

            #Display
            form_layout.addRow(my_combo)
            n=[0]
            enter_button=qtw.QPushButton("Enter",clicked=lambda: enter_clicked(course_dict,my_combo.currentIndex()+1,lst,n))
            form_layout.addRow(enter_button)

        #printer function
        def printer(txt):
            printer_label=qtw.QLabel("")
            printer_label.setText(txt)
            form_layout.addRow(printer_label)

        #Enter clicked button function
        def enter_clicked(course_dict,val,lst,n):
            st=''
            current_dict=course_dict[val]
            st+=f'\nCourse Name: {current_dict["Course_name"]}\n'
            st+=f'Course Initial: {current_dict["Course"]}\n'
            st+=f'Section: {current_dict["Section"]}\n'
            st+=f'Faculty: {current_dict["Faculty"]}\n'
            for ele in lst:
                if ele["cell"][2]==current_dict["Course"] and ele["cell"][4]==current_dict["Section"]:
                    if ele["cell"][5]=='Saturday' or ele["cell"][5]=='Thursday':
                        day1='Saturday'
                        day2='Thursday'
                    elif ele["cell"][5]=='Sunday' or ele["cell"][5]=='Tuesday':
                        day1='Sunday'
                        day2='Tuesday'
                    elif ele["cell"][5]=='Monday' or ele["cell"][5]=='Wednesday':
                        day1='Monday'
                        day2='Wednesday'
                    st+=f'Your class days are: {day1} and {day2}\n'
                    st+=f'Class time start: {ele["cell"][6]}\nClass time end: {ele["cell"][7]}\n'
                    st+=f'Your class room is: {ele["cell"][8]}\n'
                    if current_dict["Section"][0]!='S':
                        st+=f'Building Number: {ele["cell"][8][2]}\nFloor Number: {int(ele["cell"][8][3:5:])}\nRoom Number: {int(ele["cell"][8][5:7])}\n'
                    break
            if n[0]==0:
                n[0]+=1
                down_print.setText(st)
                form_layout.addRow(down_print)
            else:
                down_print.setText(st)

app=qtw.QApplication([])
mw=MainWindow()
app.exec_()