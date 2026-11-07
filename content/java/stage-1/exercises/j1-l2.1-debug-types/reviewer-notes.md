Two type errors: `int` can't hold 2.75 ("possible lossy conversion from double to int"), and
`"true"` is a String where a boolean is needed. Fix: make coffeePrice a `double`, and return
`true` without quotes. Rounding the price (wrong/rounded-price) must fail.
