'''
greenhouse-iot-system
Author: Efraim Manurung
MSc Thesis in Information Technology Group, Wageningen University

efraim.efraimpartoginahotasi@wur.nl
efraim.manurung@gmail.com

Refactor main program with finite state machine
'''

def setPointsState():
    print("Set points state")
    return "MONITOR"

def monitorState():
    print("Monitor state")
    return "ACTUATE"

def actuateState():
    print("Actuate state")
    return "TERMINATE"
    
def terminateState():
    print("Terminate state")
    return "MONITOR"

# Define possible states of the system
states = {
    "SETPOINTS": setPointsState,
    "MONITOR": monitorState,
    "ACTUATE": actuateState,
    "TERMINATE": terminateState
}
current_state = "MONITOR"

while True:
    next_state = states[current_state]()
    if next_state in states:
        current_state = next_state
    else:
        print("Unknown state")
        break

