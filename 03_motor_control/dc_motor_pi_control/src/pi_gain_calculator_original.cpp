#include <cstdio>
#include <cmath>
#include <iostream>

// 공통 상수
const double PI_ = 3.14159265358979323846;

void interactive_mode();
void table_mode();

int main()
{
    int mode = 0;
    printf("===== DC Motor PI Controller Gain Calculator =====\n");
    printf("(슬라이드 2.4 Current Controller, 2.5 Speed Controller 반영)\n\n");
    printf("1) Interactive single case (과제 값 기본 제공)\n");
    printf("2) Table mode (여러 fsw, r_cc=10/20)\n");
    printf("Select mode (1 or 2): ");
    if (scanf_s("%d", &mode) != 1) {
        printf("입력 오류입니다.\n");
        return 0;
    }
    if (mode == 2)
        table_mode();
    else
        interactive_mode();
    return 0;
}

void interactive_mode()
{
    double Ra = 0.1;      // 슬라이드 기본값
    double La = 0.02;     // 0.02H
    double J = 0.075;     // 0.075 kg*m^2
    double Kt;
    double fsw, r_cc = 10.0, r_cs = 5.0;

    printf("\n[Interactive Mode - 과제 기본값 적용]\n");
    printf("Ra = 0.1 Ohm, La = 0.02 H, J = 0.075 kg*m^2\n");
    printf("Kt (N*m/A) 입력 (예: 0.4078): ");
    if (scanf_s("%lf", &Kt) != 1) return;
    printf("Switching frequency fsw (Hz) 입력 (예: 10000): ");
    if (scanf_s("%lf", &fsw) != 1) return;
    printf("r_cc 입력 (10~20, 보통 10): ");
    if (scanf_s("%lf", &r_cc) != 1) r_cc = 10.0;

    // Current Controller
    double w_cc = 2.0 * PI_ * fsw / r_cc;
    double Kpc = La * w_cc;
    double Kic = Ra * w_cc;

    // Speed Controller (슬라이드 2.5)
    double w_cs = w_cc / r_cs;           // r_cs = 5
    double Kps = J * w_cs / Kt;
    double Kis = Kps * (w_cs / r_cs);    // w_pi = w_cs / 5

    printf("\n=== 계산 결과 ===\n");
    printf("fsw = %.0f Hz, r_cc = %.1f\n", fsw, r_cc);
    printf("ω_cc = %.2f rad/s\n", w_cc);
    printf("ω_cs = %.2f rad/s\n\n", w_cs);

    printf("[Current Controller PI Gain]\n");
    printf("Kpc = %.6f\n", Kpc);
    printf("Kic = %.6f\n\n", Kic);

    printf("[Speed Controller PI Gain]\n");
    printf("Kps = %.6f\n", Kps);
    printf("Kis = %.6f\n\n", Kis);

    printf("※ 이 값을 MATLAB/Simulink 또는 PSIM에 입력하여\n");
    printf("  15%% 1. Speed step response\n");
    printf("  15%% 2. Current step response 확인하세요.\n");
}

void table_mode()
{
    double Ra = 0.1, La = 0.02, J = 0.075, Kt;
    int n = 0;

    printf("\n[Table Mode]\n");
    printf("Ra = 0.1, La = 0.02, J = 0.075 고정\n");
    printf("Kt (N*m/A): ");
    if (scanf_s("%lf", &Kt) != 1) return;
    printf("계산할 fsw 개수: ");
    if (scanf_s("%d", &n) != 1 || n <= 0) return;

    double* fsw_list = new double[n];
    for (int i = 0; i < n; ++i) {
        printf("fsw[%d] (Hz): ", i + 1);
        if (scanf_s("%lf", &fsw_list[i]) != 1) {
            delete[] fsw_list;
            return;
        }
    }

    printf("\n==========================================================================\n");
    printf(" fsw(Hz)   r_cc   ω_cc(rad/s)   Kpc      Kic      Kps      Kis\n");
    printf("--------------------------------------------------------------------------\n");

    for (int i = 0; i < n; ++i) {
        double fsw = fsw_list[i];
        for (int k = 0; k < 2; ++k) {
            double r_cc = (k == 0) ? 10.0 : 20.0;
            double w_cc = 2.0 * PI_ * fsw / r_cc;
            double Kpc = La * w_cc;
            double Kic = Ra * w_cc;
            double w_cs = w_cc / 5.0;
            double Kps = J * w_cs / Kt;
            double Kis = Kps * (w_cs / 5.0);

            printf("%8.0f   %4.0f   %10.2f   %8.4f  %8.4f  %8.4f  %8.4f\n",
                fsw, r_cc, w_cc, Kpc, Kic, Kps, Kis);
        }
    }
    printf("==========================================================================\n");
    delete[] fsw_list;
}