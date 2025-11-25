# Raw Data Documentation

> **Purpose:** This file tracks the lineage and renaming logic of raw data files before they are entered into the Data Version Control (DVC) pipeline.
>
> **Workflow:** Download -> Rename (via tools/rename_raw_data.py) -> dvc add -> Git Commit.

## 1. Crime Incident Data
**Source:** [Atlanta Police Department Open Data Portal](https://aggregated-crime-data-atlantapd.fandom.com/wiki/Main_Page) / Axon
**Last Accessed:** Nov 25, 2025

| Final Filename | Original Filename | Format | Description |
| :--- | :--- | :--- | :--- |
| **`apd_crime_2021_2024.csv`** | `OpenDataWebsite_Crime_view_-1943907682062759239.csv` | CSV | Primary crime dataset. Filtered for 2021-2024. |
| **`apd_crime_2021_2024.geojson`** | `OpenDataWebsite_Crime_view_8524236547521519883.geojson` | GeoJSON | GeoJSON version of the crime dataset. |

---

`Note: APD Shapefile was originally included as well, but it exceeded GitHub file size limits.`

---
## 2. City of Atlanta Boundaries
**Source:** Atlanta Department of City Planning / Open Data
**Last Accessed:** Nov 25, 2025

| Final Filename | Original Filename | Description |
| :--- | :--- | :--- |
| **`atl_npu_boundaries.shp`** | `Official_NPU_-_Open_Data.shp` | Official geometries for Neighborhood Planning Units (NPUs). |
| **`atl_neighborhoods.shp`** | `Official_Neighborhoods_-_Open_Data.shp` | Official geometries for individual neighborhoods. |
| **`apd_police_zones_2019.shp`** | `APD_Zone_2019.shp` | Police Zone boundaries (specifically the 2019 revision). |

---

## 3. Census & State Geography
**Source:** US Census Bureau (TIGER/Line & Cartographic Boundaries)
**Last Accessed:** Nov 25, 2025

| Final Filename | Original Filename | Description |
| :--- | :--- | :--- |
| **`ga_census_places_2024.shp`** | `cb_2024_13_place_500k.shp` | Census "Places" (Cities/Towns) for Georgia (FIPS 13). Scale 1:500k. |
| **`ga_census_landmarks_2023.shp`** | `tl_2023_13_arealm.shp` | Area Landmarks (Parks, Schools, large campuses) for Georgia. |

---

## 4. Renaming Logic
*Files were renamed using the automated utility script located at `tools/rename_raw_data.py` to ensure consistency across Shapefile components (.shp, .dbf, .shx, .prj, .cpg).*