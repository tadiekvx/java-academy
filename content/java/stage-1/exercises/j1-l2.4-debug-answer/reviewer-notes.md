Bug: `==` compares object identity (MC05). The literal "paris" input passes by coincidence (interning), which is exactly why the bug survives casual testing.
