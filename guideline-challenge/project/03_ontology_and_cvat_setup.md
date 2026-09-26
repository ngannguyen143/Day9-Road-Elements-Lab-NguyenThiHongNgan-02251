# Ontology + CVAT setup

Bảng ontology là **source of truth** cho schema CVAT: `03_cvat_labels.json` phải khớp từng dòng ở đây. Thay mọi
placeholder mới là xong (gate G2).

## Ontology table

| Name | Geometry | Type (class / attribute) | Allowed values | Default | Mutable? | Rationale |
|---|---|---|---|---|---|---|
| `traffic_light` | Rectangle | Class | — | — | — | Duy nhất 1 class, tránh nổ taxonomy theo tổ hợp màu × hướng × mức liên quan |
| `state` | — | Attribute | red / yellow / green / off / unknown | unknown | Có | Đổi theo frame; downstream cần biết đèn đang "nói" gì |
| `relevance` | — | Attribute | relevant_to_ego / not_relevant / unknown_relevance | unknown_relevance | Có | Quyết định critical nhất — đèn có điều khiển ego không |
| `direction` | — | Attribute | round / arrow_left / arrow_right / arrow_straight / unknown | unknown | Ít đổi hơn state | Hình dạng lens quyết định ego được rẽ/đi thẳng theo tín hiệu nào |
| `occluded` | — | Attribute | none / partial / heavy | none | Có | Cờ mức độ che, phục vụ QC & ngưỡng escalate |
| `evidence` | — | Attribute (text ngắn) | tự do | "" | Có | Bắt buộc điền khi `state`/`relevance` = unknown, để reviewer hiểu vì sao |

## Class hay attribute

Chỉ có 1 class (`traffic_light`) vì mọi light head trong scope là cùng một loại object downstream cần phát hiện —
tách theo màu/hướng/mức liên quan thành class riêng sẽ nổ ra hàng chục tổ hợp không cần thiết. `state`, `relevance`,
`direction`, `occluded`, `evidence` là attribute vì cùng một object (cùng box, cùng track) có thể đổi giá trị các
thuộc tính này theo frame hoặc góc nhìn, và không có geometry/QA rule riêng khác với `traffic_light`.

Default có thể gây bias:

- `state`/`relevance`/`direction` = `unknown`/`unknown_relevance`: an toàn (không đoán), nhưng nếu annotator lười
  sẽ để nguyên default thay vì thực sự quan sát → QA phải kiểm tỉ lệ `unknown` bất thường cao ở một annotator.
- `occluded` = `none`: default lạc quan — nếu annotator quên đổi, ảnh có che nhẹ sẽ bị ghi nhận thành "không che",
  làm sai lệch số liệu occlusion downstream dùng để đánh giá độ khó.

## CVAT

- **Phiên bản CVAT:** 2.75.1 (theo xác nhận của thành viên đã setup; `make cvat-status` báo CVAT hiện không
  chạy tại thời điểm viết file này — chạy `docker compose start` trong thư mục CVAT rồi `make cvat-status` lại
  trước khi nộp để double-check số phiên bản khớp).
- **Tên task calibration** (có version guideline, ví dụ `team07-calib-v1`): TODO — cần tên team ở `00_team.md`
  (đang TODO) trước khi đặt tên task, ví dụ `<team>-calib-v2` (giữ đúng version guideline hiện tại là v2).
- **Guide của task đã dán `02_guideline.md`?** Chưa — task đã tạo (CVAT 2.75.1, Shape) nhưng chưa dán. Cần vào
  task → **Labels → Raw**, dán toàn bộ nội dung `03_cvat_labels.json`; và ở phần mô tả task (task description),
  dán toàn bộ nội dung `02_guideline.md` (v2) trước khi mời thành viên vào label calibration.
- **Nhóm dùng Track hay Shape, vì sao:** **Shape**, cho toàn bộ task. Nguồn ảnh hiện tại là `data_team` — 28 ảnh
  tĩnh độc lập (không phải sequence/video liên tục như `lisa` dùng thử ban đầu), mỗi ảnh là một khoảnh khắc riêng
  biệt không có object identity xuyên frame để giữ, nên không có lý do dùng Track. Nếu sau này nhóm bổ sung dữ
  liệu dạng sequence, chuyển sample đó sang Track + Attribute Annotation Mode theo đúng quy tắc ở `02_guideline.md`
  mục 3.

## Setup test

Một thành viên **chưa tham gia setup** mở task và trả lời: label gì, dùng tool nào, gán attribute nào, khi nào
escalate. Ghi lại ai test và chỗ họ vấp:

**Cách làm:** người test mở task calibration trên CVAT, chỉ đọc Guide của task (không hỏi người setup), rồi trả lời
4 câu dưới đây. Người setup so với đáp án chuẩn; câu nào sai hoặc phải hỏi lại thì ghi vào cột "Chỗ vấp" và sửa
guideline/Guide trước khi label calibration. Người test phù hợp: Lưu Thị Lan Anh hoặc Phan Khánh Hoàng (vai tìm
data, không tham gia setup task).

**Đáp án chuẩn (theo `02_guideline.md`):**

| # | Câu hỏi | Đáp án chuẩn |
|---|---|---|
| 1 | Label gì? | Một class duy nhất `traffic_light`: mỗi light head của đèn tín hiệu xe cơ giới nhìn thấy được là 1 object, kể cả đèn không điều khiển làn của ego (vẫn label, gán `not_relevant`). Không label: đèn người đi bộ/xe đạp, đèn hậu xe, phản chiếu trên kính/biển LED, đèn đếm ngược số giây (mục 1, 5). |
| 2 | Dùng tool nào? | **Rectangle**, chế độ **Shape** (ảnh tĩnh, không dùng Track). Box ôm sát viền light head, không lấy cột/cần đèn; một cột có N head thì vẽ N box riêng (mục 2, 3). Export bằng **CVAT for images 1.1**, tắt "Save images". |
| 3 | Gán attribute nào? | Đủ 5 attribute cho mỗi box: `state` (red/yellow/green/off/unknown), `relevance` (relevant_to_ego/not_relevant/unknown_relevance), `direction` (round/arrow_left/arrow_right/arrow_straight/unknown), `occluded` (none/partial/heavy), và `evidence` — bắt buộc điền khi `state` hoặc `relevance` là unknown. Không để sót giá trị `__undefined__` (mục 4). |
| 4 | Khi nào escalate? | Khi đèn bị che gần hết (≥ 90%) và không xác định được cả vị trí chính xác của light head, hoặc gặp case guideline chưa lường trước (vd. dãy đèn liên tục không tách được từng head). Khi đó không tự vẽ box đoán: ghi `evidence` = "ESCALATE: <lý do>" và báo Lead (mục 6, 7). Thiếu bằng chứng cho một attribute thì dùng `unknown`, không phải escalate. |

**Kết quả test:**

| Người test | Ngày | Câu trả lời sai / phải hỏi lại | Chỗ vấp (thao tác CVAT hoặc rule khó hiểu) | Đã sửa gì sau test |
|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO |
