Bug: `IO.print` is used for every line, so the address prints on one line. Fix: use `IO.println`
(at least for the first two lines).
