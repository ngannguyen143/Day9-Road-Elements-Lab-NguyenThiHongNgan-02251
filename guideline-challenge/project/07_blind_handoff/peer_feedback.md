# Peer feedback + owner response

Phần 1 do **nhóm peer** trả lời (gửi kèm file export). Phần 2 do **nhóm owner** điền. Thay mọi placeholder mới
là xong (gate G5).

- **Nhóm peer:** nhóm Đồng tình
- **Người label blind:** Trường

## 1. Peer trả lời

1. Rule nào rõ nhất / giúp quyết định nhanh nhất? rule về cách label traffic light khá rõ hàng, các attribution đèu được định nghĩa rất minh bạch, chi tiết và đầy đủ. 
2. Rule nào mơ hồ hoặc phải tự suy diễn? rule về cụm đèn có hơi chút mơ hồ nhưng khi nhìn ảnh (cụm đèn là gồm nhiều đèn giao thông gộp thành một chùm) thì tôi hiểu mỗi light head là một cái đèn giao thông tiêu chuản gồm đủ 3 màu.
3. Sample nào khiến guideline "vỡ"? sample về egde case Giao lộ có ≥2 cột, khá rõ ràng nhưng tôi chưa biết làm sao xác định xe của mình đang ở phần đường nào để biết gán cái nào relevant_to_ego, cái nào not_relevent. 
4. Attribute / default nào trong CVAT dễ gây thao tác sai? các định nghĩa khá rõ ràng và chi tiết ạ, chỉ nhiều nên cần nhớ và nắm đầy đủ.
5. Một thay đổi cụ thể giúp annotator mới ít hỏi hơn? tôi chỉ hơi khó hiểu từ light head trong phần Annotation unit; hình dạng của đèn giao thông ban đêm, nó chỉ hiển thị mỗi cái đốm sang thay vì cả một cái đèn, nên tôi không chắc mình nên vẽ box sao cho chính xác nhất ví dụ hình TEAM15, TEAM19.

## 2. Owner phân loại

Owner không tranh luận để bảo vệ guideline. Mỗi feedback và mỗi decision peer làm sai được xếp vào một hướng xử lý.

| Feedback / decision sai | Nguyên nhân (guideline gap / data ambiguity / execution error) | Xử lý (accept + revise / reject with evidence / add escalation rule) | Bằng chứng |
|---|---|---|---|
| Q3 — không biết xác định xe mình đang ở làn nào để gán `relevant_to_ego`/`not_relevant` (case giao lộ ≥2 cột) | guideline gap | accept + revise: v3 thêm mục "Cách xác định làn/hướng của ego" vào mục 7 (ego ở giữa đáy ảnh, đèn quay mặt về camera và nằm phía trên/trước làn ego, đèn cùng hướng trái/phải cùng relevance) | 2/3 critical sai đều do relevance: `TEAM16` d2 (gán thêm đèn đỏ ở cụm trái là relevant_to_ego), `TEAM19` d2 (đèn gần bên trái gán not_relevant) |
| Q5 — khó hiểu "light head"; ban đêm chỉ thấy đốm sáng, không biết vẽ box thế nào (`TEAM15`, `TEAM19`) | guideline gap | accept + revise: v3 định nghĩa rõ light head ở mục 2 và thêm rule vẽ box ban đêm ở mục 3 (thấy vỏ đèn thì ôm vỏ; chỉ thấy đốm sáng thì ôm phần lens đang sáng, không ôm cả vùng lóa) | Box của peer ở `TEAM15`/`TEAM19` ôm sát đốm sáng, box GT ôm cả quầng lóa rộng hơn — hai cách đều không sai theo v2 vì v2 chưa có rule ban đêm |
| Q2 — rule cụm đèn hơi mơ hồ | guideline gap | accept + revise: gộp vào định nghĩa light head mới ở mục 2 (mỗi đầu đèn có vỏ riêng là 1 box, dù gắn chung giá) | Peer tự suy ra đúng: `TEAM16` d1 vẽ đủ 5 box |
| `TEAM19` d1 — bỏ sót 2 đèn nhỏ ở xa | guideline gap | accept + revise: thêm vào checklist mục 10 bước "đếm lại các đèn nhỏ ở xa ở zoom 100%"; rule đèn nhỏ/ở xa (mục 5) đã có nhưng chưa có ví dụ ban đêm | 2/4 đèn bị bỏ sót, cùng kiểu bất đồng đếm box đã thấy ở calibration `TEAM05` |
| `TEAM30` d1 — gán relevant/not_relevant cho ảnh chụp từ vỉa hè, bỏ sót đèn dọc trên cột phải | data ambiguity | add escalation rule: v3 ghi rõ ảnh không chụp từ trong xe thì mọi đèn là `unknown_relevance` | Ảnh gốc `23.png` chụp từ vỉa hè, không có làn ego |
| `TEAM15` d1 — gold ghi đèn trái `unknown_relevance`, đèn phải `relevant_to_ego`; peer gán cả hai `relevant_to_ego` | guideline gap (lỗi gold của owner) | accept + revise: peer đúng theo case 2 (đèn cùng hướng trái/phải phải cùng relevance); chấm peer đúng, sửa gold ở lần freeze sau | Gold tự mâu thuẫn với ví dụ case 2 mục 9 |
| `TEAM16` d3 — gold ghi `off` cho đầu đèn quay ngang, peer ghi `unknown` | guideline gap (lỗi gold của owner) | accept + revise: peer đúng theo định nghĩa `off` ở mục 4; chấm peer đúng | Đầu đèn quay ngang không thấy lens, không thể "chắc chắn tắt" |
| `TEAM29` d1 — peer vẽ thêm 1 đầu đèn quay ngang mà gold không có | guideline gap (lỗi gold của owner) | accept + revise: đầu đèn đó là đèn xe thật trong scope; không trừ điểm peer, bổ sung vào gold lần sau | Box peer ~(199,56)–(215,98) trên cột giữa ảnh `10.png` |
| `TEAM16` d2 — gán thêm đèn đỏ ở cụm trái là `relevant_to_ego` (critical) | guideline gap | accept + revise: như dòng Q3 — cách xác định làn ego ở mục 7 v3 | Critical escape 1/2 |
| `TEAM19` d2 — đèn gần bên trái gán `not_relevant` (critical) | guideline gap | accept + revise: như dòng Q3; thêm câu "đèn quay mặt về camera, ở phía trước làn ego thì relevant, dù ở lề trái hay phải" | Critical escape 2/2 |
