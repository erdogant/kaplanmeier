.. include:: add_top.add

Create kaplanmeier plot
####################################

In the following example we load the patient dataset and create the kaplanmeier plot, and compute the log-rank test.

.. code:: python
	
	# Import library
	import kaplanmeier as km
	
	# Import example data
	df = km.example_data()

	# Data
	time_event = df['time']
	censoring = df['Died'] 
	y = df['group']

	print(df)
	#       time  Died  group
	# 0     485     0      1
	# 1     526     1      2
	# 2     588     1      2
	# 3     997     0      1
	# 4     426     1      1
	# ..    ...   ...    ...
	# 175   183     0      1
	# 176  3196     0      1
	# 177   457     1      2
	# 178  2100     1      1
	# 179   376     0      1
        # 
	# [180 rows x 3 columns]

	# Compute Survival
	results = km.fit(time_event, censoring, y)

	# Plot
	km.plot(results)


.. |fig1| image:: ../figs/fig2.png

.. table:: kaplanmeier plot.
   :align: center

   +----------+
   | |fig1|   |
   +----------+



Change colormap and confidence intervals
############################################

.. code:: python
	
	# Plot
	km.plot(results, cmap='Set1', cii_lines='dense', cii_alpha=0.05)


.. |fig3| image:: ../figs/fig3.png

.. table:: kaplanmeier plot.
   :align: center

   +----------+
   | |fig3|   |
   +----------+


Custom colormap
############################################

.. code:: python
	
	# Plot
	km.plot(results, cmap=[(1, 0, 1),(0, 1, 1)])


.. |fig4| image:: ../figs/fig4.png

.. table:: kaplanmeier plot.
   :align: center

   +----------+
   | |fig4|   |
   +----------+


Use custom kaplanmeier method
############################################

.. code:: python
	
	# Plot
	km.plot(results, cmap='Set2', methodtype='custom')


.. |fig6| image:: ../figs/fig6.png

.. table:: kaplanmeier plot.
   :align: center

   +----------+
   | |fig6|   |
   +----------+





.. include:: add_bottom.add