#!/bin/sh
# Compilazione del solutore (Ottavia). Richiede gfortran.
set -e
cd "$(dirname "$0")"
mkdir -p bin
gfortran -O2 -std=f2008 -Wall -Wextra -fcheck=bounds -o bin/telaio2d src/telaio2d.f90
echo "compilato: $(pwd)/bin/telaio2d"
