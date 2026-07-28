# Publication Matrix

| Artifact class | Public | Reason |
|---|---:|---|
| Author-written HDL and C++ source | Yes | 기술 검토 및 재현 가능 |
| Public-domain style equations and independent calculations | Yes | 결과 검증 가능 |
| Portfolio redraw diagrams and derived charts | Yes | 원본 사실을 공개용으로 재구성 |
| Selected historical result images | Yes, labeled | Existing Result Archive로만 사용 |
| Raw reports and assignment PDFs | No | 저작권·개인정보·과제 원문 보호 |
| Licensed EDA project files | No | 실행환경/라이선스 종속 |
| Power-system model containing personal metadata | No | 개인정보 포함 |
| Workbooks with formula errors or mismatched design cases | No | 오해 방지 |
| Teammate names and student identifiers | No | 개인정보 |
| Local absolute paths and temporary files | No | 개인정보·재현성 |

## 공개 판정 기준

공개 파일은 `scripts/validate_publication.py`로 개인정보 패턴, 절대경로, 금지 확장자, 링크·manifest·asset 누락을 검사합니다. 스캐너 자체에도 실제 개인정보 문자열을 저장하지 않습니다.
