.PHONY: generate-one generate-all check-structure

CONTEXT ?= content/problems/lc-39-combination-sum.md


generate-one:
	python3 tools/generate_problem_html.py --context $(CONTEXT)

generate-all:
	python3 tools/generate_problem_html.py --all-md

check-structure:
	python3 tools/check_structure.py
