# Revision log

Guideline v1 = bản nháp đầu; v2 = sau calibration nội bộ; v3 = sau blind handoff. Mỗi lần tăng `Version` trong
`02_guideline.md`, thêm một hoặc nhiều dòng vào bảng: đổi gì và vì sao, kèm bằng chứng (sample_id, dòng
calibration report, câu hỏi trong clarification log, feedback của peer).

Cột Version ghi dạng `v1`, `v2`, `v3` — `make status` tìm dòng bảng có `v2` và dòng có `v3`.

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| v1 | Bản nháp đầu: schema `traffic_light` + attribute `state`/`relevance`/`direction`; chưa có ngưỡng occlusion theo %, chưa có cây quyết định relevance, chưa phân biệt `off` thật với `unknown` do glare, chưa có rule `ESCALATE` tách khỏi `UNKNOWN` | Viết trước pilot-test, chỉ đủ khung cơ bản để có cái gì đó cho người ngoài nhóm thử | Bản nháp lưu tại lịch sử phiên bản, nội dung gốc hiện còn ở `02_guideline_v1_1.md` |
| v2 | Thêm bảng ngưỡng occlusion theo % (< 50% / 50–90% / ≥ 90%); thêm cây quyết định `relevance` 5 bước; phân biệt rõ `off` (chắc chắn tắt) với `unknown` (nghi ngờ do chói/che); thêm attribute `occluded` và `evidence`; tách `ESCALATE` khỏi `UNKNOWN` cho case chưa lường trước (đèn tạm/di động); mở rộng inclusion/exclusion với ví dụ cụ thể pilot đã nhầm (phản chiếu, đèn hậu, đèn người đi bộ); mở rộng ví dụ từ 5 lên 10, khớp `04_edge_cases/edge_case_cards.md`; thêm checklist tự chấm trước khi nộp | 1 người ngoài nhóm pilot-test 3 ảnh demo bằng guideline v1 — cho thấy rule thiếu ngưỡng cụ thể nên mỗi người tự đoán "che nhiều" khác nhau, và dễ nhầm object ngoài scope vào box | Pilot-test 3 ảnh demo (v1 → v2); nội dung đầy đủ ở `02_guideline_v2.md`, nay đã hợp nhất vào `02_guideline.md` |
| v2 (sau calibration) | Mục 5: thêm rule cho đèn rất nhỏ/ở xa (vẫn vẽ box nếu nhận ra vỏ đèn, state/direction=unknown). Mục 10: thêm bước lọc box unknown thiếu `evidence` và box còn `__undefined__`. Mục 9: 5 edge case kèm ảnh CVAT; mục 4/6: thống nhất ngưỡng `occluded` (partial < 50%, heavy ≥ 50%). | Calibration 2 người (Thịnh, Ngân) trên 4 ảnh: đồng thuận count 50%, attribute 50%; bất đồng tập trung ở `TEAM05` (giàn nhiều đầu đèn nhỏ) và `TEAM07` | `06_calibration_measure.csv`, `06_calibration_report.csv` |
