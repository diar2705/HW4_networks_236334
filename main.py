from simulator import Simulator
import sys

def main():
    
    T = int(sys.argv[1])
    N = int(sys.argv[2])
    
    p_end = 3 + N
    λ_index = p_end
    q_end = λ_index + 1 + N
    µ_index = q_end
    
    P = [float(x) for x in sys.argv[3 : p_end]]
    λ = float(sys.argv[λ_index])
    Q = [int(x) for x in sys.argv[λ_index + 1 : q_end]]
    µ = [int(x) for x in sys.argv[µ_index : µ_index + N]]
    
    simulator = Simulator(T, N, P, λ, Q, µ)
    simulator.run()
    simulator.print_results()
    
    

if __name__ == "__main__":
    main()
