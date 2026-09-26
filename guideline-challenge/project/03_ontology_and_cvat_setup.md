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
- **Tên task calibration** (có version guideline): `khungdien-calib-v2` — task gồm 8 ảnh `TEAM*` trong
  `build/calibration/`, label theo guideline v2 (job 19 trên CVAT).
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
| Nguyễn Thị Hồng Ngân | 26/09/2026 | Q2: để `direction=round` cho các đầu đèn rất nhỏ ở xa không nhìn rõ hình lens (đúng ra là `unknown`). Q3: 1 box còn `occluded=__undefined__`; để trống `evidence` dù gán `state=unknown`. Q1: vẽ box cho hộp đèn người đi bộ hình bàn tay (`6.png`), trong khi đèn người đi bộ thuộc loại ngoài scope | Không nhận ra attribute nào còn `__undefined__` vì CVAT không bắt buộc chọn; rule `evidence` bắt buộc chỉ nằm trong phần định nghĩa, dễ bỏ sót khi label nhanh; chưa phân biệt được đèn người đi bộ của Mỹ (hộp vuông, bàn tay cam) với đèn xe | Thêm rule đèn rất nhỏ/ở xa vào mục 5; thêm bước lọc box `unknown` thiếu `evidence` và box còn `__undefined__` vào checklist mục 10; gold `TEAM06`, `TEAM09` ghi rõ đèn người đi bộ là IGNORE |
| Bùi Việt Nam | 26/09/2026 | Q3: 3 box ở `13.png` để cả 4 attribute `__undefined__`; ở `16.png` gán `state=yellow` nhưng `evidence` lại ghi "thấy một chấm màu xanh". Làm đúng: điền `evidence` cho 13/14 box `unknown`; không vẽ đèn đỏ người đi bộ ở `17.png`; dùng `state=unknown` cho đèn bị camera làm lệch màu | Vẽ box xong nhưng quên chọn attribute cho các box sau — CVAT không cảnh báo; đèn nhỏ ở xa khó phân biệt vàng với xanh | Như trên: checklist mục 10 thêm bước kiểm tra `__undefined__` trước khi export; rule đèn rất nhỏ/ở xa ở mục 5 (không đọc chắc màu thì `state=unknown`) |

*Ghi chú: setup test được đánh giá qua bài label thật của hai bạn trên CVAT (`team_exports/ngan_anh01-10.zip`,
`team_exports/nam_anh11-20.zip`, và calibration `06_calibration_exports/ngan.zip`) — đối chiếu từng box với đáp án
chuẩn ở trên, thay vì phỏng vấn riêng 4 câu hỏi.*
