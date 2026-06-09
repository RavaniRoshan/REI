# REI - Repository Evolution Intelligence

<div class=\"hero-root\">

![REI mascot](../../assets/mascot.svg){ width=\"180px\" }

# Predict which files will break when you change a file

<div class=\"tagline\">
REI combines static dependency analysis with commit history co-change patterns
to tell you exactly what will be affected before you even hit save.
</div>

<div class=\"hero-buttons\">
[:octicons-rocket-24: Quick Start](introduction/motivation.md){ .md-button .md-button--primary }
[:octicons-book-24: Read the Docs](introduction/quick-start.md){ .md-button }
[:material-github: GitHub](https://github.com/RavaniRoshan/REI){ .md-button .md-button--outline }
</div>

</div>

## How It Works

<div class=\"benefits-grid\">

<div class=\"benefit-card\">
<div class=\"icon\">:material-pencil: </div>
<strong>Ingest</strong>
<p>Initialize REI in any repo. Commits, files, and Python imports are extracted automatically.</p>
</div>

<div class=\"benefit-card\">
<div class=\"icon\">:material-magnify: </div>
<strong>Analyze</strong>
<p>Build a static dependency graph and an evolutionary coupling graph from commit history.</p>
</div>

<div class=\"benefit-card\">
<div class=\"icon\">:material-chart-timeline-variant-shimmer: </div>
<strong>Predict</strong>
<p>Query any file and get ranked predictions of affected files using query-aware scoring.</p>
</div>

<div class=\"benefit-card\">
<div class=\"icon\">:material-check-decagram: </div>
<strong>Evaluate</strong>
<p>Measure prediction accuracy against held-out commits with a date-based train/test split.</p>
</div>

</div>

## Benchmarks

| Metric | Accuracy |
|--------|----------|
| Baseline (static + global popularity) | 13.29% |
| Fair evaluation (query-aware scoring) | **24.85%** |
| Full coupling graph upper bound | **46.50%** |
