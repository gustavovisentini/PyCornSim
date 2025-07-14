# PyCornSim


This is a tool designed to run automated simulations using the DSSAT (CERES-Maize) model, integrating NASA POWER weather data, soil profiles, and genetic parameters provided via the `config.json` file.

---

## 1. **Loading Configuration**

The script loads simulation settings from the `config.json` file, including:

- User name (`name`)
- Simulation latitude and longitude
- Simulation start year (`sim_year`)
- Planting year (`planting_year`)
- Management type (irrigated or rainfed)
- Genotype (`ingeno`)
- Hybrid name (`cname`)

---

## 2. **Downloading Weather Data**

Uses the **NASA POWER** API to download historical weather data (temperature, radiation, precipitation) for the specified location and formats it for DSSAT compatibility.

---

## 3. **Identifying Soil Profile**

Finds the closest matching soil profile from the `US.SOL` file based on the provided coordinates (lat, lon), which is essential for the simulation.

---

## 4. **Extracting Initial Soil Conditions (IC)**

Uses a spatial soil dataset to estimate and extract initial soil conditions, such as residual nitrogen and moisture levels.

---

## 5. **Creating Simulation Structure**

Creates a new directory for the simulation, named based on the hybrid (`RUN_ID + ingeno`), and inserts the identified soil profile into the `SOIL.SOL` file.

---

## 6. **Configuring the `.SNX` File**

Modifies the `.SNX` simulation file dynamically to include:

- Weather station ID
- Genotype and hybrid name
- Planting dates and initial soil conditions
- Soil ID

---

## 7. **Running the DSSAT Model**

Executes the DSSAT model (`dscsm048`) inside the simulation folder with the proper command to run the simulation based on the defined settings.

---

## 8. **Post-processing the Results**

Reads the `summary.OUT` file, filters key metrics such as yield, and saves a processed CSV (`processed_output.csv`) with summarized results.

---


# Usage

First step, download the soil files and dssat executable.

[US.SOIL file](https://drive.google.com/file/d/1Tp_vavwiyU948b757wmaz1tSCQ4Pl4qK/view?usp=sharing)

The US.SOIL file must be placed inside the soil folder 
For dssat executable, just chanfe the absolute path to executable inside the dssat folder within the code afterwards.

You need to create a python virtual environment venv to run the project. At the same level as the project folder create the venv vistaa-venv


```bash
  python -m venv pycornsim-venv
```

Activate the venv 

```bash
  source vistaa-venv/bin/activate
```

Install the packages Pandas, Rich, Geopy

```bash
  pip install pandas rich geopy

```

For run sin single core use the command

```bash
  python run.py
```

## Project Structure

```bash
.
├── classes
│   ├── fertilizer_modifier.py
│   ├── ic_soil_extractor.py
│   ├── post_processing.py
│   ├── prepare_simulation.py
│   ├── run_command.py
│   ├── soil_profile_appender.py
│   ├── soil_profile_finder.py
│   ├── template_modifier.py
│   └── weather_downloader.py
├── config.json
├── dssat
│   └── dscsm048
├── OUTPUT
│   ├── INGENO_IB0068
│   └── processed_output.csv
├── pycornsim-venv
│   ├── bin
│   ├── include
│   ├── lib
│   └── pyvenv.cfg
├── README.md
├── run.py
├── soil
│   ├── ICREN.asc
│   ├── ICRES.asc
│   ├── ICRT.asc
│   ├── soil_profile_number.asc
│   ├── SOIL.SOL
│   └── US.SOL
├── template
│   ├── MZCER048.CUL
│   ├── MZCER048.ECO
│   ├── MZCER048.SPE
│   ├── readme.md
│   ├── UFGA0001.SNX
│   └── UFGA0002.SNX
└── weather
    └── WSTATION.WTH

```


## Demonstration


```bash
  python run.py
```

Output example on processed_output.csv

```bash
Apr_2_250N_Rainfed       ,2018,2018103,2018122,0
Apr_2_300N_Rainfed       ,2018,2018103,2018122,0
Apr_2_350N_Rainfed       ,2018,2018103,2018122,0
Apr_2_400N_Rainfed       ,2018,2018103,2018122,0
Apr_3_50N_Rainfed        ,2018,2018114,2018125,8872
Apr_3_100N_Rainfed       ,2018,2018114,2018125,11426
Apr_3_150N_Rainfed       ,2018,2018114,2018125,12633
Apr_3_200N_Rainfed       ,2018,2018114,2018125,13591
Apr_3_250N_Rainfed       ,2018,2018114,2018125,14176
Apr_3_300N_Rainfed       ,2018,2018114,2018125,14854
Apr_3_350N_Rainfed       ,2018,2018114,2018125,15601
Apr_3_400N_Rainfed       ,2018,2018114,2018125,16126
May_1_50N_Rainfed        ,2018,2018125,2018135,10276
May_1_100N_Rainfed       ,2018,2018125,2018135,12417
May_1_150N_Rainfed       ,2018,2018125,2018135,13349
May_1_200N_Rainfed       ,2018,2018125,2018135,14370
May_1_250N_Rainfed       ,2018,2018125,2018135,15099

```

Note that there are different treatments created in the UFGA0002.SNX file. In the last column we have the yield in kg/ha

## Authors

- [@gustavovisentini](https://www.github.com/gustavovisentini)

