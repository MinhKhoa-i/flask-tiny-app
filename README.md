Vương Nguyễn Minh Khoa - 22681791 <br>
Võ Anh Kiệt - 22001245


# RELEASE NOTES - flask-tiny-app

## Mô tả Project
**flask-tiny-app** là một ứng dụng web đơn giản được xây dựng bằng Flask, cho phép người dùng quản lý danh sách công việc (To-Do List). Ứng dụng hỗ trợ đăng ký, đăng nhập, quản lý bài viết/nhiệm vụ, và có trang quản trị để quản lý người dùng. Các tính năng chính bao gồm:
- Đăng ký/đăng nhập với xác thực bảo mật.
- Người dùng có thể thêm, sửa, xóa các bài viết/nhiệm vụ của mình.
- Hỗ trợ xóa nhiều bài viết/nhiệm vụ cùng lúc.
- Quản trị viên có thể khóa hoặc đặt lại mật khẩu của người dùng.
- Phân trang danh sách bài viết/nhiệm vụ.
- Đóng gói và triển khai với Docker.

## Hướng dẫn cài đặt và chạy
### Cách 1: Chạy ứng dụng trên môi trường local
1. **Clone repo** về máy:
   ```sh
   git clone https://github.com/MinhKhoa-i/flask-tiny-app.git
   cd flask-tiny-app
   ```
2. **Tạo môi trường ảo và cài đặt thư viện**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Trên macOS/Linux
   venv\Scripts\activate  # Trên Windows
   pip install -r requirements.txt
   ```
3. **Chạy ứng dụng**:
   ```sh
   flask run
   ```
4. **Mở trình duyệt và truy cập**:
   ```
   http://127.0.0.1:5000
   ```

### Cách 2: Chạy ứng dụng bằng Docker
1. **Cài đặt Docker (nếu chưa có)**
2. **Build Docker Image**:
   ```sh
   docker build -t tiny-app .
   ```
3. **Chạy ứng dụng**:
   ```sh
   docker run -p 5000:5000 tiny-app
   ```
4. **Mở trình duyệt và truy cập**:
   ```
   http://localhost:5000
   ```

## Version 1.0.0 (Initial Release)
- Đẩy mã nguồn ban đầu của ứng dụng Flask lên GitHub.
- Ứng dụng hỗ trợ tạo và quản lý danh sách To-Do.
- Cấu trúc thư mục gọn gàng, dễ mở rộng.
- File README.md cung cấp hướng dẫn cài đặt và chạy ứng dụng.

## Version 2.0.0 (User Authentication)
- Thêm chức năng đăng nhập/đăng ký tài khoản.
- Bảo mật mật khẩu bằng **bcrypt**.
- Xác thực phiên đăng nhập bằng **Flask-Login**.
- Hiển thị thông báo lỗi nếu đăng nhập thất bại.

## Version 3.0.0 (Admin Panel)
- Thêm trang quản trị để quản lý người dùng.
- Admin có thể **block** user, khiến họ không thể đăng nhập.
- Admin có thể reset mật khẩu cho user.
- Nếu tài khoản bị khóa, hiển thị thông báo "Tài khoản của bạn đã bị khóa".

## Version 4.0.0 (Post/Task Management)
- Cho phép user quản lý bài viết (posts) hoặc nhiệm vụ (tasks).
- Thêm chức năng **xoá nhiều bài viết/nhiệm vụ cùng lúc**.
- Giao diện hỗ trợ checkbox chọn nhiều bài viết/nhiệm vụ để xoá.

## Version 5.0.0 (Pagination)
- Thêm dữ liệu giả lập để kiểm thử chức năng phân trang.
- Hiển thị tối đa **10 posts/tasks** trên mỗi trang.
- Thêm điều hướng giữa các trang (Next/Previous Page).

## Version 6.0.0 (Installation Script)
- Viết **bash script** để cài đặt toàn bộ project.
- Script tự động thiết lập môi trường ảo, cài đặt thư viện, và khởi động ứng dụng.
- Hướng dẫn chạy script trong README.md.

## Version 7.0.0 (Dockerization)
- Đóng gói ứng dụng vào Docker container.
- Viết **Dockerfile** để chạy Flask app.
- Tạo **docker-compose.yml** để quản lý môi trường và database.
- Hướng dẫn sử dụng Docker để deploy ứng dụng.

---


