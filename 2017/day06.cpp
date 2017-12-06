#include <iostream>
#include <map>
#include <sstream>
#include <vector>

int index_to_rebalance(std::vector<int> config) {
  int idx = 0, m = config[0];
  for (int i = 1; i < config.size(); i++) {
    if (config[i] > m) {
      idx = i;
      m = config[i];
    }
  }
  return idx;
}

std::vector<int> rebalance(std::vector<int> config) {
  int idx = index_to_rebalance(config);
  int n = config[idx];
  config[idx] = 0;

  while (n > 0) {
    idx = (idx + 1) % config.size();
    config[idx] += 1;
    n--;
  }

  return config;
}

int main() {
  std::string line;
  std::getline(std::cin, line);

  int n;
  std::istringstream iss(line);
  std::vector<int> config;
  while (iss >> n) {
    config.push_back(n);
  }

  std::map<std::vector<int>, int> seen_configs;
  seen_configs[config] = 0;

  for (int rebalancings = 1;; rebalancings++) {
    config = rebalance(config);
    auto it = seen_configs.find(config);
    if (it != seen_configs.end()) {
      std::cout << rebalancings << std::endl;
      std::cout << (rebalancings - it->second) << std::endl;
      break;
    }
    seen_configs[config] = rebalancings;
  }
}
