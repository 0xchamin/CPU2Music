
set logging file cpu_instructions.log
set logging overwrite on
set logging on
set args "Chamin Nalinda Lokugam Hewage"
break process_name
run
set logging off
quit
