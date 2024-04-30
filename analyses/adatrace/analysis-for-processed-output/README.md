# File Structure

- - output_approx_blgd_level: when running AdaTrace on KTH data, the output x-y coordirates do not correspond directly to any building indices. Hence for the purpose of synthetic trajectory analysis based on real building indices, this file provides an approximation script on Euclidean distance.
- - output_error_graph: AdaTrace's Experiments module gives trip, length, and diameter errors. This file plots these errors.
  - path-length-dist: contains plotting script for path length distribution for synthetic trajectories.
  - trajectory-graphing: contains plotting for the original & synthetic trajectories on x-y coordinates
