# Problem statement + downstream contract

Tối đa nửa trang, viết **trước khi mở CVAT**. Đây là bằng chứng của gate G1 (topic lock). Thay mọi placeholder
mới là xong.

## Bài toán

Traffic-light **state + ego relevance** tại giao lộ có nhiều đầu đèn (multi-head gantry/cột đèn): khó ở việc xác
định đèn nào thực sự điều khiển ego lane khi có nhiều đầu đèn cùng lúc, và đọc đúng màu khi đèn nhỏ/xa hoặc bị che
một phần (ban đêm, chạng vạng).

## Downstream contract

1. **Downstream task / model / user là ai?** Module nhận diện đèn tín hiệu cho ADAS / ego-vehicle perception —
   output được driving policy tiêu thụ trực tiếp để quyết định dừng hay đi.
2. **Output annotation nào thực sự cần?** Rectangle (Track nếu là sequence) cho mỗi light head nhìn thấy được,
   kèm attribute `state` (red/yellow/green/off/unknown), `relevance` (relevant_to_ego/not_relevant/unknown_relevance),
   `direction` (round/arrow_left/arrow_right/arrow_straight/unknown), `occluded` (none/partial/heavy), `evidence`
   (text ngắn, bắt buộc khi state/relevance = unknown).
3. **Failure nào gây hậu quả lớn nhất?** Gán sai `relevance` — đèn thực sự điều khiển ego bị đánh `not_relevant`
   (xe có thể đi sai lúc đèn đỏ) hoặc ngược lại (xe dừng nhầm vì đèn của lane khác) → đây là decision `critical`
   trong gold.
4. **Khi ambiguity không resolve được, ai / ở đâu là escalation path?** Khi occlusion ≥ 90% và không xác định được
   cả vị trí chính xác của light head, hoặc cây quyết định relevance (5 bước ở `02_guideline.md` mục 7) vẫn không
   đủ bằng chứng sau bước cuối → **ESCALATE**, ghi case vào `04_edge_cases/edge_case_cards.md` và quyết định cuối
   cùng do Lab Coach / gold owner của nhóm chốt trước `make freeze`.

## Scope

- **Trong scope (bắt buộc label):** mọi đèn tín hiệu xe cơ giới nhìn thấy được, ở bất kỳ khoảng cách/góc nào, kể
  cả khi không relevant cho ego (gán `not_relevant`, không bỏ qua).
- **Ngoài scope (ignore):** đèn người đi bộ/xe đạp, đèn hậu xe (tail light), phản chiếu đèn trên kính/biển quảng
  cáo LED (không có cột đèn vật lý tại vị trí đó), đèn đếm ngược hiển thị số giây.
- **Geometry tolerance:** box ôm sát viền light head/lamp housing nhìn thấy được, không lấy cột/giá đỡ; lệch ≤ 2 px
  mỗi cạnh là đạt.

## Output chấm được

Bốn loại decision, mỗi loại phải thấy được trong file export CVAT:

- **LABEL** — đủ bằng chứng: box + `state`/`relevance`/`direction` cụ thể (không phải unknown).
- **IGNORE** — object ngoài scope (mục 1, 5 ở guideline): không tạo box, không xuất hiện trong export.
- **UNKNOWN** — occlusion 50–90% hoặc bằng chứng không đủ rõ: box vẫn có, `state`/`relevance` = unknown,
  `occluded` tương ứng, và `evidence` giải thích lý do.
- **ESCALATE** — occlusion ≥ 90% và không xác định được vị trí: không tự vẽ box đoán, ghi vào edge case card +
  gold decision thay vì annotate trực tiếp.

## Dữ liệu và giới hạn

- **Nguồn ảnh:** `data_team` — 32 ảnh do nhóm tự chụp/sưu tầm (thay cho `bdd100k`/`lisa` dùng thử ban đầu). Đã
  khảo sát toàn bộ 32 ảnh, đăng ký 28 ảnh vào `data/catalog.csv` (`TEAM01`–`TEAM28`); 15 ảnh trong số đó được
  dùng trong `project/sample_pack.csv` (3 example, 7 calibration, 5 blind), số còn lại giữ lại trong catalog làm
  nguồn dự phòng cho v3/gold sau này.
- **4 ảnh bị loại khỏi catalog (không dùng):** các ảnh gốc `10.png`, `11.png`, `23.png`, `24.png` là ảnh chụp
  góc nhìn người thứ ba/tư liệu đường phố (không phải góc nhìn từ trong xe — ego-vehicle), không đại diện cho
  input mà module ADAS/ego-vehicle perception thực sự nhận được (khác hẳn về góc máy, chiều cao camera, chuyển
  động so với dashcam) → loại khỏi catalog thay vì gán tag để tránh làm lệch phân bố dữ liệu huấn luyện/kiểm thử.
- **Giới hạn đã biết:** `TEAM03`/`TEAM04` là cùng một giao lộ chụp cách nhau ít khoảnh khắc (đèn round chuyển từ
  đỏ sang xanh) — cả hai chỉ dùng trong `calibration`, không đưa sang `blind`, để tránh lộ đáp án qua trùng cảnh.
  Một số ảnh (`TEAM07` đèn kiểm soát làn sân bay, `TEAM20` đèn trong hầm, `TEAM25` đèn di động trên rơ-moóc) là
  thiết bị đèn không chuẩn (không phải cột đèn giao lộ 3 màu thông thường) — được xếp vào `calibration`/`blind`
  có chủ đích để kiểm tra việc áp dụng đúng ranh giới scope ở mục trên, không phải lỗi chọn data.
