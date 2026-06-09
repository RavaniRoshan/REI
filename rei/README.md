# REI — Repository Evolution Intelligence

REI predicts downstream file and function impact when a developer changes a file in a Python repository. It ingests git history, builds static dependency graphs via AST analysis, mines co-change patterns, and combines both signals to rank which files are most likely affected by a given change.
