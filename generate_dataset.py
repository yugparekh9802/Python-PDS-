"""
Optional dataset generator for the Student Management System.
It uses Python's built-in random module and Pandas.
WARNING: Running this script replaces students.csv with a new sample dataset.
"""

import random
import pandas as pd

SEED = 20261012  # Change this number to create a different sample dataset.
N = 150

random.seed(SEED)

male_names = ["Aarav", "Vivaan", "Dhruv", "Krish", "Om", "Jay", "Harsh", "Mihir", "Rahul", "Yash"]
female_names = ["Riya", "Isha", "Priya", "Neha", "Kavya", "Diya", "Anjali", "Pooja", "Hetal", "Zeel"]
last_names = ["Patel", "Shah", "Desai", "Mehta", "Joshi", "Modi", "Trivedi", "Parekh", "Gandhi", "Vora"]
cities = ["Surat", "Navsari", "Bharuch", "Vadodara", "Valsad", "Ahmedabad"]
departments = ["Computer", "IT", "Mechanical", "Civil", "Electrical"]

def calculate_grade(total):
    if total >= 85:
        return "A+"
    if total >= 75:
        return "A"
    if total >= 65:
        return "B"
    if total >= 50:
        return "C"
    if total >= 40:
        return "D"
    return "F"

rows = []
for student_id in range(1001, 1001 + N):
    gender = random.choice(["Male", "Female"])
    first_name = random.choice(male_names if gender == "Male" else female_names)
    assignment = random.randint(4, 20)
    midterm = random.randint(5, 30)
    final = random.randint(5, 50)
    total = assignment + midterm + final
    rows.append({
        "student_id": student_id,
        "name": f"{first_name} {random.choice(last_names)}",
        "gender": gender,
        "age": random.randint(19, 23),
        "department": random.choice(departments),
        "city": random.choice(cities),
        "semester": random.choice([3, 5, 7]),
        "attendance": round(random.uniform(45, 100), 1),
        "study_hours": round(random.uniform(0.5, 8), 1),
        "assignment_marks": assignment,
        "midterm_marks": midterm,
        "final_marks": final,
        "total": total,
        "result": "Pass" if total >= 40 else "Fail",
        "grade": calculate_grade(total)
    })

pd.DataFrame(rows).to_csv("students.csv", index=False)
print(f"Created students.csv with {N} sample student records.")
