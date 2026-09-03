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

  // Mirror the tiers offered on GitHub Sponsors ($1 and $100 a month). The
  // first entry has no `monthlyDollars` and acts as the catch-all bucket that
  // sponsorkit requires (exactly one tier must have none); leaving its title
  // out keeps a heading for it from being rendered.
  tiers: [
    { preset: tierPresets.base },
    { title: 'Backers', monthlyDollars: 1, preset: tierPresets.base },
    { title: 'Sponsors', monthlyDollars: 100, preset: tierPresets.large },
  ],

  // Keep one-time sponsors visible for the number of months their payment
  // covers at the lowest paid tier, rather than dropping them as soon as
  // GitHub marks the sponsorship inactive. A $50 one-time payment stays in
  // Backers ($1 a month) for 50 months, then ages out on its own.
  prorateOnetime: true,
})
