#include <iostream>
#include <map>
#include <sstream>

bool is_valid_1(std::string phrase) {
  std::map<std::string, bool> words;
  std::istringstream iss(phrase);
  std::string word;

  while (iss >> word) {
    auto it = words.find(word);
    if (it != words.end()) {
      return false;
    }
    words[word] = true;
  }
  return true;
}

bool is_valid_2(std::string phrase) {
  std::map<std::string, bool> words;
  std::istringstream iss(phrase);
  std::string word;

  while (iss >> word) {
    std::sort(word.begin(), word.end());
    auto it = words.find(word);
    if (it != words.end()) {
      return false;
    }
    words[word] = true;
  }
  return true;
}

int main() {
  int valid1 = 0;
  int valid2 = 0;

  for (;;) {
    std::string line;
    if (!std::getline(std::cin, line)) {
      break;
    }
    if (is_valid_1(line)) {
      valid1++;
    }
    if (is_valid_2(line)) {
      valid2++;
    }
  }

  std::cout << valid1 << std::endl;
  std::cout << valid2 << std::endl;
}
