#include <algorithm>
#include <iostream>
#include <map>
#include <sstream>
#include <vector>

void rebalance(std::vector<int> &config) {
  auto it = std::max_element(config.begin(), config.end());
  auto idx = it - config.begin();
  auto n = config[idx];

  config[idx] = 0;

  while (n-- > 0) {
    idx = (idx + 1) % config.size();
    config[idx] += 1;
  }
}

int main() {
  std::string line;
  std::getline(std::cin, line);

  std::vector<int> config;

  int n;
  std::istringstream iss(line);
  while (iss >> n) {
    config.push_back(n);
  }

  std::map<std::vector<int>, int> seen_configs = {{config, 0}};

  for (;;) {
    rebalance(config);

    auto s = seen_configs.size();
    auto it = seen_configs.find(config);

    if (it != seen_configs.end()) {
      std::cout << s << std::endl;
      std::cout << (s - it->second) << std::endl;
      break;
    }

    seen_configs[config] = s;
  }
}
