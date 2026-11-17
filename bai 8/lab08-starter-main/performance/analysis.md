# Lab 4 — Phân tích kết quả

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
|---|---:|---:|---:|---:|---:|---:|
| A | 10 | 2 | 30s |26 |0% | 4.91|
| B | 50 | 5 | 60s | 35|0.15% |23.31 |
| C | 200 | 50 | 30s |1100 | 0.08%| 87.37|

1. Kịch bản có p95 cao nhất là gì? Dùng số liệu quan sát để giải thích.
kịch bản C có p95=1100ms là cao nhất. Điều này có thể liên quan đến giới hạn tài nguyên của máy  SQLite

2. Endpoint nào tăng failure rate? Phân biệt lỗi HTTP thực và lỗi đánh dấu trong Locust.
GET /books?year={year} là endpoint duy nhất ghi nhận failure: A = 0/16, B = 2/220 (0.91%), C = 2/352 (0.57%). Hai failure ở B và C là client-side simulated failure do Locust gọi response.failure() sau khi response có HTTP 200, không phải HTTP 500 do server phát ra. Tỷ lệ không tăng đều từ B lên C vì failure được tạo ngẫu nhiên.

3. Với SLO giả định p95 < 300 ms, kịch bản nào đạt? Nêu giới hạn của phép đo.
Kịch bản A và B đạt SLO. Phép đo có thể chịu ảnh hưởng tìa nguyên của máy, dữ liệu và tính ngẫu nhiên của workload

4. Nếu connection pool bị giới hạn ở 5, bạn sẽ kiểm chứng ảnh hưởng như thế nào?
Cấu hình pool tối đa 5 kết nối (và tắt overflow nếu thư viện hỗ trợ), sau đó chạy lại A, B, C với cùng cấu hình tải. So sánh p95, RPS, failure/timeout và thời gian chờ lấy connection với baseline; đồng thời theo dõi số connection đang dùng và thời gian chờ trong pool. Nếu tải vượt khả năng phục vụ của 5 kết nối, có thể thấy thời gian chờ và p95 tăng, RPS giảm hoặc xuất hiện timeout.

> Không điền số liệu giả định vào bảng. Không khẳng định hiệu năng production
> từ SQLite + Flask development server trên máy cá nhân.
