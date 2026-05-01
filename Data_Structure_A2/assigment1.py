class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades  # This is a list of numbers

    def calculate_average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def get_performance(self):
        avg = self.calculate_average()
        if avg >= 90:
            return "Excellent"
        elif avg >= 75:
            return "Good"
        elif avg >= 50:
            return "Pass"
        else:
            return "Needs Improvement"

# --- Main Program ---
students_list = []

# Using a loop to process multiple students
while True:
    name = input("\nEnter student name (or type 'exit' to finish): ")
    if name.lower() == 'exit':
        break
    
    # Simple way to take multiple grades at once
    grades_input = input(f"Enter grades for {name} separated by spaces: ")
    # Convert string input into a list of integers
    grade_list = [int(g) for g in grades_input.split()]
    
    # Create the Student object and add to our list
    new_student = Student(name, grade_list)
    students_list.append(new_student)

print("\n--- Final Grade Report ---")
for s in students_list:
    avg = s.calculate_average()
    perf = s.get_performance()
    print(f"Student: {s.name} | Average: {avg:.2f} | Status: {perf}")