import numpy as np

SENSOR_LABEL = { # http://www.ioccg.org/sensors/seawifs.html
	'CZCS'   : 'Nimbus-7',
	'TM'     : 'Landsat-5',
	'ETM'    : 'Landsat-7',
	'OLI'    : 'Landsat-8',
	'L10'    : 'Landsat-10',
	'OSMI'   : 'Arirang-1',
	'POLDER' : 'POLDER',
	'AER'    : 'AERONET',
	'OCTS'   : 'ADEOS-1',
	'SEAWIFS': 'OrbView-2',
	'VI'     : 'Suomi-NPP',
	'MOS'    : 'MOS-1',
	'MOD'    : 'MODIS',
	'MODA'   : 'MODIS-Aqua',
	'MODT'   : 'MODIS-Terra',
	'MSI'    : 'Sentinel-2',
	'S2A'    : 'Sentinel-2A',
	'S2B'    : 'Sentinel-2B',
	'S3A'    : 'Sentinel-3A',
	'S3B'    : 'Sentinel-3B',
	'OLCI'   : 'Sentinel-3',
	'MERIS'  : 'Envisat-1',
	'HICO'   : 'HICO',
	'HYPER'  : '1nm Hyperspectral',
	'PRISMA' : 'PRISMA',
}


duplicates = {}

# Add duplicate sensors
for sensor, dups in duplicates.items():
	for dup in dups:
		SENSOR_LABEL[dup] = SENSOR_LABEL[sensor]


def get_sensor_label(sensor):
	sensor, *ext = sensor.split('-')
	assert(sensor in SENSOR_LABEL), f'Unknown sensor: {sensor}'

	label = SENSOR_LABEL[sensor]
	if 'pan' in ext:
		label += '+Pan'
	return label

# --------------------------------------------------------------

SENSOR_BANDS = {
	'CZCS'     : [     443,           520, 550,                     670                                   ],
	'TM'       : [               490,      560,                     660                                   ],
	'ETM'      : [               483,      560,                     662                                   ],
	'ETM-pan'  : [               483,      560,                     662,                               706],
	'OLI'      : [     443,      482,      561,                     655                                   ],
	'OLI-pan'  : [     443,      482,      561,   589,              655,                                  ],
	'OLI-full' : [     443,      482,      561,                     655,                               865],
	'OLI-nan'  : [     443,      482,      561,   589,              655,                               865],
	'OLI-rho'  : [     443,      482,      561,                     655,                               865, 1609],
	'L10'      : [409, 444,      490,      558,      621, 650,      667,      707, 742                    ],
	'OSMI'     : [412, 443,      490,      555,                                              765          ],
	'POLDER'   : [     443,      490,      565,                     670,                     765          ],
	'AER'      : [412, 442,      490, 530, 551,                     668                                   ],
	'OCTS'     : [412, 443,      490, 520, 565,                     670,                     765          ],
	'SEAWIFS'  : [412, 443,      490, 510, 555,                     670,                     765          ],
	'VI'       : [410, 443,      486,      551,                     671,           745                    ],
	'MOS'      : [408, 443,      485, 520, 570,      615, 650,      685,           750                    ],
	'MOD'      : [412, 443, 469, 488, 531, 551, 555,      645, 667, 678,           748                    ],
	'MOD-IOP'  : [412, 443, 469, 488, 531, 551, 555,      645, 667, 678,                                  ],
	'MOD-poly' : [412, 443,      488, 531, 551,                667, 678,           748                    ],
	'MSI'      : [     443,      490,      560,                     665,      705, 740,                783],
	'MSI-rho'  : [     443,      490,      560,                     665,      705, 740,                783, 865],
	'OLCI'     : [411, 442,      490, 510, 560,      619,      664, 673, 681, 708, 753, 761, 764, 767, 778],
	'OLCI-no760'     : [411, 442,      490, 510, 560,      619,      664, 673, 681, 708, 753,  778],

	'OLCI-noB'     : [510, 560,      619,      664, 673, 681, 708, 753, 761, 764, 767, 778],
	'OLCI-noBG'     : [560,      619,      664, 673, 681, 708, 753, 761, 764, 767, 778],
	'OLCI-noNIR'     : [411, 442,      490, 510, 560,      619,      664, 673, 681, 708],

	'OLCI-noNIR_LB'     : [442,      490, 510, 560,      619,      664, 673, 681, 708],
	'OLCI-noBnoNIR'     : [ 510, 560,      619,      664, 673, 681, 708],
	'OLCI-SimisFull'     : [ 442,      490, 510, 560,      619,      664, 673, 681, 708, 753, 761, 764, ],
	'OLCI-Simis2007'     : [ 619,      664, 708, 778 ],

	'OLCI-e'   : [411, 442,      490, 510, 560,      619,      664, 673, 681, 708, 753,                778],
	'OLCI-poly': [411, 442,      490, 510, 560,      619,      664,      681, 708, 753,                778],
	'OLCI-sat' : [411, 442,      490, 510, 560,      619,      664, 673, 681, 708, 753, 761, 764, 767,    ],
	'MERIS'    : [412, 442,      490, 510, 560,      620,      665,      681, 708, 753, 760,           778],
	'PRISMA'   : [402, 411, 419, 427, 434, 441, 449, 456, 464, 471, 478, 485, 493, 500, 507, 515, 523, 530,
				  538, 546, 554, 563, 571, 579, 588, 596, 605, 614, 623, 632, 641, 651, 660, 670, 679, 689, 
				  699, 709, 719, 729, 739, 749, 760, 770, 781, 791, 802, 812, 823, 833, 844, 855, 866, 876, 
				  887, 898, 908, 919, 929, 940, 943, 951, 959, 969],
	'PRISMA-Simis'   : [441, 493, 554, 623,670, 709, 781,],
	'PRISMA-noBnoNIR'   : [500, 507, 515, 523, 530,
				  538, 546, 554, 563, 571, 579, 588, 596, 605, 614, 623, 632, 641, 651, 660, 670, 679, 689, 
				  699, 709, 719, ],
	'PRISMA-SimisFull'   : [441, 449, 456, 464, 471, 478, 485, 493, 500, 507, 515, 523, 530,
				  538, 546, 554, 563, 571, 579, 588, 596, 605, 614, 623, 632, 641, 651, 660, 670, 679, 689, 
				  699, 709, 719, 729, 739, 749, 760,],	
	'PRISMA-SimisFullMatchup'   : [441, 449, 456, 464, 471, 478, 485, 493, 500, 507, 515, 523, 530,
				  538, 546, 554, 563, 571, 579, 588, 596, 605, 614, 623, 632, 641, 651, 660, 670, 679, 689, 
				  699, 709, 719, 729, 739, 749, 760, 770, 781,],	


	'HICO'     : [409, 415, 421, 426, 432, 438, 444, 449, 455, 461, 467, 472, 478, 484, 490, 495, 501, 507,
				  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713,
				  719, 724, 730, 736, 742, 747, 753, 759, 764], #Removed 770-787, due to lack of in situ data
				  
	'HICO-SimisFull'     : [444, 449, 455, 461, 467, 472, 478, 484, 490, 495, 501, 507,
				  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713,
				  719, 724, 730, 736, 742, 747, 753, 759, 764],
	'HICO-Simis'     : [444,490,553,621,667,673,707,776,], 
	'HICO-Simis2007'     : [621,667,707,787,], 

	'HICO-Schalles'      : [621,650,], 
	'HICO-Hunter'      : [598,616,724], 

	'HICO-noB' :  [501, 507,
				  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713,
				  719, 724, 730, 736, 742, 747, 753, 759, 764], 

	'HICO-noBG': [553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713,
				  719, 724, 730, 736, 742, 747, 753, 759, 764], 

	'HICO-noNIR': [409, 415, 421, 426, 432, 438, 444, 449, 455, 461, 467, 472, 478, 484, 490, 495, 501, 507,
				  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713,
				  719, 724], 
	'HICO-noNIR_LB': [ 415, 421, 426, 432, 438, 444, 449, 455, 461, 467, 472, 478, 484, 490, 495, 501, 507,
				  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713,
				  719, 724], 
	'HICO-noBnoNIR': [501, 507,
				  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713,
				  719, 724], 				  
	# 'HICO'     : [409, 415, 421, 426, 432, 438, 444, 449, 455, 461, 467, 472, 478, 484, 490, 495, 501, 507,
	# 			  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
	# 			  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713,
	# 			  719, 724, 730, 736, 742, 747, 753, 759, 764, 770, 776, 782, 787],
	'HICO-chl' : [501, 507, 512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598,
				  604, 610, 616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701,
				  707, 713],
	'HICO-IOP' : [409, 415, 421, 426, 432, 438, 444, 449, 455, 461, 467, 472, 478, 484, 490, 495, 501, 507,
				  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690], # absorption data becomes negative > 690nm
	'HICO-sat' : [409, 415, 421, 426, 432, 438, 444, 449, 455, 461, 467, 472, 478, 484, 490, 495, 501, 507,
				  512, 518, 524, 530, 535, 541, 547, 553, 558, 564, 570, 575, 581, 587, 593, 598, 604, 610,
				  616, 621, 627, 633, 638, 644, 650, 656, 661, 667, 673, 679, 684, 690, 696, 701, 707, 713],

	'HYPER'    : list(range(400, 799)),
	'test':[1]
}

duplicates = {
	'MOD' : ['MODA', 'MODT'],
	'MSI' : ['S2A', 'S2B'],
	'OLCI' : ['S3A', 'S3B'],
}

# Add duplicate sensors
for sensor in list(SENSOR_BANDS.keys()):
	for sensor2, dups in duplicates.items():
		if sensor2  in sensor:
			for dup in dups:
				SENSOR_BANDS[sensor.replace(sensor2, dup)] = SENSOR_BANDS[sensor]

# Add partial-band satellite keys to the label dictionary
for sensor in SENSOR_BANDS:
	if '-' in sensor:
		s = sensor.split('-')[0]
		if sensor not in SENSOR_LABEL:
			SENSOR_LABEL[sensor] = SENSOR_LABEL[s]


def get_sensor_bands(sensor, args=None):
	assert(sensor in SENSOR_BANDS), f'Unknown sensor: {sensor}'
	bands = set()
	if args is not None:

		# Specific bands can be passed via args in order to override those used
		if hasattr(args, 'bands'):
			return np.array(args.bands.split(',') if isinstance(bands, str) else args.bands)

		# The provided bands can change if satellite bands with certain products are requested
		elif args.sat_bands:
			product_keys = {
				'chl' : ['chl'],
				'IOP' : ['aph', 'a*ph', 'ag', 'ad'],
			}

			for key, products in product_keys.items():
				for product in args.product.split(','):
					if (f'{sensor}-{key}' in SENSOR_BANDS) and (product in products):
						bands |= set(SENSOR_BANDS[f'{sensor}-{key}'])

			if len(bands) == 0 and f'{sensor}-sat' in SENSOR_BANDS:
				sensor = '{sensor}-sat'

	if len(bands) == 0:
		bands = SENSOR_BANDS[sensor]
	return np.sort(list(bands))

# --------------------------------------------------------------

# Ancillary parameters for certain models
ANCILLARY = [
	'humidity',    # Relative humidity (%)
	'ice_frac',    # Ice fraction (0=no ice, 1=all ice)
	'no2_frac',    # Fraction of tropospheric NO2 above 200m
	'no2_strat',   # Stratospheric NO2 (molecules/cm^2)
	'no2_tropo',   # Tropospheric NO2 (molecules/cm^2)
	'ozone',       # Ozone concentration (cm)
	'pressure',    # Surface pressure (millibars)
	'mwind',       # Meridional wind speed @ 10m (m/s)
	'zwind',       # Zonal wind speed @ 10m (m/s)
	'windangle',   # Wind direction @ 10m (degree)
	'windspeed',   # Wind speed @ 10m (m/s)
	'scattang',    # Scattering angle (degree)
	'senz',        # Sensor zenith angle (degree)
	'sola',        # Solar azimuth angle (degree)
	'solz',        # Solar zenith angle (degree)
	'water_vapor', # Precipitable water vapor (g/cm^2)
	'time_diff',   # Difference between in situ measurement and satellite overpass (in situ prior to overpass = negative)
]

# Ancillary parameters which are periodic (e.g. 0 degrees == 360 degrees)
PERIODIC = [
	'windangle',
]
