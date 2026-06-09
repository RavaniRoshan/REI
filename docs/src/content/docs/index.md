---
title: REI — Repository Evolution Intelligence
description: Predict downstream file impact from any code change
template: splash
editUrl: false
lastUpdated: false
hero:
  tagline: Predict which files will break when you change a file. Combines static dependency analysis with commit history co-change patterns.
  actions:
    - text: Quick Start
      link: /REI/introduction/quick-start
      icon: right-arrow
      variant: primary
    - text: GitHub
      link: https://github.com/RavaniRoshan/REI
      icon: external
      variant: minimal
---

import { Card, CardGrid, LinkCard } from "@astrojs/starlight/components";

<style>
  :root {
    --sl-color-accent-low: #1e1b4b;
    --sl-color-accent: #6366f1;
    --sl-color-accent-high: #8b5cf6;
  }

  .hero .title {
    font-size: 2.8rem;
    background: linear-gradient(135deg, #6366f1, #06b6d4);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero .tagline {
    font-size: 1.15rem;
    max-width: 600px;
    line-height: 1.7;
  }

  .cards-section {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--sl-color-gray-5);
  }

  .cards-section h2 {
    text-align: center;
    font-size: 1.6rem;
    margin-bottom: 1.5rem;
  }

  .card-grid-wrapper :global(.sl-card) {
    border: 1px solid var(--sl-color-gray-5);
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(6, 182, 212, 0.05));
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .card-grid-wrapper :global(.sl-card:hover) {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
  }

  .card-grid-wrapper :global(.sl-card-title) {
    color: var(--sl-color-accent-high);
  }

  .stats-table {
    margin: 2rem auto;
    max-width: 500px;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--sl-color-gray-5);
  }

  .stats-table th {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #fff;
    padding: 0.75rem 1.25rem;
    text-align: left;
    font-weight: 600;
  }

  .stats-table td {
    padding: 0.65rem 1.25rem;
    border-bottom: 1px solid var(--sl-color-gray-5);
  }

  .stats-table tr:last-child td {
    border-bottom: none;
  }

  .stats-table tr:nth-child(even) td {
    background: rgba(99, 102, 241, 0.04);
  }

  .stats-table td:last-child {
    font-weight: 700;
    font-family: var(--sl-font-mono);
    color: var(--sl-color-accent-high);
  }

  .mascot-section {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    margin: 3rem auto;
    max-width: 700px;
    padding: 2rem;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08), rgba(6, 182, 212, 0.06));
    border: 1px solid rgba(99, 102, 241, 0.15);
  }

  .mascot-section img {
    width: 160px;
    height: 160px;
    flex-shrink: 0;
    filter: drop-shadow(0 4px 12px rgba(99, 102, 241, 0.3));
  }

  .mascot-text h3 {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #6366f1, #06b6d4);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .mascot-text p {
    color: var(--sl-color-gray-2);
    line-height: 1.7;
  }

  .cta-links {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 2rem;
  }

  .cta-links :global(a) {
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 500;
  }
</style>

<div class="mascot-section">
  <img src="/REI/mascot.svg" alt="REI mascot" />
  <div class="mascot-text">
    <h3>Meet REI</h3>
    <p>
      Your intelligent code companion. REI watches how your codebase evolves, learns which files change together, and tells you exactly what will break — before you even hit save.
    </p>
  </div>
</div>

<div class="card-grid-wrapper">
  <div class="cards-section">
    <h2>How It Works</h2>
    <CardGrid>
      <Card title="Ingest" icon="pencil">
        Initialize REI in any repo. Commits, files, and dependencies are extracted automatically.
      </Card>
      <Card title="Analyze" icon="magnifier">
        Build a static dependency graph and evolutionary coupling graph from commit history.
      </Card>
      <Card title="Predict" icon="random">
        Query any file and get ranked predictions of affected files using query-aware scoring.
      </Card>
      <Card title="Evaluate" icon="checkmark">
        Measure prediction accuracy against held-out commits with date-based train/test split.
      </Card>
    </CardGrid>
  </div>
</div>

<div class="cards-section">
  <h2>Benchmarks</h2>
  <table class="stats-table">
    <thead>
      <tr><th>Metric</th><th>Accuracy</th></tr>
    </thead>
    <tbody>
      <tr><td>Baseline (static + global popularity)</td><td>13.29%</td></tr>
      <tr><td>Fair evaluation (query-aware scoring)</td><td>24.85%</td></tr>
      <tr><td>Full coupling graph upper bound</td><td>46.50%</td></tr>
    </tbody>
  </table>
</div>

<div class="cta-links">
  <LinkCard title="Read the Docs" href="/REI/introduction/motivation" description="Architecture, evaluation, and CLI reference." />
  <LinkCard title="View on GitHub" href="https://github.com/RavaniRoshan/REI" description="Source code, issues, and contributions." />
</div>
