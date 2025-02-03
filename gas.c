
#include <stdio.h>
#include "Sensirion/sensirion_gas_index_algorithm.h"

int main() {
     GasIndexAlgorithmParams params;
     GasIndexAlgorithm_init_with_sampling_interval(
          &params,
          GasIndexAlgorithm_ALGORITHM_TYPE_VOC,
          60);

     int32_t sraw, gas_index;
     while (scanf("%d", &sraw) != EOF) {
          GasIndexAlgorithm_process(&params, sraw, &gas_index);
          printf("%d\n", gas_index);
     }
     return 0;
}
