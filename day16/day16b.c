#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void printv(int* a) {
    for (int i=0; i<8; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");
}

void compute(int *aa, unsigned int size) {
    //int base_pattern[4] = {0, 1, 0, -1};
    int *b_arr = malloc(sizeof(int) * 6500000);
    if (b_arr == NULL) {
        fprintf(stderr, "couldn't allocate b");
        exit(1);
    }
    memset(b_arr, 0, sizeof(int) * 6500000); // NOLINT
    int *b = b_arr;
    int *a = aa;
    for (unsigned int ni=0; ni<100; ni++) {
        for (unsigned int i=0; i<size; i++) {
            b[i] = 0;
            unsigned int pn = 0;
            int p = 1;
            for (unsigned int j=i; j<size; j++) {
                b[i] += p * a[j];
                pn++;
                if (pn > i) {
                    pn = 0;
                    p = -p;
                    j += i+1;
                }
            }
            b[i] = abs(b[i] % 10);
        }
        int *tmp = b;
        b = a;
        a = tmp;
    }
    if (a != aa) memcpy(aa, a, size); // NOLINT
    free(b_arr);
}

int main() {
    int *a = malloc(sizeof(int) * 6500000);
    if (a == NULL) {
        fprintf(stderr, "couldn't allocate a");
        exit(1);
    }
    char input[] = "59762770781817719190459920638916297932099919336473880209100837309955133944776196290131062991588533604012789279722697427213158651963842941000227675363260513283349562674004015593737518754413236241876959840076372395821627451178924619604778486903040621916904575053141824939525904676911285446889682089563075562644813747239285344522507666595561570229575009121663303510763018855038153974091471626380638098740818102085542924937522595303462725145620673366476987473519905565346502431123825798174326899538349747404781623195253709212209882530131864820645274994127388201990754296051264021264496618531890752446146462088574426473998601145665542134964041254919435635";
    for (int i=0; i<650; i++) {
        for (int j=0; j<10000; j++) {
            a[i+j*650] = input[i] - 48;
        }
    }

    compute(a, 650*10);
    printv(a);
    free(a);
}
