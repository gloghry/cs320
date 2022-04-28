# make source for Garett's project.
# it should be noted that we did not discuss which version of python everyone is on
garett: main_GUI.py
	python3 main_GUI.py

# line count finder
# grep -v -E '^\s*(/[*/].*|}\s*|\*.*||#.*|\{\s*)$' <filename> |wc -l
