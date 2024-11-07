+++
title = "Statistics"
description = "Statistics"
weight = 4
+++

# Projects on GitHub

<div>
  <canvas id="discovered"></canvas>
</div>

# Release Downloads

## Total

<div>
  <canvas id="total_download"></canvas>
</div>

## By Version

<div>
  <canvas id="version_download"></canvas>
</div>

## Platform

<div>
  <canvas id="platform_download"></canvas>
</div>


<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>

<script>
  async function get_db() {
    const requestURL = "https://raw.githubusercontent.com/veryl-lang/discovery/refs/heads/main/db/db.json";
    const request = new Request(requestURL);
    const response = await fetch(request);
    const data = await response.json();
    return data;
  }

  async function plot() {
    Chart.defaults.color = '#d7d7d7';
    const db = await get_db();
    plot_discovered(db);
    plot_download(db);
  }

  function plot_discovered(db) {
    var labels   = [];
    var projects = [];
    var sources  = [];
    for (const entry of db.discovered) {
      var date = new Date(0);
      date.setUTCSeconds(entry.date);
      labels.push(date);
      projects.push(entry.projects.length);
      sources.push(entry.sources);
    }

    const cfg = {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Projects',
          data: projects,
          borderWidth: 1,
          yAxisID: 'y_prj'
        },
        {
          label: 'Sources',
          data: sources,
          borderWidth: 1,
          yAxisID: 'y_src'
        }]
      },
      options: {
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'week'
            }
          },
          y_prj: {
            type: 'linear',
            position: 'left',
            title: {
              display: true,
              text: 'Projects'
            }
          },
          y_src: {
            type: 'linear',
            position: 'right',
            title: {
              display: true,
              text: 'Sources'
            }
          }
        }
      }
    }

    const ctx = document.getElementById('discovered');
    new Chart(ctx, cfg);
  }

  function plot_download(db) {
    var data = {};
    var versions = [];
    var platform_downloads = {};
    for (const version in db.veryl_downloads) {
      versions.push(version);
      for (const entry of db.veryl_downloads[version]) {
        const date = entry.date;
        var counts = 0;
        for (const platform in entry.counts) {
          counts += entry.counts[platform];
        }
        if (date in data) {
          data[date].push({version: version, counts: counts});
        } else {
          data[date] = [{version: version, counts: counts}];
        }
      }

      const last_entry = db.veryl_downloads[version].slice(-1)[0];
      for (const platform in last_entry.counts) {
        if (platform in platform_downloads) {
          platform_downloads[platform] += last_entry.counts[platform];
        } else {
          platform_downloads[platform] = last_entry.counts[platform];
        }
      }
    }

    // sort by semantic version
    versions = versions.map( a => a.split('.').map( n => +n+100000 ).join('.') ).sort()
                       .map( a => a.split('.').map( n => +n-100000 ).join('.') );

    var labels   = [];
    var downloads = {};
    var total_downloads = [];

    for (const version of versions) {
      downloads[version] = [];
    }

    var dates = Object.keys(data).sort();
    for (const date of dates) {
      var label_date = new Date(0);
      label_date.setUTCSeconds(date);
      labels.push(label_date);

      var sum = 0;
      var inserted = [];
      for (const entry of data[date]) {
        const version = entry.version;
        if (version in downloads) {
          downloads[version].push(entry.counts);
          sum += entry.counts;
          inserted.push(version);
        }
      }
      for (const version in downloads) {
        if (!(inserted.includes(version))) {
          const last = downloads[version].slice(-1)[0];
          if (last) {
            sum += last;
          }
          downloads[version].push(last);
        }
      }
      total_downloads.push(sum);
    }

    var datasets = [];
    latest_versions = versions.slice(-5);

    for (const version in downloads) {
      if (latest_versions.includes(version)) {
        datasets.push({
          label: version,
          data: downloads[version],
          borderWidth: 1
        });
      }
    }

    {
      const cfg = {
        type: 'line',
        data: {
          labels: labels,
          datasets: datasets
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'week'
              }
            }
          }
        }
      }

      const ctx = document.getElementById('version_download');
      new Chart(ctx, cfg);
    }

    {
      const cfg = {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'total',
            data: total_downloads,
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'week'
              }
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      }

      const ctx = document.getElementById('total_download');
      new Chart(ctx, cfg);
    }

    {
      var labels = [];
      var data = [];
      for (const platform in platform_downloads) {
        if (platform == 'X86_64Linux') {
          labels.push('x86_64-linux');
        } else if (platform == 'X86_64Mac') {
          labels.push('x86_64-mac');
        } else if (platform == 'Aarch64Mac') {
          labels.push('aarch64-mac');
        } else if (platform == 'X86_64Windows') {
          labels.push('x86_64-windows');
        }
        data.push(platform_downloads[platform]);
      }

      const cfg = {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data
          }]
        },
        options: {
          responsive: false
        }
      }

      const ctx = document.getElementById('platform_download');
      new Chart(ctx, cfg);
    }
  }

  plot();

</script>
