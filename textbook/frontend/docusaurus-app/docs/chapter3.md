---
sidebar_position: 4
---

# Chapter 3: ROS 2 Fundamentals (The Robotic Nervous System)

This chapter introduces the Robot Operating System 2 (ROS 2), an open-source framework designed for developing complex robotic applications. Often referred to as the "robotic nervous system," ROS 2 provides the tools, libraries, and conventions necessary to build modular, distributed, and robust robotic software.

## 3.1 Introduction to ROS 2

**ROS 2** is a flexible framework for writing robot software. It's not an operating system in the traditional sense, but rather a set of software libraries and tools that help in building robot applications. ROS 2 is fundamentally a **distributed system** that allows different processes (nodes) to communicate with each other, often across different machines.

**Why ROS 2?**
ROS 2 emerged as a successor to ROS 1, addressing several key limitations:
*   **Distributed System:** Built on a robust Data Distribution Service (DDS) middleware, allowing for multi-robot systems and better network communication.
*   **Real-time Capabilities:** Designed with quality-of-service (QoS) settings to support real-time control applications.
*   **Security:** Native security features for authentication, encryption, and access control.
*   **Windows and macOS Support:** Improved cross-platform compatibility beyond Linux.
*   **Unified API:** A more consistent API across different programming languages (primarily C++ and Python).

## 3.2 Core Concepts of ROS 2

ROS 2's power comes from its modular and distributed nature, built upon several core communication mechanisms.

### Nodes

A **Node** is an executable process that performs computation. In ROS 2, every functional unit of a robot (e.g., a camera driver, a motor controller, a navigation algorithm) is typically implemented as a separate node. Nodes are designed to be small, single-purpose, and reusable.

### Topics

**Topics** are named buses over which nodes exchange messages asynchronously using a **publish/subscribe** model. A node **publishes** messages to a topic, and any other node **subscribes** to that topic to receive those messages. This is the primary way for nodes to stream data.

#### Code Example: Publisher (Python)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello, ROS 2! %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### Code Example: Subscriber (Python)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Services

**Services** enable synchronous request/response communication between nodes. When a node needs a specific computation from another node and expects an immediate result, it uses a service.

#### Code Example: Service Server (Python)

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # Standard ROS 2 service

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request: a: %d b: %d' % (request.a, request.b))
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    minimal_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### Code Example: Service Client (Python)

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import sys

class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    minimal_client.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' %
        (minimal_client.req.a, minimal_client.req.b, response.sum))
    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Actions

**Actions** are used for long-running tasks that provide periodic feedback and can be cancelled. They are built on topics and services, offering a structured way to handle goals, feedback, and results for complex operations (e.g., moving a robot arm to a specific target, navigating to a distant location).

#### Code Example: Action Server (Python - simplified conceptual)

```python
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci # Standard ROS 2 action

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)
        self.get_logger().info('Fibonacci action server started.')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal: %d' % goal_handle.request.order)
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.sequence.append(feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            self.get_logger().info('Feedback: {0}'.format(feedback_msg.sequence))
            goal_handle.publish_feedback(feedback_msg)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info('Goal succeeded.')
        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
    fibonacci_action_server.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### Code Example: Action Client (Python - simplified conceptual)

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci
import time

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.sequence))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info('Received feedback: {0}'.format(feedback_msg.feedback.sequence))

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()
    action_client.send_goal(10) # Request 10th Fibonacci number
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```

### Parameters

**Parameters** are dynamic configuration values for nodes. They allow you to change a node's behavior without recompiling the code. Parameters can be set at runtime, loaded from YAML files, or modified using command-line tools.

## 3.3 ROS 2 Architecture and Middleware (DDS)

At the heart of ROS 2's distributed communication is the **Data Distribution Service (DDS)**, an open standard for real-time, peer-to-peer data exchange.

*   **DDS:** Provides a robust, scalable, and real-time data connectivity framework. It handles discovery, serialization, transport, and delivery of messages.
*   **RMW (ROS Middleware Interface):** ROS 2 uses an abstraction layer called the ROS Middleware Interface (RMW), which allows it to swap out different DDS implementations (e.g., Fast RTPS, Cyclone DDS, RTI Connext) without changing the ROS 2 application code.
*   **Communication Graph:** The collection of all nodes, topics, services, and actions, and their connections, forms the ROS 2 communication graph. This graph is dynamic; nodes can come and go, and connections are established automatically through DDS discovery.

## 3.4 Development Tools and Workflow

Developing with ROS 2 involves a specific set of tools and a structured workflow.

### Workspaces

A **ROS 2 workspace** is a directory that contains one or more ROS 2 packages. It's typically named `colcon_ws` (for `colcon` build tool).

### Packages

A **package** is the fundamental unit of organization in ROS 2. It contains all the necessary files for a module: source code, message definitions, launch files, configuration files, and a `package.xml` manifest.

*   **`package.xml`:** A manifest file that describes the package, including its name, version, description, maintainers, and most importantly, its dependencies.

### Build System

**`colcon`** is the primary build tool for ROS 2. It orchestrates the building of multiple packages in a workspace.

```bash
# Build all packages in the current workspace
colcon build

# Build a specific package
colcon build --packages-select my_package

# Install dependencies (using rosdep)
rosdep install --from-paths src --ignore-src -r -y
```

### Command Line Tools

ROS 2 provides a rich set of command-line tools for inspecting and interacting with a running system.

*   `ros2 run <package_name> <executable_name>`: Runs an executable from a package.
*   `ros2 topic list`: Lists active topics.
*   `ros2 topic echo <topic_name>`: Displays messages being published on a topic.
*   `ros2 node list`: Lists active nodes.
*   `ros2 service list`: Lists available services.
*   `ros2 param list`: Lists parameters exposed by nodes.
*   `ros2 launch <package_name> <launch_file_name>`: Starts a system using a launch file.

## 3.5 Message Types and Custom Messages

Messages are the data structures used for communication in ROS 2.

### Standard Message Types

ROS 2 provides a set of common message types for basic data (e.g., `std_msgs/String`, `std_msgs/Int32`) and robotic primitives (e.g., `geometry_msgs/Twist` for linear/angular velocity, `sensor_msgs/Image` for camera images).

### Custom Message Definition

You can define your own custom messages, services, and actions when standard types are insufficient. These are defined in `.msg`, `.srv`, and `.action` files within a package.

#### Code Example: `MyCustomMessage.msg`

Create a file `msg/MyCustomMessage.msg` in your package:

```
string header
float32 temperature
string[] status_messages
```

#### Code Example: `package.xml` Update

Add build and run dependencies for custom messages:

```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

#### Code Example: `CMakeLists.txt` Update

Enable message generation in `CMakeLists.txt`:

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/MyCustomMessage.msg"
  "srv/MyCustomService.srv"  # if you had a custom service
  "action/MyCustomAction.action" # if you had a custom action
)
```

After defining custom messages and updating `package.xml` and `CMakeLists.txt`, you need to rebuild your workspace.

## 3.6 Launching ROS 2 Systems

For complex robotic systems with many nodes, manual startup can be tedious. **Launch files** provide a convenient way to define and run a collection of nodes, set parameters, and manage their relationships. They can be written in XML or Python.

#### Code Example: Simple Python Launch File (`my_robot_launch.py`)

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='minimal_publisher',
            name='my_publisher',
            output='screen',
            parameters=[{'timer_period': 1.0}] # Example of setting a parameter
        ),
        Node(
            package='my_package',
            executable='minimal_subscriber',
            name='my_subscriber',
            output='screen'
        ),
        Node(
            package='my_package',
            executable='minimal_service',
            name='my_service_server',
            output='screen'
        ),
    ])
```

To run this launch file:
```bash
ros2 launch my_package my_robot_launch.py
```

## 3.7 Simulation with Gazebo and RViz

Simulation is a crucial part of robotics development, allowing testing and debugging in a safe, controlled environment.

*   **Gazebo:** A powerful 3D physics simulator. It allows you to create virtual worlds, simulate robot models (with sensors and actuators), and interact with them as if they were real. ROS 2 provides integration packages (`ros_gz_sim`) to bridge Gazebo with the ROS 2 communication graph.
*   **RViz:** The ROS Visualization tool. It's not a simulator but a visualization framework for 3D data. RViz can display sensor data (e.g., camera images, LiDAR scans), robot models (URDF), navigation paths, and more, helping developers understand what their robot perceives and how it plans to act.

## 3.8 Case Study: Building a Simple ROS 2 Robot (Conceptual)

Imagine building a simple wheeled robot for indoor navigation.

1.  **Hardware Interface Node:** A node written in C++ or Python that communicates directly with the robot's motors and encoders (using low-level drivers). It publishes wheel odometry (position) and subscribes to velocity commands.
2.  **Lidar Sensor Node:** A node that interfaces with a LiDAR sensor, publishing scan data on a `/scan` topic.
3.  **Navigation Stack Nodes:** A collection of pre-existing ROS 2 navigation nodes that subscribe to `/scan` (LiDAR), `/odom` (odometry), and `/goal_pose` (target location), and publish velocity commands to the hardware interface node.
4.  **Teleoperation Node:** A simple node that subscribes to keyboard inputs and publishes velocity commands for manual control.
5.  **Launch File:** An overarching launch file to bring up all these nodes simultaneously, configure their parameters, and establish the communication graph.

This modular approach, facilitated by ROS 2, allows different teams or developers to work on separate components concurrently, integrating them seamlessly into a functional robotic system.

## Key Concepts

| Term              | Definition                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| **ROS 2**         | Robot Operating System 2, an open-source framework for robotic software development.                         |
| **Node**          | An executable process in ROS 2 that performs computation.                                                    |
| **Topic**         | A named data bus for asynchronous, publish/subscribe message exchange.                                       |
| **Service**       | A synchronous request/response communication mechanism between nodes.                                        |
| **Action**        | A communication pattern for long-running tasks with goals, feedback, and results.                            |
| **DDS**           | Data Distribution Service, the underlying middleware for ROS 2 communication.                                |
| **RMW**           | ROS Middleware Interface, an abstraction layer for different DDS implementations.                            |
| **`colcon`**      | The build tool used for ROS 2 packages and workspaces.                                                       |
| **`package.xml`** | A manifest file describing a ROS 2 package and its dependencies.                                             |
| **`ros2 launch`** | A command-line tool for starting complex ROS 2 systems using launch files.                                   |
| **Gazebo**        | A powerful 3D physics simulator for robotic systems.                                                         |
| **RViz**          | ROS Visualization, a 3D visualization tool for displaying robot data and models.                             |
