#include <stdio.h>
#include <string.h>

int main() {
    int slowpos[4][3] = {
        {-7, -1, 6},
        {6, -9, -9},
        {-12, 2, -7},
        {4, -17, -12}
    };
    int* slowpos_ = &slowpos[0][0];
    int fastpos[4][3] = {
        {-7, -1, 6},
        {6, -9, -9},
        {-12, 2, -7},
        {4, -17, -12}
    };
    int* fastpos_ = &fastpos[0][0];

    int fastvel[4][3] = {0};
    int slowvel[4][3] = {0};
    int* fastvel_ = &fastvel[0][0];
    int* slowvel_ = &slowvel[0][0];

    long unsigned int step = 0;
    for (; step<10000000000lu; step++) {
        // slow
        for (int i=0; i<3; i++) { // coord
            for (int j=0; j<4; j++) { // planet
                int a = (slowpos[j][i] < slowpos[0][i]) - (slowpos[j][i] > slowpos[0][i]) +
                    (slowpos[j][i] < slowpos[1][i]) - (slowpos[j][i] > slowpos[1][i]) +
                    (slowpos[j][i] < slowpos[2][i]) - (slowpos[j][i] > slowpos[2][i]) +
                    (slowpos[j][i] < slowpos[3][i]) - (slowpos[j][i] > slowpos[3][i]);
                slowvel[j][i] += a;
            }
        }
        for (int i=0; i<12; i++) {
            slowpos_[i] += slowvel_[i];
        }
        // fast 1
        for (int i=0; i<3; i++) { // coord
            for (int j=0; j<4; j++) { // planet
                int a = (fastpos[j][i] < fastpos[0][i]) - (fastpos[j][i] > fastpos[0][i]) +
                    (fastpos[j][i] < fastpos[1][i]) - (fastpos[j][i] > fastpos[1][i]) +
                    (fastpos[j][i] < fastpos[2][i]) - (fastpos[j][i] > fastpos[2][i]) +
                    (fastpos[j][i] < fastpos[3][i]) - (fastpos[j][i] > fastpos[3][i]);
                fastvel[j][i] += a;
            }
        }
        for (int i=0; i<12; i++) {
            fastpos_[i] += fastvel_[i];
        }
        // fast 2
        for (int i=0; i<3; i++) { // coord
            for (int j=0; j<4; j++) { // planet
                int a = (fastpos[j][i] < fastpos[0][i]) - (fastpos[j][i] > fastpos[0][i]) +
                    (fastpos[j][i] < fastpos[1][i]) - (fastpos[j][i] > fastpos[1][i]) +
                    (fastpos[j][i] < fastpos[2][i]) - (fastpos[j][i] > fastpos[2][i]) +
                    (fastpos[j][i] < fastpos[3][i]) - (fastpos[j][i] > fastpos[3][i]);
                fastvel[j][i] += a;
            }
        }
        for (int i=0; i<12; i++) {
            fastpos_[i] += fastvel_[i];
        }
        // check
        if (memcmp(slowpos, fastpos, sizeof(slowpos)) == 0) {
            break;
        }
    }

    printf("%lu\n", step);

    for (int i=0; i<3; i++) {
        printf("%d ", slowpos[0][i]);
    }
    printf("\n");
}
