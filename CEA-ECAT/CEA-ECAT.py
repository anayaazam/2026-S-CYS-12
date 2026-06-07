"""
ECAT EXAM APPLICATION — DUAL PORTAL SYSTEM
"""
import time  # recording exam time
#  marking scheme
CORRECT_MARKS =  4
WRONG_MARKS    = -1
SKIP_MARKS     =  0
MIN_QUESTIONS  = 10
#  credentials
ADMIN_USERNAME   = "ecat_admin"
ADMIN_PASSWORD   = "ecat@2024"
STUDENT_USERNAME = "student"
STUDENT_PASSWORD = "student123"
questions = [
    {   "id": 1,
        "subject": "Mathematics",
        "question": "What is the value of 2^10?",
        "choices": {"A": "512", "B": "1024", "C": "2048", "D": "256"},
        "answer": "B"},
    {   "id": 2,
        "subject": "Mathematics",
        "question": "If x² = 144, what is the positive value of x?",
        "choices": {"A": "11", "B": "13", "C": "12", "D": "14"},
        "answer": "C"},
    {   "id": 3,
        "subject": "Mathematics",
        "question": "What is the derivative of sin(x)?",
        "choices": {"A": "-cos(x)", "B": "cos(x)", "C": "-sin(x)", "D": "tan(x)"},
        "answer": "B"},
    {   "id": 4,
        "subject": "Physics",
        "question": "What is the SI unit of electric current?",
        "choices": {"A": "Volt", "B": "Watt", "C": "Ohm", "D": "Ampere"},
        "answer": "D"},
    {   "id": 5,
        "subject": "Physics",
        "question": "Which law states F = ma?",
        "choices": {"A": "Newton's 1st Law", "B": "Newton's 2nd Law",
                    "C": "Newton's 3rd Law", "D": "Hooke's Law"},
        "answer": "B"},
    {   "id": 6,
        "subject": "Physics",
        "question": "What is the speed of light in vacuum (approx)?",
        "choices": {"A": "3×10⁶ m/s", "B": "3×10⁷ m/s",
                    "C": "3×10⁸ m/s", "D": "3×10⁹ m/s"},
        "answer": "C"},
    {   "id": 7,
        "subject": "Chemistry",
        "question": "What is the atomic number of Carbon?",
        "choices": {"A": "4", "B": "6", "C": "8", "D": "12"},
        "answer": "B" },
    {   "id": 8,
        "subject": "Chemistry",
        "question": "Which gas is known as laughing gas?",
        "choices": {"A": "NO", "B": "NO₂", "C": "N₂O", "D": "N₂O₃"},
        "answer": "C"},
    {   "id": 9,
        "subject": "Chemistry",
        "question": "What is the pH of pure water at 25°C?",
        "choices": {"A": "6", "B": "8", "C": "7", "D": "9"},
        "answer": "C"},
    {   "id": 10,
        "subject": "English",
        "question": "Choose the correct sentence:",
        "choices": {
            "A": "She don't like mangoes.",
            "B": "She doesn't likes mangoes.",
            "C": "She doesn't like mangoes.",
            "D": "She not like mangoes."
        },
        "answer": "C"}
]
# student attempts
all_results = []
#  HELPER / UTILITY FUNCTIONS
def print_line(char="─", length=60):
    """Print a decorative separator line."""
    print(char * length)
def print_header(title):
    print_line("═")
    print(f"  {title}")
    print_line("═")
def pause(seconds=1.5):
    time.sleep(seconds)
def calculate_grade(percentage):
    if percentage >= 80:
        return "EXCELLENT"
    elif percentage >= 65:
        return "GOOD"
    elif percentage >= 50:
        return "AVERAGE"
    else:
        return "BELOW AVERAGE"
def calculate_score(answers_dict):
    correct = 0
    wrong   = 0
    skipped = 0
    for idx, chosen in answers_dict.items():
        correct_ans = questions[idx]["answer"]
        if chosen == "S":
            skipped += 1
        elif chosen == correct_ans:
            correct += 1
        else:
            wrong += 1
    total_score   = (correct * CORRECT_MARKS) + (wrong * WRONG_MARKS)
    max_possible  = len(questions) * CORRECT_MARKS
    return total_score, correct, wrong, skipped, max_possible
def admin_login():
    print_header("ADMIN LOGIN — ECAT Team Portal")
    attempts = 0
    while attempts < 3:
        remaining = 3 - attempts
        print(f"\n  Attempts remaining: {remaining}")
        username = input("  Username: ").strip()
        password = input("  Password: ").strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("\n Login successful! Welcome, ECAT Admin.")
            pause()
            return True
        else:
            attempts += 1
            print("Incorrect credentials. Try again.")
    print("\n Account locked after 3 failed attempts. Returning to main menu.")
    pause()
    return False
def student_login():
    print_header("STUDENT LOGIN — ECAT Exam Portal")
    attempts = 0
    while attempts < 3:
        remaining = 3 - attempts
        print(f"\n  Attempts remaining: {remaining}")
        username = input("  Username : ").strip()
        password = input("  Password : ").strip()
        if username == STUDENT_USERNAME and password == STUDENT_PASSWORD:
            print("\n Credentials verified!")
            name = input("  Enter your full name : ").strip()
            roll = input("  Enter your roll number: ").strip()
            print(f"\n  Welcome, {name}! Good luck on your exam.")
            pause()
            return name, roll
        else:
            attempts += 1
            print("Incorrect credentials. Try again.")
    print("\n Account locked after 3 failed attempts. Ask for help.")
    pause()
    return None, None
#  ADMIN PORTAL FUNCTIONS
def admin_view_all_questions():
    print_header("QUESTION BANK — All Questions")
    if not questions:
        print("  No questions found in the bank.")
        return
    for i, q in enumerate(questions):
        print(f"\n  Q{i + 1}. [{q['subject']}] {q['question']}")
        for letter, choice in q["choices"].items():
            # Mark the correct answer with ✔
            marker = "✔" if letter == q["answer"] else " "
            print(f"       {marker} {letter}) {choice}")
    print()
    input("  Press ENTER to go back...")
def admin_add_question():
    print_header("ADD NEW QUESTION")
    subject  = input("  Subject (e.g. Mathematics, Physics): ").strip()
    question = input("  Question text: ").strip()
    print("  Enter 4 answer choices:")
    choice_a = input("    A) ").strip()
    choice_b = input("    B) ").strip()
    choice_c = input("    C) ").strip()
    choice_d = input("    D) ").strip()
    while True:
        answer = input("  Correct answer (A/B/C/D): ").strip().upper()
        if answer in ["A", "B", "C", "D"]:
            break
        print("  ✘  Please enter A, B, C, or D only.")
    # Build new question dict and append
    new_q = {
        "id"      : len(questions) + 1,
        "subject" : subject,
        "question": question,
        "choices" : {"A": choice_a, "B": choice_b, "C": choice_c, "D": choice_d},
        "answer"  : answer
    }
    questions.append(new_q)
    print(f"\n Question added! Total questions: {len(questions)}")
    pause()
def admin_delete_question():
    print_header("DELETE A QUESTION")
    if not questions:
        print(" No questions to delete.")
        pause()
        return
    # Show a quick numbered list
    for i, q in enumerate(questions):
        print(f"  {i + 1}. [{q['subject']}] {q['question'][:55]}...")
    print()
    try:
        num = int(input(f"  Enter question number to delete (1–{len(questions)}): "))
        if 1 <= num <= len(questions):
            removed = questions.pop(num - 1)
            print(f"\n Deleted: '{removed['question']}'")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")
    pause()
def admin_question_stats():
    # Show total question count and breakdown by subject.
    print_header("QUESTION BANK — Statistics")
    # Count questions per subject using a dictionary
    subject_counts = {}
    for q in questions:
        subj = q["subject"]
        subject_counts[subj] = subject_counts.get(subj, 0) + 1
    print(f"\n  Total Questions : {len(questions)}")
    print(f"  Minimum Required: {MIN_QUESTIONS}")
    print_line()
    print("  Breakdown by Subject:")
    for subj, count in subject_counts.items():
        print(f"    • {subj:<20} {count} question(s)")
    print()
    input("  Press ENTER to go back...")
def admin_view_all_results():
    print_header("ALL STUDENT RESULTS — Summary")
    if not all_results:
        print("  No student results yet.")
        input("\n  Press ENTER to go back...")
        return
    print(f"\n  {'#':<4} {'Name':<20} {'Roll':<12} {'Score':<8} {'%':<8} {'Grade':<14} {'Time'}")
    print_line()
    for i, result in enumerate(all_results):
        print(f"  {i + 1:<4} {result['name']:<20} {result['roll']:<12} "
              f"{result['score']:<8} {result['percentage']:<8.1f} "
              f"{result['grade']:<14} {result['timestamp']}")
    print()
    input("  Press ENTER to go back...")
def admin_view_detailed_result():
    """Show a full question-by-question breakdown for one student attempt."""
    print_header("DETAILED RESULT — Per Student")
    if not all_results:
        print("  No student results yet.")
        input("\n  Press ENTER to go back...")
        return
    # List students to pick from
    for i, result in enumerate(all_results):
        print(f"  {i + 1}. {result['name']} (Roll: {result['roll']}) — {result['timestamp']}")
    print()
    try:
        num = int(input(f"  Enter student number (1–{len(all_results)}): "))
        if not (1 <= num <= len(all_results)):
            print("  ✘  Invalid number.")
            pause()
            return
    except ValueError:
        print("  ✘  Please enter a valid number.")
        pause()
        return
    result = all_results[num - 1]
    print_header(f"Result for: {result['name']} | Roll: {result['roll']}")
    # Question-by-question review
    for idx, q in enumerate(questions):
        student_answer = result["answers"].get(idx, "S")
        correct_answer = q["answer"]
        if student_answer == "S":
            outcome = "SKIPPED  (0)"
        elif student_answer == correct_answer:
            outcome = f"CORRECT  (+{CORRECT_MARKS})"
        else:
            outcome = f"WRONG    ({WRONG_MARKS})"
        print(f"\n  Q{idx + 1}. {q['question']}")
        print(f"       Your Answer   : {student_answer}")
        print(f"       Correct Answer: {correct_answer}")
        print(f"       Result        : {outcome}")
    print_line()
    print(f"  Final Score : {result['score']}  |  "
          f"Percentage: {result['percentage']:.1f}%  |  "
          f"Grade: {result['grade']}")
    print()
    input("  Press ENTER to go back...")
def admin_class_stats():
    """Show class-wide statistics: highest, lowest, average, grade distribution."""
    print_header("CLASS RESULT STATISTICS")
    if not all_results:
        print("  No student results yet.")
        input("\n  Press ENTER to go back...")
        return
    scores = [r["score"] for r in all_results]
    highest = max(scores)
    lowest  = min(scores)
    average = sum(scores) / len(scores)
    pass_count = sum(1 for r in all_results if r["percentage"] >= 50)
    fail_count = len(all_results) - pass_count
    # Grade distribution
    grade_dist = {}
    for r in all_results:
        g = r["grade"]
        grade_dist[g] = grade_dist.get(g, 0) + 1
    print(f"\n  Total Attempts   : {len(all_results)}")
    print(f"  Highest Score    : {highest}")
    print(f"  Lowest Score     : {lowest}")
    print(f"  Average Score    : {average:.2f}")
    print(f"  Passed (≥50%)    : {pass_count}")
    print(f"  Failed (<50%)    : {fail_count}")
    print_line()
    print("  Grade Distribution:")
    for grade, count in grade_dist.items():
        print(f"    • {grade:<16} {count} student(s)")
    print()
    input("  Press ENTER to go back...")
#  STUDENT PORTAL FUNCTIONS
def show_exam_rules():
    print_header("EXAM RULES & MARKING SCHEME")
    print("""
  INSTRUCTIONS:
  • The exam contains multiple-choice questions.
  • For each question, enter A, B, C, or D to answer.
  • Enter S to skip the question (no marks deducted).
  • Type SUBMIT at any question to end the exam early.
  • The exam auto-submits when all questions are answered.
  MARKING SCHEME:
  • Correct Answer : +4 marks       • Wrong Answer   : -1 mark          • Skipped        :  0 marks
  GRADE BOUNDARIES:
  • EXCELLENT   → 80% and above    • GOOD  → 65% – 79%  • AVERAGE→ 50% – 64%  • BELOW AVERAGE→ Below 50%""")
    input("  Press ENTER to go back...")
def start_exam(name, roll):
    print_header(f"EXAM STARTING — {name} | Roll: {roll}")
    print("  Type A/B/C/D to answer | S to skip | SUBMIT to finish early\n")
    answers = {}
    start_time = time.time()
    for idx in range(len(questions)):
        q = questions[idx]
        print_line()
        print(f"\n  Question {idx + 1} of {len(questions)}  [{q['subject']}]")
        print(f"  {q['question']}\n")
        for letter, choice in q["choices"].items():
            print(f"    {letter}) {choice}")
        print()
        while True:
            raw = input("  Your answer: ").strip().upper()
            if raw == "SUBMIT":
                # Early exit — mark remaining as skipped
                print("\n Exam submitted early.")
                for remaining in range(idx, len(questions)):
                    answers[remaining] = "S"
                idx = len(questions)
                break
            elif raw in ["A", "B", "C", "D"]:
                answers[idx] = raw
                break
            elif raw == "S":
                answers[idx] = "S"
                print("  → Question skipped.")
                break
            else:
                print("  ✘  Invalid input. Enter A, B, C, D, S, or SUBMIT.")
        if idx == len(questions):
            break
    elapsed = int(time.time() - start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    total_score, correct, wrong, skipped, max_possible = calculate_score(answers)
    percentage = (total_score / max_possible) * 100 if max_possible > 0 else 0
    percentage = max(0, percentage)  # Score can't go below 0% on display
    grade      = calculate_grade(percentage)
    timestamp  = time.strftime("%Y-%m-%d %H:%M")
    print_header(f"EXAM RESULT — {name}")
    print(f"  Score    : {total_score} / {max_possible}")
    print(f"  Correct  : {correct}  |  Wrong: {wrong}  |  Skipped: {skipped}")
    print(f"  Percentage: {percentage:.1f}%")
    print(f"  Grade    : {grade}")
    print(f"  Time Taken: {minutes}m {seconds}s")
    print_line()
    print("\n  ANSWER REVIEW:")
    for idx2, q in enumerate(questions):
        student_ans = answers.get(idx2, "S")
        correct_ans = q["answer"]
        if student_ans == "S":
            result_text = "SKIPPED"
        elif student_ans == correct_ans:
            result_text = "CORRECT ✔"
        else:
            result_text = f"WRONG ✘ (correct: {correct_ans})"
        print(f"  Q{idx2 + 1}. {q['question'][:45]}...")
        print(f"       You: {student_ans}  →  {result_text}")
    all_results.append({
        "name":name,"roll": roll,"score":total_score,"percentage":percentage,"grade":grade,"correct":correct,"wrong": wrong,"skipped": skipped,"timestamp":timestamp,"answers":answers,})
    print(f"\n  ✔  Result saved! Total attempts on file: {len(all_results)}")
    input("\n  Press ENTER to return to the student menu...")
def admin_menu():
    while True:
        print_header("ADMIN PORTAL — Main Menu")
        print("  1. View All Questions")
        print("  2. Add New Question")
        print("  3. Delete a Question")
        print("  4. Question Bank Statistics")
        print("  5. View All Student Results")
        print("  6. View Detailed Result (Per Student)")
        print("  7. Class Result Statistics")
        print("  8. Logout")
        choice = input("  Select option (1–8): ").strip()
        if   choice == "1": admin_view_all_questions()
        elif choice == "2": admin_add_question()
        elif choice == "3": admin_delete_question()
        elif choice == "4": admin_question_stats()
        elif choice == "5": admin_view_all_results()
        elif choice == "6": admin_view_detailed_result()
        elif choice == "7": admin_class_stats()
        elif choice == "8":
            print("\n  Logging out of Admin Portal...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")
def student_menu(name, roll):
    while True:
        print_header(f"STUDENT PORTAL — {name} | Roll: {roll}")
        print("1. View Exam Rules")
        print("2. Start Exam")
        print("3. Logout")
        print()
        choice = input(" Select option (1–3): ").strip()
        if   choice == "1": show_exam_rules()
        elif choice == "2": start_exam(name, roll)
        elif choice == "3":
            print(f"\n Goodbye, {name}! Good luck with your studies.")
            pause()
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
#  MAIN ENTRY POINT
def main():
    while True:
        print_header("ECAT EXAM APPLICATION — UET Lahore")
        print("Welcome! Please select a portal to continue.\n")
        print("1. Admin Portal   (ECAT Team)")
        print("2. Student Portal (Exam Taker)")
        print("3. Exit Application")
        print()
        choice = input("  Select portal (1–3): ").strip()
        if choice == "1":
            if admin_login():
                admin_menu()
        elif choice == "2":
            name, roll = student_login()
            if name:  # Login succeeded
                student_menu(name, roll)
        elif choice == "3":
            print("\n  Thank you for using the ECAT Exam App. Goodbye!\n")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            pause(0.5)
# Run the program
if __name__ == "__main__":
    main()