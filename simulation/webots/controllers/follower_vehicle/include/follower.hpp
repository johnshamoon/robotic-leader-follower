#ifndef FOLLOWER_H
#define FOLLOWER_H
#include <cmath>
#include <memory>
#include <string>

#include <webots/DistanceSensor.hpp>
#include <webots/vehicle/Driver.hpp>
#include <webots/Camera.hpp>

/**
 * Follower class to make a vehicle follow another one.
 *
 * Inherits from webots::Driver to provide the vehicle control API. Requires
 * that a vehicle be equipped with a camera mounted at the front of the
 * vehicle.
 */
class Follower : public webots::Driver {
  public:
    /**
     * Default constructor.
     *
     * Provides the camera with a default name of "camera" and enables image
     * recognition by default.
     *
     * @return A Follower object.
     */
    Follower();
    /**
     * Constructor.
     *
     * @param camera_name Name of defined in Webots world.
     * @param enable_recognition Enables camera image recognition.
     *
     * @return A Follower object.
     */
    Follower(std::string camera_name, bool enable_recognition);
    /**
     * Destructor.
     */
    ~Follower();

    /**
     * Follows the detected object.
     *
     * Should be called in the main loop of the Webots controller.
     */
    void follow();
  private:
    /**
     * Gets the camera object's distance on the x-axis
     *
     * A positive value means that the object is to the right of the ego
     * vehicle. A negative value means that the object is to the left of the
     * ego vehicle. A value of zero means that the object is directly in front
     * of the ego vehicle.
     *
     * @return double Object's distance on the x-axis.
     */
    double getCameraObjectX();
    /**
     * Gets the camera object's distance on the z-axis
     *
     * The distance on the z-axis is how far the oject is in front of the ego
     * vehicle.
     *
     * @return double Object's distance on the z-axis.
     */
    double getCameraObjectZ();

    /**
     * Controls the speed of the ego vehicle.
     *
     * Keeps a distance between kMinDistance and kMaxDistance.
     */
    void controlSpeed();
    /** Camera mounted at the front of the vehicle. */
    std::unique_ptr<webots::Camera> camera_;

    // Leader's maximum speed in kph.
    static constexpr float kLeaderMaxSpeed = 15;
    // Follower's maximum speed in kph.
    static constexpr float kFollowerMaxSpeed = kLeaderMaxSpeed + 5;
    // Follower's minimum speed.
    static constexpr float kFollowerMinSpeed = 0;
    // The length of a Tesla Model 3
    static constexpr float kCarLength = 4.7;
    // Distance buffer to keep the ego vehicle in range of the leader vehicle.
    static constexpr float kDistanceBuffer = 0.5;
    // Minimum distance to be fron the leader vehicle.
    static constexpr float kMinDistance = kCarLength / 2;
    // Camera's mounting offset on the ego vehicle.
    static constexpr float kCameraMountingOffset = 2.5;
    // Maximum cycle limit before accelerating.
    static constexpr int kMaxCycleLimit = 10;

    // The ego vehicle's speed.
    float speed_;
    // The ego vehicle's current cycle count.
    float cycle_count_;
};

#endif
