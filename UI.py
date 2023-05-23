import PySimpleGUI as sg
from Driving_simulation import *
import numpy as np

sg.theme('Black')
def run_UI():
    layout = [[sg.Text("Vehicle Parameters:", font=("Helvetica", 15, "bold"))],
            [sg.HorizontalSeparator()],
                [sg.Text('Wheelbase: 1.5 m'), sg.Text('trackwidth: 0.5 m')], 
                [sg.Text('COG-position: '), sg.InputText(default_text="45"), sg.Text ("in")], 
                [sg.Text('Vehicle mass: '), sg.InputText(default_text="120"), sg.Text("lbs")],
                [sg.Text('Driver mass: '), sg.InputText(default_text="110"), sg.Text("lbs")],
                [sg.Text('frontal area: '), sg.InputText(default_text='0.36'), sg.Text("m^2")],
                [sg.Text('Drag coefficient: '), sg.InputText(default_text='0.1')], 
                [sg.Text('Powertrain efficiency: '), sg.InputText(default_text='0.9')],
                [sg.Text('Gear ratio: '), sg.InputText(default_text='0.0556')],
                [sg.Text("Wheel Parameters:", font=("Helvetica", 15, "bold"))],
                [sg.HorizontalSeparator()],
                [sg.Text('Toe: '), sg.InputText(default_text="0"), sg.Text ("degrees")], 
                [sg.Text('Camber: '), sg.InputText(default_text="0"), sg.Text("degrees")],
                [sg.Text('Diameter: '), sg.InputText(default_text="20"), sg.Text("inches")],
                [sg.Text("Tire Parameters:", font=("Helvetica", 15, "bold"))],
                [sg.HorizontalSeparator()],
                [sg.Text('Pressure '), sg.InputText(default_text="60"), sg.Text ("psi")],
                [sg.Text('Cornering stiffness coefficients can be found within code')],
                [sg.Text("Engine Parameters:", font=("Helvetica", 15, "bold"))],
                [sg.HorizontalSeparator()],
                [sg.Text('Average BSFC: '), sg.InputText(default_text="0.426"), sg.Text ("Kg/Kwhr")], 
                [sg.Text('Inertia: '), sg.InputText(default_text="0.09"), sg.Text("kg * m^2")],
                [sg.Text('power and torque curves uploaded as csvs')],
                [sg.Text("Competition parameters:", font=("Helvetica", 15, "bold"))],
                [sg.HorizontalSeparator()],
                [sg.Text("track uploaded as csv")],
                [sg.Text("Lower and Upper limit speeds: "), sg.InputText(default_text="15"), sg.InputText(default_text="20"), sg.Text("mph")], 
                [sg.HorizontalSeparator()],
                [sg.Button("Run Simulation")], 
                [sg.Text("mpg: "), sg.Text(size=(10, 1), key="-MPG-"), sg.Text("Average Speed: "), sg.Text(size=(15, 1), key="-AVE-SPEED-")]]

    # Create the window
    window = sg.Window("Eco Simulation", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        print (values.values())
        values = np.array(list(values.values())).astype(float)
        print (values)
        # End program if user closes window or
        if event == "Run Simulation": 
            Eco = Vehicle(values)
            t, x, y, velocities, fuel, total_mpg, ave_velocity = run_simulation(Eco)
            window["-MPG-"].update(total_mpg)
            window["-AVE-SPEED-"].update(ave_velocity)
        if event == sg.WIN_CLOSED:
            break

    window.close()
