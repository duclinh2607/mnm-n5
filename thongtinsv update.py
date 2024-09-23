import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog


def load_data(file_path):
    """Tải dữ liệu từ file CSV vào mảng numpy."""
    try:
        print(f"Đang tải dữ liệu từ: {file_path}")
        data = np.genfromtxt(file_path, delimiter=',', dtype=str, encoding='ISO-8859-1', skip_header=1)
        if data.size == 0:
            print("Dữ liệu tải về trống.")
        return data
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu: {e}")
        return np.array([])


def search_student(data, student_id):
    """Tìm kiếm thông tin sinh viên theo ID."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    if not student_id:
        return "Vui lòng nhập ID sinh viên."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        return "\n".join([", ".join(row) for row in student_data])


def search_subject(data, subject_name, sort_order):
    """Tìm kiếm điểm của một môn học cụ thể và sắp xếp kết quả."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    if not subject_name:
        return "Vui lòng nhập tên môn học."

    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        return f"Không tìm thấy điểm cho môn học {subject_name}."
    else:
        try:
            subject_data = subject_data[subject_data[:, 3].astype(float).argsort()]  # Sắp xếp theo cột điểm
            if sort_order == '2':  # Nếu chọn giảm dần, đảo ngược thứ tự
                subject_data = subject_data[::-1]

            return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Điểm: {row[3]}" for row in subject_data])
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."


def calculate_average(data, student_id):
    """Tính trung bình điểm cho một sinh viên cụ thể."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    if not student_id:
        return "Vui lòng nhập ID sinh viên."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        try:
            grades = student_data[:, 3].astype(float)  # Chuyển đổi điểm sang số thực
            average_grade = np.mean(grades)
            return f"Trung bình cộng điểm của sinh viên có ID {student_id} là {average_grade:.2f}."
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."


def show_all_students(data, sort_order):
    """Hiển thị thông tin tất cả sinh viên và sắp xếp theo điểm."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    try:
        sorted_data = data[data[:, 3].astype(float).argsort()]  # Sắp xếp theo cột điểm
        if sort_order == '2':  # Nếu chọn giảm dần, đảo ngược thứ tự
            sorted_data = sorted_data[::-1]

        return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Môn học: {row[2]}, Điểm: {row[3]}" for row in sorted_data])
    except ValueError:
        return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."


def find_high_low_averages(data):
    """Tìm sinh viên có điểm trung bình cao nhất và thấp nhất."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    try:
        unique_ids = np.unique(data[:, 0])
        averages = []

        for student_id in unique_ids:
            student_data = data[data[:, 0] == student_id]
            grades = student_data[:, 3].astype(float)
            average_grade = np.mean(grades)
            averages.append((student_id, student_data[0, 1], average_grade))

        # Tìm sinh viên có điểm trung bình cao nhất và thấp nhất
        highest = max(averages, key=lambda x: x[2])
        lowest = min(averages, key=lambda x: x[2])

        result = (
            f"Sinh viên có điểm trung bình cao nhất:\n"
            f"ID: {highest[0]}, Tên: {highest[1]}, Trung bình: {highest[2]:.2f}\n\n"
            f"Sinh viên có điểm trung bình thấp nhất:\n"
            f"ID: {lowest[0]}, Tên: {lowest[1]}, Trung bình: {lowest[2]:.2f}"
        )
        return result

    except ValueError:
        return "Có lỗi khi tính toán điểm trung bình. Vui lòng kiểm tra dữ liệu."


def find_students_by_grade(data, grade_type):
    """Tìm sinh viên theo loại điểm (giỏi, khá, trung bình)."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    try:
        unique_ids = np.unique(data[:, 0])
        results = []

        for student_id in unique_ids:
            student_data = data[data[:, 0] == student_id]
            grades = student_data[:, 3].astype(float)
            average_grade = np.mean(grades)

            if (grade_type == '1' and average_grade >= 8.0):  # Giỏi
                results.append((student_id, student_data[0, 1], average_grade))
            elif (grade_type == '2' and 6.5 <= average_grade < 8.0):  # Khá
                results.append((student_id, student_data[0, 1], average_grade))
            elif (grade_type == '3' and average_grade < 6.5):  # Trung bình
                results.append((student_id, student_data[0, 1], average_grade))

        if results:
            return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Trung bình: {row[2]:.2f}" for row in results])
        else:
            return "Không tìm thấy sinh viên nào đạt loại điểm này."
    except ValueError:
        return "Có lỗi khi tính toán điểm trung bình. Vui lòng kiểm tra dữ liệu."


def search_action():
    choice = choice_var.get()
    student_id = id_entry.get().strip()
    subject_name = subject_entry.get().strip()
    sort_order = sort_order_var.get()

    if choice == '1':  # Tìm kiếm thông tin sinh viên
        result = search_student(data, student_id)
    elif choice == '2':  # Tìm kiếm điểm môn học
        result = search_subject(data, subject_name, sort_order)
    elif choice == '3':  # Tính TBC điểm của sinh viên
        result = calculate_average(data, student_id)
    elif choice == '4':  # Hiển thị tất cả sinh viên
        result = show_all_students(data, sort_order)
    elif choice == '5':  # Tìm sinh viên có TBC cao nhất và thấp nhất
        result = find_high_low_averages(data)
    elif choice == '6':  # Tìm sinh viên đạt loại điểm
        grade_type = grade_choice_var.get()
        result = find_students_by_grade(data, grade_type)
    else:
        result = "Lựa chọn không hợp lệ."

    messagebox.showinfo("Kết quả", result)
    # Xóa các trường nhập sau khi tìm kiếm
    id_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)


def main():
    global data
    # Mở hộp thoại để chọn file CSV
    file_path = filedialog.askopenfilename(title="Chọn file CSV", filetypes=[("CSV files", "*.csv")])
    if file_path:  # Kiểm tra nếu có file được chọn
        data = load_data(file_path)
    else:
        print("Chưa chọn file nào.")
        return  # Dừng chương trình nếu không có file được chọn

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Tìm kiếm thông tin sinh viên")

    # Thêm các widget
    tk.Label(root, text="Chọn hành động:").grid(row=0, column=0, columnspan=2, pady=5)

    global choice_var
    choice_var = tk.StringVar(value='1')

    tk.Radiobutton(root, text="Tìm kiếm thông tin sinh viên", variable=choice_var, value='1').grid(row=1, column=0, sticky='w')
    tk.Radiobutton(root, text="Tìm kiếm điểm môn học", variable=choice_var, value='2').grid(row=2, column=0, sticky='w')
    tk.Radiobutton(root, text="Tính TBC điểm của sinh viên", variable=choice_var, value='3').grid(row=3, column=0, sticky='w')
    tk.Radiobutton(root, text="Hiển thị tất cả sinh viên", variable=choice_var, value='4').grid(row=4, column=0, sticky='w')
    tk.Radiobutton(root, text="Tìm sinh viên có TBC cao nhất/thấp nhất", variable=choice_var, value='5').grid(row=5, column=0, sticky='w')
    tk.Radiobutton(root, text="Tìm sinh viên theo loại điểm", variable=choice_var, value='6').grid(row=6, column=0, sticky='w')

    tk.Label(root, text="ID sinh viên (nếu có):").grid(row=7, column=0, pady=5, sticky='w')
    global id_entry
    id_entry = tk.Entry(root)
    id_entry.grid(row=7, column=1)

    tk.Label(root, text="Tên môn học (nếu có):").grid(row=8, column=0, pady=5, sticky='w')
    global subject_entry
    subject_entry = tk.Entry(root)
    subject_entry.grid(row=8, column=1)

    # Thêm phần lựa chọn loại điểm
    global grade_choice_var
    grade_choice_var = tk.StringVar(value='1')  # Mặc định là giỏi
    tk.Label(root, text="Chọn loại điểm:").grid(row=9, column=0, pady=5, sticky='w')
    tk.Radiobutton(root, text="Giỏi", variable=grade_choice_var, value='1').grid(row=10, column=0, sticky='w')
    tk.Radiobutton(root, text="Khá", variable=grade_choice_var, value='2').grid(row=10, column=1, sticky='w')
    tk.Radiobutton(root, text="Trung bình", variable=grade_choice_var, value='3').grid(row=10, column=2, sticky='w')

    # Thêm phần lựa chọn sắp xếp
    tk.Label(root, text="Sắp xếp điểm:").grid(row=11, column=0, pady=5, sticky='w')

    global sort_order_var
    sort_order_var = tk.StringVar(value='1')  # Mặc định là tăng dần
    tk.Radiobutton(root, text="Tăng dần", variable=sort_order_var, value='1').grid(row=12, column=0, sticky='w')
    tk.Radiobutton(root, text="Giảm dần", variable=sort_order_var, value='2').grid(row=12, column=1, sticky='w')

    tk.Button(root, text="Tìm kiếm", command=search_action).grid(row=13, column=0, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
