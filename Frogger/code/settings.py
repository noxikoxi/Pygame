WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

CAR_START_POSITIONS = [(-100, 1312), (-100, 1632), (-100,1888), 
	(-100, 2471), (-100,2853), (-100, 3080), (3300, 1400), 
	(3300,1760), (3300, 1970), (3300, 2550), (3300, 2981)]

SIMPLE_OBJECTS = {
	'green': [(969.0,3104.17),(986.833,3164.67),(1327.33,3288.67),(1114.67,3084.0),(1468.67,3165.33),(1589.33,3305.33),(1456.67,3298.67),(1659.0,3112.0),
			  (2358.67,3254.67),(2437.33,3315.33),(2470.0,3107.33),(2154.67,3275.33),(1729.33,3210.0),(1747.33,3288.67),(1188.0,3186.67),(1019.67,3262.67),
			  (1552.67,3324.0),(1814.0,3351.33),(2402.0,3366.67),(1047.0,3304.0),(980.5,3327.0),(1050.0,3365.5),(2278.0,2624.0),(2346.0,2560.0),
			  (2209.0,2594.0),(2229.0,2665.0),(834.667,2149.33),(928.0,2209.33),(2473.33,2121.33),(2449.33,2232.67),(877.333,766.667),
			  (648.0,941.3299999999999),(681.333,897.33), (1346.00,1070.00), (1794.00,1070.00)],
	'green_bush': [(1626.5,3235.67),(1482.67,3264.0),(1520.0,3304.0),(1407.33,3390.67),(1084.67,3172.67),(1003.83,3145.83),(1010.67,3261.0),
				   (1385.0,2627.0),(865.0,2675.0),(941.0,2614.0),(1086.0,2693.0),(1275.0,2723.0),(1407.0,2716.0),(1166.0,2618.0),
				   (826.0,2720.0),(1066.0,2714.0),(1220.0,2726.0),(1244.0,2709.0),(652.0,2198.67),(916.0,2190.67),(2274.0,2218.0),
				   (2280.0,2246.0),(2382.0,2286.0),(2364.0,2213.33),(2413.33,1134.67),(2165.33,1126.67),(2065.33,985.3299999999999),
				   (2361.33,956.0)],
	'green_mini': [(1140.67,3175.33),(1338.0,3130.67),(1368.67,3236.67),(1108.0,3278.67),(1173.33,3338.0),(1226.0,3216.67),(1272.0,3178.67),
				   (1268.66,3270.0),(2348.67,3417.33),(2456.67,3204.67),(2323.33,3162.0),(2091.33,3372.67),(1776.67,3165.33),(1938.67,3157.33),
				   (1846.0,3279.33),(1081.0,3383.5),(1010.0,2665.0),(1163.0,2690.0),(1344.0,2651.0),(2204.0,2695.0),(2262.0,2729.0),(664.0,2288.0),
				   (858.667,2230.67)],
	'green_small_potted': [(1504.00, 936.00), (1740.00,936.0)],
	'barrel_1': [(642.5,3138.0),(663.0,3164.0),(2560.67,2174.0),(2566.0,2116.0),(2616.67,2072.0),(2616.67,2118.0),(2683.33,2160.0),
				 (2677.33,2116.0),(2680.0,2038.0),(664.0,2718.0),(2572.0,1466.0),(678.0,3319.83),(700.667,3334.5)],
	'barrel_2': [(2579.33,2147.33),(2568.0,2050.0),(2635.33,2150.0),(2607.33,2046.0),(2600.0,2088.0), (2566.00,1576.00), (2546.00,1538.00)],
	'barrel_3': [(2560.0,2080.0),(2696.0,2106.0),(2657.33,2058.0),(860.667,2289.0)],
	'hydrant': [(919.333,2093.0),(650.0,3245.83)],
	'bench_down': [(1235.33,3333.33), (2213.0,3157.0)],
	'bench_left': [(2522.0,3263.33),(2518.67,2233.33)],
	'letterbox_down': [(1418.67,928.67)],
	'yellow_up': [(819.00,3224.50)],
	'red_right': [(740.00,3315.50)],
	'red_left': [(550.67,1200.00)],
	'green_down': [(713.00,3236.50), (510.67,1276.67)],
	'barrier_1': [(647.0,2633.0)],
	'barrier_4': [(898.0,3147.5),(694.667,2669.67),(661.333,2745.67),(608.0,1528.0),(588.0,1462.0)],
	'barrier_5': [(2368.06,3471.44)],
	'box_4': [(716.0,865.333),(866.667,892.0)],
	'box_7': [(782.667,942.667),(752.0,888.0),(817.333,845.333)],
	'box_10': [(730.667,951.33), (865.333,952.67), (805.333,900.667)]}

LONG_OBJECTS = {
	'light_both': [(2333.5,2669.0),(2112.67,2669.33),(1087.33,2278.67),(2012.67,2035.33)],
	'light_green': [(2439.33,2116.0), (911.333,2170.67), (2284.67,3089.33)],
	'light_wooden': [(795.913,2087.96), (1106.0,1430.0), (2046.0,1428.0), (2202.67,2016.0)],
	'sign_2': [(1882.00,956.00)]}