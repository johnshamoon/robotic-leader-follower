#include "include/follower.hpp"
#include <memory>

#define END_SIMULATION -1

int main(int argc, char** argv) {
  std::unique_ptr<Follower> follower = std::make_unique<Follower>();

  while (follower->step() != END_SIMULATION) {
    follower->follow();
  }

  return 0;
}
