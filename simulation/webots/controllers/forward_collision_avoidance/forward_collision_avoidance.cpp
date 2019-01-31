#include <webots/DistanceSensor.hpp>
#include <webots/vehicle/Driver.hpp>

#define END_SIMULATION -1
#define FIVE_METERS 5

using namespace webots;

int main(int argc, char** argv) {
  Driver* egoVehicle = new Driver();
  DistanceSensor* distanceSensor = new DistanceSensor("distance sensor");

  // Get the cycle time for this world (in ms).
  int timeStep = (int) egoVehicle->getBasicTimeStep();

  distanceSensor->enable(timeStep);

  // Accelerate to 20 kph.
  egoVehicle->setCruisingSpeed(20);

  // Main loop: perform simulation steps until Webots stops the controller.
  // Drive straight until there is an object at most 5 meters ahead, then stop.
  while (egoVehicle->step() != END_SIMULATION) {
    if (distanceSensor->getValue() <= FIVE_METERS) {
      egoVehicle->setCruisingSpeed(0);
      break;
    }
  }

  delete egoVehicle;
  delete distanceSensor;

  return 0;
}
