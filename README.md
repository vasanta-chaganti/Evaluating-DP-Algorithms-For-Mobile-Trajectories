# Differential Privacy for Mobile User Trajectories

## Overview

This repository contains our analyses on differentially private trajectory publishing algorithms.

## Dataset

The primary dataset used in this research is the **KTH wireless trace dataset**, obtained from CRAWDAD kth/campus. This dataset provides a rich, fine-grained collection of mobility traces, ideal for evaluating the effectiveness of differential privacy algorithms in a real-world context.

## Repository Structure

Below is an overview of the repository's structure:

- **`/LICENSE`**
  - Contains the licensing information for the use and distribution of the software and data within this repository.

- **`/README.md`**
  - Provides an overview and general information about the project.

- **`/analyses`**
  - Contains Jupyter notebooks and scripts of our analyses:
    - **`/adatrace`**: Analysis of the AdaTrace algorithm.
    - **`/kth-traj`**: Analysis of KTH trajectory data.
    - **`/ngram`**: Analysis of the ngram algorithm.

- **`/data`**
  - **`/processed`**: Processed data that serve as the inputs for DP algorithms.
  - **`/raw`**: Original, unmodified datasets.

- **`/docs`**
  - Documentation related to the project.

- **`/results`**
  - Output trajectories, organized by algorithm:
    - **`/adatrace`**
    - **`/ngram`**

- **`/src`**
  - Source code necessary to run the analyses and algorithms:
    - **`/adatrace`**: AdaTrace implementation.
    - **`/ngram`**: Code for the ngram algorithm.

## Getting Started

To get started with this repository:
1. Clone the repo to your local machine.
2. Ensure that you have the necessary Python environment set up (see environment requirements in each sub-directory).
3. Explore the `/data` directory to understand the dataset structures.
4. Run Jupyter notebooks in `/analyses` to see our analyses.
