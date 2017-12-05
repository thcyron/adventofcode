#include <iostream>
#include <vector>

int jumps_to_escape_1(std::vector<int> ins) {
  int i = 0;
  int jumps = 0;

  while (i < ins.size()) {
    int n = ins[i];
    ins[i] = ins[i] + 1;
    i += n;
    jumps++;
  }

  return jumps;
}

int jumps_to_escape_2(std::vector<int> ins) {
  int i = 0;
  int jumps = 0;

  while (i < ins.size()) {
    int n = ins[i];
    if (n >= 3) {
      ins[i] = ins[i] - 1;
    } else {
      ins[i] = ins[i] + 1;
    }
    i += n;
    jumps++;
  }

  return jumps;
}

int main() {
  std::vector<int> ins;

  for (;;) {
    std::string line;
    if (!std::getline(std::cin, line)) {
      break;
    }
    ins.push_back(std::stoi(line));
  }

  std::cout << jumps_to_escape_1(ins) << std::endl;
  std::cout << jumps_to_escape_2(ins) << std::endl;
}
