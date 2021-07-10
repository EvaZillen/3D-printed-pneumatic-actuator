## Results - pneumatic actuator
Here our 3D printed pneumatic actuators are evaluated on static leakage, dynamic leakage, and dynamic sliding friction force.

### Code
Simply run `jupyter notebook` in this folder to view the interactive Notebooks

As alternative, the scripts can be run with native Python by `python3 results_dynamic_leakage.py`

### Data
All the data used in this research is collected with our own experimental test setup. The collected data is split in four different folders, each containing the data for that specific test. 
##### /data/dynamic
Contains one `.csv` file for each tested model. Each model is extended and retracted for 200 times and each test took approximately 20 minutes to assess the (possible) dynamic leakage.
##### /data/static
Contains one `.csv` file for each tested model. Each model is moved to a high pressure position and held there for approcimately 20 minutes to assess the (possible) static leakage.
##### /data/friction
Contains one `.csv` file for each presure level tested per model. Each dataset contains 10 test runs which each took approximately 1 minute to perform.
##### /data/repeatability
Contains two extra datasets, created to assess the repeatability of all above tests

#### Data headers
Each `.csv` consists of the following seven columns: 
| Time (in ms) | Laser (in V) | Pressure (in V) | Force (in V) | Laser (in mm) | Pressure (in bar) | Force (in N) |
|--------------|--------------|-----------------|--------------|---------------|-------------------|--------------|
