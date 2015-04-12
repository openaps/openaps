
# openaps utility belt

These are the [core utilities][proposal] needed to develop an open source
artificial pancreas.

[proposal]: https://gist.github.com/bewest/a690eaf35c69be898711

This is not an artificial pancreas, but rather tools which independently allow:

* monitor - Collect data about environment, and operational status of devices.
  Aggregate as much data relevant to therapy as possible into one place.
  We propose a tool, `openaps-get` as a proof of concept.

* predict - Can make predictions about what should happen next.

* control - Can enact changes in the world: emails, placing phone calls, SMS,
  issuing commands to pumps.



