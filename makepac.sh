#!/bin/bash
python buildpac.py except.txt direct.txt DIRECT name1.txt "PROXY 10.9.0.1:3128" name2.txt "PROXY 10.9.0.1:3128"
