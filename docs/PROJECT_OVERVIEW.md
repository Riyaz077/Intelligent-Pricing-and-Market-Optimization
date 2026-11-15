# Project Overview

PriceSense AI demonstrates a pricing intelligence workflow: ingest product and competitor reference prices, explore historical-like sales patterns, fit a demand model, simulate demand over a bounded price grid, and rank candidate prices by predicted revenue.

The competitor component compares the submitted price with a synthetic competitor reference. It does not scrape websites or connect to retailer APIs. The recommendation is model-based and should not be interpreted as causal proof that changing a price will produce the predicted outcome.
