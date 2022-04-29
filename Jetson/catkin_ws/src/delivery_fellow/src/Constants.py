MAX_MOTORS = 2000
MIN_MOTORS = 0
MAX_SPEED = 20

TOPIC = "cmd_vel"
TICKS_PER_METER = 25
WHEEL_SEPARATION = 1

ADJUST_SPEED = 7
ADJUST_TURN = 6

CAMERA_MAX_TURN_ANGLE = 1.34
CAMERA_MAX_TWIST_ANGULAR = 0.5
CAMERA_MAX_SIZE = 0.0014
CAMERA_MIN_SIZE = 0.0007
CAMERA_MAX_LINEAR = 0.35
CAMERA_DEADZONE = 0.07

TWIST_BACK_CORRECTION = 0.001

## AUTOFOLLOW

DETECT_MODEL_NAME = "ssd-inception-v2"  # the name of NN that is used to detect objects in AutoFollow           [ssd-mobilenet-v1,  ssd-mobilenet-v2,   ssd-inception-v2,   pednet,     multiped    ]
DETECT_MODEL_PERSON_ID = 1              # id of person in the used NN.                                          [1,                 1,                  1,                  0,          0           ]
DETECT_MODEL_PROBABILITY = 0.4          # the minimum probability for detect to pass as a person

TIMEOUT_NEW_PERSON = 10                 # time from last seeing the target to accepting new people
TIMEOUT_BEFORE_RECHECK = 1e10           # how often should the algorithm verify if the person is correct (useless?)
TIMEOUT_BLIND_GUESS = 1.5               # how long will the robot continue to show steering info without actually seeing the person
MULTIP_BLIND_GUESS = 0.4                # when blind guessing, return smaller steering angle by this multipier

THRESHOLD_BBOX_SIMILARITY = 0.5         # (higher => more similar) limit on bounding box similarity
THRESHOLD_BBOX_MIN_SIZE = 0.015         # min size for the detection to be allowed to pass as human

HIST_CROP_TOP = 0.1                     # % cut from the TOP edge when making histograms
HIST_CROP_BOTTOM = 0.3                  # % cut from the BOTTOM edge when making histograms
HIST_CROP_LEFT = 0.15                   # % cut from the LEFT edge when making histograms
HIST_CROP_RIGHT = 0.15                  # % cut from the RIGHT edge when making histograms
HIST_CREATE_METHOD = 1                  # 
HIST_COMPARE_METHOD = 1                 # 
THRESHOLD_HIST_SIMILARITY_NEW = 0.7     # (higher => more similar) limit on histogram similarity
THRESHOLD_HIST_SIMILARITY_NEXT = 0.5    # (higher => more similar) limit on histogram similarity
WORLD_HIST_MULTIP = 0.75                # world histogram subtraction multipier

NEXT_VEL_RATIO = 0.2                    # ratio between old and *new* approximate velocity when taking over
NEXT_HIST_RATIO = 0.6                   # ratio between old and *new* histogram when taking over
NEXT_WORLD_RATIO = 0.25

## HISTOGRAM VALUES THAT WORKED WELL
# [cr0 co0 nw0.7 nx0.4 wm0.4] decent
