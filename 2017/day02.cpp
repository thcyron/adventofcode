#include <iostream>
#include <sstream>
#include <vector>

std::vector<int> numbers_in_row(std::string row) {
  std::istringstream iss(row);
  std::string number;
  std::vector<int> numbers;

  while (iss >> number) {
    numbers.push_back(std::stoi(number));
  }

  return numbers;
}

int max_min_diff(std::vector<int> numbers) {
  int min, max;
  min = max = numbers[0];
  for (int n : numbers) {
    if (n < min) {
      min = n;
    }
    if (n > max) {
      max = n;
    }
  }
  return max - min;
}

int quot_of_evenly_divisible(std::vector<int> numbers) {
  for (int n : numbers) {
    for (int m : numbers) {
      if (m >= n) {
        continue;
      }
      if (n % m == 0) {
        return n / m;
      }
    }
  }
  return -1;
}

int main(int argc, char *argv[]) {
  std::vector<std::string> rows;

  for (;;) {
    std::string line;
    if (!std::getline(std::cin, line)) {
      break;
    }
    rows.push_back(line);
  }

  int sum1 = 0;
  int sum2 = 0;

  for (auto row : rows) {
    sum1 += max_min_diff(numbers_in_row(row));
    sum2 += quot_of_evenly_divisible(numbers_in_row(row));
  }

  std::cout << sum1 << std::endl;
  std::cout << sum2 << std::endl;

  return 0;
}
