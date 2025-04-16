+++
title = "Call for publishing Veryl source code on GitHub"
+++

Veryl is a new hardware description language as an alternate to SystemVerilog.

This article is written to call you for publishing Veryl source code on GitHub.
By publishing your source code, even if it is very simple like just "Hello World", the followings become possible.
Please cooperate with us!

## Syntax highlighting support on GitHub

The criteria of adding a language to the syntax highlighting library of GitHub is defined like below:

* at least 2000 files per extension indexed in the last year (the number you see at the top of the search results), unless the extension is expected to only occur once per repo, then 200 files.
* with a reasonable distribution across unique `:user/:repo` combinations assessed by manually and randomly clicking through the results.

The first means that at least 2000 `*.veryl` files are necessary, and the second means that the bias to the specific repositories like `veryl-lang/veryl` is excluded.
The current status is gathered periodically, and published at the following site.

[https://veryl-lang.org/statistics/](https://veryl-lang.org/statistics/)

## Unexpected breaking change detection

The repository of Veryl compiler has some testcases to detect unexpected breaking changes, but they are insufficient to cover all cases.
So we are periodically gathering Veryl projects published on GitHub, and checking whether they are compiled successfully.
Along with increasing actual Veryl projects, various use cases become to be covered.

The gathering tool and gathered DB is in the following repository.

[https://github.com/veryl-lang/discovery](https://github.com/veryl-lang/discovery)
