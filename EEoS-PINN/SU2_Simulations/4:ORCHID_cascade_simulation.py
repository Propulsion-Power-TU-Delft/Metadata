#!/usr/bin/env python3
###############################################################################################
#       #      _____ __  _____      ____        __        __  ____                   #        #  
#       #     / ___// / / /__ \    / __ \____ _/ /_____ _/  |/  (_)___  ___  _____   #        #  
#       #     \__ \/ / / /__/ /   / / / / __ `/ __/ __ `/ /|_/ / / __ \/ _ \/ ___/   #        #      
#       #    ___/ / /_/ // __/   / /_/ / /_/ / /_/ /_/ / /  / / / / / /  __/ /       #        #  
#       #   /____/\____//____/  /_____/\__,_/\__/\__,_/_/  /_/_/_/ /_/\___/_/        #        #
#       #                                                                            #        #
###############################################################################################

####################### FILE NAME: 4:ORCHID_cascade_simulation.py #############################
#=============================================================================================#
# author: Evert Bunschoten                                                                    |
#    :PhD Candidate ,                                                                         |
#    :Flight Power and Propulsion                                                             |
#    :TU Delft,                                                                               |
#    :The Netherlands                                                                         |
#                                                                                             |
#                                                                                             |
# Description:                                                                                |
# Prepare SU2 configuration files and run the flow calculations for the ORCHID linear cascade |
# for which the results are presented in the manuscript.                                      |
#                                                                                             |  
# Version: 2.0.0                                                                              |
#                                                                                             |
#=============================================================================================#

from mpi4py import MPI 
from pysu2 import CSinglezoneDriver
from su2dataminer.config import Config_NICFD

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

p_t_inlet = 1.8093e+06  # Inlet stagnation pressure.
p_s_outlet = 2e5        # Outlet static pressure.
T_t_inlet = 523.0       # Inlet stagnation temperature.

n_iter_firstorder=1e3   # Number of iterations for first-order ROE calculation.
n_iter_secondorder=2e4  # Number of iterations for second-order JST calculation.

# MLP file names.
PINN_filename="MLP_PINN"
MTNN_upper_name = "MLP_high"
MTNN_lower_name = "MLP_low"

# SU2 solver options.
solver_options = """ 
% Turbulent simulation (RANS)                      
SOLVER= RANS

% SA turbulence model
KIND_TURB_MODEL= SA
SA_OPTIONS= NONE
"""

# Flow initialization options.
init_options = """ 
RESTART_SOL=__RESTART_SOL__
% Mach number (non-dimensional, based on the free-stream values)
MACH_NUMBER= 0.05

% Free-stream pressure 
FREESTREAM_PRESSURE= __P_T_INLET__

% Free-stream temperature 
FREESTREAM_TEMPERATURE= __T_T_INLET__

% Free-stream Turbulence Intensity
FREESTREAM_TURBULENCEINTENSITY = 0.1

% Free-stream Turbulent to Laminar viscosity ratio
FREESTREAM_TURB2LAMVISCRATIO = 100.0

FREESTREAM_OPTION= TEMPERATURE_FS

INIT_OPTION= TD_CONDITIONS

REF_DIMENSIONALIZATION= DIMENSIONAL

ITER=__N_ITER__
"""

# Fluid model options
fluid_model_options = """ 
FLUID_MODEL= __FLUID_MODEL__
FLUID_NAME= __FLUID_NAME__
USE_PINN=__USE_PINN__
INTERPOLATION_METHOD = MLP
FILENAMES_INTERPOLATOR = (__MLP_FILENAMES__)
DATADRIVEN_NEWTON_RELAXATION = 1.0

% Ratio of specific heats (1.4 default and the value is hardcoded for the model STANDARD_AIR)
GAMMA_VALUE= 1.025

% Specific gas constant (287.058 J/kg*K default and this value is hardcoded for the model STANDARD_AIR)
GAS_CONSTANT= 51.2

% Critical Temperature (273.15 K by default)
CRITICAL_TEMPERATURE= 518.75

% Critical Pressure (101325.0 N/m^2 by default)
CRITICAL_PRESSURE= 1939000.0

% Acentric factor (0.035 (air))
ACENTRIC_FACTOR= 0.418

VISCOSITY_MODEL= CONSTANT_VISCOSITY

% Molecular Viscosity that would be constant (1.716E-5 by default)
MU_CONSTANT= 1.1616248692182084e-05

% Sutherland Viscosity Ref (1.716E-5 default value for AIR SI)
MU_REF= 1.716E-5

% Sutherland Temperature Ref (273.15 K default value for AIR SI)
MU_T_REF= 273.15

% Sutherland constant (110.4 default value for AIR SI)
SUTHERLAND_CONSTANT= 110.4

CONDUCTIVITY_MODEL= CONSTANT_PRANDTL 
PRANDTL_LAM=1.2297874884638853
TURBULENT_CONDUCTIVITY_MODEL=CONSTANT_PRANDTL_TURB
PRANDTL_TURB=1.2297874884638853

% Molecular Thermal Conductivity that would be constant (0.0257 by default)
THERMAL_CONDUCTIVITY_CONSTANT= 0.086
"""

# Boundary conditions
boundary_conditions = """ 
MARKER_HEATFLUX= (wall1, 0.0)
MARKER_GILES= (inflow, TOTAL_CONDITIONS_PT, __P_T_INLET__, __T_T_INLET__, 1.0, 0.0, 0.0, 0.8, 0.8, outflow, STATIC_PRESSURE,__P_S_OUTLET__, 0.0, 0.0, 0.0, 0.0, 0.8, 0.8)
SPATIAL_FOURIER=YES

% Kind of Average (ALGEBRAIC_AVERAGE, AREA_AVERAGE, MIXEDOUT_AVERAGE)
AVERAGE_PROCESS_KIND= MASSFLUX
MIXEDOUT_COEFF=(0.1, 1e-5, 15.0)
TURBOMACHINERY_KIND= AXIAL
TURBO_PERF_KIND=TURBINE
NUM_SPANWISE_SECTIONS= 1
% Specify ramp option for Outlet pressure (YES, NO) default NO
RAMP_OUTLET_PRESSURE= __ENABLE_RAMP__

% Parameters of the outlet pressure ramp (starting outlet pressure, updating-iteration-frequency, total number of iteration for the ramp)
RAMP_OUTLET_PRESSURE_COEFF= (__P_T_INLET__, 10, 200)

% Periodic boundary marker(s) (NONE = no marker)
% Format: ( periodic marker, donor marker, rot_cen_x, rot_cen_y, rot_cen_z, rot_angle_x-axis, rot_angle_y-axis, rot_angle_z-axis, translation_x, translation_y, translation_z)
MARKER_PERIODIC= (periodic1, periodic2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.045, 0.0)

OBJECTIVE_FUNCTION=EFFICIENCY

MARKER_PLOTTING= (wall1)

MARKER_MONITORING= (wall1)
MARKER_TURBOMACHINERY= (inflow, outflow)
DV_MARKER=(wall1)
"""

# Numerics options
numerics="""
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CFL_NUMBER= 4
CFL_ADAPT= YES
CFL_ADAPT_PARAM= ( 0.99, 1.01, 1.0, 1000.0)

LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= LU_SGS
LINEAR_SOLVER_ERROR= 1E-5
LINEAR_SOLVER_ITER= 20
CONV_NUM_METHOD_FLOW= __CONV_METHOD__
MUSCL_FLOW= NO
ENTROPY_FIX_COEFF= 0.001
JST_SENSOR_COEFF= ( 0.5, 0.12 )
SLOPE_LIMITER_FLOW= VENKATAKRISHNAN
VENKAT_LIMITER_COEFF=0.5
TIME_DISCRE_FLOW= EULER_IMPLICIT
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB = NO
SLOPE_LIMITER_TURB= VENKATAKRISHNAN
TIME_DISCRE_TURB= EULER_IMPLICIT
CFL_REDUCTION_TURB= 0.01
"""

# IO options
input_output="""
MESH_FILENAME= __MESH_FILENAME__
MESH_FORMAT= SU2
TABULAR_FORMAT= CSV
CONV_FILENAME= __CONV_FILENAME__
RESTART_FILENAME= __RESTART_FILENAME__
SOLUTION_FILENAME=__SOLUTION_FILENAME__
VOLUME_FILENAME= __VOLUME_FILENAME__
OUTPUT_WRT_FREQ= 20
HISTORY_WRT_FREQ_INNER= 1
HISTORY_OUTPUT= (INNER_ITER, WALL_TIME, RMS_RES,CFL_NUMBER)
VOLUME_OUTPUT= (SOLUTION, PRIMITIVE, RESIDUAL, MPI,SENSITIVITY,MESH_QUALITY)
OUTPUT_FILES=(RESTART,PARAVIEW_MULTIBLOCK)
"""

def WriteSU2ConfigFile(options:dict):
    """Write configuration file for SU2 simulation for the ORCHID linear cascade.

    :param options: dictionary with solver options.
    :type options: dict
    """
    solver_options_out = solver_options
    init_options_out = init_options
    fluid_model_options_out = fluid_model_options
    boundary_conditions_out = boundary_conditions
    numerics_out = numerics 
    input_output_out = input_output

    for option in options.keys():
        solver_options_out = solver_options_out.replace(option, options[option])
        init_options_out = init_options_out.replace(option, options[option])
        fluid_model_options_out = fluid_model_options_out.replace(option, options[option])
        boundary_conditions_out = boundary_conditions_out.replace(option, options[option])
        numerics_out = numerics_out.replace(option, options[option])
        input_output_out = input_output_out.replace(option, options[option])
    
    with open(options["config_name"],"w+") as fid:
        fid.write(solver_options_out)
        fid.write(init_options_out)
        fid.write(fluid_model_options_out)
        fid.write(boundary_conditions_out)
        fid.write(numerics_out)
        fid.write(input_output_out)
    return 

def RunSU2(options_firstorder:dict, options_secondorder:dict):
    """Run first-order ROE and second-order JST flow calculations in SU2.

    :param options_firstorder: options for first-order calculation.
    :type options_firstorder: dict
    :param options_secondorder: options for second-order calculation.
    :type options_secondorder: dict
    """
    driver = CSinglezoneDriver(options_firstorder["config_name"], 1, comm)
    driver.StartSolver()
    driver.Finalize()

    driver = CSinglezoneDriver(options_secondorder["config_name"], 1, comm)
    driver.StartSolver()
    driver.Finalize()
    return 

# Default solver options
su2_options = {"config_name" : "config.cfg",\
               "__RESTART_SOL__" : "NO",\
               "__P_T_INLET__" : "%.16e" % p_t_inlet,\
               "__P_S_OUTLET__" : "%.16e" % p_s_outlet,\
               "__T_T_INLET__" : "%.16e" % T_t_inlet,\
               "__N_ITER__" : "%i" % n_iter_firstorder,\
               "__FLUID_MODEL__" : "DATADRIVEN_FLUID",\
               "__USE_PINN__" : "YES",\
               "__MLP_FILENAMES__" : PINN_filename + ".mlp",\
               "__FLUID_NAME__" : "MM",\
               "__ENABLE_RAMP__" : "YES",\
               "__CONV_METHOD__" : "ROE",\
               "__MESH_FILENAME__" : "LinearCascadeORCHI_fine.su2",\
               "__CONV_FILENAME__" : "history_ROE_EEoS_PINN",\
               "__RESTART_FILENAME__" : "restart_ROE_EEoS_PINN",\
               "__SOLUTION_FILENAME__" : "solution_EEoS_PINN",\
               "__VOLUME_FILENAME__" : "vol_solution_ROE_EEoS_PINN"}

# Options for EEoS-PINN flow calculations
options_PINN_firstorder = su2_options.copy()
options_PINN_firstorder["config_name"] = "config_EEoS-PINN_firstorder.cfg"
options_PINN_firstorder["__N_ITER__"] ="%i" %  n_iter_firstorder
options_PINN_firstorder["__FLUID_MODEL__"] = "DATADRIVEN_FLUID"
options_PINN_firstorder["__CONV_METHOD__"] = "ROE"
options_PINN_firstorder["__ENABLE_RAMP__"] = "YES"
options_PINN_firstorder["__CONV_FILENAME__"] = "history_ROE_EEoS_PINN"
options_PINN_firstorder["__RESTART_FILENAME__"] = "restart_ROE_EEoS_PINN"
options_PINN_firstorder["__VOLUME_FILENAME__"] = "vol_solution_ROE_EEoS_PINN"

options_PINN_secondorder = options_PINN_firstorder.copy()
options_PINN_secondorder ["config_name"] = "config_EEoS-PINN_secondorder.cfg"
options_PINN_secondorder["__RESTART_SOL__"] = "YES"
options_PINN_secondorder["__N_ITER__"] = "%i" % n_iter_secondorder
options_PINN_secondorder["__ENABLE_RAMP__"] = "NO"
options_PINN_secondorder["__CONV_METHOD__"] = "JST"
options_PINN_secondorder["__CONV_FILENAME__"] = "history_JST_EEoS_PINN"
options_PINN_secondorder["__RESTART_FILENAME__"] = "restart_JST_EEoS_PINN"
options_PINN_secondorder["__SOLUTION_FILENAME__"] = "restart_ROE_EEoS_PINN"
options_PINN_secondorder["__VOLUME_FILENAME__"] = "vol_solution_JST_EEoS_PINN"

# Options for EEoS-MTNN flow calculations
options_MTNN_firstorder = su2_options.copy()
options_MTNN_firstorder["config_name"] = "config_EEoS-MTNN_firstorder.cfg"
options_MTNN_firstorder["__N_ITER__"] ="%i" %  n_iter_firstorder
options_MTNN_firstorder["__FLUID_MODEL__"] = "DATADRIVEN_FLUID"
options_MTNN_firstorder["__MLP_FILENAMES__"] = MTNN_lower_name + ".mlp," + MTNN_upper_name+".mlp"
options_MTNN_firstorder["__CONV_METHOD__"] = "ROE"
options_MTNN_firstorder["__ENABLE_RAMP__"] = "YES"
options_MTNN_firstorder["__CONV_FILENAME__"] = "history_ROE_EEoS_MTNN"
options_MTNN_firstorder["__RESTART_FILENAME__"] = "restart_ROE_EEoS_MTNN"
options_MTNN_firstorder["__VOLUME_FILENAME__"] = "vol_solution_ROE_EEoS_MTNN"

options_MTNN_secondorder = options_MTNN_firstorder.copy()
options_MTNN_secondorder ["config_name"] = "config_EEoS-MTNN_secondorder.cfg"
options_MTNN_secondorder["__RESTART_SOL__"] = "YES"
options_MTNN_secondorder["__N_ITER__"] = "%i" % n_iter_secondorder
options_MTNN_secondorder["__ENABLE_RAMP__"] = "NO"
options_MTNN_secondorder["__CONV_METHOD__"] = "JST"
options_MTNN_secondorder["__CONV_FILENAME__"] = "history_JST_EEoS_MTNN"
options_MTNN_secondorder["__RESTART_FILENAME__"] = "restart_JST_EEoS_MTNN"
options_MTNN_secondorder["__SOLUTION_FILENAME__"] = "restart_ROE_EEoS_MTNN"
options_MTNN_secondorder["__VOLUME_FILENAME__"] = "vol_solution_JST_EEoS_MTNN"

# Options for HEoS flow calculations
options_HEoS_firstorder = su2_options.copy()
options_HEoS_firstorder["config_name"] = "config_HEoS_firstorder.cfg"
options_HEoS_firstorder["__N_ITER__"] ="%i" %  n_iter_firstorder
options_HEoS_firstorder["__FLUID_MODEL__"] = "COOLPROP"
options_HEoS_firstorder["__CONV_METHOD__"] = "ROE"
options_HEoS_firstorder["__ENABLE_RAMP__"] = "YES"
options_HEoS_firstorder["__CONV_FILENAME__"] = "history_ROE_HEoS"
options_HEoS_firstorder["__RESTART_FILENAME__"] = "restart_ROE_HEoS"
options_HEoS_firstorder["__VOLUME_FILENAME__"] = "vol_solution_ROE_HEoS"

options_HEoS_secondorder = options_HEoS_firstorder.copy()
options_HEoS_secondorder["config_name"] = "config_HEoS_secondorder.cfg"
options_HEoS_secondorder["__N_ITER__"] ="%i" %  n_iter_secondorder
options_HEoS_secondorder["__CONV_METHOD__"] = "JST"
options_HEoS_secondorder["__ENABLE_RAMP__"] = "NO"
options_HEoS_secondorder["__RESTART_SOL__"] = "YES"
options_HEoS_secondorder["__CONV_FILENAME__"] = "history_JST_HEoS"
options_HEoS_secondorder["__RESTART_FILENAME__"] = "restart_JST_HEoS"
options_HEoS_secondorder["__SOLUTION_FILENAME__"] = "restart_ROE_HEoS"
options_HEoS_secondorder["__VOLUME_FILENAME__"] = "vol_solution_JST_HEoS"

# Options for CEoS flow calculations
options_CEoS_firstorder = su2_options.copy()
options_CEoS_firstorder["config_name"] = "config_CEoS_firstorder.cfg"
options_CEoS_firstorder["__N_ITER__"] ="%i" %  n_iter_firstorder
options_CEoS_firstorder["__FLUID_MODEL__"] = "PR_GAS"
options_CEoS_firstorder["__CONV_METHOD__"] = "ROE"
options_CEoS_firstorder["__ENABLE_RAMP__"] = "YES"
options_CEoS_firstorder["__CONV_FILENAME__"] = "history_ROE_CEoS"
options_CEoS_firstorder["__RESTART_FILENAME__"] = "restart_ROE_CEoS"
options_CEoS_firstorder["__VOLUME_FILENAME__"] = "vol_solution_ROE_CEoS"

options_CEoS_secondorder = options_CEoS_firstorder.copy()
options_CEoS_secondorder["config_name"] = "config_CEoS_secondorder.cfg"
options_CEoS_secondorder["__N_ITER__"] ="%i" %  n_iter_secondorder
options_CEoS_secondorder["__CONV_METHOD__"] = "JST"
options_CEoS_secondorder["__RESTART_SOL__"] = "YES"
options_CEoS_secondorder["__ENABLE_RAMP__"] = "NO"
options_CEoS_secondorder["__CONV_FILENAME__"] = "history_JST_CEoS"
options_CEoS_secondorder["__RESTART_FILENAME__"] = "restart_JST_CEoS"
options_CEoS_secondorder["__SOLUTION_FILENAME__"] = "restart_ROE_CEoS"
options_CEoS_secondorder["__VOLUME_FILENAME__"] = "vol_solution_JST_CEoS"

if rank == 0:

    # Write MLP files for PINN and MTNNs. 

    config_PINN = Config_NICFD("../PINN.cfg")
    config_PINN.WriteSU2MLP(PINN_filename)

    config_MTNN_low = Config_NICFD("../Direct_low.cfg")
    config_MTNN_low.WriteSU2MLP(MTNN_lower_name)
    config_MTNN_high = Config_NICFD("../Direct_high.cfg")
    config_MTNN_high.WriteSU2MLP(MTNN_upper_name)
    
    # Write SU2 configuration files for the four thermodynamic models.
    WriteSU2ConfigFile(options_PINN_firstorder)
    WriteSU2ConfigFile(options_PINN_secondorder)

    WriteSU2ConfigFile(options_MTNN_firstorder)
    WriteSU2ConfigFile(options_MTNN_secondorder)

    WriteSU2ConfigFile(options_HEoS_firstorder)
    WriteSU2ConfigFile(options_HEoS_secondorder)
    
    WriteSU2ConfigFile(options_CEoS_firstorder)
    WriteSU2ConfigFile(options_CEoS_secondorder)

comm.Barrier()

# Run EEoS-PINN simulations
RunSU2(options_PINN_firstorder, options_PINN_secondorder)

# Run EEoS-MTNN simulations
RunSU2(options_MTNN_firstorder, options_MTNN_secondorder)

# Run CEoS simulations
RunSU2(options_CEoS_firstorder, options_CEoS_secondorder)

