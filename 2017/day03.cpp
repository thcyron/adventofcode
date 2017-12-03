#include <cmath>
#include <iostream>
#include <map>
#include <vector>

struct coord {
  int x;
  int y;
};

struct coord coord_for_number(int s, int n) {
  int br = s * s;               // bottom right
  int bl = s * s - 1 * (s - 1); // bottom left
  int tl = s * s - 2 * (s - 1); // top left
  int tr = s * s - 3 * (s - 1); // top right

  // bottom
  if (n >= bl && n <= br) {
    return {s - (br - n) - 1, 0};
  }

  // left
  if (n >= tl && n <= bl) {
    return {0, bl - n};
  }

  // top
  if (n >= tr && n <= tl) {
    return {tl - n, s - 1};
  }

  // right
  return {s - 1, s - 1 - (tr - n)};
}

int number_for_coord(int s, struct coord c) {
  // bottom
  if (c.y == 0) {
    return s * s - (s - c.x - 1);
  }

  // left
  if (c.x == 0) {
    return s * s - s + 1 - c.y;
  }

  // top
  if (c.y == s - 1) {
    return s * s - 2 * (s - 1) - c.x;
  }

  // right
  if (c.x == s - 1) {
    return s * s - 3 * (s - 1) - (s - c.y - 1);
  }

  // middle
  return number_for_coord(s - 2, {c.x - 1, c.y - 1});
}

int distance_from_center(int n) {
  int s = std::ceil(std::sqrt(n));
  auto c = coord_for_number(s, n);
  struct coord center = {s / 2, s / 2};
  return std::abs(center.x - c.x) + std::abs(center.y - c.y);
}

std::vector<int> adjacent_numbers(int n) {
  std::vector<int> numbers;

  int s = std::ceil(std::sqrt(n));
  if (s % 2 == 0) {
    s++;
  }

  auto c = coord_for_number(s, n);

  for (int x = c.x - 1; x <= c.x + 1; x += 1) {
    for (int y = c.y - 1; y <= c.y + 1; y += 1) {
      if (x == c.x && y == c.y) {
        continue;
      }
      if (x < 0 || y < 0 || x > s - 1 || y > s - 1) {
        continue;
      }
      auto nn = number_for_coord(s, {x, y});
      if (nn < n) {
        numbers.push_back(nn);
      }
    }
  }

  return numbers;
}

int first_value_greater_than(int input) {
  std::map<int, int> value_for_number = {{1, 1}};

  for (int n = 2;; n++) {
    int value = 0;
    for (auto m : adjacent_numbers(n)) {
      auto it = value_for_number.find(m);
      if (it != value_for_number.end()) {
        value += it->second;
      }
    }
    if (value > input) {
      return value;
    }
    value_for_number[n] = value;
  }
}

int main() {
  int input;
  std::cin >> input;

  std::cout << distance_from_center(input) << std::endl;
  std::cout << first_value_greater_than(input) << std::endl;

  return 0;
}
