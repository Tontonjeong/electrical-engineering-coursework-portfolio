#include <math.h>

// --- [1] 정적 변수 (Static Variables) ---
static double SpeedErrInt = 0.0; 
static double CurrErrInt = 0.0;  
static double CNT = 0.0;         
static double Vt_out = 0.0;      

#ifndef PI
#define PI 3.14159265359
#endif

_declspec(dllexport) void simuser(double t, double dt, double* in, double* out)
{
    // ==========================================================
    // [1] 변수 선언부 (모든 변수를 여기서 먼저 선언 - 에러 방지)
    // ==========================================================
    double Tsamp, Ke_RPM;
    double Kpc, Kic, Kps, Kis;
    double Ia_meas, Speed_meas, Speed_ref;
    double SpeedErr, Ia_ref_cal, Ia_ref;
    double CurrErr, Ea, Vt_cal;

    // ==========================================================
    // [2] 파라미터 및 게인 설정
    // ==========================================================
    
    // [수정] 스위칭 주파수 20,000Hz (20kHz) -> 주기 0.00005초
    Tsamp = 0.00005; 

    // 역기전력 상수
    Ke_RPM = 0.955 * 2.0 * (2.0 * PI / 60.0);

    // 게인 설정 (기존 값 유지)
    Kpc = 62.83;
    Kic = 314.16;
    Kps = 24.8;
    Kis = 3895.0;

    // ==========================================================
    // [3] 입력 데이터 읽기
    // ==========================================================
    Ia_meas = in[0];      
    Speed_meas = in[1];   

    // ==========================================================
    // [4] 목표 속도 프로파일 (기존 로직 유지)
    // ==========================================================
    Speed_ref = 0.0;

    if (t < 1.5) {
        Speed_ref = (850.0 / 1.5) * t;          // 0 ~ 850 RPM
    }
    else if (t < 2.0) {
        Speed_ref = 850.0;                      // 850 RPM
    }
    else if (t < 3.5) {
        Speed_ref = 850.0 + ((350.0 / 1.5) * (t - 2.0)); // 850 ~ 1200 RPM
    }
    else {
        Speed_ref = 1200.0;                     // 1200 RPM
    }

    // ==========================================================
    // [5] 제어 알고리즘
    // ==========================================================
    CNT += dt;

    if (CNT >= Tsamp) {
        CNT = 0.0;

        // ------------------------------------
        // 1. 속도 제어기
        // ------------------------------------
        SpeedErr = Speed_ref - Speed_meas; 
        
        // PI 제어 연산
        Ia_ref_cal = (Kps * SpeedErr) + (Kis * (SpeedErrInt + SpeedErr * Tsamp));

        // 전류 제한 (Anti-windup)
        if (Ia_ref_cal >= 10.0) {
            Ia_ref = 10.0;
        }
        else if (Ia_ref_cal <= -10.0) {
            Ia_ref = -10.0;
        }
        else {
            SpeedErrInt += SpeedErr * Tsamp; 
            Ia_ref = Ia_ref_cal;
        }

        // ------------------------------------
        // 2. 전류 제어기
        // ------------------------------------
        CurrErr = Ia_ref - Ia_meas;
        
        // 역기전력 보상
        Ea = Ke_RPM * Speed_meas; 
        
        // PI 제어 연산
        Vt_cal = (Kpc * CurrErr) + (Kic * (CurrErrInt + CurrErr * Tsamp)) + Ea;

        // 전압 제한
        if (Vt_cal >= 200.0) {
            Vt_out = 200.0;
        }
        else if (Vt_cal <= -200.0) {
            Vt_out = -200.0;
        }
        else {
            CurrErrInt += CurrErr * Tsamp;
            Vt_out = Vt_cal;
        }
    }

    // ==========================================================
    // [6] 출력
    // ==========================================================
    out[0] = Vt_out;    
    out[1] = Speed_ref; 
    out[2] = 0.0;
}