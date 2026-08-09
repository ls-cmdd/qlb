#include <stdio.h>
#include <math.h>
#include <stdbool.h>

#define جذر sqrt
#define جيب sin
#define جيب_تمام cos
#define ط M_PI

int main() {
    double ن = 0;
    double مضروب = 0;
    double عداد = 0;

    ن = 5.0;
    مضروب = 1.0;
    عداد = 1.0;
    while ((عداد < (ن + 1))) {
        مضروب = (مضروب * عداد);
        عداد = (عداد + 1.0);
    }
    printf("%s\n", "مضروب العدد 5 هو:");
    printf("%g\n", (double)(مضروب));
    return 0;
}
