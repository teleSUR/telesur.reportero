#! /bin/sh

for filename in `find src/telesur/reportero/ -iname "*.py"`; do
    pep8 $filename
    pyflakes $filename
done
