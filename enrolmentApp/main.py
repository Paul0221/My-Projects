<<<<<<< HEAD
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
=======
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
>>>>>>> e8aaad4 (Added initial training and test sets)
from fastapi.templating import Jinja2Templates
<<<<<<< HEAD
=======
import mysql.connector
from enrolmentApp.config import DB_CONFIG
from typing import Optional
import nltk
from nltk.corpus import stopwords
from rake_nltk import Rake
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

#nltk.download()
>>>>>>> 1412968 (Test of rake_nltk able to process sample statement into keyphrases)
=======
from sklearn.model_selection import train_test_split
>>>>>>> e8aaad4 (Added initial training and test sets)
=======
from itertools import combinations
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
>>>>>>> b668329 (Reverted back to binomial approach as it is more suitable for keyphrase analysis)
=======
from fuzzywuzzy import fuzz
>>>>>>> 506b8e0 (Added fuzzwuzzy to ensure similar phrases to keyphrases are found)

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
                   "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
    req_sub_one_check = cursor.fetchall()

    cursor.execute("SELECT IFNULL(req_subject_two, 'None') AS req_subject_two "
                   " FROM sys.uni_courses "
                   "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
    req_sub_two_check = cursor.fetchall()

    cursor.execute("SELECT req_sub_one_grade "
                   " FROM sys.uni_courses "
                   "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
    req_sub_one_grade = cursor.fetchall()

    cursor.execute("SELECT req_sub_two_grade "
                   " FROM sys.uni_courses "
                   "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
    req_sub_two_grade = cursor.fetchall()

    print("req_sub_one_check = ", req_sub_one_check[0][0])
    print("req_sub_two_check = ", req_sub_two_check[0][0])

    if (first_name is not None and last_name is not None and email_address is not None
            and select_uni is not None and select_course is not None and first_subject is not None
            and first_grade is not None and second_subject is not None and second_grade is not None
            and third_subject is not None and third_grade is not None and personal_statement is not None):

        if req_sub_one_check[0][0] != "None":

            req_one_grad_idx = possible_grades.index(req_sub_one_grade[0][0])

            print("req_one_grad_idx = ", req_one_grad_idx)

            print("first_subject = ", first_subject)

            print("second_subject = ", second_subject)

            cursor.execute("SELECT subject_name "
                           " FROM sys.required_subjects "
                           "WHERE id = %s", (req_sub_one_check[0][0],))
            req_sub_one_check = cursor.fetchall()

            cursor.execute("SELECT subject_name "
                           " FROM sys.required_subjects "
                           "WHERE id = %s", (req_sub_two_check[0][0],))
            req_sub_two_check = cursor.fetchall()

            print("req_sub_one_check = ", req_sub_one_check[0][0])

            print("req_sub_two_check = ", req_sub_two_check[0][0])

            if first_subject == req_sub_one_check[0][0]:

                first_grade_idx = possible_grades.index(first_grade[0][0])

                print("first_grade_idx = ", first_grade_idx)

                if first_grade_idx == req_one_grad_idx:
                    grade_score += 1
                    print("first_grade_idx == req_one_grad_idx")
                elif first_grade_idx < req_one_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_one_grad_idx + 1) - (first_grade_idx + 1)
                    print("first_grade_idx < req_one_grad_idx")
                else:
                    grade_score = -1
                    print("grade set to -1")

                sub_one_flag = True

                print("sub_one_flag = ", sub_one_flag)

            if second_subject == req_sub_one_check[0][0]:

                second_grade_idx = possible_grades.index(second_grade[0][0])

                print("second_grade_idx = ", second_grade_idx)

                if second_grade_idx == req_one_grad_idx:
                    grade_score += 1
                    print("second_grade_idx == req_one_grad_idx")
                elif second_grade_idx < req_one_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_one_grad_idx + 1) - (second_grade_idx + 1)
                    print("second_grade_idx < req_one_grad_idx")
                else:
                    grade_score = -1
                    print("grade set to -1")

                sub_two_flag = True
                print("sub_two_flag = ", sub_two_flag)

            if third_subject == req_sub_one_check[0][0]:

                third_grade_idx = possible_grades.index(third_grade[0][0])

                if third_grade_idx == req_one_grad_idx:
                    grade_score += 1
                elif third_grade_idx < req_one_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_one_grad_idx + 1) - (third_grade_idx + 1)
                else:
                    grade_score = -1

                sub_three_flag = True

            if other_subject is not None and other_subject == req_sub_one_check[0][0]:

                other_grade_idx = possible_grades.index(other_grade[0][0])

                if other_grade_idx == req_one_grad_idx:
                    grade_score += 1
                elif other_grade_idx < req_one_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_one_grad_idx + 1) - (other_grade_idx + 1)
                else:
                    grade_score = -1

                sub_other_flag = True

        if req_sub_two_check[0][0] != "None" and grade_score != -1:

            req_two_grad_idx = possible_grades.index(req_sub_two_grade[0][0])

            print("req_two_grad_idx = ", req_two_grad_idx)

            print("first_subject = ", first_subject)

            print("req_sub_two_check = ", req_sub_two_check[0][0])

            if first_subject == req_sub_two_check[0][0]:

                first_grade_idx = possible_grades.index(first_grade[0][0])

                print("first_grade_idx = ", first_grade_idx)

                if first_grade_idx == req_two_grad_idx:
                    grade_score += 1
                    print("first_grade_idx == req_two_grad_idx")
                elif first_grade_idx < req_two_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_two_grad_idx + 1) - (first_grade_idx + 1)
                    print("first_grade_idx < req_two_grad_idx")
                else:
                    grade_score = -1
                    print("grade score set to -1")

                sub_one_flag = True
                print("sub_one_flag = ", sub_one_flag)

            if second_subject == req_sub_two_check[0][0]:

                print("req_sub_two_check = ", req_sub_two_check[0][0])

                second_grade_idx = possible_grades.index(second_grade[0][0])

                print("second_grade_idx = ", second_grade_idx)

                if second_grade_idx == req_two_grad_idx:
                    grade_score += 1
                    print("second_grade_idx == req_two_grad_idx")
                elif second_grade_idx < req_two_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_two_grad_idx + 1) - (second_grade_idx + 1)
                    print("second_grade_idx < req_two_grad_idx")
                else:
                    grade_score = -1
                    print("grade set to -1")

                sub_two_flag = True
                print("sub_two_flag = ", sub_two_flag)

            if third_subject == req_sub_two_check[0][0]:

                third_grade_idx = possible_grades.index(third_grade[0][0])

                if third_grade_idx == req_two_grad_idx:
                    grade_score += 1
                elif third_grade_idx < req_two_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_two_grad_idx + 1) - (third_grade_idx + 1)
                else:
                    grade_score = -1

                sub_three_flag = True

            if other_subject is not None and other_subject == req_sub_two_check[0][0]:

                other_grade_idx = possible_grades.index(other_grade[0][0])

                if other_grade_idx == req_two_grad_idx:
                    grade_score += 1
                elif other_grade_idx < req_two_grad_idx:
                    # gets the difference between the 2 grades
                    grade_score += (req_two_grad_idx + 1) - (other_grade_idx + 1)
                else:
                    grade_score = -1

                sub_other_flag = True

        while sub_one_flag is False or sub_two_flag is False or sub_three_flag is False or sub_other_flag is False:
            print("Flag check:")
            print("sub_one_flag = ", sub_one_flag)
            print("sub_two_flag = ", sub_two_flag)
            print("sub_three_flag = ", sub_three_flag)
            print("sub_other_flag = ", sub_other_flag)
            if sub_one_flag is False:

                print("Hits sub_one_flag == False")

                cursor.execute("SELECT IFNULL(req_grade_one, 'Checked') AS req_grade_one "
                               " FROM sys.uni_courses "
                               "WHERE uni_id = %s AND course_id = %s",
                               (select_uni, select_course))
                req_grade_one = cursor.fetchall()

                if req_grade_one[0][0] != "Checked":

                    req_grade_one_idx = possible_grades.index(req_grade_one[0][0])

                    first_grade_idx = possible_grades.index(first_grade[0][0])

                    if first_grade_idx == req_grade_one_idx:
                        grade_score += 1
                    elif first_grade_idx < req_grade_one_idx:
                        grade_score += (req_grade_one_idx + 1) - (first_grade_idx + 1)
                    else:
                        grade_score += -1 # add -1 rather than setting it to automatically be rejected

                sub_one_flag = True

            elif sub_two_flag is False:

                print("Hits sub_two_flag == False")

                cursor.execute("SELECT IFNULL(req_grade_two, 'Checked') AS req_grade_two "
                               " FROM sys.uni_courses "
                               "WHERE uni_id = %s AND course_id = %s",
                               (select_uni, select_course))
                req_grade_two = cursor.fetchall()

                if req_grade_two[0][0] != "Checked":

                    req_grade_two_idx = possible_grades.index(req_grade_two[0][0])

                    second_grade_idx = possible_grades.index(second_grade[0][0])

                    if second_grade_idx == req_grade_two_idx:
                        grade_score += 1
                    elif second_grade_idx < req_grade_two_idx:
                        grade_score += (req_grade_two_idx + 1) - (second_grade_idx + 1)
                    else:
                        grade_score += -1

                sub_two_flag = True

            elif sub_three_flag is False:

                print("Hits sub_three_flag == False")

                cursor.execute("SELECT IFNULL(req_grade_three, 'Checked') AS req_grade_three "
                               " FROM sys.uni_courses "
                               "WHERE uni_id = %s AND course_id = %s",
                               (select_uni, select_course))
                req_grade_three = cursor.fetchall()

                print("req_grade_three = ", req_grade_three)

                if req_grade_three[0][0] != "Checked":

                    req_grade_three_idx = possible_grades.index(req_grade_three[0][0])

                    print("req_grade_three_idx = ", req_grade_three_idx)

                    third_grade_idx = possible_grades.index(third_grade[0][0])

                    print("third_grade_idx = ", third_grade_idx)

                    if third_grade_idx == req_grade_three_idx:
                        grade_score += 1
                        print("third_grade_idx == req_grade_three_idx")
                    elif third_grade_idx < req_grade_three_idx:
                        grade_score += (req_grade_three_idx + 1) - (third_grade_idx + 1)
                        print("third_grade_idx < req_grade_three_idx")
                    else:
                        grade_score += -1
                        print("Grade score set to -1")

                sub_three_flag = True

                print("sub_three_flag = ", sub_three_flag)

            else:

                print("Entered other subject check")

                cursor.execute("SELECT IFNULL(req_grade_four, 'Checked') AS req_grade_four "
                               " FROM sys.uni_courses "
                               "WHERE uni_id = %s AND course_id = %s",
                               (select_uni, select_course))
                req_grade_four = cursor.fetchall()

                if req_grade_four[0][0] != "Checked":

                    req_grade_four_idx = possible_grades.index(req_grade_four[0][0])

                    other_grade_idx = possible_grades.index(other_grade[0][0])

                    if other_grade_idx == req_grade_four_idx:
                        grade_score += 1
                    elif other_grade_idx < req_grade_four_idx:
                        grade_score += (req_grade_four_idx + 1) - (other_grade_idx + 1)
                    else:
                        grade_score += -1

                sub_other_flag = True

        cursor.execute("SELECT id "
                       " FROM sys.uni_courses "
                       "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
        course_id = cursor.fetchall()

        print("course_id = ", course_id)

        keyterms_array = []

        course_id_val = course_id[0][0]

        cursor.execute("SELECT keyterms"
                       " FROM sys.uni_course_keyterms "
                       "WHERE uni_course_id = %s", (course_id_val,))

        for term in cursor:
            keyterms_array.append(term)

        processed_statement = personal_statement.lower().replace(".", "").replace(",", "").replace("'", "")

        set(stopwords.words('english'))

        r_nltk = Rake()

        r_nltk.extract_keywords_from_text(processed_statement)

        statement_keyphrases = r_nltk.get_ranked_phrases()

        statement_score = 0

        for keyphrase in statement_keyphrases:
            found = False
            for keyterm in keyterms_array:
                if fuzz.partial_ratio(keyterm, keyphrase) > 80:
                    found = True
                    break
            if found:
                statement_score += 1

        approved = 'T'  # 'T' = TBC

        if grade_score == -1:
            total_score = -1
        else:
            total_score = grade_score + statement_score

        cursor.execute("INSERT INTO sys.uni_application (first_name, last_name, email_address, uni_id, course_id, "
                       "first_grade, second_grade, third_grade, other_grade, grade_score, personal_statement, ps_score, "
                       "total_score, approved_mkr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (first_name, last_name, email_address, select_uni, select_course, first_grade, second_grade,
                        third_grade, other_grade, grade_score, personal_statement, statement_score, total_score,
                        approved))
        conn.commit()

        # first find the average of total_score
        cursor.execute("SELECT IFNULL(AVG(total_score), 0) AS average_total"
                       " FROM sys.uni_application ")
        avg_total = cursor.fetchone()

        avg_total_val = avg_total[0]

        # if total_score < average then approved = 'N' (rejected)
        cursor.execute("UPDATE sys.uni_application SET approved_mkr = 'N' WHERE total_score < %s", (avg_total_val,))
        conn.commit()
        # if total_score >= average, find averages for grade_score and statement_score
        cursor.execute("SELECT IFNULL(AVG(grade_score), 0) AS average_grade"
                       " FROM sys.uni_application ")
        avg_grade = cursor.fetchone()
        avg_grade_val = avg_grade[0]

        cursor.execute("SELECT IFNULL(AVG(ps_score), 0) AS average_statement"
                       " FROM sys.uni_application ")
        avg_ps = cursor.fetchone()
        avg_ps_val = avg_ps[0]

        # if grade_score > average grade_score and statement_score > average statement_score then approved = 'U' (unconditional)
        cursor.execute("UPDATE sys.uni_application SET approved_mkr = 'U' WHERE total_score > %s AND grade_score > %s AND ps_score > %s",
                       (avg_total_val, avg_grade_val, avg_ps_val))
        conn.commit()
        # else approved = 'C' (conditional)
        cursor.execute("UPDATE sys.uni_application SET approved_mkr = 'C' WHERE total_score >= %s AND (grade_score <= %s OR ps_score <= %s)",
                       (avg_total_val, avg_grade_val, avg_ps_val))
        conn.commit()

        cursor.close()

        return {"message": "Success: required fields are correctly processed"}
    else:
        return {"message": "Error: appllication process failed to be completed"}

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

    nltk.download('punkt')
    nltk.download('stopwords')


    test_keywords = """\
    skilled programmer
    creative thinker
    problem solving
    technical skills
    algorithm design
    programming
    collaborative
    project management
    """

    test_keywords = test_keywords.strip()

    keyword_array = test_keywords.splitlines()

    keyword_array = [keyword.strip() for keyword in keyword_array]

    sample_statement_one = """ My fascination with technology was sparked when, as a child I thought it would be a great idea to take apart my Playstation console. Aware of the danger, I was still eager to see how it all worked inside. I find it intriguing how fast society has been shaped and continues to be, by the influence of Computer Science. A few years ago if someone were to have claimed that cars would become autonomous, people would have doubted them. Now we are at a stage where nearly anything is possible and this is due to the relentless problem solving of computer scientists. The latest software update released by Tesla motors allows their cars to learn how to drive themselves, and is an example of artificial intelligence, a sector which I am most interested in. I want to study Computer Science because I want to gain the knowledge needed to be able to help find solutions to world problems, with the efficient use of computer technology. With the knowledge and skills, I will attain from this course, the creative ideas that I could bring into fruition would be endless. I hope to become one of the computer scientists who adapt technology to help the human race evolve. One possibility would be for artificially intelligent gadgets to recognise different people and adjust to their individual needs based on personal preferences. I have been teaching myself Objective-C syntax in my spare time and have completed online programming courses, which have allowed me to explore the endless possibilities that computer science can bring to the world. I have also learnt to create a simple iOS game using Apple’s syntax called ‘Swift’, in XCode alongside Photoshop.

I understand that computer science is not just about programming and hardware but also about the ethics entailed in the process of a design as well as innovative thinking. Studying A-Level Philosophy and Ethics has given me an insight into many ethical situations that may arise around computer science such as the creation of artificial intelligence. This raises controversy of whether or not we should be trying to create artificial intelligence, as people have different beliefs and faiths. One example of such controversy was during the development of Honda’s Asimo robot when engineers had to visit the Vatican to seek permission to continue the project due to how human-like the robot was developed to walk. During a week of volunteering on NCS I visited Wazoku, the creators of an idea-sharing software used by major corporations such as Waitrose and The BBC. I was given an insight into the working environment that I hope to join after completing my degree. I am applying for work experience at Wazoku, in order to learn about how the software industry can influence the progress of companies.

I am constantly seeking to learn new skills and gain experience from various activities. I have been a member of the RAF Air Cadets for four years, where I have learnt many valuable life skills such as discipline, leadership, charity and confidence. Alongside these life skills I have gained various qualifications such as The St. John’s Ambulance Youth First Aid qualification and Leading Cadet qualification. Being a cadet also involved doing charity work such as raising money for the RAF Benevolence Fund and the Poppy Appeal. Through all these experiences I have learnt how to work with people from all walks of life, different backgrounds and people who have different beliefs and ideas to the ones I do. This has enabled me to adjust my approach to solving different problems and situations. 

Technological advancements take place around us everyday, from the evolution of bulky antenna phones into smart phones to the introduction of smart virtual assistants such as Apple’s Siri, Google Now and Windows’ Cortana. I am inspired by the fact that computer science has become a fundamental element in the development of a better, smarter future for our world and my goal is to be part of that development process."""

    # preprocess the statement

    processed_text = sample_statement_one.lower().replace(".", "").replace(",", "").replace("'", "")

    # get stop words

    set(stopwords.words('english'))

    r_nltk = Rake()

    r_nltk.extract_keywords_from_text(processed_text)

    keywords = r_nltk.get_ranked_phrases()

    print("keyword_array = ", keyword_array)

    # removed train_test_split as this is inappropriate for binomial approach

    correct = 0

    score = 0

    total = 0

    for keyphrase in keywords:
        found = False
        for keyword in keyword_array:
            if fuzz.partial_ratio(keyword, keyphrase) > 80:
                found = True
                print(keyword)
                break
        if found:
            correct += 1
            score += 1
        total += 1

    if total == 0:
        accuracy = 0
    else:
        accuracy = (correct / total) * 100

    print("Accuracy = ", accuracy, "%")
    print("Total = ", total)
    print("Personal statement score = ", score)

    return {"message": "Success: required fields are correctly processed"}
    # else:
        # return {"message": "Error: there is 1 or more fields that didn't process correctly"}
>>>>>>> 1412968 (Test of rake_nltk able to process sample statement into keyphrases)
