import json # thư viện làm việc với định dạng json
import tkinter as tk # thư viện để tao giao diện người dùng
from tkinter import messagebox, simpledialog #messagebox và simpledialog de hien thi thong bao

class Sach: 
    def __init__(self, ma_sach, tieu_de, tac_gia, nam_xuat_ban, so_luong_con_lai):
        self.ma_sach = ma_sach
        self.tieu_de = tieu_de
        self.tac_gia = tac_gia
        self.nam_xuat_ban = nam_xuat_ban
        self.so_luong_con_lai = so_luong_con_lai

    def to_dict(self):
        return self.__dict__

class Nguoi_dung:
    def __init__(self, ten, email, so_dien_thoai):
        self.ten = ten
        self.email = email
        self.so_dien_thoai = so_dien_thoai

    def to_dict(self):
        return self.__dict__

class Du_lieu_thu_vien:
    def __init__(self, tep_sach='books.json', tep_nguoi_dung='users.json'):
        self.tep_sach = tep_sach
        self.tep_nguoi_dung = tep_nguoi_dung
        self.sach = self.load_data(tep_sach)
        self.nguoi_dung = self.load_data(tep_nguoi_dung)

    def load_data(self, tep_tin):
        try:
            with open(tep_tin, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Error decoding JSON from {tep_tin}")
            return []

    def luu_du_lieu(self, du_lieu, tep_tin):
        try:
            with open(tep_tin, 'w') as f:
                json.dump(du_lieu, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {e}")

    def them_sach(self, sach):
        self.sach.append(sach.to_dict())
        self.luu_du_lieu(self.sach, self.tep_sach)

    def them_nguoi_dung(self, nguoi_dung):
        self.nguoi_dung.append(nguoi_dung.to_dict())
        self.luu_du_lieu(self.nguoi_dung, self.tep_nguoi_dung)

    def xoa_sach(self, ma_sach):
        sach_can_xoa = None
        for sach in self.sach:
            if sach.get('ma_sach') == ma_sach:
                sach_can_xoa = sach
                break
        if sach_can_xoa:
            self.sach.remove(sach_can_xoa)
            self.luu_du_lieu(self.sach, self.tep_sach)
            messagebox.showinfo("Thành Công", f"Đã xóa sách có mã {ma_sach}")
        else:
            messagebox.showerror("Lỗi", f"Không tìm thấy sách có mã {ma_sach}")

    def xoa_nguoi_dung(self, email):
        nguoi_dung_can_xoa = None
        for nguoi_dung in self.nguoi_dung:
            if nguoi_dung.get('email') == email:
                nguoi_dung_can_xoa = nguoi_dung
                break
        if nguoi_dung_can_xoa:
            self.nguoi_dung.remove(nguoi_dung_can_xoa)
            self.luu_du_lieu(self.nguoi_dung, self.tep_nguoi_dung)
            messagebox.showinfo("Thành Công", f"Đã xóa người dùng có email {email}")
        else:
            messagebox.showerror("Lỗi", f"Không tìm thấy người dùng có email {email}")

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.data = Du_lieu_thu_vien()

        self.tao_chuc_nang()

    def tao_chuc_nang(self):
        tk.Button(self.root, text="Thêm Sách", command=self.them_sach).pack(pady=5)
        tk.Button(self.root, text="Hiển Thị Tất Cả Sách", command=self.hien_thi_tat_ca_sach).pack(pady=5)
        tk.Button(self.root, text="Tìm Kiếm Sách", command=self.tim_kiem_sach).pack(pady=5)
        tk.Button(self.root, text="Thêm Người Dùng", command=self.them_nguoi_dung).pack(pady=5)
        tk.Button(self.root, text="Hiển Thị Tất Cả Người Dùng", command=self.hien_thi_tat_ca_nguoi_dung).pack(pady=5)
        tk.Button(self.root, text="Xóa Sách", command=self.xoa_sach).pack(pady=5)  # Thêm nút xóa sách
        tk.Button(self.root, text="Xóa Người Dùng", command=self.xoa_nguoi_dung).pack(pady=5)  # Thêm nút xóa người dùng

    def them_sach(self):
        ma_sach = simpledialog.askstring("Nhập", "Nhập mã sách:")
        tieu_de = simpledialog.askstring("Nhập", "Nhập tiêu đề sách:")
        tac_gia = simpledialog.askstring("Nhập", "Nhập tác giả sách:")
        nam_xuat_ban = simpledialog.askinteger("Nhập", "Nhập năm xuất bản sách:")
        so_luong_con_lai = simpledialog.askinteger("Nhập", "Nhập số lượng còn lại của sách:")
        if ma_sach and tieu_de and tac_gia and nam_xuat_ban and so_luong_con_lai:
            sach = Sach(ma_sach, tieu_de, tac_gia, nam_xuat_ban, so_luong_con_lai)
            self.data.them_sach(sach)
            messagebox.showinfo("Thành Công", "Thêm sách thành công!")
        else:
            messagebox.showerror("Lỗi", "Tất cả các trường đều bắt buộc!")

    def hien_thi_tat_ca_sach(self):
        sach = self.data.sach
        if sach:
            danh_sach_sach = "\n".join([f"{book.get('ma_sach', 'N/A')} - {book.get('tieu_de', 'N/A')} bởi {book.get('tac_gia', 'N/A')}, Năm: {book.get('nam_xuat_ban', 'N/A')}, Số lượng: {book.get('so_luong_con_lai', 'N/A')}" for book in sach])
            messagebox.showinfo("Tất Cả Sách", danh_sach_sach)
        else:
            messagebox.showinfo("Tất Cả Sách", "Không có sách nào")

    def tim_kiem_sach(self):
        tu_khoa_tim_kiem = simpledialog.askstring("Nhập", "Nhập mã sách, tiêu đề hoặc tác giả để tìm kiếm:")
        if tu_khoa_tim_kiem:
            sach = self.data.sach
            ket_qua = [book for book in sach if tu_khoa_tim_kiem.lower() in book.get('tieu_de', '').lower() or tu_khoa_tim_kiem.lower() in book.get('tac_gia', '').lower() or tu_khoa_tim_kiem.lower() in book.get('ma_sach', '').lower()]
            if ket_qua:
                danh_sach_ket_qua = "\n".join([f"{book.get('ma_sach', 'N/A')} - {book.get('tieu_de', 'N/A')} bởi {book.get('tac_gia', 'N/A')}, Năm: {book.get('nam_xuat_ban', 'N/A')}, Số lượng: {book.get('so_luong_con_lai', 'N/A')}" for book in ket_qua])
                messagebox.showinfo("Kết Quả Tìm Kiếm", danh_sach_ket_qua)
            else:
                messagebox.showinfo("Kết Quả Tìm Kiếm", "Không tìm thấy sách nào")
        else:
            messagebox.showerror("Lỗi", "Cần nhập từ khóa tìm kiếm")

    def them_nguoi_dung(self):
        ten = simpledialog.askstring("Nhập", "Nhập tên người dùng:")
        email = simpledialog.askstring("Nhập", "Nhập email người dùng:")
        so_dien_thoai = simpledialog.askstring("Nhập", "Nhập số điện thoại người dùng:")
        if ten and email and so_dien_thoai:
            nguoi_dung = Nguoi_dung(ten, email, so_dien_thoai)
            self.data.them_nguoi_dung(nguoi_dung)
            messagebox.showinfo("Thành Công", "Thêm người dùng thành công!")
        else:
            messagebox.showerror("Lỗi", "Tất cả các trường đều bắt buộc!")

    def hien_thi_tat_ca_nguoi_dung(self):
        nguoi_dung = self.data.nguoi_dung
        if nguoi_dung:
            danh_sach_nguoi_dung = "\n".join([f"{user.get('ten', 'Không có thông tin')} - {user.get('email', 'Không có thông tin')}, Số điện thoại: {user.get('so_dien_thoai', 'Không có thông tin')}" for user in nguoi_dung])
            messagebox.showinfo("Tất Cả Người Dùng", danh_sach_nguoi_dung)
        else:
            messagebox.showinfo("Tất Cả Người Dùng", "Không có người dùng nào")

    def xoa_sach(self):
        ma_sach = simpledialog.askstring("Nhập", "Nhập mã sách cần xóa:")
        if ma_sach:
            self.data.xoa_sach(ma_sach)

    def xoa_nguoi_dung(self):
        email = simpledialog.askstring("Nhập", "Nhập email người dùng cần xóa:")
        if email:
            self.data.xoa_nguoi_dung(email)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
