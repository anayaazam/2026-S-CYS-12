# marking scheme
CORRECT_MARKS = 4
WRONG_MARKS   = -1
SKIP_MARKS    = 0
MAX_ATTEMPTS  = 3
# credentials
ADMIN_USER, ADMIN_PASS     = "ecat_admin", "ecat@2024"
STUDENT_USER, STUDENT_PASS = "student",    "student123"
questions = [
{"subject": "Math",    "q": "What is 2 + 2?",                "choices": ["3","4","5","6"],                                    "answer": "B"},
{"subject": "Math",    "q": "Square root of 144?",           "choices": ["10","11","12","13"],                                "answer": "C"},
{"subject": "Math",    "q": "What is 15% of 200?",           "choices": ["25","30","35","40"],                                "answer": "B"},
{"subject": "Physics", "q": "Unit of force?",                "choices": ["Joule","Newton","Watt","Pascal"],                   "answer": "B"},
{"subject": "Physics", "q": "Speed of light (approx)?",      "choices": ["3×10⁶ m/s","3×10⁸ m/s","3×10¹⁰ m/s","3×10⁴ m/s"],   "answer": "B"},
{"subject": "Physics", "q": "Which law: F = ma?",            "choices": ["1st","2nd","3rd","Law of gravity"],                 "answer": "B"},
{"subject": "Chem",    "q": "Chemical symbol of Gold?",      "choices": ["Go","Gd","Au","Ag"],                                "answer": "C"},
{"subject": "Chem",    "q": "Atomic number of Carbon?",      "choices": ["4","5","6","7"],                                    "answer": "C"},
{"subject": "Chem",    "q": "pH of pure water?",             "choices": ["5","6","7","8"],                                    "answer": "C"},
{"subject": "English", "q": "Synonym of 'Happy'?",           "choices": ["Sad","Joyful","Angry","Tired"],                     "answer": "B"},
{"subject": "English", "q": "Plural of 'Child'?",            "choices": ["Childs","Childes","Children","Childrens"],          "answer": "C"},
{"subject": "English", "q": "Antonym of 'Ancient'?",         "choices": ["Old","Modern","Historic","Classic"],                "answer": "B"},
]
all_results = []
def sep():
    print("-" * 50)
def grade(pct):
    if pct >= 80: return "EXCELLENT"
    if pct >= 65: return "GOOD"
    if pct >= 50: return "AVERAGE"
    return "BELOW AVERAGE"
import time
def login(expected_user, expected_pass):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        u = input("Username: ").strip()
        p = input("Password: ").strip()
        if u == expected_user and p == expected_pass:
            print("Login successful!")
            time.sleep(0.5)
            return True
        print(f"Wrong credentials. Attempt {attempt}/{MAX_ATTEMPTS}.")
    print("Too many failed attempts. Locked out.")
    return False
def view_questions():
    if not questions:
        print("No questions in bank.")
        return
    for i, q in enumerate(questions, 1):
        print(f"\n[{i}] ({q['subject']}) {q['q']}")
        for letter, choice in zip("ABCD", q["choices"]):
            mark = " ✓" if letter == q["answer"] else ""
            print(f" {letter}. {choice}{mark}")
def add_question():
    print("\n-- Add New Question --")
    subject  = input("Subject: ").strip()
    text     = input("Question: ").strip()
    choices  = [input(f"Choice {l}: ").strip() for l in "ABCD"]
    answer   = input("Correct answer (A/B/C/D): ").strip().upper()
    if answer not in "ABCD":
        print("Invalid answer key. Question not added.")
        return
    questions.append({"subject": subject, "q": text, "choices": choices, "answer": answer})
    print("Question added!")
def delete_question():
    view_questions()
    try:
        n = int(input("\nEnter question number to delete: "))
        if 1 <= n <= len(questions):
            removed = questions.pop(n - 1)
            print(f"Deleted: {removed['q']}")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")
def question_stats():
    sep()
    print(f"Total questions: {len(questions)}")
    subjects = {}
    for q in questions:
        subjects[q["subject"]] = subjects.get(q["subject"],0) + 1
    for subj, count in subjects.items():
        print(f"  {subj}: {count}")
    sep()
def view_all_results():
    if not all_results:
        print("No exam results yet.")
        return
    sep()
    print(f"{'#':<4} {'Name':<20} {'Roll':<12} {'Score':<8} {'%':<8} {'Grade':<14} {'Time'}")
    sep()
    for i, r in enumerate(all_results, 1):
        print(f"{i:<4} {r['name']:<20} {r['roll']:<12} {r['score']:<8} {r['pct']:<8.1f} {r['grade']:<14} {r['time']}")
    sep()
def view_detailed_result():
    view_all_results()
    if not all_results:
        return
    try:
        n = int(input("Enter result number to view: "))
        if not (1 <= n <= len(all_results)):
            print("Invalid number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return
    r = all_results[n - 1]
    sep()
    print(f"Result for {r['name']}  |  Roll: {r['roll']}  |  Time: {r['time']}")
    sep()
    for i, q in enumerate(questions):
        given  = r["answers"].get(i, "S")
        status = "SKIP" if given == "S" else ("✓" if given == q["answer"] else "✗")
        print(f"Q{i+1}. {q['q']}")
        print(f"     Your answer: {given}  |  Correct: {q['answer']}  |  {status}")
    sep()
    print(f"Score: {r['score']}  |  {r['pct']:.1f}%  |  {r['grade']}")
    sep()
def class_statistics():
    if not all_results:
        print("No results to analyse.")
        return
    scores = [r["score"] for r in all_results]
    sep()
    print(f"Students: {len(scores)}  |  High: {max(scores)}  |  Low: {min(scores)}  |  Avg: {sum(scores)/len(scores):.1f}")
    passed = sum(1 for r in all_results if r["pct"] >= 50)
    print(f"Pass: {passed}  |  Fail: {len(scores) - passed}")
    grade_dist = {}
    for r in all_results:
        grade_dist[r["grade"]] = grade_dist.get(r["grade"], 0) + 1
    print("Grade distribution:", grade_dist)
    sep()
def admin_portal():
    print("\n     ADMIN PORTAL")
    if not login(ADMIN_USER, ADMIN_PASS):
        return
    menu = {
        "1":("View All Questions",       view_questions),
        "2":("Add New Question",         add_question),
        "3":("Delete Question",          delete_question),
        "4":("Question Bank Statistics", question_stats),
        "5":("View All Student Results", view_all_results),
        "6":("View Detailed Result",     view_detailed_result),
        "7":("Class Result Statistics",  class_statistics),
        "8":("Logout",                   None),}
    while True:
        print("\n-- Admin Menu --")
        for k, (label, _) in menu.items():
            print(f"  {k}. {label}")
        choice = input("Choose: ").strip()
        if choice == "8":
            print("Logged out.")
            break
        if choice in menu:
            menu[choice][1]()
        else:
            print("Invalid choice.")
def exam_rules():
    print("EXAM RULES & MARKING SCHEME")
    print("""   INSTRUCTIONS:\n1. The exam contains multiple-choice questions (MCQs).\n2. Enter A,B,C,or D to select an answer.
3. Enter S to skip a question — no marks are deducted for skipping./n4. Type SUBMIT at any question to end the exam early.
5. The exam auto-submits once all questions have been answered.
    MARKING SCHEME:\n Correct Answer: +4 marks \n Wrong Answer  : -1 mark \n Skipped       : 0 marks
    GRADE BOUNDARIES: \n EXCELLENT    :80% and above \n GOOD         :65% – 79% \n AVERAGE      :50% – 64% \n BELOW AVERAGE:Below 50%
  """)
def run_exam(name, roll):
    print("\nExam starting... Good luck!\n")
    answers = {}
    for i, q in enumerate(questions):
        print(f"Q{i+1}/{len(questions)}. [{q['subject']}] {q['q']}")
        for letter, choice in zip("ABCD", q["choices"]):
            print(f"   {letter}. {choice}")
        while True:
            ans = input("Answer (A/B/C/D / S=Skip / SUBMIT): ").strip().upper()
            if ans in ("A", "B", "C", "D", "S"):
                answers[i] = ans
                break
            if ans == "SUBMIT":
                print("Exam submitted early.")
                return save_result(name, roll,answers)
            print("Invalid input. Try again.")
    return save_result(name,roll,answers)
def save_result(name,roll,answers):
    correct = wrong = skipped = 0
    for i, q in enumerate(questions):
        given = answers.get(i, "S")
        if given == "S":
            skipped += 1
        elif given == q["answer"]:
            correct+= 1
        else:
            wrong+= 1
    max_score = len(questions) * CORRECT_MARKS
    score     = correct * CORRECT_MARKS + wrong * WRONG_MARKS
    pct       = (score / max_score) * 100 if max_score else 0
    g         = grade(pct)
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    result = {"name": name, "roll": roll, "score": score, "pct": round(pct, 1),
              "grade": g, "time": timestamp, "answers": answers,
              "correct": correct, "wrong": wrong, "skipped": skipped}
    all_results.append(result)
    sep()
    print(f"RESULT — {name}  |  Roll: {roll}  |  {timestamp}")
    sep()
    print(f"Correct: {correct}  |  Wrong: {wrong}  |  Skipped: {skipped}")
    print(f"Score:   {score} / {max_score}")
    print(f"Percent: {pct:.1f}%")
    print(f"Grade:   {g}")
    sep()
    show = input("Show per-question review? (Y/N): ").strip().upper()
    if show == "Y":
        for i, q in enumerate(questions):
            given  = answers.get(i, "S")
            status = "SKIP" if given == "S" else ("✓" if given == q["answer"] else "x")
            print(f"Q{i+1}. {q['q']}")
            print(f"You: {given} | Correct: {q['answer']} | {status}")
def student_portal():
    print("\n      STUDENT PORTAL")
    if not login(STUDENT_USER,STUDENT_PASS):
        return
    name = input("Full Name: ").strip()
    roll = input("Roll Number: ").strip()
    while True:
        print("\n     Student Menu")
        print("1.View Exam Rules")
        print("2.Start Exam")
        print("3.Logout")
        choice = input("Choose:").strip()
        if choice =="1":
            exam_rules()
        elif choice =="2":
            run_exam(name, roll)
        elif choice =="3":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")
def main():
    print("-"*30)
    print(" ECAT EXAM APPLICATION — Dual Portal System")
    print("-"*30)
    while True:
        print("1. Admin Portal")
        print("2. Student Portal")
        print("3. Exit")
        choice = input("Select portal: ").strip()
        if choice == "1":
            admin_portal()
        elif choice == "2":
            student_portal()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
main()