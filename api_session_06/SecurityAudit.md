Các điểm có thể bị lộ:
1. Lộ access token và refresh token: token có thể bị lộ qua log, URL, thông tin debug hoặc nơi lưu trữ phía client
2. Lộ thông tin về tài khoản qua `/auth/login`: nếu API trả về “username không tồn tại” và “password sai” bằng hai thông báo khác nhau, kẻ tấn công có thể dò tìm tài khoản đang tồn tại
3. Sử dụng lại refresh token bị đánh cắp: nếu refresh token bị đánh cắp và vẫn còn hiệu lực, kẻ tấn công có thể xin cấp access token mới để tiếp tục truy cập
4. Token được lưu trong trình duyệt có nguy cơ bị lộ qua XSS
5. Lộ dữ liệu qua lỗi API: response lỗi có thể chứa stack trace, câu truy vấn sql, đường dẫn hệ thống hoặc thông tin cấu hình nội bộ