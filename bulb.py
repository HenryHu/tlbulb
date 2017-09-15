import json
import urllib.request

call_url_template = "https://wap.tplinkcloud.com/?token=%s&appName=%s" + \
    "&appVer=%s&termID=%s&ospf=%s&netType=%s&locale=%s"

class Bulb(object):
    def __init__(self, token, deviceId, transition=50, appName="Kasa_Android",
                 appVer="1.8.3.674", termID="", ospf="Android%2B7.1.1", netType="wifi",
                 locale="en"):
        self.token = token
        self.deviceId = deviceId
        self.call_url = call_url_template % (
            token, appName, appVer, termID, ospf, netType, locale)
        self.transition = transition
        self.state = None

    def on(self):
        self.request({"on_off": 1})

    def off(self):
        self.request({"on_off": 0})

    def white_mode(self, color_temp=2700):
        self.request({"color_temp": color_temp})

    def color_mode(self):
        self.request({"color_temp": 0})

    def set_brightness(self, brightness=50):
        self.request({"brightness": brightness})

    def set_hue(self, hue=50):
        self.request({"hue": hue})

    def set_saturation(self, sat=50):
        self.request({"saturation": sat})

    def set_transition(self, transition=50):
        self.transition = transition

    def set(self, hue=50, sat=50, brightness=50):
        self.request({"hue": hue, "saturation": sat, "brightness": brightness})

    def request(self, new_state):
        new_state['transition_period'] = self.transition
        requestData = {
            "smartlife.iot.smartbulb.lightingservice": {
                "transition_light_state": new_state
            }
        }

        request = {
            "method":"passthrough",
            "params": {
                "deviceId": self.deviceId,
                "requestData": json.dumps(requestData)
            }
        }

        sReq = json.dumps(request)

        req = urllib.request.Request(self.call_url, sReq.encode('utf-8'), headers = {
            "Content-Type": "application/json"})
        ret = urllib.request.urlopen(req)
        sRet = ret.read().decode('utf-8')

        ret = json.loads(sRet)

        if ret["error_code"] == 0:
            sResp = ret["result"]["responseData"]
            resp = json.loads(sResp)
            state = resp["smartlife.iot.smartbulb.lightingservice"]["transition_light_state"]
            if "on_off" in state:
                self.state = state

    def dump_state(self):
        if self.state["on_off"] == 0:
            print("OFF")
            return

        if "mode" in self.state and self.state["mode"] != "normal":
            print("Mode:", self.state["mode"])
        if "brightness" in self.state:
            print("Brightness:", self.state["brightness"])
        if "color_temp" in self.state and self.state["color_temp"] != 0:
            print("Color temp:", self.state['color_temp'])
        else:
            print("Hue / Sat:", self.state["hue"], self.state["saturation"])
