# Guideline — Traffic Light Annotation

**Version:** v1 — bản nháp đầu, viết trước khi pilot-test với người ngoài nhóm
**Chủ đề:** Traffic Light | **Hình học CVAT:** Rectangle (Track nếu là video/sequence)
**Nguồn dữ liệu tham chiếu:** DriveU Traffic Light Dataset (DTLD) — chỉ dùng cho nghiên cứu/giảng dạy, cấm thương mại, cấm chia sẻ ra ngoài lớp; mỗi người tự đăng ký tải theo quyền của mình. Nguồn thay thế nếu không có quyền DTLD: Bosch Small Traffic Lights, BDD100K (`trafficLightColor`), hoặc dashcam tự quay (đã làm mờ mặt người/biển số).

> **Không có rule ngầm.** File này là văn bản duy nhất nhóm chấm chéo sẽ nhận được. Một quyết định chỉ thống nhất bằng lời nói trong nhóm mà không viết vào đây thì coi như không tồn tại đối với người đọc ngoài nhóm.

---

## 1. Mục đích và phạm vi

Nhãn traffic light phục vụ module nhận diện đèn cho hệ thống hỗ trợ lái (ADAS)/ego-vehicle perception — output được driving policy tiêu thụ trực tiếp để quyết định dừng hay đi. Vì vậy annotation không chỉ trả lời "đèn màu gì" mà còn phải trả lời "đèn này có điều khiển xe của tôi không".

- **Trong phạm vi:** mọi đèn tín hiệu giao thông dành cho xe cơ giới, nhìn thấy được trong khung hình, ở bất kỳ hướng nào — kể cả đèn không áp dụng cho ego, miễn nhìn thấy được.
- **Ngoài phạm vi:** đèn người đi bộ/xe đạp, đèn hậu xe, phản chiếu trên kính/biển quảng cáo, đèn đếm ngược hiển thị số giây. Các đối tượng này **không tạo box** (xem mục 5).

## 2. Annotation unit

Đơn vị gán nhãn là **1 light head nhìn thấy được** (1 "mặt đèn" phát sáng) — không phải cả cột đèn hay cả cụm đèn. Một cột có nhiều head (ví dụ 1 đèn tròn + 1 đèn mũi tên) → vẽ **nhiều box**, mỗi box ứng với 1 head.

## 3. Geometry rule

Box bao sát viền ngoài của light head/lamp housing nhìn thấy được — không lấy cả cột (pole) hay giá đỡ (gantry). Ảnh tĩnh dùng Rectangle (Shape); video/sequence dùng Rectangle (Track) để giữ object identity qua các frame.

## 4. Taxonomy — class & attribute

Chỉ có **1 class**: `traffic_light`. Không tách state/relevance/direction thành class riêng vì đây là thuộc tính có thể đổi theo frame của cùng một object — tách thành class sẽ làm taxonomy nổ ra không cần thiết.

| Attribute | Giá trị hợp lệ | Mutable? |
|---|---|---|
| `state` | red / yellow / green / off / unknown | Có |
| `relevance` | relevant_to_ego / not_relevant / unknown_relevance | Có |
| `direction` | round / arrow_left / arrow_right / arrow_straight / unknown | Có (thường ít đổi hơn state) |

(Bảng ontology đầy đủ — kèm default value và rationale — sẽ chuyển sang `03_ontology_and_cvat_setup.md`, phải khớp chính xác với schema CVAT.)

## 5. Inclusion / exclusion

- **Không** tạo box cho: đèn người đi bộ/xe đạp, đèn hậu xe, phản chiếu trên kính/biển quảng cáo, đèn đếm ngược.
- **Có** tạo box cho: mọi đèn xe cơ giới nhìn thấy được, kể cả đèn không áp dụng cho ego (gán `relevance=not_relevant`, không phải bỏ qua).

## 6. Visibility / occlusion

Nếu đèn bị che một phần nhưng vẫn xác định được vị trí và ít nhất một phần màu sáng → vẽ box, gán state theo phần nhìn thấy. Nếu không xác định được màu do che khuất/quá xa/chói sáng → `state=unknown`, không đoán.

## 7. Ambiguity / escalation

Khi không đủ bằng chứng để quyết định state hoặc relevance, dùng `unknown` / `unknown_relevance` tương ứng — **không** được bỏ qua object (không box) và **không** được đoán. Ghi lý do vào decision log kèm ảnh minh hoạ.

## 8. Temporal rule

*(Áp dụng khi dùng video/Track)* Giữ cùng object identity qua các frame nếu vẫn là 1 đèn. Nếu state đổi, cập nhật attribute tại frame đó. Bản v1 này chưa có rule chi tiết về ngưỡng chuyển trạng thái bất thường hay ngưỡng che theo % — sẽ bổ sung ở v2 sau khi pilot.

## 9. Examples

| # | Tình huống | Quyết định |
|---|---|---|
| 1 | Đèn tròn đỏ, rõ ràng, đúng hướng ego | `state=red`, `relevance=relevant_to_ego` |
| 2 | Đèn mũi tên xanh rẽ trái, ego đang đi thẳng | `state=green`, `direction=arrow_left`, `relevance=not_relevant` |
| 3 | Đèn xa, không rõ màu | `state=unknown` |
| 4 | Đèn người đi bộ cạnh cột đèn xe | Không box |
| 5 | Đèn tắt hẳn, không sáng | `state=off` |

## 10. Common mistakes

- Đoán màu khi không chắc thay vì dùng `unknown`.
- Bỏ qua (không box) đèn không liên quan tới ego thay vì gán `not_relevant`.
- Vẽ 1 box cho cả cụm nhiều head thay vì tách riêng từng head.

---

**Lịch sử phiên bản**

| Version | Thời điểm | Ghi chú |
|---|---|---|
| v1 | Trước pilot | Bản nháp đầu — schema cơ bản, chưa có ngưỡng occlusion, chưa có cây quyết định relevance chi tiết |
