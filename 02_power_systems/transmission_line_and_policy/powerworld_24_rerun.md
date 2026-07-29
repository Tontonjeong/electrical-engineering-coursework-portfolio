# PowerWorld 24 원본 케이스 재실행 기록

## 실행 조건

| 항목 | 값 |
|---|---|
| 실행일 | 2026-07-29 KST |
| 프로그램 | PowerWorld Simulator 24 Evaluation |
| 원본 파일 | `전력시스템공학/중간과제/newcase.pwb` |
| 해석 | Solve Power Flow — Newton |
| 저장된 부하 표시 | 2214 MW / 0 Mvar |
| 초기 화면 | Bus 1: 1.00 pu, Bus 2: 1.64 pu |
| 재실행 상태 | **Blackout** |
| 프로그램 메시지 | `System Can No Longer Supply Load BLACKOUT!!! Simulation MUST BE ReStarted` |

## 해석 경계

이 결과는 원본 PWB 파일을 현재 설치된 PowerWorld 24에서 실제로 다시
열고 실행한 진단 결과다. 보고서에 서술된 3000/3100/3200 MW 단계와
동일한 저장 상태라고 단정할 수 없으므로 서로 합치지 않는다.

- `Source-Derived`: 보고서의 부하 단계·무효전력 보상 서술
- `Tool-Rerun`: `newcase.pwb`의 2214 MW 저장 상태에서 발생한 blackout
- `Engineering Interpretation`: 초기 1.64 pu와 재실행 blackout은 검증된
  송전 성능이 아니라 모델 초기화·파라미터·운전점 점검이 필요한 진단 신호
- `Publicly Withheld`: 화면에 포함된 이름과 학번

개인정보가 들어 있는 GUI 캡처는 공개 자산으로 커밋하지 않았다.
