// Portable portfolio adaptation.
// The recovered source uses Windows-specific scanf_s and a fixed speed-loop Ki.
// This version produces deterministic CI output and preserves the discrepancy.

#include <cmath>
#include <iomanip>
#include <iostream>

int main() {
    constexpr double pi = 3.14159265358979323846;
    constexpr double armature_r = 0.1;
    constexpr double armature_l = 0.02;
    constexpr double current_bandwidth_hz = 500.0;
    constexpr double speed_kp_reported = 24.8;
    constexpr double speed_ki_report_calculation = 3898.0;
    constexpr double speed_ki_recovered_source = 3895.0;

    const double omega_current = 2.0 * pi * current_bandwidth_hz;
    const double current_kp = armature_l * omega_current;
    const double current_ki = armature_r * omega_current;

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "current_kp=" << current_kp << '\n';
    std::cout << "current_ki=" << current_ki << '\n';
    std::cout << "speed_kp_reported=" << speed_kp_reported << '\n';
    std::cout << "speed_ki_report_calculation=" << speed_ki_report_calculation << '\n';
    std::cout << "speed_ki_recovered_source=" << speed_ki_recovered_source << '\n';

    if (std::abs(current_kp - 62.831853) > 1e-3 ||
        std::abs(current_ki - 314.159265) > 1e-3 ||
        speed_ki_report_calculation == speed_ki_recovered_source) {
        return 1;
    }
    return 0;
}
