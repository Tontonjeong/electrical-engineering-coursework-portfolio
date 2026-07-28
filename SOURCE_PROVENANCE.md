# Source Provenance

이 저장소는 개인 학습 아카이브를 공개용으로 재구성한 것입니다. 아래 분류는 “무엇을 했는가”뿐 아니라 “어떤 근거로 공개하는가”를 설명합니다.

| 영역 | 공개 근거 | 상태 | 공개하지 않은 자료 |
|---|---|---|---|
| Controller Logic | VHDL 원본 4개, 보고서 기반 인터페이스 | Recovered Original + Portable Reconstruction | Vivado 생성물, 로컬 경로, 보고서 PDF |
| Transformer | 보고서의 설계조건·코어 비교·최종 수치 | Source-Derived + Independent Recalculation | 원본 PDF, 오류/이종 입력 워크북 |
| Power Systems | 보고서 계산, PowerWorld 결과 화면의 판독, 정부 원문 | Source-Derived + Source Verification | 개인정보 포함 PWB, 라이선스 모델 |
| Motor Control | 보고서 파라미터, 원본 C++ 계산기, 기존 결과 그림 | Recovered Original + Existing Result Archive | 원본 PDF, PSIM/MATLAB 프로젝트 |
| RF/Microwave | 보고서 설계값 및 시뮬레이션 화면 | Source-Derived + Existing Result Archive | Cadence 프로젝트, 튜토리얼 원문 |
| Sensor Applications | 연구제안서의 아키텍처와 검증 계획 | Concept / Proposal | 특허 전략 세부, 운용 세부 |

## 해석 원칙

1. 서로 다른 입력 조건의 결과는 같은 설계로 합치지 않습니다.
2. 수렴하지 않은 모델은 실계통 결과로 주장하지 않습니다.
3. 기존 결과 화면은 재실행 결과로 표시하지 않습니다.
4. 구현되지 않은 연구 제안은 성능 달성 또는 실증으로 표현하지 않습니다.
5. 재구성 RTL은 회수 원본과 다른 디렉터리에 두고 헤더에 상태를 명시합니다.
