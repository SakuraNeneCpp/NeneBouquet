# 並列プログラミングをしよう

```cpp
#include <time.h>
#include <NeneMath/FiniteField.hpp>
#include <NeneMath/LinearAlgebra.hpp>
#include <NeneIcecream/NeneIcecream.hpp>

#include <omp.h>

using GF256 = uint8GF256<>;
using matrix = Matrix<GF256>;

matrix random_matrix(int r, int c, uint64_t seed){
    return matrix(r, c, GF256::random_vec_mt(r*c, seed));
}

int main(){
    omp_set_dynamic(0);      // 動的調整OFF(念のため)
    omp_set_num_threads(10); // スレッド数設定(書かなければ使用可能な最大スレッドで動作する)
    clock_t start = clock();
    #pragma omp parallel for
    for(int i=0; i<1000; i++){
        matrix A = random_matrix(100, 100, i);
        matrix B = random_matrix(100, 100, i+1);
        matrix C = A*B;
        GF256 detC = C.det();
    }
    clock_t end = clock();
    const double time = static_cast<double>(end - start) / CLOCKS_PER_SEC;
    ic(time);
}
```

`#include <omp.h>`を書いて, 並列処理したいfor文の直前に`#pragma omp parallel for`と追加するだけ.

```cmake
find_package(OpenMP REQUIRED)
target_link_libraries(your_target PRIVATE OpenMP::OpenMP_CXX)
```

cmakeにもOpenMPを追加する.