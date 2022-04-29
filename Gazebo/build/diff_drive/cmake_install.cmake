# Install script for directory: /home/shashank/ARMS/delivery-fellow/Gazebo/src/diff_drive

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/shashank/ARMS/delivery-fellow/Gazebo/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/diff_drive/action" TYPE FILE FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/src/diff_drive/action/GoToPose.action")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/diff_drive/msg" TYPE FILE FILES
    "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/diff_drive/msg/GoToPoseAction.msg"
    "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/diff_drive/msg/GoToPoseActionGoal.msg"
    "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/diff_drive/msg/GoToPoseActionResult.msg"
    "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/diff_drive/msg/GoToPoseActionFeedback.msg"
    "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/diff_drive/msg/GoToPoseGoal.msg"
    "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/diff_drive/msg/GoToPoseResult.msg"
    "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/diff_drive/msg/GoToPoseFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/diff_drive" TYPE PROGRAM FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_drive_odometry")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/diff_drive" TYPE PROGRAM FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_drive_controller")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/diff_drive" TYPE PROGRAM FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_drive_go_to_goal")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/diff_drive" TYPE PROGRAM FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_drive_mock_robot")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/diff_drive/cmake" TYPE FILE FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_drive-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/include/diff_drive")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/roseus/ros/diff_drive")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/common-lisp/ros/diff_drive")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/share/gennodejs/ros/diff_drive")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/home/shashank/.pyenv/shims/python3" -m compileall "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/lib/python3.8/site-packages/diff_drive")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3.8/site-packages" TYPE DIRECTORY FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/lib/python3.8/site-packages/diff_drive" REGEX "/\\_\\_init\\_\\_\\.py$" EXCLUDE REGEX "/\\_\\_init\\_\\_\\.pyc$" EXCLUDE)
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3.8/site-packages" TYPE DIRECTORY FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/lib/python3.8/site-packages/diff_drive" FILES_MATCHING REGEX "/home/shashank/ARMS/delivery-fellow/Gazebo/devel/lib/python3.8/site-packages/diff_drive/.+/__init__.pyc?$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_drive.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/diff_drive/cmake" TYPE FILE FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_drive-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/diff_drive/cmake" TYPE FILE FILES
    "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_driveConfig.cmake"
    "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive/catkin_generated/installspace/diff_driveConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/diff_drive" TYPE FILE FILES "/home/shashank/ARMS/delivery-fellow/Gazebo/src/diff_drive/package.xml")
endif()

