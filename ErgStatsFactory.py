import dynrow_args 

# get erg data from either PyRow or pyerg
if not dynrow_args.args.pyerg:
    from PyRow.ErgStats import ErgStats
else:
    from pyerg_adapter.ErgStats import ErgStats
