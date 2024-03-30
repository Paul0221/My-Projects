from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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

    if (first_name is not None and last_name is not None and email_address is not None
            and select_uni is not None and select_course is not None and first_subject is not None
            and first_grade is not None and second_subject is not None and second_grade is not None
            and third_subject is not None and third_grade is not None and personal_statement is not None):

        # First check to see if there's any mandatory subjects that applicants must have studied for their chosen course

        cursor.execute("SELECT IFNULL(req_subject_one, 'None') AS req_subject_one "
                       " FROM sys.uni_courses "
                       "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
        req_sub_one_check = cursor.fetchall()
        cursor.execute("SELECT IFNULL(req_subject_two, 'None') AS req_subject_two "
                       " FROM sys.uni_courses "
                       "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
        req_sub_two_check = cursor.fetchall()
        if req_sub_one_check != "None":
            cursor.execute("SELECT req_sub_one_grade "
                           " FROM sys.uni_courses "
                           "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
            req_sub_one_grade = cursor.fetchall()

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
            cursor.execute("SELECT req_sub_two_grade "
                           " FROM sys.uni_courses "
                           "WHERE uni_id = %s AND course_id = %s", (select_uni, select_course))
            req_sub_two_grade = cursor.fetchall()

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
async def submit_sign_in(username: str = Form(...), password: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is null when it should not")
    if password is None:
        raise HTTPException(status_code=401, detail="Password is null when it should not")

    print("Entered post for /submit_sign_in")
    print("username = " + username)
    print("password = " + password)
    cursor.execute("SELECT user_name, user_password FROM sys.users WHERE user_name = 'admin' AND user_password = %s)",
                   (username, password))
    current_user = cursor.fetchone()
    cursor.close()
    if not current_user:
        raise HTTPException(status_code=402, detail="Incorrect login details, please try again.")
    else:
        return RedirectResponse(url='/', status_code=302)  # redirect to admissions main screen
>>>>>>> 8aed0c1 (Completed checks for required subject grades)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
