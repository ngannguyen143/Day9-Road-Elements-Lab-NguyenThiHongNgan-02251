# QA plan + quality gates

Không được viết "reviewer kiểm tra lại". Phải có sampling, metric, threshold và action khi fail. Thay mọi placeholder
mới là xong (gate G6).

## Flow

Guideline → Calibration → Production → Self-QC → Review → Rework → Quality Gate. Ghi cụ thể cho project của nhóm:

- **Ai review, review bao nhiêu:** QA owner (vai trò ở `00_team.md`) review 100% ảnh có tag `critical`,
  `ambiguity`, `occlusion`, `small_far`; 30% random trên còn lại. Annotator vừa qua calibration (chưa ổn định)
  được review 100% cho tới khi 3 batch liên tiếp không có defect `critical`.
- **Chọn sample theo rule nào:** risk-based sampling, không random đều — ưu tiên theo tag rủi ro trong
  `sample_pack.csv` trước, vì decision `relevance` sai (critical) tập trung ở ảnh nhiều đầu đèn/occlusion, không
  rải đều trên toàn bộ ảnh.
- **Issue được ghi ở đâu, đóng thế nào:** trong giai đoạn calibration, ghi vào `06_calibration_report.csv`
  (`diagnosis` + `action`); ngoài calibration, mọi defect `critical`/`major` ghi thành 1 card trong
  `04_edge_cases/edge_case_cards.md` (Decision/Expected/Common mistake). Issue đóng khi: guideline được sửa (nếu
  `diagnosis=guideline_gap`) hoặc annotator re-label lại đúng sample bị flag (nếu `execution_error`).
- **Khi phát hiện guideline gap thì update và version ra sao:** sửa rule trong `02_guideline.md`, tăng version
  (v1 → v2 → v3), thêm dòng tương ứng vào `08_revision_log.md` kèm `sample_id` là bằng chứng; không sửa gold sau
  `make freeze` — lỗi phát hiện sau freeze ghi `gold sai:` trong `note` của `transfer_score.csv`, xử lý ở guideline
  v3 thay vì sửa gold.

## Defect severity

Nhóm được đổi mapping nếu downstream contract khác, nhưng phải giải thích và chốt trước khi QA.

| Severity | Định nghĩa cho project này | Ví dụ | Action mặc định |
|---|---|---|---|
| Critical | `relevance` sai — đèn điều khiển ego bị đánh `not_relevant` hoặc ngược lại (khớp mục 3 `01_problem_statement.md`) | Đèn rẽ trái điều khiển ego bị gán `not_relevant` vì annotator nhìn nhầm sang đèn làn kế bên | Reject batch, escalate ngay cho QA owner, không đưa vào production set tới khi sửa |
| Major | `state` đọc sai khi occlusion < 50% (đủ bằng chứng nhưng annotator đọc nhầm), hoặc thiếu box cho 1 light head trong cụm nhiều đầu đèn | Cụm 2 đèn (tròn + mũi tên) chỉ vẽ 1 box | Rework — trả lại annotator sửa batch, không cần dừng pipeline |
| Minor | Geometry lệch > 2px tolerance (mục 3 `01_problem_statement.md`), hoặc `direction` sai nhưng không đổi `relevance`/`state` | Box hụt 3–4px một cạnh so với viền lamp housing | Rework nhẹ, ghi note, gộp sửa theo batch định kỳ |
| Question | Case chưa có rule rõ trong guideline — annotator escalate hoặc để `unknown` đúng quy trình, không phải lỗi | Đèn bị xe khác che gần hết, annotator hỏi có nên escalate không | Không tính defect; đưa thành edge case card, cân nhắc thêm rule ở guideline version sau |

## Metrics

| Metric | Cách tính | Vì sao phù hợp với bài toán |
|---|---|---|
| Decision accuracy | % `state`/`relevance`/`direction` khớp gold hoặc khớp giữa annotator (calibration) trên sample review | Đo trực tiếp chất lượng downstream contract — đây là input driving policy dùng thật |
| Critical defect rate | Số decision `relevance` sai / tổng decision `relevance` trong sample review | Tách riêng vì đây là loại lỗi duy nhất ảnh hưởng an toàn (dừng/đi sai) |
| Escalation precision | Số `ESCALATE` hợp lý (QA owner xác nhận thật sự thiếu bằng chứng) / tổng số `ESCALATE` | Annotator escalate bừa để né quyết định cũng là một lỗi cần bắt, không chỉ bắt lỗi đoán ẩu |
| Geometry compliance | % box đạt tolerance ≤ 2px trên sample review | Ảnh hưởng khả năng crop/track downstream dù không đổi decision |

Metric high-risk tách riêng: **critical escape rate** = số decision `relevance` sai lọt qua review / tổng decision
`relevance` đã review — đây chính là chỉ số **C** mà `make gts` tính tự động từ `07_blind_handoff/transfer_score.csv`
sau blind test.

## Quality gate

Threshold là đề xuất của nhóm, không phải chuẩn ngành. Giải thích trade-off cost/risk.

```text
PASS if:
  critical defect rate == 0% trên sample đã review
  AND decision accuracy >= 90%
  AND escalation precision >= 80%
REWORK if:
  0% < critical defect rate <= 5%
  OR decision accuracy trong khoảng 75-90%
  (trả lại đúng annotator/batch bị flag, không dừng pipeline)
REJECT / ESCALATE if:
  critical defect rate > 5%
  OR có >= 1 decision `relevance` sai không bị bắt ở review mà phát hiện ở blind test (`make gts` báo critical
  escape > 0)
  (dừng batch, QA owner review lại toàn bộ, xét revise guideline version)
```

Trade-off: siết threshold `critical` gần bằng 0 vì đây là input trực tiếp cho driving policy — chấp nhận review
nhiều hơn (cost thời gian QA owner) để đổi risk an toàn thấp hơn. Ngược lại `minor`/geometry cho threshold rộng hơn
(REWORK ở mức lệch nhẹ) vì downstream (nhận diện đèn) không nhạy với sai số hình học nhỏ bằng sai `relevance`.
