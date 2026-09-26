# Edge-case library

Tối thiểu **8 card**, khuyến nghị 10–12. Một edge case tốt là case mà hai annotator hợp lý có thể làm khác nhau nếu
guideline chưa rõ. Tám ảnh dễ có label rõ ràng không được tính là edge-case library.

Cần có đủ độ đa dạng: occlusion / truncation / small-far · ambiguous semantics · conflicting road elements · **một case
critical-risk** · **một case guideline cho phép escalation**.

File này là kho nội bộ của nhóm, **không gửi cho peer**. Card dùng ảnh example/calibration thì chép rule + ví dụ sang
`02_guideline.md` (mục 7 và 9) để peer đọc được. Card về ảnh blind chỉ nằm ở đây, và decision của nó phải có trong
`gold_decisions.csv` trước `make freeze`.

`make status` đếm số dòng `CASE ID:` đã điền (đã thay placeholder). Copy khối dưới cho mỗi case.

---

CASE ID: EC01
Sample: TEAM03 (calibration)
Scene: Chạng vạng, giao lộ nhiều đầu đèn — một đầu arrow_left màu đỏ, một đầu round màu đỏ trên cùng cột.
Observation: Hai light head khác hình dạng lens (mũi tên rẽ trái vs hình tròn) nằm sát nhau, cùng màu đỏ tại thời điểm chụp.
Decision: LABEL x2 — mỗi head một box riêng, `direction` khác nhau (`arrow_left` và `round`), `state=red` cho cả hai.
Expected: 2 box tách biệt; box arrow_left có `direction=arrow_left`; box round có `direction=round`; cả hai `state=red`.
Rationale: `direction` quyết định ego được rẽ/đi thẳng theo tín hiệu nào (mục 3 `02_guideline.md`) — gộp hai head
thành một box sẽ làm mất thông tin downstream cần để phân biệt lane rẽ trái và lane đi thẳng.
Common mistake: Chỉ vẽ 1 box cho cả cụm đèn, hoặc gán `direction=round` cho cả hai vì không để ý hình mũi tên.
Diversity: conflicting road elements (nhiều head, nhiều direction).

---

CASE ID: EC02
Sample: TEAM04 (calibration)
Scene: Cùng giao lộ với EC01/TEAM03, chụp cách nhau ít khoảnh khắc — đầu round đã chuyển từ đỏ sang xanh, đầu
arrow_left vẫn đỏ.
Observation: Ảnh trông rất giống TEAM03 nên annotator dễ suy diễn state từ ảnh đã label trước đó thay vì quan sát
lại từ đầu.
Decision: LABEL x2 — arrow_left `state=red`, round `state=green`, đúng theo bằng chứng của chính ảnh này.
Expected: `state` của từng head đọc độc lập theo frame hiện tại, không copy từ sample khác dù cùng góc máy.
Rationale: Temporal rule (`02_guideline.md` mục 8) — mỗi ảnh độc lập là một annotation unit riêng trừ khi thuộc
cùng một track; hai ảnh rời rạc từ cùng giao lộ không mặc nhiên có cùng state.
Common mistake: Copy state từ TEAM03 sang vì "cùng giao lộ, chắc vẫn vậy".
Diversity: ambiguous semantics / temporal.

---

CASE ID: EC03
Sample: TEAM05 (calibration)
Scene: Ban ngày, cột đèn nhiều lane với 3 head khác nhau: đỏ tròn, xanh tròn, xanh mũi tên — mỗi head phục vụ một
lane khác nhau.
Observation: Ba light head cùng lúc hiển thị ba trạng thái khác nhau trên cùng một cột.
Decision: LABEL x3 — mỗi head một box, `state`/`direction` riêng theo đúng lane nó phục vụ.
Expected: Không gộp nhiều head thành một object; mỗi box có `direction` khớp hình lens quan sát được.
Rationale: Object nào cũng phải được xác định `relevance` độc lập — lane ego đi phải khớp đúng head, nhầm head
là nhầm relevance.
Common mistake: Chỉ label head "dễ thấy nhất" (thường là head to nhất) và bỏ sót hai head còn lại.
Diversity: conflicting road elements / multi-head.

---

CASE ID: EC04
Sample: TEAM06 (example)
Scene: Ban ngày, đường dân cư — đèn xe bị mép trên khung hình cắt; trên cột bên trái có hộp đèn người đi bộ hình bàn tay.
Observation: Đèn xe chỉ thấy phần dưới vỏ, không thấy lens đang sáng; hộp đèn bên trái trông giống đèn tín hiệu nhưng là đèn người đi bộ.
Decision: UNKNOWN cho đèn xe (vẫn vẽ box, `state=unknown`, `relevance=relevant_to_ego`, `evidence` ghi truncation); IGNORE đèn người đi bộ.
Expected: 1 box cho đèn xe ở mép trên; không có box cho hộp đèn bàn tay bên trái.
Rationale: Truncation vẫn là object trong scope nên phải vẽ box; đèn người đi bộ ngoài scope (mục 1, 5 guideline).
Common mistake: Bỏ qua đèn bị cắt vì "không thấy rõ"; hoặc vẽ box cho đèn người đi bộ và gán `occluded=heavy`.
Diversity: truncation / ambiguous semantics.
---

CASE ID: EC05
Sample: TEAM07 (calibration)
Scene: Ban ngày, mưa, khu vực đón/trả khách sân bay — đèn kiểm soát làn dạng tròn màu xanh gắn trên mái che, không
phải cột đèn giao lộ chuẩn.
Observation: Thiết bị đèn có chức năng điều khiển xe (báo được phép tiến vào làn đón khách) nhưng hình dạng và vị
trí lắp đặt khác hẳn đèn giao lộ thông thường.
Decision: LABEL — vẫn tính là `traffic_light` vì trực tiếp điều khiển hành vi dừng/đi của ego, đúng định nghĩa
"đèn tín hiệu xe cơ giới" ở Scope (`01_problem_statement.md`).
Expected: Box quanh head đèn xanh; `direction=round`; `relevance=relevant_to_ego` vì đèn áp dụng cho làn xe đang
đi.
Rationale: Scope quy định "mọi đèn tín hiệu xe cơ giới nhìn thấy được" không giới hạn ở giao lộ đường phố chuẩn —
loại bỏ case này sẽ làm hẹp phạm vi ngoài ý muốn.
Common mistake: IGNORE vì nghĩ đây không phải "traffic light thật" do bối cảnh sân bay khác thường.
Diversity: ambiguous semantics (ranh giới định nghĩa object).

---

CASE ID: EC06
Sample: TEAM09 (example)
Scene: Ban đêm, đèn màu cam nằm cạnh biển "People are crossing"; phía trước có 2 đèn xanh của hướng ego.
Observation: Đốm sáng màu cam trông giống đèn đỏ của xe, nhưng màu cam và vị trí cạnh lối qua đường cho thấy đây là đèn bàn tay cho người đi bộ.
Decision: IGNORE đèn cam; LABEL 2 đèn xanh (`state=green`, `relevance=relevant_to_ego`).
Expected: 2 box đèn xanh; không có box cho đèn cam.
Rationale: Đây là **case critical-risk**: nếu vẽ đèn cam thành đèn đỏ `relevant_to_ego`, downstream sẽ dừng xe sai lúc đèn của ego đang xanh.
Common mistake: Coi đèn cam là đèn đỏ của xe vì cùng tông màu nóng.
Diversity: **critical-risk** / ambiguous semantics.
---

CASE ID: EC07
Sample: TEAM15 (blind)
Scene: Ban đêm — 2 đèn bị camera làm ngả xanh dương; bên phải có một đèn đỏ nhỏ, ngay dưới là hình người đi bộ màu trắng.
Observation: Không đọc chắc được màu của 2 đèn chính; đèn đỏ bên phải là đèn người đi bộ chứ không phải đèn xe của hướng khác.
Decision: LABEL 2 đèn với `state=unknown` (đèn phải `relevant_to_ego`, đèn trái `unknown_relevance`); IGNORE đèn đỏ người đi bộ.
Expected: 2 box riêng, `evidence` ghi "màu bị camera làm lệch"; không có box cho đèn đỏ.
Rationale: Đây là **case critical-risk** thứ hai trong bộ blind — vẽ đèn đỏ người đi bộ thành `relevant_to_ego` sẽ khiến xe dừng sai.
Common mistake: Gán `state=green` theo phỏng đoán, hoặc vẽ box cho đèn đỏ vì "thấy đỏ là phải dừng".
Diversity: **critical-risk** / low visibility / ambiguous semantics.
---

CASE ID: EC08
Sample: TEAM17 (trong catalog, không thuộc split nào — case tham khảo nội bộ)
Scene: Ban ngày, mưa, đèn đỏ ở xa bị một xe buýt che một phần thân đèn.
Observation: Vẫn thấy được lens đang sáng đỏ nhưng phần vỏ dưới bị xe buýt che khuất một phần.
Decision: LABEL — `state=red`, `occluded=partial`.
Expected: Box quanh phần đèn nhìn thấy được (không đoán phần bị che); `occluded=partial`; `evidence` không bắt
buộc vì `state` vẫn đọc được rõ ràng.
Rationale: Occlusion 50–90% mới bắt buộc `state=unknown`; occlusion nhẹ hơn vẫn LABEL bình thường kèm cờ
`occluded` đúng mức — phân biệt với EC04 (truncation, không phải occlusion vật lý).
Common mistake: Gán `occluded=none` vì vẫn đọc được màu, bỏ qua việc vật cản thực sự làm giảm diện tích nhìn
thấy được.
Diversity: occlusion / small-far.

---

CASE ID: EC09
Sample: TEAM20 (trong catalog, không thuộc split nào — case tham khảo nội bộ)
Scene: Trong hầm — một dãy đèn tròn màu xanh liên tiếp gắn trên trần hầm, dùng để kiểm soát làn thay vì một cột
đèn giao lộ đơn lẻ.
Observation: Các lens xanh nằm sát nhau thành một dải liên tục do góc nhìn và khoảng cách, không xác định được
ranh giới rõ ràng giữa từng head riêng lẻ; ánh sáng lóa (glare) trong hầm cũng làm mờ viền từng đèn.
Decision: ESCALATE — không tự vẽ nhiều box đoán ranh giới; ghi case này vào edge case card và chờ Lab Coach/gold
owner chốt cách đếm object trước khi đưa vào guideline chính thức.
Expected: Không tạo box đoán số lượng head; ghi rõ trong log là cần quyết định thêm (số lượng object, có tính là
`traffic_light` lane-control hay loại thiết bị khác) trước khi annotate chính thức.
Rationale: Đây là **case guideline cho phép escalation** — vị trí chính xác từng light head không xác định được
do các lens liền kề và glare, đúng điều kiện ESCALATE ở Output chấm được (`01_problem_statement.md` mục 4).
Common mistake: Vẽ đại một box bao trọn cả dải đèn, hoặc đoán số lượng head theo cảm tính.
Diversity: **escalation-permitted** / ambiguous semantics.

---

CASE ID: EC10
Sample: TEAM24 (trong catalog, không thuộc split nào — case tham khảo nội bộ)
Scene: Ban ngày, khu vực băng qua đường trong khuôn viên trường — chỉ có đèn cảnh báo dành cho người đi bộ
(pedestrian beacon), không có bất kỳ đèn tín hiệu xe cơ giới nào trong khung hình.
Observation: Cụm đèn vàng nhỏ trên biển báo người đi bộ dễ bị nhầm là traffic light do hình dạng tròn, gắn trên
cột cao tương tự.
Decision: IGNORE toàn bộ frame — không tạo box nào.
Expected: File export không có object nào cho ảnh này.
Rationale: Theo Scope, "đèn người đi bộ/xe đạp" nằm ngoài scope (ignore); đây là negative sample kiểm tra annotator
có tự tạo box cho object ngoài scope hay không.
Common mistake: LABEL nhầm cụm đèn cảnh báo người đi bộ thành `traffic_light` vì hình dạng tròn tương tự.
Diversity: negative / ambiguous semantics (ranh giới định nghĩa object).

---

CASE ID: EC11
Sample: TEAM26 (ảnh gốc `30.png`; không nằm trong sample_pack, dùng làm ví dụ 3(b) trong guideline)
Scene: Ban ngày, đường nông thôn — đèn tín hiệu gắn trên rơ-moóc di động đang được xe kéo chở đi, đèn tắt hoàn
toàn.
Observation: Thiết bị có hình dạng đúng chuẩn đèn giao thông (các module đèn xếp theo cụm) nhưng đang trong quá
trình vận chuyển, không lắp đặt tại vị trí điều khiển giao thông nào.
Decision: LABEL — `state=off`, `relevance=not_relevant`.
Expected: Box quanh cụm đèn trên rơ-moóc; `state=off`; `relevance=not_relevant` vì đèn chưa lắp đặt nên không điều
khiển làn nào tại vị trí chụp.
Rationale: `state=off` là giá trị hợp lệ trong ontology — không nên bỏ qua hoàn toàn (vì vẫn là một
`traffic_light` vật lý nhìn thấy được) cũng không nên đoán màu đang hoạt động.
Common mistake: Bỏ qua không label vì "đèn không hoạt động", hoặc đoán một màu thay vì gán `state=off`.
Diversity: ambiguous semantics / off-state.

---
