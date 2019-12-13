#include <stdio.h>
#include <string.h>

int main() {
    /* // exampel 1 2770
    int ipositions[12] = {
        -1, 0, 2,
        2, -10, -7,
        4, -8, 8,
        3, 5, -1,
    };
    int positions[4][3] = {
        {-1, 0, 2},
        {2, -10, -7},
        {4, -8, 8},
        {3, 5, -1}
    };
    */
    // example 2, 4686774924
    int ipositions[12] = {
        -8, -10, 0,
        5, 5, 10,
        2, -7, 3,
        9, -8, -3
    };
    int positions[4][3] = {
        {-8, -10, 0},
        {5, 5, 10},
        {2, -7, 3},
        {9, -8, -3}
    };
    /*
    int ipositions[12] = {
        -7, -1, 6,
        6, -9, -9,
        -12, 2, -7,
        4, -17, -12
    };
    int positions[4][3] = {
        {-7, -1, 6},
        {6, -9, -9},
        {-12, 2, -7},
        {4, -17, -12}
    };
    */
    int* positions_ = &positions[0][0];

    int velocities[4][3] = {0};
    int* velocities_ = &velocities[0][0];

    long unsigned int step = 0;
    for (; step<100000000000lu; step++) {
        int allzero = 1;
        for (int i=0; i<3; i++) { // coord
            for (int j=0; j<4; j++) { // planet
                int a = (positions[j][i] < positions[0][i]) - (positions[j][i] > positions[0][i]) +
                    (positions[j][i] < positions[1][i]) - (positions[j][i] > positions[1][i]) +
                    (positions[j][i] < positions[2][i]) - (positions[j][i] > positions[2][i]) +
                    (positions[j][i] < positions[3][i]) - (positions[j][i] > positions[3][i]);
                velocities[j][i] += a;
                if (velocities[j][i]) allzero = 0;
            }
        }
        for (int i=0; i<12; i++) {
            positions_[i] += velocities_[i];
        }
        if (allzero && memcmp(positions, ipositions, sizeof(positions)) == 0) {
            break;
        }
    }

    printf("%lu\n", step);

    for (int i=0; i<3; i++) {
        printf("%d ", positions[0][i]);
        printf("%d ", velocities[0][i]);
    }
    printf("\n");
}
