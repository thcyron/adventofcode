#include <iostream>

typedef std::function<int(int, int)> next_function;

int captcha(std::string input, next_function nf) {
  int len = input.length();
  int sum = 0;

  for (int i = 0; i < len; i++) {
    char c = input[i];
    char n = input[nf(i, len)];
    if (c == n) {
      sum += c - '0';
    }
  }

  return sum;
}

int main(int argc, char *argv[]) {
  std::string input = argv[1];

  next_function nf1 = [](int i, int len) -> int { return (i + 1) % len; };
  std::cout << captcha(input, nf1) << std::endl;

  next_function nf2 = [](int i, int len) -> int {
    return (i + (len / 2)) % len;
  };
  std::cout << captcha(input, nf2) << std::endl;

  return 0;
}
