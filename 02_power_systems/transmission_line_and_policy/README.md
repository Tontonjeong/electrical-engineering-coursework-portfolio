# Power Systems — 765 kV Transmission Line & Policy Review

**Term:** 3-1 · **Project type:** Team Project · Individual contribution unconfirmed  
**Evidence:** Source-Derived / Independent Recalculation / Existing Model Archive / Source Verification

## Engineering question

765 kV 장거리 송전선로의 분포정수 모델을 계산하고, PowerWorld 사례와 국가 전력수급 정책을 검토했습니다. 이 페이지는 **해석 가능한 계산**, **비수렴 모델**, **정책 출처**를 분리합니다.

## Given line model

| Parameter | Value |
|---|---:|
| Line-to-line voltage | 765 kV |
| Frequency | 60 Hz |
| Length | 350 km |
| Series impedance | j0.3 Ω/km |
| Shunt admittance | j4.6 µS/km |

For a lossless distributed line:

```text
Zc = sqrt(z / y)
SIL = V_LL² / Zc
```

The independent script obtains approximately **255.6 Ω** and **2.29 GW**, corresponding to about **1.73 kA** at SIL.

## Model result boundary

회수된 PowerWorld 3-bus 사례의 full-load 결과는 수렴하지 않았고, 비현실적인 per-unit 전압과 blackout 상태를 보였습니다.

```text
Model setup → solver divergence → non-physical state values
                         ↓
          Modeling/debugging evidence only
```

따라서 해당 값은 “765 kV 계통의 실제 전압”이나 “검증된 전압붕괴”로 사용하지 않습니다. 공개 저장소에는 개인정보가 포함된 원본 PWB도 배포하지 않습니다.

## Policy source reconciliation

과제 보고서가 다룬 제11차 전력수급기본계획의 날짜와 수치는 산업통상자원부 원문으로 교차검증했습니다. 정부 발표 기준 확정일은 **2025-02-21**이며, 보고서 내 3월 표기는 수정이 필요합니다. 검증 링크와 차이는 [source_verification.md](data/source_verification.md)에 기록했습니다.

## What is validated

| Claim | Status |
|---|---|
| Zc and SIL arithmetic | Independently recalculated |
| Three-bus model existed | Existing model archive |
| Full-load case converged | **Not validated; source indicates divergence** |
| Policy date/capacity figures | Checked against official government release |

## Boundary

동적 안정도, 보호계전, N-1 신뢰도, 실계통 조류 검증은 수행 증거가 없습니다. 정책 보고서는 AI 보조 작성이 명시된 과제였으므로, 정부 원문과 충돌하는 문장은 원문보다 낮은 신뢰도로 취급합니다.
