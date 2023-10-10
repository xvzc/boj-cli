#include <bits/stdc++.h>

#define endl '\n'
#define fi first
#define se second
#define all(x) (x).begin(), (x).end()
#define debug \
  if constexpr (IS_LOCAL) std::cout

#ifdef LOCAL
constexpr bool IS_LOCAL = true;
#else
constexpr bool IS_LOCAL = false;
#endif

typedef long long ll;
typedef unsigned long long ull;

using namespace std;

/* Authored by xvzc, 2023-10-08 17:54:13 */
int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(0);

  if constexpr (IS_LOCAL) (void)!freopen("input.txt", "r", stdin);
  int m1[100][100] = {
      0,
  };

  int m2[100][100] = {
      0,
  };

  int n, m; cin >> n >> m;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      cin >> m1[i][j];
    }
  }

  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
      cin >> m2[i][j];
      m2[i][j] += m1[i][j];
      cout << m2[i][j] << ' ';
    }
    cout << endl;
  }

  return 0;
}
