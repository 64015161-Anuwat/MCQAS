class ItemAnalysis:
    def __init__(self, exam_results):
        self.exam_results = exam_results

    def calculate_item_difficulty(self, item_number):
        """
        Calculate the difficulty of an item.
        Difficulty is calculated as the percentage of students who answered the item correctly.
        """
        total_students = len(self.exam_results)
        correct_count = sum(result[item_number] for result in self.exam_results)

        if total_students == 0:
            return 0

        difficulty = correct_count / total_students
        return difficulty

    def calculate_item_discrimination(self, item_number):
        """
        Calculate the discrimination index of an item.
        Discrimination index is the difference in the percentage of top and bottom scoring groups.
        """
        sorted_results = sorted(self.exam_results, key=lambda x: x[item_number])

        total_students = len(sorted_results)
        if total_students == 0:
            return 0  # Handle the case when there are no students

        top_group_count = max(int(total_students * 0.27), 1)  # Ensure at least one student in the group
        bottom_group_count = max(int(total_students * 0.27), 1)  # Ensure at least one student in the group

        top_group_correct = sum(result[item_number] for result in sorted_results[-top_group_count:])
        bottom_group_correct = sum(result[item_number] for result in sorted_results[:bottom_group_count])

        discrimination_index = (top_group_correct / top_group_count) - (bottom_group_correct / bottom_group_count)
        return discrimination_index



# Example exam results (each tuple represents a student's answers)
exam_results = [
    (1, 1, 0, 1, 0),
    (0, 1, 0, 1, 1),
    (1, 0, 1, 0, 1),
    # Add more exam results as needed
]

# Create an instance of ItemAnalysis
analysis = ItemAnalysis(exam_results)

# Calculate difficulty and discrimination for each item
for item_number in range(len(exam_results[0])):
    item_difficulty = analysis.calculate_item_difficulty(item_number)
    item_discrimination = analysis.calculate_item_discrimination(item_number)
    print(f"Item {item_number + 1}: Difficulty={item_difficulty:.2f}, Discrimination={item_discrimination:.2f}")
