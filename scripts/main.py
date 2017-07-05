#!python
if __name__ == "__main__":
	import particlefilter
	print("Staring the script...")
	pf = particlefilter.ParticleFilter(2600*16)
	pf.measurement(45,[2,2])
else:
	print("Just WHAT THE FUCK?")
