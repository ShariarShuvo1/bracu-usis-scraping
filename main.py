import requests
import json
from bs4 import BeautifulSoup


#login
email=input('Enter your USIS email: ')
password=input('Enter your USIS password: ')
s = requests.Session()
s.get("https://usis.bracu.ac.bd/academia/j_spring_security_check")
s.post("https://usis.bracu.ac.bd/academia/j_spring_security_check", data={'j_username': email, 'j_password': password})

#name print
name=s.get('https://usis.bracu.ac.bd/academia/dashBoard/show')
soup = BeautifulSoup( name.content , 'html.parser')
spans = soup.find_all('span', attrs={'class':'text'})
name=str(spans[0])
name=name[name.find('Welcome')+8:name.find('|')-2:]
print(f'\n################################\nHello {name}\n################################')

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
print(f'\nYou took {len(course_dict)} courses this semester!\n')

#File Download
soup = s.get(f'https://usis.bracu.ac.bd/academia/studentCourse/showClassScheduleInTabularFormatInGrid?query=&academiaSession=627119&_search=falsend=1663435687760&rows=-1&page=1&sidx=course_code&sord=asc').text, 'html.parser'
dct=json.loads(str(soup[0]))
lst=dct['rows']

#Display
while True:
    for key,value in course_dict.items():
        print(f'{key} -> {value["Course"]}')
    do_break=False
    while True:
        val=int(input('\nEnter course number(1/2/3/4) to see details (0 to exit): '))
        if val in course_dict.keys():
            break
        elif val==0:
            do_break=True
            break
        else:
            print('Try again with valid number')
            continue
    if do_break:
        print('See ya! {Made by Shariar :( )}')
        break
    current_dict=course_dict[val]
    print('\n','#'*35)
    print(f'\nCourse Name: {current_dict["Course_name"]}')
    print(f'Course Initial: {current_dict["Course"]}')
    print(f'Section: {current_dict["Section"]}')
    print(f'Faculty: {current_dict["Faculty"]}')
    print('-'*35)
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
            print(f'Your class days are: {day1} and {day2}')
            print(f'Class time start: {ele["cell"][6]}\nClass time end: {ele["cell"][7]}')
            print(f'Your class room is: {ele["cell"][8]}')
            if current_dict["Section"][0]!='S':
                print(f'Building Number: {ele["cell"][8][2]}\nFloor Number: {int(ele["cell"][8][3:5:])}\nRoom Number: {int(ele["cell"][8][5:7])}\n')
            break
    print('\n','#'*50,'\n')