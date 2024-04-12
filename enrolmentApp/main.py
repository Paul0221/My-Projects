from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
<<<<<<< HEAD
=======
import mysql.connector
from enrolmentApp.config import DB_CONFIG
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from rake_nltk import Rake

#nltk.download()
>>>>>>> 1412968 (Test of rake_nltk able to process sample statement into keyphrases)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

<<<<<<< HEAD
=======
conn = mysql.connector.connect(**DB_CONFIG)

>>>>>>> 1412968 (Test of rake_nltk able to process sample statement into keyphrases)
@app.get("/")
<<<<<<< HEAD
async def root():
    return {"message": "Home page, uvicorn"}
=======
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")
        #, context={"id": id})


@app.post("/submit_application")
async def submit_application(first_name: str = Form(...), last_name: str = Form(...),
                             email_address: str = Form(...),select_uni: str = Form(...), select_course: str = Form(...),
                             first_subject: str = Form(...), first_grade: str = Form(...),
                             second_subject: str = Form(...), second_grade: str = Form(...),
                             third_subject: str = Form(...), third_grade: str = Form(...),
                             other_subject: Optional[str] = Form(None), other_grade: Optional[str] = Form(None),
                             personal_statement: str = Form(...)):
    cursor = conn.cursor()

    print("First name = " + first_name + "\n")
    print("Last name = " + last_name + "\n")
    print("Email address = " + email_address + "\n")
    print("Uni choice = " + select_uni + "\n")
    print("Course choice = " + select_course + "\n")
    print("First subject = " + first_subject + "\n")
    print("First grade = " + first_grade + "\n")
    print("Second subject = " + second_subject + "\n")
    print("Second grade = " + second_grade + "\n")
    print("Third subject = " + third_subject + "\n")
    print("Third grade = " + third_grade + "\n")
    print("Personal statement = " + personal_statement + "\n")

    possible_grades = ["A*", "A", "B", "C", "D", "E", "U"]
    grade_score = 0
    sub_one_flag = False
    sub_two_flag = False
    sub_three_flag = False
    if other_subject is None:
        sub_other_flag = True
    else:
        sub_other_flag = False

    # First check to see if there's any mandatory subjects that applicants must have studied for their chosen course

    cursor.execute("SELECT IFNULL(req_subject_one, 'None') AS req_subject_one "
                   " FROM sys.uni_courses "
                   "WHERE uni_id = %i AND course_id = %i", (select_uni, select_course))
    req_sub_one_check = cursor.fetchall()

    cursor.execute("SELECT IFNULL(req_subject_two, 'None') AS req_subject_two "
                   " FROM sys.uni_courses "
                   "WHERE uni_id = %i AND course_id = %i", (select_uni, select_course))
    req_sub_two_check = cursor.fetchall()

    cursor.execute("SELECT req_sub_one_grade "
                   " FROM sys.uni_courses "
                   "WHERE uni_id = %i AND course_id = %i", (select_uni, select_course))
    req_sub_one_grade = cursor.fetchall()

    cursor.execute("SELECT req_sub_two_grade "
                   " FROM sys.uni_courses "
                   "WHERE uni_id = %i AND course_id = %i", (select_uni, select_course))
    req_sub_two_grade = cursor.fetchall()


    if (first_name is not None and last_name is not None and email_address is not None
            and select_uni is not None and select_course is not None and first_subject is not None
            and first_grade is not None and second_subject is not None and second_grade is not None
            and third_subject is not None and third_grade is not None and personal_statement is not None):

        if req_sub_one_check != "None":

            req_one_grad_idx = possible_grades.index(req_sub_one_grade)

            if first_subject == req_sub_one_check:

                first_grade_idx = possible_grades.index(first_grade)

                if first_grade_idx == req_one_grad_idx:
                    grade_score += 1
                elif first_grade_idx < req_one_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_one_grad_idx + 1) - (first_grade_idx + 1)
                else:
                    grade_score = -1

                sub_one_flag = True

            if second_subject == req_sub_one_check:

                second_grade_idx = possible_grades.index(second_grade)

                if second_grade_idx == req_one_grad_idx:
                    grade_score += 1
                elif second_grade_idx < req_one_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_one_grad_idx + 1) - (second_grade_idx + 1)
                else:
                    grade_score = -1

                sub_two_flag = True

            if third_subject == req_sub_one_check:

                third_grade_idx = possible_grades.index(third_grade)

                if third_grade_idx == req_one_grad_idx:
                    grade_score += 1
                elif third_grade_idx < req_one_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_one_grad_idx + 1) - (third_grade_idx + 1)
                else:
                    grade_score = -1

                sub_three_flag = True

            if other_subject is not None and other_subject == req_sub_one_check:

                other_grade_idx = possible_grades.index(other_grade)

                if other_grade_idx == req_one_grad_idx:
                    grade_score += 1
                elif other_grade_idx < req_one_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_one_grad_idx + 1) - (other_grade_idx + 1)
                else:
                    grade_score = -1

                sub_other_flag = True

        elif req_sub_two_check != "None" and grade_score != -1:

            req_two_grad_idx = possible_grades.index(req_sub_two_grade)

            if first_subject == req_sub_two_check:

                first_grade_idx = possible_grades.index(first_grade)

                if first_grade_idx == req_two_grad_idx:
                    grade_score += 1
                elif first_grade_idx < req_two_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_two_grad_idx + 1) - (first_grade_idx + 1)
                else:
                    grade_score = -1

                sub_one_flag = True

            if second_subject == req_sub_two_check:

                second_grade_idx = possible_grades.index(second_grade)

                if second_grade_idx == req_two_grad_idx:
                    grade_score += 1
                elif second_grade_idx < req_two_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_two_grad_idx + 1) - (second_grade_idx + 1)
                else:
                    grade_score = -1

                sub_two_flag = True

            if third_subject == req_sub_two_check:

                third_grade_idx = possible_grades.index(third_grade)

                if third_grade_idx == req_two_grad_idx:
                    grade_score += 1
                elif third_grade_idx < req_two_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_two_grad_idx + 1) - (third_grade_idx + 1)
                else:
                    grade_score = -1

                sub_three_flag = True

            if other_subject is not None and other_subject == req_sub_two_check:

                other_grade_idx = possible_grades.index(other_grade)

                if other_grade_idx == req_two_grad_idx:
                    grade_score += 1
                elif other_grade_idx < req_two_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_two_grad_idx + 1) - (other_grade_idx + 1)
                else:
                    grade_score = -1

                sub_other_flag = True

            while sub_one_flag == False or sub_two_flag == False or sub_three_flag == False or sub_other_flag == False:
                if sub_one_flag == False:

                    cursor.execute("SELECT IFNULL(req_grade_one, 'Checked') AS req_grade_one "
                                   " FROM sys.uni_courses "
                                   "WHERE uni_id = %i AND course_id = %i AND (req_grade_one != %s OR req_grade_one != %s)",
                                   (select_uni, select_course, req_sub_one_grade, req_sub_two_grade))
                    req_grade_one = cursor.fetchall()

                    if req_grade_one != "Checked":

                        req_grade_one_idx = possible_grades.index(req_grade_one)

                        first_grade_idx = possible_grades.index(first_grade)

                        if first_grade_idx == req_grade_one_idx:
                            grade_score += 1
                        elif first_grade_idx < req_grade_one_idx:
                            grade_score += (req_grade_one_idx + 1) - (first_grade_idx + 1)
                        else:
                            grade_score += -1 # add -1 rather than setting it to automatically be rejected

                    sub_one_flag = True

                elif sub_two_flag == False:

                    cursor.execute("SELECT IFNULL(req_grade_two, 'Checked') AS req_grade_two "
                                   " FROM sys.uni_courses "
                                   "WHERE uni_id = %i AND course_id = %i AND (req_grade_two != %s OR req_grade_two != %s)",
                                   (select_uni, select_course, req_sub_one_grade, req_sub_two_grade))
                    req_grade_two = cursor.fetchall()

                    if req_grade_two != "Checked":

                        req_grade_two_idx = possible_grades.index(req_grade_two)

                        second_grade_idx = possible_grades.index(second_grade)

                        if second_grade_idx == req_grade_two_idx:
                            grade_score += 1
                        elif second_grade_idx < req_grade_two_idx:
                            grade_score += (req_grade_two_idx + 1) - (second_grade_idx + 1)
                        else:
                            grade_score += -1

                    sub_two_flag = True

                elif sub_three_flag == False:

                    cursor.execute("SELECT IFNULL(req_grade_three, 'Checked') AS req_grade_three "
                                   " FROM sys.uni_courses "
                                   "WHERE uni_id = %i AND course_id = %i AND (req_grade_three != %s OR req_grade_three != %s)",
                                   (select_uni, select_course, req_sub_one_grade, req_sub_two_grade))
                    req_grade_three = cursor.fetchall()

                    if req_grade_three != "Checked":

                        req_grade_three_idx = possible_grades.index(req_grade_three)

                        third_grade_idx = possible_grades.index(third_grade)

                        if third_grade_idx == req_grade_three_idx:
                            grade_score += 1
                        elif third_grade_idx < req_grade_three_idx:
                            grade_score += (req_grade_three_idx + 1) - (third_grade_idx + 1)
                        else:
                            grade_score += -1

                    sub_three_flag = True

                else:

                    cursor.execute("SELECT IFNULL(req_grade_four, 'Checked') AS req_grade_four "
                                   " FROM sys.uni_courses "
                                   "WHERE uni_id = %i AND course_id = %i AND (req_grade_four != %s OR req_grade_four != %s)",
                                   (select_uni, select_course, req_sub_one_grade, req_sub_two_grade))
                    req_grade_four = cursor.fetchall()

                    if req_grade_four != "Checked":

                        req_grade_four_idx = possible_grades.index(req_grade_four)

                        other_grade_idx = possible_grades.index(other_grade)

                        if other_grade_idx == req_grade_four_idx:
                            grade_score += 1
                        elif other_grade_idx < req_grade_four_idx:
                            grade_score += (req_grade_four_idx + 1) - (other_grade_idx + 1)
                        else:
                            grade_score += -1

                    sub_other_flag = True

        cursor.close()

        return {"message": "Success: required fields are correctly processed"}
    else:
        return {"message": "Error: there is 1 or more fields that didn't process correctly"}

    '''if new_username is None:
        raise HTTPException(status_code=400, detail="Username is null when it should not")
    if new_password is None:
        raise HTTPException(status_code=401, detail="Password is null when it should not")
    if retyped_password is None:
        raise HTTPException(status_code=402, detail="Retyped password is null when it should not")

    if new_password == retyped_password:
        cursor.execute("INSERT INTO sys.users (user_name, user_password) VALUES (%s, %s)", (new_username, new_password))
        conn.commit()

        return RedirectResponse(url='/', status_code=302)
    else:
        return {"message": "Error: unable to create account"}'''


@app.get("/upload_application", response_class=HTMLResponse)
async def upload_application(request: Request):
    cursor = conn.cursor()

    cursor.execute("SELECT id, university_name FROM sys.universities")
    uni_list = cursor.fetchall()
    cursor.execute("SELECT id, CONCAT(qualification_code, ' ', course_name) FROM sys.courses")
    course_list = cursor.fetchall()
    cursor.close()
    print(uni_list)
    uni_options = "<option value=''> Select a university:</option>"
    course_options = "<option value=''> Select a course:</option>"
    for name in uni_list:
        uni_options += f"<option value='{name[0]}'>{name[1]}</option>"
    print(uni_options)
    for course in course_list:
        course_options += f"<option value='{course[0]}'>{course[1]}</option>"

    select_uni = f"""
    <select name="select_uni" id="select_uni" required>
        {uni_options}
    </select>
    """

    print(select_uni)

    select_course = f"""
    <select name="select_course" id="select_course" required>
        {course_options}
    </select>
    """
    return templates.TemplateResponse("upload_application.html", {"request": request, "select_uni": select_uni,
                                                                  "select_course": select_course})


@app.post("/submit_sign_in")
async def submit_sign_in(request: Request, username: str = Form(...), password: str = Form(...)):
    cursor = conn.cursor()

    if username is None:
        raise HTTPException(status_code=400, detail="Username is null when it should not")
    if password is None:
        raise HTTPException(status_code=401, detail="Password is null when it should not")

    print("Entered post for /submit_sign_in")
    print("username = " + username)
    print("password = " + password)
    cursor.execute("SELECT user_name, user_password FROM sys.users WHERE user_name = 'admin' AND user_password = %s", (password,))
    current_user = cursor.fetchone()
    cursor.close()
    if not current_user:
        raise HTTPException(status_code=402, detail="Incorrect login details, please try again.")
    else:
<<<<<<< HEAD
        return RedirectResponse(url='/', status_code=302)  # redirect to admissions main screen
>>>>>>> 8aed0c1 (Completed checks for required subject grades)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
=======
        return templates.TemplateResponse(request=request, name="admin_home.html")  # redirect to admissions main screen


@app.get("/sign_in", response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse(request=request, name="sign_in.html")


@app.get("/course_selection", response_class=HTMLResponse)
async def course_selection(request: Request):
    cursor = conn.cursor()

    cursor.execute("SELECT id, university_name FROM sys.universities")
    uni_list = cursor.fetchall()
    cursor.execute("SELECT id, CONCAT(qualification_code, ' ', course_name) FROM sys.courses")
    course_list = cursor.fetchall()
    uni_options = "<option value=''> Select a university:</option>"
    course_options = "<option value=''> Select a course:</option>"
    for name in uni_list:
        uni_options += f"<option value='{name[0]}'>{name[1]}</option>"
    for course in course_list:
        course_options += f"<option value='{course[0]}'>{course[1]}</option>"

    select_uni = f"""
    <select name="select_uni" id="select_uni" required>
        {uni_options}
    </select>
    """

    select_course = f"""
    <select name="select_course" id="select_course" required>
        {course_options}
    </select>
    """

    cursor.close()
    return templates.TemplateResponse("course_selection.html", {"request": request, "select_uni": select_uni,
                                                                "select_course": select_course})

@app.post("/submit_course_selection")
async def submit_course_selection(select_uni: str = Form(...), select_course: str = Form(...)):
    ''' cursor = conn.cursor()

    print("Uni choice = " + select_uni + "\n")
    print("Course choice = " + select_course + "\n")

    cursor.execute("SELECT id FROM sys.uni_courses WHERE uni_id = %i AND course_id = %i", (select_uni, select_course))
    selected_course = cursor.fetchone()

    cursor.execute("SELECT IFNULL(id, -1) FROM sys.uni_course_keyterms WHERE uni_course_id = %i", selected_course)
    keyterms_id = cursor.fetchone()

    if keyterms_id != -1:
        cursor.execute("SELECT keyterms FROM sys.uni_course_keyterms WHERE id = %i", keyterms_id)
        keyterms = cursor.fetchall()



    # cursor.execute("SELECT id, university_name FROM sys.universities")
    # uni_list = cursor.fetchall()


    # if select_uni is not None and select_course is not None:



       #  cursor.close()

    '''

    nltk.download('punkt')
    nltk.download('stopwords')

    test_keywords = """\
    skilled programmer
    creative thinker
    problem solving
    algorithm design
    collaborative
    """

    keyword_array = test_keywords.splitlines()

    print("Line 1:", keyword_array[0])
    print("Line 2:", keyword_array[1])
    print("Line 3:", keyword_array[2])
    print("Line 4:", keyword_array[3])
    print("Line 5:", keyword_array[4])

    '''
    keywords_nospace = []

    for i in range (0, len(keyword_array) - 1):
        keywords_nospace.append(keyword_array[i])

    print("Line 1:", keywords_nospace[0])
    print("Line 2:", keywords_nospace[1])
    print("Line 3:", keywords_nospace[2])
    print("Line 4:", keywords_nospace[3])
    print("Line 5:", keywords_nospace[4]) 
    '''

    sample_statement = "My fascination with technology was sparked when, as a child I thought it would be a great idea to take apart my Playstation console. Aware of the danger, I was still eager to see how it all worked inside. I find it intriguing how fast society has been shaped and continues to be, by the influence of Computer Science. A few years ago if someone were to have claimed that cars would become autonomous, people would have doubted them. Now we are at a stage where nearly anything is possible and this is due to the relentless problem solving of computer scientists. The latest software update released by Tesla motors allows their cars to learn how to drive themselves, and is an example of artificial intelligence, a sector which I am most interested in. I want to study Computer Science because I want to gain the knowledge needed to be able to help find solutions to world problems, with the efficient use of computer technology. With the knowledge and skills, I will attain from this course, the creative ideas that I could bring into fruition would be endless. I hope to become one of the computer scientists who adapt technology to help the human race evolve. One possibility would be for artificially intelligent gadgets to recognise different people and adjust to their individual needs based on personal preferences. I have been teaching myself Objective-C syntax in my spare time and have completed online programming courses, which have allowed me to explore the endless possibilities that computer science can bring to the world. I have also learnt to create a simple iOS game using Apple’s syntax called ‘Swift’, in XCode alongside Photoshop."

    # preprocess the statement

    processed_text = sample_statement.lower().replace(".", "").replace(",", "").replace("'", "")

    # statement_tokens = word_tokenize(processed_text)

    # get stop words

    stop_words = set(stopwords.words('english'))

    # this separates statement into individual words

    # statement_tokens = [x for x in statement_tokens if x not in stop_words]

    # print(statement_tokens)

    r_nltk = Rake()

    r_nltk.extract_keywords_from_text(processed_text)

    keywords = r_nltk.get_ranked_phrases()

    for x in keywords:
        print(x)

    return {"message": "Success: required fields are correctly processed"}
    # else:
        # return {"message": "Error: there is 1 or more fields that didn't process correctly"}
>>>>>>> 1412968 (Test of rake_nltk able to process sample statement into keyphrases)
