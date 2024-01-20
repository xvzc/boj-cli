#include <bits/stdc++.h>

#ifdef LOCAL
#define IF_LOCAL if constexpr (true)
#else
#define IF_LOCAL if constexpr (false)
#endif

#define debug IF_LOCAL std::cout << "[DEBUG] "
#define endl '\n'
#define fi first
#define se second
#define all(x) (x).begin(), (x).end()

typedef long long ll;
typedef unsigned long long ull;

using namespace std;

int main() {
  ios_base::sync_with_stdio(false), cin.tie(0);

  int arr[42] = {
    0,
  };

  int temp;
  for (int i = 0; i < 10; ++i) {
    cin >> temp;
    arr[temp % 42]++;
  }

  int answer = 0;
  for (int i = 0; i < 42; ++i) {
    if (arr[i]) answer++;
  }

  cout << answer;

  return 0;
}
