# CFD Setup Summary

This folder holds the ANSYS Fluent case and data files for the nozzle simulation. The notes below describe the setup so the run can be understood without opening Fluent.

## Solver and Software
- ANSYS Fluent 2024 R1
- 2D axisymmetric density-based solver in double precision

## Models
- Energy equation on
- k-omega SST turbulence model with viscous heating and a production limiter
- Air as an ideal gas with gamma = 1.4

## Operating Conditions
- Operating pressure set to 0 so all entered pressures are absolute
- Chamber total pressure 500,000 Pa
- Chamber total temperature 3,000 K

## Boundary Conditions
- Inlet is a pressure inlet at 500,000 Pa gauge total pressure and 3,000 K total temperature, with a supersonic initial gauge pressure of 460,000 Pa
- Outlet is a pressure outlet set to the back-pressure for each regime, with a backflow total temperature of 300 K
- Axis along the bottom edge
- Wall along the nozzle contour

## Back-Pressures by Regime
| Regime | Back-pressure |
|--------|--------------|
| Under-expanded | 5,000 Pa |
| Design (ideal) | 14,893 Pa |
| Over-expanded | 70,000 Pa |

## Solution Methods
- Started first-order upwind for stability, then switched to second-order upwind near iteration 1000
- Roe-FDS flux with high-speed numerics enabled
- Reference values computed from the inlet

## Mesh
- 12,508 quad-dominant elements at 0.5 mm element size
- Wall inflation of 15 layers with a 0.005 mm first layer and 1.2 growth rate for low y+
- Minimum orthogonal quality 0.48 and average 0.99

## Convergence
Judged primarily by exit quantities reaching steady values, with residual levels used as a secondary check. The over-expanded case holds slightly elevated continuity residuals near 3e-2 because of the flow separation, which is expected physics rather than a convergence failure.

## File Notes
The case and data files capture one regime, whichever was loaded when the solution was saved. The exit monitor logs (exit_mach and exit_temp) record how the exit quantities converged over iterations and can be opened in any text editor.
