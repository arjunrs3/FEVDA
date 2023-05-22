import PySimpleGUI as sg
from Driving_simulation import *

layout = [[sg.Text("Run Simulation")], [sg.Button("Run Simulation")], [sg.Text("mpg: "), sg.Text(size=(40, 1), key="-MPG-")]]

# Create the window
window = sg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    if event == "Run Simulation": 
        t, x, y, velocities, fuel, total_mpg, ave_velocity = run_simulation()
        window["-MPG-"].update(total_mpg)
    if event == sg.WIN_CLOSED:
        break

window.close()