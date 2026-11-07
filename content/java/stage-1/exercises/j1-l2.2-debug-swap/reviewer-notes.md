Bug: the naive swap overwrites `morning` before saving it (MC02), so both end up "Tea". Accept any
fix that saves one value first. Hard-coding the strings would also pass the test; the mentor and
the explain exercise target the reasoning.
