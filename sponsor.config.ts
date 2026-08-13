import { defineConfig, tierPresets } from 'sponsorkit'

export default defineConfig({
  // Write the generated image into the site's static assets.
  outputDir: 'static/img',
  name: 'sponsors',
  formats: ['svg'],
  width: 800,
  renderer: 'tiers',

  // GitHub Sponsors (organization account).
  // The token is provided via the SPONSORKIT_GITHUB_TOKEN environment
  // variable and needs the `read:user` and `read:org` scopes.
  github: {
    login: 'veryl-lang',
    type: 'organization',
  },

  // Open Collective is configured via environment variables:
  //   SPONSORKIT_OPENCOLLECTIVE_KEY, SPONSORKIT_OPENCOLLECTIVE_SLUG=veryl

  // Merge the same backer across GitHub Sponsors and Open Collective so a
  // person who appears on both platforms is shown only once.
  sponsorsAutoMerge: true,

  // GitHub Sponsors funds routed through the Open Source Collective fiscal
  // host also show up on Open Collective as an aggregate "GitHub Sponsors"
  // entry. Drop it so it does not appear as a stray avatar; the individual
  // GitHub sponsors are already fetched directly from GitHub.
  filter: sponsor =>
    sponsor.sponsor.login !== 'github-sponsors'
    && sponsor.sponsor.name !== 'GitHub Sponsors',

  tiers: [
    { title: 'Backers', preset: tierPresets.base },
    { title: 'Sponsors', monthlyDollars: 100, preset: tierPresets.large },
  ],
})
