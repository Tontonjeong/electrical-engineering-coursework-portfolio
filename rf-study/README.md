# RF · Microwave study workspace

RFDH의 공개 학습 페이지를 읽고, 수식을 다시 계산한 뒤 기존 고주파공학
Cadence 자료와 연결한 재현용 workspace입니다. RFDH 원문·이미지를 복제하지 않고
URL·주제 index, 자체 도식, 표준 라이브러리 계산 코드만 보관합니다.

수식과 용어는 주제에 맞춰 [Keysight의 VNA 기초 자료](https://www.keysight.com/us/en/assets/7018-06841/application-notes/5965-7707.pdf),
[Analog Devices의 RF 사양 해설](https://www.analog.com/en/resources/technical-articles/understand-wireless-data-sheet-specifications--part-1.html),
[TI mmWave Radar 자료](https://www.ti.com/design-development/embedded-development/mmwave-radar.html),
[ITU-R 주파수 대역 명명법](https://www.itu.int/rec/r-rec-v.431/en)과 함께 확인했습니다.

## 읽기 순서

1. [Transmission lines](transmission-lines/README.md)
2. [Smith chart](smith-chart/README.md)
3. [Impedance matching](matching/README.md)
4. [Linearity](linearity/README.md)
5. [Circuit blocks](circuit-blocks/README.md)
6. [Instrumentation](instrumentation/README.md)
7. [RF calculators](calculators/rf_calculators.py)

전체 공개 공부글은
[RF · Microwave 공부 시작점](https://dororok9061.github.io/blog/rf/start-here/)에서
이어집니다. 내 실제 과제 화면과 저장된 simulation 범위는
[기존 passive-network 기록](../04_rf_microwave/passive_network_design/README.md)에
그대로 분리되어 있습니다.

## 재현

```powershell
python -m unittest discover -s rf-study/tests -p "test_*.py"
python rf-study/calculators/rf_calculators.py
```

계산 결과는 학습·초기 설계 비교값입니다. EM simulation, 제작, calibration된 VNA
측정으로 바꾸어 말하지 않습니다.
