# Guideline — Traffic Light Annotation

**Version:** v2 — cập nhật sau khi 1 người ngoài nhóm pilot-test 3 ảnh demo bằng guideline v1
**Chủ đề:** Traffic Light | **Hình học CVAT:** Rectangle (Track nếu là video/sequence)
**Nguồn dữ liệu tham chiếu:** DriveU Traffic Light Dataset (DTLD) — hơn 230k annotation, bbox + attribute (relevance, state, orientation, pictogram, occlusion) + track identity. Giấy phép: đăng ký tại Ulm University, chỉ dùng nghiên cứu/giảng dạy, **cấm thương mại, cấm chia sẻ cho bên thứ ba** — mỗi người tự tải theo quyền của mình, không re-host DTLD trong repo lớp. Nguồn thay thế: Bosch Small Traffic Lights (đèn nhỏ/xa, chiếu sáng khó), BDD100K (`trafficLightColor`), dashcam tự quay (đã làm mờ mặt người/biển số).

> **Không có rule ngầm.** File này là văn bản duy nhất nhóm chấm chéo sẽ nhận được, không kèm giải thích bằng miệng. Một quyết định không nằm trong file này hoặc trong `04_edge_cases/edge_case_cards.md` (dùng làm ví dụ) thì coi như không tồn tại.

> **Hai nguyên tắc tách bạch:** (1) Rule lấy trực tiếp từ dataset gốc (DTLD) khác với "quy ước lớp học" — ví dụ nhóm chọn `relevant_to_ego / not_relevant / unknown_relevance` thay vì bộ giá trị gốc của DTLD, quy ước này chỉ để đưa dữ liệu vào bài tập CVAT, không phải chuẩn chính thức của dataset (xem ghi chú tương thích ở mục 4). (2) Không so annotation của mình với ground truth trước khi nhóm khác làm xong bài test — GT giữ riêng trong `gt_reference/`, chỉ upload ảnh cho nhóm khác.

---

## 1. Mục đích và phạm vi

*(không đổi so với v1)* Nhãn traffic light phục vụ module nhận diện đèn cho ADAS/ego-vehicle perception — output tiêu thụ trực tiếp bởi driving policy để quyết định dừng/đi. Annotation phải trả lời được "đèn này có điều khiển xe của tôi không", không chỉ "đèn màu gì".

- **Trong phạm vi:** mọi đèn tín hiệu xe cơ giới nhìn thấy được, ở bất kỳ khoảng cách/góc nào, kể cả không áp dụng cho ego.
- **Ngoài phạm vi** (không tạo box — pilot-test đã cho thấy đây là chỗ hay nhầm nhất, xem mục 10):
  - Đèn người đi bộ — hình dạng icon người/xe đạp khác hẳn đèn tròn/mũi tên.
  - Đèn hậu xe (tail light) — dễ nhầm vào ban đêm vì cũng có màu đỏ sáng.
  - Phản chiếu đèn trên kính toà nhà, kính xe, hoặc biển quảng cáo LED — không có cột đèn vật lý tại vị trí đó.
  - Đèn đếm ngược hiển thị số giây — ngoài scope schema này.

## 2. Annotation unit

Đơn vị là **1 light head nhìn thấy được**. Một cột/gantry có N head (ví dụ 1 đèn tròn + 1 đèn mũi tên rẽ trái) → **N box riêng biệt**, mỗi box 1 head — **không gộp thành 1 box bao cả cụm** (pilot đã mắc đúng lỗi này, xem edge case EC-02).

## 3. Geometry rule

Box bao sát viền light head/lamp housing nhìn thấy được, không lấy cột/giá đỡ. Ảnh tĩnh: Rectangle (Shape). Video/sequence: Rectangle (Track) để giữ object identity; đặt keyframe mới khi box hoặc state đổi rõ rệt, sau đó dùng **Attribute Annotation Mode** trong CVAT để gán state/relevance nhanh cho cả chuỗi thay vì sửa từng frame một.

## 4. Taxonomy — class & attribute

Chỉ 1 class `traffic_light`. State/relevance/direction là attribute vì cùng object có thể đổi các giá trị này theo frame/góc nhìn — tách thành class riêng sẽ làm taxonomy nổ ra không cần thiết (mỗi tổ hợp màu × hướng × mức liên quan sẽ thành hàng chục class nếu tách sai).

**Ontology đầy đủ (phải khớp chính xác `03_ontology_and_cvat_setup.md`):**

| Name            | Geometry  | Class/Attribute        | Allowed values                                              | Default           | Mutable?             | Rationale                                                                                    |
| --------------- | --------- | ---------------------- | ----------------------------------------------------------- | ----------------- | -------------------- | -------------------------------------------------------------------------------------------- |
| `traffic_light` | Rectangle | Class                  | —                                                          | —                | —                   | Duy nhất 1 class, tránh nổ taxonomy                                                       |
| `state`         | —        | Attribute              | red / yellow / green / off / unknown                        | unknown           | Có                  | Đổi theo frame; downstream cần biết đèn đang "nói" gì                               |
| `relevance`     | —        | Attribute              | relevant_to_ego / not_relevant / unknown_relevance          | unknown_relevance | Có                  | Quyết định critical nhất — đèn có điều khiển ego không                           |
| `direction`     | —        | Attribute              | round / arrow_left / arrow_right / arrow_straight / unknown | unknown           | Ít đổi hơn state | Hình dạng lens quyết định ego được rẽ/đi thẳng theo tín hiệu nào               |
| `occluded`      | —        | Attribute              | none / partial / heavy                                      | none              | Có                  | Cờ mức độ che, phục vụ QC & ngưỡng escalate (mới ở v2)                             |
| `evidence`      | —        | Attribute (text ngắn) | tự do                                                      | ""                | Có                  | Bắt buộc điền khi`state`/`relevance` = unknown, để reviewer hiểu vì sao (mới ở v2) |

**Ghi chú tương thích với DTLD:** bản gốc DTLD tách riêng `pictogram` (circle/arrow/pedestrian/bicycle…) với `orientation` (bố trí vật lý của đèn: vertical/horizontal), và dùng `relevant/not_relevant/unknown` cho relevance. Nhóm gộp `pictogram` vào attribute `direction` (round/arrow_*) vì bài này không cần phân biệt orientation vật lý, và đổi `relevant` → `relevant_to_ego` cho rõ nghĩa hơn với người đọc ngoài nhóm. Khi so với GT gốc DTLD: **không remap state trước** — đọc đúng vocabulary trong JSON v2 của DTLD (có cả state chuyển tiếp như `red-yellow`), chỉ map sang schema project này sau, bằng bảng mapping có ghi version.

## 5. Inclusion / exclusion

*(không đổi so với v1, chỉ thêm ví dụ cụ thể ở mục 9–10)* Không box: đèn người đi bộ/xe đạp, đèn hậu, phản chiếu, đèn đếm ngược. Có box: mọi đèn xe cơ giới nhìn thấy được kể cả không relevant cho ego (gán `not_relevant`, không phải bỏ qua).

## 6. Visibility / occlusion

**Mới ở v2** — pilot cho thấy v1 thiếu ngưỡng số cụ thể, mỗi người tự đoán "che nhiều" khác nhau:

| Mức che | Hành động |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| < 50% diện tích light head | Vẫn xác định màu bình thường; gán`occluded=partial` nếu có che dù nhẹ |
| 50–90% | `state=unknown`, `occluded=partial`, ghi lý do vào `evidence` |
| ≥ 90% (chỉ còn thấy viền hộp, không thấy màu) | `state=unknown`, `occluded=heavy`; nếu không xác định được cả vị trí chính xác → **ESCALATE** thay vì tự vẽ box đoán |

Không dùng frame trước/sau để "bịa" ra màu của frame đang bị che — chỉ dùng context để xác nhận vị trí/identity của đèn, không để suy luận state.

## 7. Ambiguity / escalation

**Cây quyết định `relevance`** (làm đúng thứ tự, không nhảy bước — mới ở v2, đưa nguyên từ đề bài vào đây):

1. Đèn có nằm trong field of view và đủ rõ để phân tích không? Không đủ rõ → `unknown_relevance`.
2. Đèn thuộc road branch/lane group nào? Dựa vào vị trí ngang, mũi tên trên đèn, gantry, hình học của làn.
3. Ego lane/hướng đi của frame này là gì: đi thẳng, rẽ trái, rẽ phải, merge, hay service lane?
4. Đèn đó điều khiển ego lane hay đối tượng khác (pedestrian, bus, bicycle, cross street)? Nếu là đối tượng khác → `not_relevant`.
5. Nếu vẫn thiếu bằng chứng sau 4 bước trên → `unknown_relevance`, không đoán.

4 loại quyết định và cách **bắt buộc** thể hiện trong CVAT export — quyết định nào không hiện trong export thì không chấm được:

| Quyết định | Ý nghĩa | Thể hiện trong CVAT |
| ------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **LABEL** | Đủ bằng chứng, gán bình thường | Box +`state`/`relevance`/`direction` cụ thể (không phải unknown) |
| **IGNORE** | Đối tượng ngoài scope (mục 1, 5) | Không tạo box — object không xuất hiện trong export |
| **UNKNOWN** | Có object thật, thiếu bằng chứng 1 attribute | Box vẫn có; attribute tương ứng =`unknown`/`unknown_relevance`; `evidence` ghi lý do |
| **ESCALATE** | Case guideline chưa lường trước (ví dụ đèn tạm/di động — xem EC-10) | Box tạm +`evidence` ghi rõ "ESCALATE: <lý do>" + 1 dòng trong decision log, chờ team lead quyết ở lần cập nhật guideline tiếp theo |

## 8. Temporal rule

State hợp lệ chuyển theo logic vật lý: `red→yellow→green` hoặc `green→yellow→red` (hoặc `red-yellow` nếu theo đúng vocab transition của DTLD). Nhảy bất thường (ví dụ đỏ → xanh không qua vàng ở frame kề) là **tín hiệu QC** cần xem lại, không tự sửa.

`relevance` không được "trôi" (drift) qua lại giữa các frame liền kề mà không có lý do hình học rõ ràng (ví dụ ego đổi làn) — nếu cùng 1 đèn lúc `relevant_to_ego` lúc `not_relevant` giữa 2 frame gần nhau, coi là lỗi tracking/rule, phải xem lại chứ không giữ nguyên.

`relevance` được định nghĩa theo **planned route hiện tại của ego** — đèn của giao lộ *kế tiếp* (nhìn xa hơn phía trước) không được đánh `relevant_to_ego` cho giao lộ đang xử lý.

Review theo cả chuỗi (sequence), không chấm từng frame độc lập — 1 lỗi state ở giữa chuỗi 20–30 frame dễ bị bỏ sót nếu chỉ xem từng ảnh rời rạc.

## 9. Examples (10 ảnh demo — khớp `04_edge_cases/edge_case_cards.md`)

| #  | Tình huống                                                              | Quyết định                                                                     |
| -- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 1  | Đèn phản chiếu trên kính toà nhà/biển LED, không có cột thật | **IGNORE** — không box                                                          |
| 2  | 1 cột có 2 head (round + arrow)                                         | **LABEL** 2 box riêng, direction khác nhau                                      |
| 3  | Đèn xa >50m, vài pixel, không phân biệt được màu                | **LABEL**, `state=unknown`                                                        |
| 4  | Bị cây/xe tải che ~60%                                                 | **LABEL**, `state=unknown`, `occluded=partial`                                    |
| 5  | Giao lộ có ≥2 cột: 1 cho làn ego, 1 cho làn cắt ngang              | **LABEL** cả 2, `relevance` khác nhau theo làn ego — **critical**             |
| 6  | Đèn`arrow_left` đặt cạnh đèn `round`                               | **LABEL** riêng, direction theo hình dạng lens, không theo state              |
| 7  | Đèn đang chuyển trạng thái / motion blur                            | **LABEL** theo màu chiếm ưu thế (>50% diện tích); không chắc → `unknown` |
| 8  | Đèn người đi bộ gần cụm đèn xe cơ giới                        | **IGNORE** — ngoài scope                                                        |
| 9  | Đèn không sáng màu nào: hỏng thật hay do chói nắng?             | `off` nếu chắc chắn không hoạt động; `unknown` nếu nghi ngờ do glare     |
| 10 | Đèn tạm/di động tại công trường thi công                        | **ESCALATE**                                                                      |

## 10. Common mistakes (checklist tự chấm trước khi nộp)

- [ ]  Có gán nhầm đèn của làn khác thành `relevant_to_ego` không? *(lỗi trọng yếu nhất theo QA — nghiêm trọng hơn box lệch vài pixel)*
- [ ]  Có đoán state khi có cả đèn tròn + đèn mũi tên cùng lúc, thay vì tách 2 box riêng không?
- [ ]  Có lỡ box nhầm phản chiếu / đèn hậu / đèn người đi bộ (out-of-scope) không?
- [ ]  Có gộp nhiều light head vào 1 box thay vì tách riêng không?
- [ ]  Có gán `off` cho trường hợp thực ra là chói nắng (đáng lẽ là `unknown`) không?
- [ ]  Có "bịa" state cho frame bị che dựa vào frame trước/sau không? (chỉ được xác nhận vị trí, không suy luận màu)
- [ ]  Mọi giá trị `unknown`/`unknown_relevance` có kèm `evidence` giải thích lý do không?
- [ ]  Case chưa từng gặp (ví dụ đèn tạm) có được ESCALATE thay vì tự quyết không?

---

**Lịch sử phiên bản**

| Version | Thời điểm                                                   | Thay đổi chính                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v1      | Trước pilot                                                  | Schema cơ bản`state`+`relevance`+`direction`; chưa có ngưỡng occlusion; chưa có cây quyết định relevance; chưa phân biệt `off` thật với `unknown` do glare; chưa có rule ESCALATE riêng biệt với UNKNOWN                                                                                                                                                                                                                                                                    |
| v2      | Sau khi 1 người ngoài nhóm pilot-test 3 ảnh demo bằng v1 | Thêm ngưỡng occlusion theo %; thêm cây quyết định relevance 5 bước (đưa nguyên vào guideline); thêm phân biệt`off` vs `unknown` do glare; thêm attribute `occluded` và `evidence`; thêm rule ESCALATE tách biệt khỏi UNKNOWN cho case chưa lường trước (đèn tạm); mở rộng inclusion/exclusion với ví dụ cụ thể pilot đã nhầm (phản chiếu, đèn hậu, đèn người đi bộ); mở rộng 5→10 ví dụ khớp edge case cards; thêm checklist tự chấm |
