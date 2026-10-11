---
title: "Netflix: Why Older Movies Can Support Growth"
date: 2026-05-03
categories: [product analytics]
tags: [business-strategy, data-analysis, netflix, content-growth]
excerpt: "A catalog analysis showing why one freshness score can hide different strategies for shows and movies."
problem: "A falling overall freshness measure made it unclear whether Netflix was weakening the catalog or building different roles for shows and movies."
result: "In US catalog additions from 2015 to 2021, same-year TV acquisitions rose from 40% to 61% while movies fell to 14%. Sparse core metadata was highest for UK titles released in the 2020s, at 12.8%."
published: false
header:
  teaser: "/images/netflix-beat01.png"
---

## Executive summary

**Business problem:** a falling freshness measure could be mistaken for a weaker catalog. **Decision:** should content investment be judged by one freshness target? **Key finding:** among US additions, same-year TV acquisitions rose while the movie share fell; UK titles in the 2020s release vintage had more sparse core metadata. **Recommended action:** use separate freshness goals and audit core metadata before launch.

## Business context

Netflix's US catalog additions appeared to be getting older. From 2015 to 2021, the share acquired in its release year fell from 72.2% to 28.1%. If freshness is treated as the only goal, that looks like a warning sign.

But a catalog is not one product. New TV shows and older movies can serve different customer needs. I reviewed the data to understand whether the overall decline in freshness represented a real problem or a change in strategy.

## Business question

Is Netflix becoming less attractive because its catalog is older, or is the company using new shows and older movies for different purposes?

The source is the 8,807-title [Netflix Movies and TV Shows dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows), preserved as a [Zenodo snapshot](https://zenodo.org/records/13925131). It records catalog details such as release year, date added, type, country, and listed genres. It does not contain viewing, licensing cost, or customer retention data.

## How I approached it

I separated the catalog into TV shows and movies, then compared freshness by content category. I also reviewed repeat director partnerships and the completeness of content information in the UK catalog. This made it possible to look beyond one headline number and find the business decisions behind the trend.

## Finding 1: TV shows became fresher while movies became older

The two content types moved in opposite directions among US additions:

- The share of TV shows added in their release year increased by 21 percentage points, from 40.0% to 61.1%.
- Movies became older overall, which increased the depth of the library.

Because the analyzed US additions contain many more movies than TV shows, the combined trend can hide the difference between the two content types. The data describes catalog timing; it does not establish that movies keep attracting viewers or that Netflix intended a specific strategy.

![US Netflix additions, 2015 to 2021: Same-year TV acquisitions rose to 61% while movies fell to 14%](/images/netflix-beat01.png)

**Why it matters:** A single freshness target could encourage the wrong decision. Shows and movies need separate goals because they play different roles in the product.

## Finding 2: The library strategy was focused

The deep-library share, defined here as an acquisition lag of more than five years, did not move equally across the movie groups. From the 2015 to 2017 period to 2018 to 2021:

- **International-drama cluster:** deep-library titles rose from 5.5% to 47.4%, a 42.0 point increase.
- **Children and family cluster:** deep-library titles rose from 16.4% to 48.0%, a 31.6 point increase.

The cluster names are interpretations of the groups' dominant genre signals. The pattern shows older additions in those groups, but it does not prove that Netflix intentionally shifted licensing strategy or that the added titles performed well.

![US movie additions, 2015 to 2021: Deep-library share rose 42.0 points in international dramas and 31.6 points in children and family movies](/images/netflix-beat03.png)

## Finding 3: Documentary partnerships may be less efficient

Family content showed strong repeat partnerships with directors. Documentaries, however, were usually made with a new director each time.

The data does not prove that repeat partnerships would improve documentary performance. It does show a possible efficiency opportunity: every new partnership requires fresh negotiations, contracts, and relationship-building.

## Finding 4: Missing information creates a customer experience risk

In the UK catalog, 12.8% of titles in the 2020s release vintage had sparse core metadata. Here, sparse means at least two of director, cast, and country are missing. This analysis does not measure description or genre-tag completeness, and the release vintage is not the year a title was added to Netflix.

This is a reason to audit metadata coverage for recent releases. It does not establish why those fields are missing or how the gaps affect discovery.

![UK Netflix titles by release vintage: 12.8% of titles from the 2020s had sparse director, cast, or country metadata](/images/netflix-beat05.png)

## Recommendations

1. **Use separate freshness goals.** Track new TV shows and the depth of the movie library separately so one trend does not hide the other.
2. **Check core metadata before launch.** Track director, cast, and country field coverage for new releases; run a separate description and tag audit before making discovery claims.
3. **Test repeat partnerships in documentaries.** Explore longer-term relationships where they could reduce negotiation effort without limiting creative choice.

## Takeaway

The US catalog additions showed two different freshness patterns for TV shows and movies. The UK metadata gap is a separate signal based on release vintage and three core fields. Neither pattern measures viewing or proves a customer outcome, so freshness and metadata should be treated as operating checks rather than success measures.

**Code and data:** [View the analysis scripts](https://github.com/hadibudhy/hadibudhy.github.io/tree/master/legacy_jekyll/scripts/netflix)
