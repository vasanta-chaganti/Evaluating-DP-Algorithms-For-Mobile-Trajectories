# README

This diractory contains Adatrace's noisy output for KTH using different epsilon budget allocations at AP and building levels

- budget_markov: This involes privacy budget for Markov mobility model only with epsilons splitted in the following way:
  ```
  double[] budgetDistnWeights = {0.01, 0.97, 0.01, 0.01};  // grid, Markov, trip, length
  ```
- budget_markov_length: This involes privacy budgets for both markov and length distribution construction
  ```
  double[] budgetDistnWeights = {0.01, 0.78, 0.01, 0.2};  // grid, Markov, trip, length
  ```
- budget_markov_trip_length: This involes privacy budgets for markov, trip, and length distribution
  ```
  double[] budgetDistnWeights = {0.01, 0.79, 0.1, 0.1};  // grid, Markov, trip, length
  ```
- default_budget: uses Adatrace's default budget:
  ```
  double[] budgetDistnWeights = {0.05, 0.35, 0.50, 0.10}; // grid, Markov, trip, length
  ```
- budget_even: uses even budgets:
  ```
  double[] budgetDistnWeights = {0.25, 0.25, 0.25, 0.25}; // grid, Markov, trip, length
  ```
