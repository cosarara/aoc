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
    int ipositions[4] = {
        -8,
        5,
        2,
        9,
    };
    int positions[4] = {
        -8,
        5,
        2,
        9,
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
    int velocities[4] = {0};

    long unsigned int step = 0;
    for (; step<100000000000lu; step++) {
        for (int j=0; j<4; j++) { // planet
            int a = (positions[j] < positions[0]) - (positions[j] > positions[0]) +
                (positions[j] < positions[1]) - (positions[j] > positions[1]) +
                (positions[j] < positions[2]) - (positions[j] > positions[2]) +
                (positions[j] < positions[3]) - (positions[j] > positions[3]);
            velocities[j] += a;
        }
        for (int i=0; i<4; i++) {
            positions[i] += velocities[i];
        }
        if (memcmp(positions, ipositions, sizeof(positions)) == 0) {
            break;
        }
    }

    printf("%lu\n", step);

    for (int i=0; i<4; i++) {
        printf("%d ", positions[i]);
    }
    printf("\n");
}
