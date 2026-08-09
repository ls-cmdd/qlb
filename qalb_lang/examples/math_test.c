#include <stdio.h>
#include <math.h>
#include <stdbool.h>

#define جذر sqrt
#define جيب sin
#define جيب_تمام cos
#define ط M_PI

int main() {
    double مساحة = 0;
    double ر = 0;
    double زاوية = 0;

    ر = 5.0;
    مساحة = (ط * جذر((ر * ر)));
    printf("%s\n", "مساحة الدائرة بنصف قطر 5 هي:");
    printf("%g\n", (double)(مساحة));
    زاوية = 0.0;
    printf("%s\n", "جيب الزاوية 0 هو:");
    printf("%g\n", (double)(جيب(زاوية)));
    return 0;
}
