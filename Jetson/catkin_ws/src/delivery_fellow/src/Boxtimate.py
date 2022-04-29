# a class storing information about the position of a frame as well as its approx velocity
class Boxtimate:

    # det       the detection object (position, type, accuracy)
    # vel       the approximate velocity as a tuple (vx, vy)
    # time      the time of capture

    def __init__(self, detection, vel, time):
        self.det = detection
        self.vel = vel
        self.time = time

    def getNextCenter(self, atTime):
        x2 = self.det.Center[0] + self.vel[0] * (atTime - self.time)
        y2 = self.det.Center[1] + self.vel[1] * (atTime - self.time)
        return (x2, y2)

    def getCenter(self):
        return self.det.Center

    def getArea(self):
        return self.det.Area

    def getHeight(self):
        return self.det.Height

    def getInterOverUnion(self, other, atTime):
        Left = self.det.Left + self.vel[0] * (atTime - self.time)
        Right = self.det.Right + self.vel[0] * (atTime - self.time)
        Top = self.det.Top + self.vel[1] * (atTime - self.time)
        Bottom = self.det.Bottom + self.vel[1] * (atTime - self.time)

        inter = (min(Right, other.Right) - max(Left, other.Left)) * \
                (min(Bottom, other.Bottom) - max(Top, other.Top))
        union = self.det.Area + other.Area - inter
        return 1.0 * inter / union
