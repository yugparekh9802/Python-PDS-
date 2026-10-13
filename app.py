"""
Student Management System - PBL 3
Built with Python, Pandas, CSV, and Streamlit.

Run:
    streamlit run app.py
"""

import os
import pandas as pd
import streamlit as st

CSV_FILE = "students.csv"
COLUMNS = [
    "student_id", "name", "gender", "age", "department", "city", "semester",
    "attendance", "study_hours", "assignment_marks", "midterm_marks",
    "final_marks", "total", "result", "grade"
]
DEPTS = ["Computer", "IT", "Mechanical", "Civil", "Electrical"]

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)


def calc_grade(total):
    """Calculate a grade from total marks out of 100."""
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


class StudentStore:
    """Read and write student records in a CSV file."""

    def __init__(self, path):
        self.path = path

    def load(self):
        if not os.path.exists(self.path):
            return pd.DataFrame(columns=COLUMNS)
        data = pd.read_csv(self.path)
        # Keep the expected column order if a CSV has all project columns.
        if all(column in data.columns for column in COLUMNS):
            data = data[COLUMNS]
        return data

    def save(self, data):
        data.to_csv(self.path, index=False)

    def next_id(self, data):
        if data.empty or "student_id" not in data.columns:
            return 1001
        return int(pd.to_numeric(data["student_id"], errors="coerce").max()) + 1

    @staticmethod
    def build_record(student_id, data):
        record = data.copy()
        total = (
            float(record["assignment_marks"])
            + float(record["midterm_marks"])
            + float(record["final_marks"])
        )
        record.update({
            "student_id": int(student_id),
            "total": total,
            "result": "Pass" if total >= 40 else "Fail",
            "grade": calc_grade(total)
        })
        return record

    def add(self, data):
        current = self.load()
        record = self.build_record(self.next_id(current), data)
        new_row = pd.DataFrame([record], columns=COLUMNS)
        self.save(pd.concat([current, new_row], ignore_index=True))

    def update(self, student_id, data):
        current = self.load()
        matching = current["student_id"].astype(int) == int(student_id)
        if matching.any():
            record = self.build_record(student_id, data)
            for column in COLUMNS:
                current.loc[matching, column] = record[column]
            self.save(current)

    def delete(self, student_id):
        current = self.load()
        current = current[current["student_id"].astype(int) != int(student_id)]
        self.save(current)


store = StudentStore(CSV_FILE)

if not os.path.exists(CSV_FILE):
    st.error("students.csv was not found. Keep it in the same folder as app.py.")
    st.stop()

df = store.load()

st.sidebar.title("🎓 Student Management")
page = st.sidebar.radio(
    "Navigate",
    [
        "📊 Dashboard",
        "📋 View / Search",
        "➕ Add Student",
        "✏️ Update / Delete"
    ]
)
st.sidebar.caption(f"Student records: {len(df)}")
st.sidebar.caption("Data is saved in students.csv")


def student_form(default=None, form_key="student_form"):
    """Display a student form and return entered values when submitted."""
    default = default or {}
    with st.form(form_key):
        left, right = st.columns(2)

        name = left.text_input("Full Name", str(default.get("name", "")))
        gender_options = ["Male", "Female", "Other"]
        old_gender = default.get("gender", "Male")
        gender_index = gender_options.index(old_gender) if old_gender in gender_options else 0
        gender = right.selectbox("Gender", gender_options, index=gender_index)

        age_value = default.get("age", 20)
        age = left.number_input("Age", min_value=16, max_value=40,
                                value=int(age_value) if pd.notna(age_value) else 20)

        old_dept = default.get("department", DEPTS[0])
        dept_index = DEPTS.index(old_dept) if old_dept in DEPTS else 0
        department = right.selectbox("Department", DEPTS, index=dept_index)

        city_value = default.get("city", "")
        city = left.text_input(
            "City", "" if pd.isna(city_value) else str(city_value)
        )

        semester_value = default.get("semester", 5)
        semester = right.selectbox(
            "Semester", list(range(1, 9)),
            index=max(0, min(7, int(semester_value) - 1))
            if pd.notna(semester_value) else 4
        )

        attendance_value = default.get("attendance", 75.0)
        attendance = left.slider(
            "Attendance (%)", 0.0, 100.0,
            float(attendance_value) if pd.notna(attendance_value) else 75.0
        )

        study_value = default.get("study_hours", 3.0)
        study_hours = right.slider(
            "Study hours per day", 0.0, 10.0,
            float(study_value) if pd.notna(study_value) else 3.0,
            step=0.5
        )

        assignment_default = default.get("assignment_marks", 10)
        assignment_marks = left.number_input(
            "Assignment marks (out of 20)", min_value=0, max_value=20,
            value=int(assignment_default) if pd.notna(assignment_default) else 10
        )

        midterm_default = default.get("midterm_marks", 15)
        midterm_marks = right.number_input(
            "Midterm marks (out of 30)", min_value=0, max_value=30,
            value=int(midterm_default) if pd.notna(midterm_default) else 15
        )

        final_default = default.get("final_marks", 25)
        final_marks = left.number_input(
            "Final marks (out of 50)", min_value=0, max_value=50,
            value=int(final_default) if pd.notna(final_default) else 25
        )

        submitted = st.form_submit_button("Save Student")
    values = {
        "name": name.strip(),
        "gender": gender,
        "age": age,
        "department": department,
        "city": city.strip(),
        "semester": semester,
        "attendance": attendance,
        "study_hours": study_hours,
        "assignment_marks": assignment_marks,
        "midterm_marks": midterm_marks,
        "final_marks": final_marks
    }
    return submitted, values


if page.startswith("📊"):
    st.title("📊 Student Dashboard")
    st.write("A simple overview of the student records stored in the CSV file.")

    col1, col2 = st.columns(2)
    col1.metric("Total Students", len(df))

    if not df.empty and "total" in df.columns:
        average = pd.to_numeric(df["total"], errors="coerce").mean()
        average_text = f"{average:.1f}" if pd.notna(average) else "N/A"
    else:
        average_text = "N/A"
    col2.metric("Average Marks", average_text)

    st.subheader("Recently listed students")
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)

elif page.startswith("📋"):
    st.title("📋 View and Search Students")

    if df.empty:
        st.info("No student records are available yet.")
    else:
        search_text = st.text_input("Search by student name or ID")
        department_filter = st.multiselect("Filter by department", DEPTS)
        result_filter = st.multiselect("Filter by result", ["Pass", "Fail"])

        filtered = df.copy()
        if search_text.strip():
            query = search_text.strip()
            filtered = filtered[
                filtered["name"].astype(str).str.contains(query, case=False, na=False)
                | filtered["student_id"].astype(str).str.contains(query, na=False)
            ]
        if department_filter:
            filtered = filtered[filtered["department"].isin(department_filter)]
        if result_filter:
            filtered = filtered[filtered["result"].isin(result_filter)]

        sort_column = st.selectbox(
            "Sort records by", ["student_id", "name", "total", "attendance"]
        )
        filtered = filtered.sort_values(
            sort_column, ascending=sort_column in ["student_id", "name"],
            na_position="last"
        )
        st.write(f"Records found: **{len(filtered)}**")
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        st.download_button(
            "Download displayed records as CSV",
            data=filtered.to_csv(index=False),
            file_name="filtered_students.csv",
            mime="text/csv"
        )

elif page.startswith("➕"):
    st.title("➕ Add a Student")
    st.write("Enter the student's details below. The record will be saved to students.csv.")
    submitted, values = student_form(form_key="add_student_form")
    if submitted:
        if not values["name"]:
            st.error("Please enter the student's name.")
        else:
            store.add(values)
            st.success(f"Student '{values['name']}' added successfully.")
            st.rerun()

else:
    st.title("✏️ Update or Delete a Student")

    if df.empty:
        st.info("There are no records to update or delete.")
    else:
        ids = df["student_id"].astype(int).tolist()
        selected_id = st.selectbox(
            "Select a student",
            ids,
            format_func=lambda sid: (
                f"{sid} - {df.loc[df['student_id'].astype(int) == sid, 'name'].iloc[0]}"
            )
        )
        selected_row = df[df["student_id"].astype(int) == int(selected_id)].iloc[0].to_dict()

        st.subheader("Update student details")
        submitted, values = student_form(
            default=selected_row, form_key="update_student_form"
        )
        if submitted:
            if not values["name"]:
                st.error("Please enter the student's name.")
            else:
                store.update(selected_id, values)
                st.success("Student record updated successfully.")
                st.rerun()

        st.divider()
        st.subheader("Delete student")
        confirm_delete = st.checkbox(
            f"I confirm that I want to delete {selected_id} - {selected_row['name']}"
        )
        if st.button("Delete selected student", type="primary", disabled=not confirm_delete):
            store.delete(selected_id)
            st.success("Student record deleted.")
            st.rerun()
