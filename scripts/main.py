#!python

def test(pf):
	pf.plot()
	print "Measuring"
	pf.measurement(90,15)
	pf.resample()
	print "Measuring"
	pf.measurement(-90,15)
	pf.resample()
	pf.measurement(0,35)
	pf.resample()
	pf.plot()
	print "Moving"
	pf.movement_position([20,0])
	pf.plot()
	print "Measuring"
	pf.measurement(-90,15)
	pf.resample()
	pf.measurement(90,45)
	pf.resample()
	pf.measurement(0,15)
	pf.resample()
	pf.plot()
	pf.movement_angle_deg(90)
	pf.movement_position([30,0])
	pf.measurement(0,15)
	pf.resample()
	#pf.movement_position([0,20])
	print "Measuring"
	pf.measurement(-90,15)
	pf.resample()
	pf.measurement(90,75)
	pf.resample()
	pf.plot()
	return

if __name__ == "__main__":
	import particlefilter
	print("Staring the script...")
	pf = particlefilter.ParticleFilter(2600*16)
	test(pf)
else:
	print("Just WHAT THE FUCK?")
