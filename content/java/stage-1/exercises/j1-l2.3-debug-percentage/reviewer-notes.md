Bug: `correct / total` is integer division, so any score below full marks becomes 0 before
multiplying by 100 (catalogue MC04). Accept any fix that makes the division happen in double
arithmetic, e.g. `correct * 100.0 / total` or `(double) correct / total * 100`.
