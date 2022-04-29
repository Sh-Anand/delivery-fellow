#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/shashank/ARMS/delivery-fellow/Gazebo/src/diff_drive"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/shashank/ARMS/delivery-fellow/Gazebo/install/lib/python3.8/site-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/shashank/ARMS/delivery-fellow/Gazebo/install/lib/python3.8/site-packages:/home/shashank/ARMS/delivery-fellow/Gazebo/build/lib/python3.8/site-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/shashank/ARMS/delivery-fellow/Gazebo/build" \
    "/home/shashank/.pyenv/shims/python3" \
    "/home/shashank/ARMS/delivery-fellow/Gazebo/src/diff_drive/setup.py" \
     \
    build --build-base "/home/shashank/ARMS/delivery-fellow/Gazebo/build/diff_drive" \
    install \
    --root="${DESTDIR-/}" \
     --prefix="/home/shashank/ARMS/delivery-fellow/Gazebo/install" --install-scripts="/home/shashank/ARMS/delivery-fellow/Gazebo/install/bin"
