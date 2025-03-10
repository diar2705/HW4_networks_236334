# Project Overview

This project simulates a queueing system using Python, modeling servers, tasks, and queueing behavior to analyze performance metrics such as wait times.

**Author:** [Diar Batheesh](https://github.com/diar2705).

## Files Overview

- **main.py**  
  Handles argument parsing and initializes the `Simulator` class.

- **simulator.py**  
  Defines the `Simulator`, `Server`, and `Task` classes, managing event processing and queue dynamics.

- **tester.py**  
  Runs multiple simulations with varying parameters and exports results to an Excel file.

- **Makefile**  
  Automates the build process for the `simulator` script.

- **simulator** (Shell script)  
  Executes the main Python script with user-provided parameters.

## Installation and Usage

### 1. Install Dependencies

Ensure you have Python 3.6+ installed, then install the required libraries:

```sh
pip install pandas numpy openpyxl
```

### 2. Run the Simulator

Execute the simulator with the required arguments:

```sh
python main.py <T> <N> <P...> <λ> <Q...> <μ...>
```

Where:

- `T` = Total simulation time (duration for which events will be processed).
- `N` = Number of servers in the system.
- `P...` = Probability distribution for selecting a server (should sum to 1 across all servers).
- `λ` = Arrival rate (average number of tasks arriving per unit time, following an exponential distribution).
- `Q...` = Queue sizes for each server (maximum number of tasks that can wait in the queue before rejection).
- `μ...` = Service rates for each server (average number of tasks a server can process per unit time, following an exponential distribution).

### 3. Run Automated Tests

To analyze average wait times across multiple scenarios:

```sh
python tester.py
```

The results will be saved in `average_wait_times.xlsx`.

## Additional Notes

- Modify `tester.py` for custom parameter configurations.
