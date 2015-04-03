#include <stdio.h>

FILE* fp;

void mask_32byte(char* out, int pos) {
    unsigned char buf[32] = {0, };

    int idx = 0, i, j, n, bit;

    fseek(fp, pos, SEEK_SET);
    fread(buf, 1, 32, fp);

    for(i = 0 ; i < 32 ; i++) {
        n = buf[i];

        for(j = 7 ; j >= 0 ; j--) {
            bit = n >> j & 1;

            if(bit == 1) out[idx] = 1;

            idx++;
        }
    }
}

void draw_korean(int cho, int jung, int jong) {
    int CHO_IDX = 0;
    int JUNG_IDX = CHO_IDX + 32 * 19 * 8;
    int JONG_IDX = JUNG_IDX + 32 * 21 * 4;

    int CHO_MAP[] = {
        0, 0, 0, 0, 0, 0, 0, 0, 1, 3,
        3, 3, 1, 2, 4, 4, 4, 2, 1, 3,
        0
    };

    int JONG_MAP[] = {
        0, 2, 0, 2, 1, 2, 1, 2, 3, 0,
        2, 1, 3, 3, 1, 2, 1, 3, 3, 1,
        1
    };

    int CHO_TYPE = -1;
    int JUNG_TYPE = -1;
    int JONG_TYPE = -1;

    char out[256] = {0, };

    int i;

    CHO_TYPE = CHO_MAP[jung];

    if(jong != 0) {
             if(CHO_TYPE == 0) CHO_TYPE = 5;
        else if(CHO_TYPE == 1) CHO_TYPE = 6;
        else if(CHO_TYPE == 2) CHO_TYPE = 6;
        else if(CHO_TYPE == 3) CHO_TYPE = 7;
        else if(CHO_TYPE == 4) CHO_TYPE = 7;
    }

    JUNG_TYPE = (cho == 0 || cho == 16) ? 0 : 1;
    JUNG_TYPE += (jong != 0) ? 2 : 0;

    JONG_TYPE = JONG_MAP[jung];

    mask_32byte(out, CHO_IDX + (32 * 19 * CHO_TYPE) + (32 * cho));

    mask_32byte(out, JUNG_IDX + (32 * 21 * JUNG_TYPE) + (32 * jung));

    if(jong != 0)
        mask_32byte(out, JONG_IDX + (32 * 27 * JONG_TYPE) + (32 * (jong - 1)));

    for(i = 0 ; i < 256 ; i++) {
        if(out[i] == 1)
            printf(" *");
        else
            printf("  ");

        if(i % 16 == 15)
            printf("\n");
    }
}

int main() {
    int cho = 0;
    int jung = 0;
    int jong = 1;

    fp = fopen("gulim16.hex", "rb");

    draw_korean(cho, jung, jong);

    fclose(fp);

    return 0;
}
