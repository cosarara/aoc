#include <stdio.h>
#include <string.h>

int main() {
    int input[4][3] = {
        {-7, -1, 6},
        {6, -9, -9},
        {-12, 2, -7},
        {4, -17, -12}
    };

    /*
    int input[4][3] = {
        {-1, 0, 2},
        {2, -10, -7},
        {4, -8, 8},
        {3, 5, -1}
    };
    */

    int loops[3];

    for (int i=0; i<3; i++) { // coord
        int initial[4];
        for (int j=0; j<4; j++) initial[j] = input[j][i];
        int positions[4];
        memcpy(positions, initial, sizeof(positions));
        int velocities[4] = {0};
        for (int step=1; step<=1000000; step++) {
            int allzero = 1;
            for (int j=0; j<4; j++) { // planet
                int a = (positions[j] < positions[0]) - (positions[j] > positions[0]) +
                    (positions[j] < positions[1]) - (positions[j] > positions[1]) +
                    (positions[j] < positions[2]) - (positions[j] > positions[2]) +
                    (positions[j] < positions[3]) - (positions[j] > positions[3]);
                velocities[j] += a;
                if (velocities[j]) allzero = 0;
            }
            for (int i=0; i<4; i++) {
                positions[i] += velocities[i];
            }
            if (memcmp(positions, initial, sizeof(positions)) == 0 && allzero) {
                loops[i] = step;
                break;
            }
        }
    }

    printf("%d %d %d\n", loops[0], loops[1], loops[2]);
}
