import numpy as np
import cv2
from controller import Display, Robot

# time in [ms] of a simulation step
TIME_STEP = 64
MAX_SPEED = 6.28

# create the robot instance.
robot = Robot()

# initialize motors
leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")
leftMotor.setPosition(float("inf"))
rightMotor.setPosition(float("inf"))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# initialize sensors
# enable camera
camera = robot.getDevice("camera1")
camera.enable(TIME_STEP)
# enable range
ranges = robot.getDevice("range-finder")
ranges.enable(TIME_STEP)


# detect blob based on lower_bound and upper_bound values and return x, y
def getBlobPositionInImage(
    image,
    lower_bound,
    upper_bound,
    min_size=500,
    show_mask=False,
    mask_name="blue_objects_mask",
):
    # convert image to HSV
    color = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # get the mask with ranges passed to this function
    mask = cv2.inRange(color, lower_bound, upper_bound)

    if show_mask:
        cv2.imshow(mask_name, mask)

    # find condurs in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # if there is found an condur, find the center otherwise return x, y as zero
    x = -1
    y = -1
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > min_size:
            moments = cv2.moments(largest_contour)
            x = int(moments["m10"] / moments["m00"])
            y = int(moments["m01"] / moments["m00"])

    return x, y


# Function to caputer the camera image, to flip the axes and return it as
# a numoy array
def getCameraImage():
    image = np.asarray(camera.getImageArray(), dtype=np.uint8)
    image = np.reshape(image, (ranges.getHeight(), ranges.getWidth(), 3))
    return image


def getDepthImage():
    image_c_ptr = ranges.getRangeImage(data_type="buffer")
    image_np = np.ctypeslib.as_array(
        image_c_ptr, (ranges.getWidth() * ranges.getHeight(),)
    )
    depth = image_np.reshape(ranges.getHeight(), ranges.getWidth())
    return depth


def showOpenCVImages(image_rgb, depth):
    # Translate to BGR image
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    cv2.imshow("camera", image_bgr)
    cv2.imshow("depth", depth)
    cv2.waitKey(10)


def getRangeAndBearing(obj_x, obj_y, depth):
    obj_r = depth[obj_y, obj_x]
    half_width = camera.getWidth() / 2
    half_fov = camera.getFov() / 2
    obj_b = -half_fov * (obj_x - half_width) / half_width
    return obj_r, obj_b


def getObjectPositionInCamera():
    image = getCameraImage()
    depth = getDepthImage()
    # Display the images in two separate windows
    showOpenCVImages(image, depth)
    # Detect blob by specifying the bounds of color in HSV values
    # Detect blue object
    obj_x_blue, obj_y_blue = getBlobPositionInImage(
        image,
        np.array([70, 50, 50]),
        np.array([100, 255, 255]),
        show_mask=True,
        mask_name="blue_objects_mask",
    )
    # Detect red object
    obj_x_red, obj_y_red = getBlobPositionInImage(
        image,
        np.array([0, 50, 50]),
        np.array([1, 255, 255]),
        show_mask=True,
        mask_name="red_objects_mask",
    )
    # Return position of red or blue object
    if obj_x_blue >= 0 and obj_y_blue >= 0:
        obj_x = obj_x_blue
        obj_y = obj_y_blue
        color = "blue"
    elif obj_x_red >= 0 and obj_y_red >= 0:
        obj_x = obj_x_red
        obj_y = obj_y_red
        color = "red"
    # Returns -1,-1 if no blob detected
    else:
        obj_x = -1
        obj_y = -1
        color = "none"
    return obj_x, obj_y, color


def searchState():
    print("Search state")
    obj_x, obj_y, color = getObjectPositionInCamera()
    if obj_x >= 0 and obj_y >= 0 and color != "none":
        print("Object found")
        return "APPROACH"
    else:
        print("Object not found, search for the object")
        leftSpeed = 0.5 * MAX_SPEED
        rightSpeed = -0.5 * MAX_SPEED
        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)
        return "SEARCH"


def approachState():
    print("Approach state")
    obj_x, obj_y, color = getObjectPositionInCamera()
    if obj_x >= 0 and obj_y >= 0 and color != "none":
        print("Object detected")
        depth = getDepthImage()
        obj_r, obj_b = getRangeAndBearing(obj_x, obj_y, depth)
        if obj_r > 0.2:
            print("  Home in on the object")
            leftSpeed = (0.75 - obj_b) * MAX_SPEED
            rightSpeed = (0.75 + obj_b) * MAX_SPEED
            leftMotor.setVelocity(leftSpeed)
            rightMotor.setVelocity(rightSpeed)
            return "APPROACH"
        elif obj_r <= 0.2 and color == "blue":
            print("  Reached a blue object")
            return "TURN"
        elif obj_r <= 0.2 and color == "red":
            print("  Reached a red object")
            return "TERMINATE"
    else:
        print("Object not found, search for the object")
        return "SEARCH"


def turnState():
    print("Turn state")
    obj_x, obj_y, color = getObjectPositionInCamera()
    if obj_x >= 0 and obj_y >= 0 and color != "none":
        print("Object detected")
        depth = getDepthImage()
        obj_r, obj_b = getRangeAndBearing(obj_x, obj_y, depth)
        if obj_r > 0.2:
            return "APPROACH"
        elif obj_r <= 0.2 and color == "blue":
            print("  Reached a blue object")
            leftSpeed = 0.5 * MAX_SPEED
            rightSpeed = -0.5 * MAX_SPEED
            leftMotor.setVelocity(leftSpeed)
            rightMotor.setVelocity(rightSpeed)
            return "TURN"
        elif obj_r <= 0.2 and color == "red":
            print("  Reached a red object")
            return "TERMINATE"
    else:
        print("Object not found, search for the object")
        return "SEARCH"


def terminateState():
    print("Terminate state")
    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)
    return "TERMINATE"


# Define possible states of the robot
states = {
    "SEARCH": searchState,
    "APPROACH": approachState,
    "TURN": turnState,
    "TERMINATE": terminateState,
}
current_state = "SEARCH"

while robot.step(TIME_STEP) != -1:
    next_state = states[current_state]()
    if next_state in states:
        current_state = next_state
    else:
        print("Unknown state")
        break
