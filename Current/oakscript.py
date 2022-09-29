# stereo.setDepthAlign(dai.CameraBoardSocket.RGB)
# camRgb.isp.link(rgbOut.input)

def manualExposure(expTimeMs, sensIso):
    if expTimeMs <= 0: return
    expTimeUs = int(round(expTimeMs * 1000))
    MIN_ISO = 100
    MAX_ISO = 1600
    MIN_EXP_TIME_US = 1
    MAX_EXP_TIME_US = 33000
    assert(sensIso >= MIN_ISO)
    assert(sensIso <= MAX_ISO)
    assert(expTimeUs >= MIN_EXP_TIME_US)
    assert(expTimeUs <= MAX_EXP_TIME_US)
    assert(sensIso > 0)
    ctrl = dai.CameraControl()
    ctrl.setManualExposure(expTimeUs, sensIso)
    qControl.send(ctrl)


def manualFocus(focus):
    if focus < 0: return
    assert(focus >= 0 and focus <= 255)
    ctrl = dai.CameraControl()
    #ctrl.setAutoFocusMode(dai.RawCameraControl.AutoFocusMode.OFF)
    ctrl.setManualFocus(focus)
    qControl.send(ctrl)


def set_fps_and_focus(fps):
    camRgb.setFps(fps)
    videoEnc.setFrameRate(fps)