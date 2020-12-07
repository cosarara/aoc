#include <omp.h>
#include <stdio.h>
#include <string.h>

int main() {
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
    int* positions_ = &positions[0][0];

    int velocities[4][3] = {0};
    int* velocities_ = &velocities[0][0];

    long unsigned int step = 0;
    for (; step<1000000lu; step++) {
#pragma omp parallel for num_threads(4) shared(positions)
        for (int i=0; i<3; i++) { // coord
            for (int j=0; j<4; j++) { // planet
                int a = (positions[j][i] < positions[0][i]) - (positions[j][i] > positions[0][i]) +
                    (positions[j][i] < positions[1][i]) - (positions[j][i] > positions[1][i]) +
                    (positions[j][i] < positions[2][i]) - (positions[j][i] > positions[2][i]) +
                    (positions[j][i] < positions[3][i]) - (positions[j][i] > positions[3][i]);
                velocities[j][i] += a;
            }
        }
        for (int i=0; i<12; i++) {
            positions_[i] += velocities_[i];
        }
        if (memcmp(positions, ipositions, sizeof(positions)) == 0) {
            break;
        }
    }

    printf("%lu\n", step);

    for (int i=0; i<3; i++) {
        printf("%d ", positions[0][i]);
    }
    printf("\n");
}
