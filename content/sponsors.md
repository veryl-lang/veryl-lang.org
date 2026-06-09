+++
title = "Sponsors"
description = "Organizations and services supporting the Veryl hardware description language project."
weight = 5
+++

Veryl is an open-source project that relies on the generous support of the following organizations.
We are grateful to everyone who helps keep the project moving forward.

# Organizations

<div class="sponsor-grid">
  <a class="sponsor-card" href="https://codspeed.io/?utm_source=veryl-lang&utm_medium=readme" target="_blank" rel="noopener">
    <img class="sponsor-logo" src="/img/codspeed-logo.png" alt="CodSpeed" />
    <div class="sponsor-body">
      <div class="sponsor-name">CodSpeed</div>
      <div class="sponsor-desc">
        Continuous performance monitoring for code. CodSpeed supports Veryl through their
        Open Source program by providing macro runner credits for our continuous benchmarking.
      </div>
    </div>
  </a>
</div>

<style>
  .sponsor-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }
  .sponsor-card {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1.25rem;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    background-color: var(--toc-background-color);
    text-decoration: none;
    color: inherit;
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
  }
  .sponsor-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    border-color: var(--primary-link-color);
  }
  .sponsor-logo {
    width: 80px;
    height: 80px;
    flex-shrink: 0;
    border-radius: 12px;
    object-fit: contain;
  }
  .sponsor-body {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }
  .sponsor-name {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--primary-text-color);
  }
  .sponsor-desc {
    font-size: 0.92rem;
    line-height: 1.5;
    color: var(--secondary-text-color);
  }
</style>

# Become a sponsor

Individual sponsorships are accepted through GitHub Sponsors.
If you or your organization would like to support Veryl, please get in touch via the
[GitHub Sponsors page](https://github.com/sponsors/dalance) or open an issue on the
[main repository](https://github.com/veryl-lang/veryl).
