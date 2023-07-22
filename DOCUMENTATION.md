# Documentation
Code documentation for FEVDA, last updated 7/22/2023 
## Tire modeling 
### Files: 
- Scripts/tires.py
- Utils/helper_functions.py
### Inputs: 
- Turning radius (or None if straight)
- Vehicle Velocity
- Tire radius
- Cornering stiffnesses
- Rolling resistance coefficients
- Camber
- Toe
### Returns: 
- Longitudinal drag force on the tires (normal force is calculated during he timestepping procedure)
### Methodology: 
- Populate tire parameters:
  - get rolling resistance coefficient as a function of camber using helper_functions/get_RRcoeff
  - get cornering stiffnesses as a function of pressure using helper_functions/get_cornering_stiffness
  - get normal forces on each tire using helper_functions/get_base_normal
- If turning
  - Use tire parameters to solve the eight equations of Pacejka's magic formula (see func in tires/get_turning_values
  - return the longitudinal tire drag as found by the solution to these equations
  - currently, the centripetal force determines the tire force towards the center of the turn but it can also be extracted from this solution
- If going straight
  - Get the longitudinal drag on each tire using helper_functions/get_f_longitudinal
    - Simply the normal force multiplied by the rolling resistance coefficient
  - If there is any toe, the longitudinal force is scaled by the cosine of the toe angle, and the cornering stiffness is multiplied by the angle of turn
    - Assumes that the wheels with toe have the same drag as a wheel turning at the same sideslip angle.
### Assumptions: 
- No tire slip (will need to be validated later)
- no shifting of normal forces during turns (bicycle model combines the two front wheels into one effective front wheel)
- Pacejka's magic formula applicable for these types of tires (this is what PAC car used in their analysis)
## Aero modeling
### File: 
- Scripts/aero.py
### Inputs: 
- Coefficient of drag
- Frontal Area
- Vehicle Velocity
### Returns: 
- Aerodynamic drag force acting on the car
### Methodology: 
- uses definition of drag force to return 1/2 * rho * v ** 2 * Cd * frontal_area
## Engine modeling
### Files: 
- Scripts/engine.py
- Utils/helper_functions.py
### Inputs: 
- Torque Polynomial curve (csv file)
- Power Polynomial curve (csv file)
  - For the Honda GX50, webplotdigitizer was used to convert this image into csv files for the torque and power polynomials
    ![torque and power polynomials for the Honda GX 50](https://www.honda-engines-eu.com/files/images/1800x_/powercurve-gx50-big.jpg)
- BSFC (Brake specific fuel consumption)
- Fuel density
- Vehicle velocity
### Returns: 
- Engine force
- Volumetric fuel flow rate
### Methodology: 
- Obtains the engine RPM using the vehicle velocity and wheel RPM
- Get the propulsive force by obtaining the torque from the torque csv and propogating it through the drivetrain
- Get the operating power using the power csv
- Obtain volumetric flow rate by power * BSFC / fuel_density
### Assumptions: 
- No wheel slip (likely will need to be validated)
- Constant BSFC (likely a reasonable assumption)
- Engine RPM a function of wheel RPM (needs to be validated)
## Battery model 
Not yet implemented
## Mission modeling
### Files:
- new_step.py
- vehicle_setup.py
- Scripts/tires.py
- Scripts/aero.py
- Scripts.engine.py
- Scripts/misc.py
### Inputs:
- Vehicle
 - Contains dynamical information delineated in separate modules
- Track
  - Contains linear distance for straight maneuvers; radius for turns
- Initial Orientation
  - Hardcoded according to track start orientation
- Initial Position
  - Hardcoded as origin for track start
### Returns:
-Array including subarrays of time steps, x-positions, y-positions, velocity vectors, fuel values, mpg and average velocity over track length
### Methodology:
- Initiate the simulation using run_simulation(); operates as top layer of simulation controller 
  - Initialzies simulated vehicle, defines arrays for time steps/solution values, accepts track CSV, and defines initial starting direction and travel distance
  - Iterate through distinct track steps
    - Step through track as a series of straight or turning maneuvers
    - Keep track of solution values and time at end of each maneuver
  - Separate and store true positions, velociites, travel distance and mpg over track maneuver individually from resultant solutions
  
- For Straight Manuevers
  - Define conditional function checks for if vehicle has either transgressed maximum speed or minimum speeds; these will act as one type of limit to be passed into the time step function indicating that the engine state will change
  - Define reached() function to assess whether track maneuver has been completed; acts as second limit to be passed into time step function
    - For straight maneuvers this means having traversed a certain linear distance
  - Initiate time stepping using numerical integration methods, accounting for the non-linearity of ODE/system variables passing a unique differential function for coasting or burning 
    - dy_dt_straight_coasting() & dy_dt_straight_burning() represent the differential or change in solution values between time steps that is used by the numerical solver to solve the non-linear ODE system

- For Turning Maneuvers
  - Define reached() function to assess whether track maneuver has been completed; acts as the only limit to be passed into time step function since turning maneuvers imply coasting throughout
    - For a turn this means having traversed a certain angular displacement
  - Initiate time stepping using numerical integration methods, accounting for the non-linearity of ODE/system variables, passing a unique differential function for turning
    -dy_dt_turning defines the differential or change in solution values between time steps that is used by the numerical solver to solve the non-linear ODE system
  
### Assumptions:
- Track CSV CSV and dimensoning are accurate/reflective of modeled track
- Numeric Solver time span is sufficently large such that limiting events are reached prior to time endpoint
-Maximum time step is sufficiently small to achieve accurate numerical solution of non-linear ODE system given various vehicle archetypes and track conditions


