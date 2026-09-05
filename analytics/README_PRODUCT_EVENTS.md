# Product event foundation

The REES46 Electronics event source contains observed view, cart, and purchase events. It has no signup, impression, order ID, quantity, or experiment assignment. The product case therefore measures an observed browse-to-purchase journey and proposes an activation test; it does not claim a deployed onboarding experiment.

The first model keeps every event, quarantines missing-session rows from ordered-session analysis, orders ties deterministically by timestamp and event key, and records source quality beside funnel metrics.
