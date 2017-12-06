#include <iostream>
#include <set>
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

int rebalancings_1(std::vector<int> config) {
  std::set<std::vector<int>> seen_configs;
  seen_configs.insert(config);

  for (int rebalancings = 1;; rebalancings++) {
    config = rebalance(config);
    if (seen_configs.find(config) != seen_configs.end()) {
      return rebalancings;
    }
    seen_configs.insert(config);
  }
}

int rebalancings_2(std::vector<int> config) {
  std::set<std::vector<int>> seen_configs;
  seen_configs.insert(config);

  for (;;) {
    config = rebalance(config);
    if (seen_configs.find(config) != seen_configs.end()) {
      break;
    }
    seen_configs.insert(config);
  }

  auto first_reseen_config = config;

  for (int rebalancings = 1;; rebalancings++) {
    config = rebalance(config);
    if (config == first_reseen_config) {
      return rebalancings;
    }
  }
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

  std::cout << rebalancings_1(config) << std::endl;
  std::cout << rebalancings_2(config) << std::endl;
}
