// Author: John Shamoon
#include "include/follower.hpp"

Follower::Follower() : Follower("camera", true) {}

Follower::Follower(std::string camera_name, bool enable_recognition) {
  int time_step = getBasicTimeStep();

  camera_ = std::make_unique<webots::Camera>(camera_name);
  camera_->enable(time_step);

  if (enable_recognition && camera_->hasRecognition()) {
    camera_->recognitionEnable(time_step);
  }

  speed_ = 0;
  cycle_count_ = 0;
}

Follower::~Follower() {}

double Follower::getCameraObjectX() {
  return camera_->getRecognitionObjects()->position[0];
}

double Follower::getCameraObjectZ() {
  // Position values represent where the ego vehicle is in relation to the
  // object. We want to treat it as a distance, so we flip the sign to
  // positive.
  return (-1 * camera_->getRecognitionObjects()->position[2])
             - kCameraMountingOffset;
}

void Follower::controlSpeed() {
  float distance = getCameraObjectZ();

  if (distance < kMinDistance) {
    // If we are too close to the object, significantly decrease speed to the
    // minimum value.
    speed_ = kFollowerMinSpeed;
  } else if ((distance > kMinDistance) &&
             (distance <= kMinDistance + kDistanceBuffer)) {
    // If we are within a specified range from the minimum distance, match the
    // leader vehicle's speed. This will keep the distance between the ego
    // vehicle and leader vehicle the same.
    speed_ = kLeaderMaxSpeed;
  } else {
    // If the ego vehicle is not in the minimum distance for 10 cycles,
    // increase speed by 1kph and reset the cycle counter.
    cycle_count_++;
    if ((cycle_count_ > kMaxCycleLimit) && (speed_ + 1 <= kFollowerMaxSpeed)) {
      speed_++;
      cycle_count_ = 0;
    }
  }
  setCruisingSpeed(speed_);
}

void Follower::follow() {
  // The arctangent returns the angle to the object in radians. Because it is
  // in radians, we need subtract pi / 2 to center the wheel. We flip the sign
  // to consider positive radians as a signal to turn right and negative
  // radians as a signal to turn left.
  float turn_angle = -1 * (atan(getCameraObjectZ() / getCameraObjectX())
                        - (M_PI / 2));
  setSteeringAngle(turn_angle);
  controlSpeed();
}

