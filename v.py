import json  #thư viện làm việc với định dạng JSON.
import tkinter as tk  # thư viện để tạo giao diện người dùng 
from tkinter import messagebox, simpledialog # messagebox và simpledialog được dùng để hiển thị thông báo và hộp thoại nhập dữ liệu

class Sach: #đại diện cho cuốn sách trong thư viện
    def __init__(self, ma_sach, tieu_de, tac_gia, nam_xuat_ban, so_luong_con_lai):  # khởi tạo một cuốn sách với các thuộc tính như mã sách, tiêu đề, tác giả, năm xuất bản và số lượng còn lại
        self.ma_sach = ma_sach 
        self.tieu_de = tieu_de
        self.tac_gia = tac_gia 
        self.nam_xuat_ban = nam_xuat_ban
        self.so_luong_con_lai = so_luong_con_lai 

    def to_dict(self):  # chuyển đổi đối tượng sách thành từ điển để lưu trữ dữ liệu dứng dạng json
        return self.__dict__

class Nguoi_dung: # đại diện cho người dùng trong thư viện
    def __init__(self, ten, email, so_dien_thoai): # khởi tạo người dùng với các thuộc tính như là tên, email và số điện thoại
        self.ten = ten 
        self.email = email
        self.so_dien_thoai = so_dien_thoai

    def to_dict(self):  # chuyển đổi đối tượng sách thành từ điển để lưu trữ dữ liệu dứng dạng json
        return self.__dict__

class Du_lieu_thu_vien: # định dạng quản quản lý dữ liệu sách và người dùng
    def __init__(self, tep_sach='books.json', tep_nguoi_dung='users.json'): # khởi tạo tệp json để lưu trữ dữ liệu sách và người dùng
        self.tep_sach = tep_sach
        self.tep_nguoi_dung = tep_nguoi_dung
        self.sach = self.load_data(tep_sach)
        self.nguoi_dung = self.load_data(tep_nguoi_dung)

    def tai_du_lieu(self, tep_tin): #tải dữ liệu từ tệp json, xử lý lỗi khi tệp không tồn tại hoặc lỗi định dạng JSON
        try:
            with open(tep_tin, 'r') as f:
                return json.tai(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Error decoding JSON from {tep_tin}")
            return []

    def luu_du_lieu(self, du_lieu, tep_tin): #lưu dữ liệu vào tệp json và xử lý lỗi trong quá trình lưu dữ liệu vào tệp json
        try:
            with open(tep_tin, 'w') as f:
                json.dump(du_lieu, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {e}")


    def them_sach(self, sach):# thêm một cuốn sách mới vào danh sách và lưu lại vào tệp json
        self.sach.append(sach.to_dict())
        self.luu_du_lieu(self.sach, self.tep_sach)

    def them_nguoi_dung(self, nguoi_dung): #thêm một người dùng mới vào danh sách và lưu lại vào tệp json
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
class LibraryApp: # tạo giao diện người dùng để tương tác với hệ thống thư viện
    def __init__(self, root): # khởi tạo cửa sổ chính và gọi phương thức để tạo các nút để giao diện với người dùng trong thư viện
        self.root = root
        self.root.title("Library Management System")
        self.data = Du_lieu_thu_vien()

        self.tao_chuc_nang() #tạo các chức năng và gắn các phương thức xử lý sự kiện

    def tao_chuc_nang(self): #tạo các chức năng và gắn các phương thức xử lý sự kiện
        tk.Button(self.root, text="Thêm Sách", command=self.them_sach).pack(pady=5)
        tk.Button(self.root, text="Hiển Thị Tất Cả Sách", command=self.hien_thi_tat_ca_sach).pack(pady=5)
        tk.Button(self.root, text="Tìm Kiếm Sách", command=self.tim_kiem_sach).pack(pady=5)
        tk.Button(self.root, text="Thêm Người Dùng", command=self.them_nguoi_dung).pack(pady=5)
        tk.Button(self.root, text="Hiển Thị Tất Cả Người Dùng", command=self.hien_thi_tat_ca_nguoi_dung).pack(pady=5)

    def them_sach(self): #lấy thông tin từ người dùng qua các hộp thoại, tạo đối tượng sách và thêm vào hệ thống
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

    def hien_thi_tat_ca_sach(self): #hiển thị tất cả sách trong hệ thống. Nếu không có sách nào, thông báo sẽ hiển thị "không có sách nào".
        sach = self.data.sach
        if sach:
            danh_sach_sach = "\n".join([f"{book.get('ma_sach', 'N/A')} - {book.get('tieu_de', 'N/A')} bởi {book.get('tac_gia', 'N/A')}, Năm: {book.get('nam_xuat_ban', 'N/A')}, Số lượng: {book.get('so_luong_con_lai', 'N/A')}" for book in sach])
            messagebox.showinfo("Tất Cả Sách", danh_sach_sach)
        else:
            messagebox.showinfo("Tất Cả Sách", "Không có sách nào")

    def tim_kiem_sach(self): #tìm kiếm sách theo mã sách, tiêu đề hoặc tác giả. Hiển thị kết quả tìm kiếm hoặc  thông báo nếu không tìm thấy sách
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

    def them_nguoi_dung(self): #lấy thông tin người dùng từ người dùng qua các hộp thoại, tạo đối tượng người dùng vào hệ thống thư viện
        ten = simpledialog.askstring("Nhập", "Nhập tên người dùng:")
        email = simpledialog.askstring("Nhập", "Nhập email người dùng:")
        so_dien_thoai = simpledialog.askstring("Nhập", "Nhập số điện thoại người dùng:")
        if ten and email and so_dien_thoai:
            nguoi_dung = Nguoi_dung(ten, email, so_dien_thoai)
            self.data.them_nguoi_dung(nguoi_dung)
            messagebox.showinfo("Thành Công", "Thêm người dùng thành công!")
        else:
            messagebox.showerror("Lỗi", "Tất cả các trường đều bắt buộc!")

    def hien_thi_tat_ca_nguoi_dung(self): # hiển thị tất cả người dùng trong hệ thống. Nếu không có người dùng nào, thông báo sẽ hiển thị "không có người dùng nào".
        nguoi_dung = self.data.nguoi_dung
        if nguoi_dung:
            danh_sach_nguoi_dung = "\n".join([f"{user.get('ten', 'Không có thông tin')} - {user.get('email', 'Không có thông tin')}, Số điện thoại: {user.get('so_dien_thoai', 'Không có thông tin')}" for user in nguoi_dung])
            messagebox.showinfo("Tất Cả Người Dùng", danh_sach_nguoi_dung)
        else:
            messagebox.showinfo("Tất Cả Người Dùng", "Không có người dùng nào")
    def tao_chuc_nang(self):
        # Các nút hiện tại của bạn
        
        # Thêm nút và các chức năng cho xóa sách và người dùng
        tk.Button(self.root, text="Xóa Sách", command=self.xoa_sach).pack(pady=5)
        tk.Button(self.root, text="Xóa Người Dùng", command=self.xoa_nguoi_dung).pack(pady=5)

    def xoa_sach(self):
        ma_sach = simpledialog.askstring("Nhập", "Nhập mã sách cần xóa:")
        if ma_sach:
            self.data.xoa_sach(ma_sach)

    def xoa_nguoi_dung(self):
        email = simpledialog.askstring("Nhập", "Nhập email người dùng cần xóa:")
        if email:
            self.data.xoa_nguoi_dung(email)

if __name__ == "__main__": #khởi chạy hệ thống quản lý  
    root = tk.Tk()
    app = LibraryApp(root) # tạo đối tương 'tk' và khởi chạy hệ thống 'LibraryApp' và 'mainloop' giữ cho cửa số tkinter hiển thị và đợi các thao tác từ người dùng.
    root.mainloop()
