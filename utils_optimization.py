from ortools.linear_solver import pywraplp
from utils_graph import calculate_cartesian_distance

def create_data_model(vertices, value_function):
    """Stores the data for the problem."""
    data = {}

    data["obj_coeffs"] = [
        [value_function(u,v) if u != v else 99999 for u in vertices] for v in vertices
    ]
    
    data["num_vars"] = len(vertices)
    data["num_constraints"] = len(vertices)
    return data

def add_lp_constraint(solver, X, x_to_branch, x_value):
    if not solver:
        return
    constraint = solver.Add(X[x_to_branch] == x_value)
    return constraint

def remove_lp_constraint(solver, constraint):
    pass # Not implemented in ortools
    
def solve_lp(solver):
    status = solver.Solve()
    return status, solver

def get_x_to_branch(X,num_vertices):
    values = []
    for i in range(num_vertices):
        for j in range(num_vertices):
            if X[i,j].solution_value() > 0:
                values.append(((i,j), X[i,j].solution_value()))
                
    differences = [(name, abs(val - 0.5)) for name,val in values]
    x_to_branch, target_value = differences[0]
    for x_next, value in differences[1:]:
        if value < target_value:
            x_to_branch = x_next
    return x_to_branch, target_value

def linnear_relaxation_tsp(vertices):
    """Linear programming on TSP -> Relaxation."""
    """Inspired by https://developers.google.com/optimization/mip/mip_var_array"""
    
    # Instantiate a Glop solver, naming it LinearExample.
    # [START solver]
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return
    # [END solver]

    # Instanstiate data model
    data = create_data_model(vertices, calculate_cartesian_distance)

    # Define decision variables
    x = {}
    for i in range(data["num_vars"]):
        for j in range(data["num_vars"]):
            x[i,j] = solver.NumVar(0, 1, f"x[{i},{j}]")
    
    # Set constraints    
    # Row constraint - Each row must sum to exactly 1
    for i in range(data["num_constraints"]):
        constraint = solver.RowConstraint(1, 1, "")
        for j in range(data["num_vars"]):
            constraint.SetCoefficient(x[i,j], 1) # note i,j
            
    # Column constraint - Each column must sum to exactly 1
    for i in range(data["num_constraints"]):
        constraint = solver.RowConstraint(1, 1, "")
        for j in range(data["num_vars"]):
            constraint.SetCoefficient(x[j,i], 1) # note j,i
            
    # Constraint to enforce exactly one cycle: Miller-Tucker-Zemlin formulation 
    u = [solver.IntVar(0, data["num_vars"] - 1, 'u[%i]' % i) for i in range(data["num_vars"])]
    for i in range(1,data["num_vars"]):
        for j in range(1,data["num_vars"]):
            if i != j:
                solver.Add(u[i] - u[j] + data["num_vars"] * x[i,j] <= data["num_vars"] - 1)
    
    # Define objective function
    objective = solver.Objective()
    for i in range(data["num_vars"]):
        for j in range(data["num_vars"]):
            objective.SetCoefficient(x[i,j], data["obj_coeffs"][i][j])
    objective.SetMinimization()
    
    status = solver.Solve()

    return status,solver,x

def lp_tsp_branch(vertices, branch_constraints):
    """Linear programming on TSP -> Relaxation."""
    """Inspired by https://developers.google.com/optimization/mip/mip_var_array"""
    
    # Instantiate a Glop solver, naming it LinearExample.
    # [START solver]
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return
    # [END solver]

    # Instanstiate data model
    data = create_data_model(vertices, calculate_cartesian_distance)

    # Define decision variables
    x = {}
    for i in range(data["num_vars"]):
        for j in range(data["num_vars"]):
            x[i,j] = solver.NumVar(0, 1, f"x[{i},{j}]")
    
    # Set constraints    
    # Row constraint - Each row must sum to exactly 1
    for i in range(data["num_constraints"]):
        constraint = solver.RowConstraint(1, 1, "")
        for j in range(data["num_vars"]):
            constraint.SetCoefficient(x[i,j], 1) # note i,j
            
    # Column constraint - Each column must sum to exactly 1
    for i in range(data["num_constraints"]):
        constraint = solver.RowConstraint(1, 1, "")
        for j in range(data["num_vars"]):
            constraint.SetCoefficient(x[j,i], 1) # note j,i
            
    # Constraint to enforce exactly one cycle: Miller-Tucker-Zemlin formulation 
    u = [solver.IntVar(0, data["num_vars"] - 1, 'u[%i]' % i) for i in range(data["num_vars"])]
    for i in range(1,data["num_vars"]):
        for j in range(1,data["num_vars"]):
            if i != j:
                solver.Add(u[i] - u[j] + data["num_vars"] * x[i,j] <= data["num_vars"] - 1)

    # Apply constraints from branching
    for x_to_branch, x_value in branch_constraints:
        add_lp_constraint(solver, x, x_to_branch, x_value)
        
    # Define objective function
    objective = solver.Objective()
    for i in range(data["num_vars"]):
        for j in range(data["num_vars"]):
            objective.SetCoefficient(x[i,j], data["obj_coeffs"][i][j])
    objective.SetMinimization()
    
    # Start solver
    status = solver.Solve()

    return status,solver,x

def LinearProgrammingExample():
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    # [START solver]
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return
    # [END solver]

    # Create the two variables and let them take on any non-negative value.
    # [START variables]
    x = solver.NumVar(0, solver.infinity(), "x")
    y = solver.NumVar(0, solver.infinity(), "y")

    print("Number of variables =", solver.NumVariables())
    # [END variables]

    # [START constraints]
    # Constraint 0: x + 2y <= 14.
    solver.Add(x + 2 * y <= 14.0)

    # Constraint 1: 3x - y >= 0.
    solver.Add(3 * x - y >= 0.0)

    # Constraint 2: x - y <= 2.
    solver.Add(x - y <= 2.0)

    print("Number of constraints =", solver.NumConstraints())
    # [END constraints]

    # [START objective]
    # Objective function: 3x + 4y.
    solver.Maximize(3 * x + 4 * y)
    # [END objective]

    # Solve the system.
    # [START solve]
    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()
    # [END solve]

    # [START print_solution]
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution:")
        print(f"Objective value = {solver.Objective().Value():0.1f}")
        print(f"x = {x.solution_value():0.1f}")
        print(f"y = {y.solution_value():0.1f}")
    else:
        print("The problem does not have an optimal solution.")
    # [END print_solution]

    # [START advanced]
    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")
    # [END advanced]
