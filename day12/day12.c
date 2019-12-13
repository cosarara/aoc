#include <stdio.h>

int main() {
    int positions[4][3] = {
        {-7, -1, 6},
        {6, -9, -9},
        {-12, 2, -7},
        {4, -17, -12}
    };
    int* positions_ = &positions[0][0];

    int velocities[4][3] = {0};
    int* velocities_ = &velocities[0][0];

    for (int step=0; step<10000000; step++) {
        for (int i=0; i<3; i++) { // coord
            for (int j=0; j<4; j++) { // moon
                for (int k=0; k<4; k++) { // other moon
                    velocities[j][i] += (positions[j][i] < positions[k][i]) -
                        (positions[j][i] > positions[k][i]);
                }
            }
        }
        for (int i=0; i<12; i++) {
            positions_[i] += velocities_[i];
        }
    }

    for (int i=0; i<3; i++) {
        printf("%d ", positions[0][i]);
    }
    printf("\n");
}
