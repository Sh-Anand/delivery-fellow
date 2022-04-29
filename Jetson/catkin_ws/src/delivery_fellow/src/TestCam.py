if __name__=="__main__":
    import Camera
    import jetson.utils
    c = Camera.Camera('csi://0', 170, 0.5)
    o = jetson.utils.videoOutput()
    while True:
        i = c.Capture()
        o.Render(i)

