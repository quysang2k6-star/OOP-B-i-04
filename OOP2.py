"""
/***************************************************
 * Mã sinh viên: 202418977
 * Họ tên:       Đào Quý Sang
 * Ngôn ngữ:     Python 3.x
 ***************************************************/
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# ==============================================================================
# A.1 & A.2 LỚP CƠ SỞ EMPLOYEE 
# ==============================================================================
class Employee(ABC):
    """Lớp cơ sở trừu tượng đại diện cho nhân sự chung."""

    # A.4 Nạp chồng Constructor qua tham số mặc định
    def __init__(self, employee_id: str, full_name: str, department: str = "Unassigned"):
        # A.2 Quy tắc bất biến
        if not employee_id or not employee_id.strip():
            raise ValueError("Lỗi: Mã nhân sự không được rỗng!")
        if not full_name or not full_name.strip():
            raise ValueError("Lỗi: Họ tên không được rỗng!")
        if not department or not department.strip():
            raise ValueError("Lỗi: Phòng ban không được rỗng!")

        self._employee_id: str = employee_id.strip()
        self._full_name: str = full_name.strip()
        self._department: str = department.strip()
        self._monthly_bonus: float = 0.0

    # Getters & Setters
    def get_employee_id(self) -> str:
        return self._employee_id

    def get_full_name(self) -> str:
        return self._full_name

    def get_department(self) -> str:
        return self._department

    def get_monthly_bonus(self) -> float:
        return self._monthly_bonus

    def reset_bonus(self) -> None:
        """Đặt lại thưởng về 0 khi bắt đầu kỳ lương mới (B.1)."""
        self._monthly_bonus = 0.0

    # A.5 Nạp chồng phương thức add_bonus
    def add_bonus(self, arg1: float, arg2: Optional[object] = None, reason: Optional[str] = None) -> None:
        # Phiên bản 3: addBonus(rate, referenceAmount, reason)
        if isinstance(arg1, (int, float)) and isinstance(arg2, (int, float)) and isinstance(reason, str):
            rate = float(arg1)
            ref_amount = float(arg2)
            if not (0 < rate <= 0.5):
                raise ValueError("Lỗi: Tỷ lệ thưởng phải lớn hơn 0 và không quá 0.5!")
            if ref_amount <= 0:
                raise ValueError("Lỗi: Giá trị tham chiếu phải lớn hơn 0!")
            if not reason.strip():
                raise ValueError("Lỗi: Nội dung lý do thưởng không được rỗng!")
            self._monthly_bonus += rate * ref_amount

        # Phiên bản 2: addBonus(amount, reason)
        elif isinstance(arg1, (int, float)) and isinstance(arg2, str):
            amount = float(arg1)
            reason_str = arg2
            if amount <= 0:
                raise ValueError("Lỗi: Tiền thưởng phải lớn hơn 0!")
            if not reason_str.strip():
                raise ValueError("Lỗi: Nội dung lý do thưởng không được rỗng!")
            self._monthly_bonus += amount

        # Phiên bản 1: addBonus(amount)
        elif isinstance(arg1, (int, float)) and arg2 is None and reason is None:
            amount = float(arg1)
            if amount <= 0:
                raise ValueError("Lỗi: Tiền thưởng phải lớn hơn 0!")
            self._monthly_bonus += amount

        else:
            raise TypeError("Lỗi: Tham số addBonus() không đúng quy cách!")

    @abstractmethod
    def calculate_gross_pay(self) -> float:
        """Phương thức tính thu nhập trước khấu trừ."""
        pass

    @abstractmethod
    def get_employee_type(self) -> str:
        """Phương thức lấy tên loại nhân viên."""
        pass

    def display_payroll_info(self) -> None:
        """Hiển thị thông tin lương tổng quan."""
        print(f"[{self.get_employee_type()}] Mã: {self._employee_id} | Tên: {self._full_name} "
              f"| Phòng: {self._department} | Thưởng: {self._monthly_bonus:,.0f} VND "
              f"| Thu nhập: {self.calculate_gross_pay():,.0f} VND")


# ==============================================================================
# A.3 & B.2 LỚP DẪN XUẤT: SALARIED EMPLOYEE
# ==============================================================================
class SalariedEmployee(Employee):
    def __init__(self, employee_id: str, full_name: str, 
                 department: str = "Unassigned", 
                 monthly_salary: float = 0.0, 
                 responsibility_allowance: float = 0.0):
        super().__init__(employee_id, full_name, department)
        if monthly_salary < 0:
            raise ValueError("Lỗi: Lương cố định tháng không được âm!")
        if responsibility_allowance < 0:
            raise ValueError("Lỗi: Phụ cấp trách nhiệm không được âm!")

        self._monthly_salary: float = monthly_salary
        self._responsibility_allowance: float = responsibility_allowance

    def calculate_gross_pay(self) -> float:
        return self._monthly_salary + self._responsibility_allowance + self._monthly_bonus

    def get_employee_type(self) -> str:
        return "Salaried Employee"

    def display_payroll_info(self) -> None:
        print(f"[{self.get_employee_type()}] Mã: {self._employee_id} | Tên: {self._full_name} | Phòng: {self._department}")
        print(f"   -> Lương cố định: {self._monthly_salary:,.0f} | Phụ cấp: {self._responsibility_allowance:,.0f} "
              f"| Thưởng: {self._monthly_bonus:,.0f} => Gross Pay: {self.calculate_gross_pay():,.0f} VND")


# ==============================================================================
# A.3 & B.3 LỚP DẪN XUẤT: HOURLY EMPLOYEE
# ==============================================================================
class HourlyEmployee(Employee):
    def __init__(self, employee_id: str, full_name: str, 
                 department: str = "Unassigned", 
                 hourly_rate: float = 0.0, 
                 worked_hours: float = 0.0):
        super().__init__(employee_id, full_name, department)
        if hourly_rate < 0:
            raise ValueError("Lỗi: Đơn giá giờ không được âm!")
        if not (0 <= worked_hours <= 250):
            raise ValueError("Lỗi: Số giờ làm việc hợp lệ từ 0 đến 250 giờ!")

        self._hourly_rate: float = hourly_rate
        self._worked_hours: float = worked_hours

    def calculate_gross_pay(self) -> float:
        if self._worked_hours <= 160:
            base_pay = self._worked_hours * self._hourly_rate
        else:
            base_pay = (160 * self._hourly_rate) + ((self._worked_hours - 160) * self._hourly_rate * 1.5)
        return base_pay + self._monthly_bonus

    def get_employee_type(self) -> str:
        return "Hourly Employee"

    def display_payroll_info(self) -> None:
        print(f"[{self.get_employee_type()}] Mã: {self._employee_id} | Tên: {self._full_name} | Phòng: {self._department}")
        print(f"   -> Đơn giá/giờ: {self._hourly_rate:,.0f} | Số giờ làm: {self._worked_hours}h "
              f"| Thưởng: {self._monthly_bonus:,.0f} => Gross Pay: {self.calculate_gross_pay():,.0f} VND")


# ==============================================================================
# A.3 & B.4 LỚP DẪN XUẤT: SALES EMPLOYEE
# ==============================================================================
class SalesEmployee(Employee):
    def __init__(self, employee_id: str, full_name: str, 
                 department: str = "Unassigned", 
                 base_salary: float = 0.0, 
                 sales_revenue: float = 0.0, 
                 commission_rate: float = 0.0):
        super().__init__(employee_id, full_name, department)
        if base_salary < 0:
            raise ValueError("Lỗi: Lương cơ bản không được âm!")
        if sales_revenue < 0:
            raise ValueError("Lỗi: Doanh số kinh doanh không được âm!")
        if not (0 <= commission_rate <= 0.3):
            raise ValueError("Lỗi: Tỷ lệ hoa hồng nằm trong khoảng từ 0 đến 0.3!")

        self._base_salary: float = base_salary
        self._sales_revenue: float = sales_revenue
        self._commission_rate: float = commission_rate

    def set_sales_revenue(self, sales_revenue: float) -> None:
        if sales_revenue < 0:
            raise ValueError("Lỗi: Doanh số kinh doanh không được âm!")
        self._sales_revenue = sales_revenue

    def calculate_gross_pay(self) -> float:
        return self._base_salary + (self._sales_revenue * self._commission_rate) + self._monthly_bonus

    def get_employee_type(self) -> str:
        return "Sales Employee"

    def display_payroll_info(self) -> None:
        print(f"[{self.get_employee_type()}] Mã: {self._employee_id} | Tên: {self._full_name} | Phòng: {self._department}")
        print(f"   -> Lương CB: {self._base_salary:,.0f} | Doanh số: {self._sales_revenue:,.0f} "
              f"| Tỷ lệ HH: {self._commission_rate * 100}% | Thưởng: {self._monthly_bonus:,.0f} "
              f"=> Gross Pay: {self.calculate_gross_pay():,.0f} VND")


# ==============================================================================
# A.7 & B.5 LỚP PAYROLL (QUẢN LÝ BẢNG LƯƠNG)
# ==============================================================================
class Payroll:
    def __init__(self, period: str):
        self._period: str = period
        self._employees: List[Employee] = []

    def add_employee(self, employee: Employee) -> bool:
        if self.find_employee(employee.get_employee_id()) is not None:
            print(f"  [LỖI]: Nhân viên mã '{employee.get_employee_id()}' đã tồn tại!")
            return False
        self._employees.append(employee)
        return True

    def find_employee(self, employee_id: str) -> Optional[Employee]:
        for emp in self._employees:
            if emp.get_employee_id() == employee_id:
                return emp
        return None

    def calculate_total_payroll(self) -> float:
        return sum(emp.calculate_gross_pay() for emp in self._employees)

    def calculate_payroll_by_department(self, department: str) -> float:
        return sum(emp.calculate_gross_pay() for emp in self._employees 
                   if emp.get_department().lower() == department.lower())

    def find_highest_paid_employee(self) -> Optional[Employee]:
        if not self._employees:
            return None
        return max(self._employees, key=lambda emp: emp.calculate_gross_pay())

    def display_payroll(self) -> None:
        print(f"\n================ BẢNG LƯƠNG KỲ: {self._period} ================")
        if not self._employees:
            print("Danh sách nhân sự rỗng!")
            return
        for emp in self._employees:
            emp.display_payroll_info()
        print("-" * 65)
        print(f" TỔNG CHI TRẢ LƯƠNG TOÀN CÔNG TY: {self.calculate_total_payroll():,.0f} VND")
        print("=================================================================\n")


# ==============================================================================
# 10 HÀM KIỂM THỬ (TEST CASES C.1)
# ==============================================================================
def create_sample_payroll() -> Payroll:
    """Hàm phụ trợ: Tạo bảng lương mẫu chuẩn theo đề bài (Phần C)."""
    payroll = Payroll("2026-09")
    e1 = SalariedEmployee("E001", "Nguyễn Minh An", "Đào tạo", 15000000, 2000000)
    e1.add_bonus(1000000)

    e2 = HourlyEmployee("E002", "Trần Thu Bình", "Hỗ trợ", 100000, 150)
    e2.add_bonus(500000)

    e3 = HourlyEmployee("E003", "Lê Hoàng Chi", "Hỗ trợ", 100000, 170)

    e4 = SalesEmployee("E004", "Phạm Quốc Dũng", "Kinh doanh", 8000000, 200000000, 0.05)
    e4.add_bonus(0.02, 50000000, "Thưởng 2% của 50tr")

    payroll.add_employee(e1)
    payroll.add_employee(e2)
    payroll.add_employee(e3)
    payroll.add_employee(e4)
    return payroll


def test_01_duplicate_employee():
    print("\n--- [TEST 1]: Kiểm thử thêm trùng mã nhân viên ---")
    payroll = create_sample_payroll()
    e_dup = SalariedEmployee("E001", "Nguyễn Văn Trùng", "Đào tạo", 10000000, 0)
    payroll.add_employee(e_dup)


def test_02_empty_id_or_name():
    print("\n--- [TEST 2]: Kiểm thử khởi tạo mã hoặc tên rỗng ---")
    try:
        SalariedEmployee("", "Trần Văn A", "Đào tạo", 5000000, 0)
    except ValueError as ex:
        print(f"  -> [BẮT NGOẠI LỆ]: {ex}")


def test_03_negative_bonus():
    print("\n--- [TEST 3]: Kiểm thử thưởng số tiền âm ---")
    e = SalariedEmployee("E010", "Nguyễn Văn B", "Đào tạo", 10000000, 0)
    try:
        e.add_bonus(-500000)
    except ValueError as ex:
        print(f"  -> [BẮT NGOẠI LỆ]: {ex}")


def test_04_invalid_bonus_rate():
    print("\n--- [TEST 4]: Kiểm thử tỷ lệ thưởng > 0.5 ---")
    e = SalariedEmployee("E010", "Nguyễn Văn B", "Đào tạo", 10000000, 0)
    try:
        e.add_bonus(0.6, 10000000, "Thưởng sai quy định")
    except ValueError as ex:
        print(f"  -> [BẮT NGOẠI LỆ]: {ex}")


def test_05_worked_hours_exceed():
    print("\n--- [TEST 5]: Kiểm thử số giờ làm > 250h ---")
    try:
        HourlyEmployee("E011", "Lê Văn Giờ", "Hỗ trợ", 100000, 260)
    except ValueError as ex:
        print(f"  -> [BẮT NGOẠI LỆ]: {ex}")


def test_06_invalid_commission_rate():
    print("\n--- [TEST 6]: Kiểm thử tỷ lệ hoa hồng > 0.3 ---")
    try:
        SalesEmployee("E012", "Vũ Hoa Hồng", "Kinh doanh", 5000000, 100000000, 0.35)
    except ValueError as ex:
        print(f"  -> [BẮT NGOẠI LỆ]: {ex}")


def test_07_empty_bonus_reason():
    print("\n--- [TEST 7]: Kiểm thử thưởng kèm lý do rỗng ---")
    e = SalariedEmployee("E010", "Nguyễn Văn B", "Đào tạo", 10000000, 0)
    try:
        e.add_bonus(500000, "")
    except ValueError as ex:
        print(f"  -> [BẮT NGOẠI LỆ]: {ex}")


def test_08_search_non_existing_employee():
    print("\n--- [TEST 8]: Kiểm thử tìm kiếm nhân viên không tồn tại ---")
    payroll = create_sample_payroll()
    result = payroll.find_employee("E999")
    print(f"  -> Kết quả tìm kiếm mã 'E999': {result}")


def test_09_department_not_found():
    print("\n--- [TEST 9]: Tính tổng lương phòng ban không tồn tại ('Marketing') ---")
    payroll = create_sample_payroll()
    total = payroll.calculate_payroll_by_department("Marketing")
    print(f"  -> Tổng lương phòng 'Marketing': {total:,.0f} VND")


def test_10_highest_paid_empty_payroll():
    print("\n--- [TEST 10]: Tìm người lương cao nhất khi bảng lương rỗng ---")
    empty_payroll = Payroll("2026-10")
    result = empty_payroll.find_highest_paid_employee()
    print(f"  -> Kết quả tìm kiếm trên bảng lương rỗng: {result}")


# ==============================================================================
# HÀM MAIN: BẬT / TẮT CHẠY TỪNG TÌNH HUỐNG KIỂM THỬ
# ==============================================================================
def main():
    # 1. Chạy chương trình chuẩn theo đề bài (Phần C)
    payroll = create_sample_payroll()
    payroll.display_payroll()

    print("=================================================================")
    print("             CHẠY CÁC TÌNH HUỐNG KIỂM THỬ ĐỘC LẬP                ")
    print("=================================================================")

    # BẬT / TẮT BẰNG CÁCH THÊM HOẶC XÓA DẤU # Ở ĐẦU DÒNG DƯỚI ĐÂY:
    # test_01_duplicate_employee()
    #test_02_empty_id_or_name()
    # test_03_negative_bonus()
    # test_04_invalid_bonus_rate()
    # test_05_worked_hours_exceed()
    #test_06_invalid_commission_rate()
    # test_07_empty_bonus_reason()
    # test_08_search_non_existing_employee()
    # test_09_department_not_found()
    test_10_highest_paid_empty_payroll()


if __name__ == "__main__":
    main()