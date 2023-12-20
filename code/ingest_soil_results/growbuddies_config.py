from enum import Enum, auto


class OutputType(Enum):
    INFLUXDB = auto()
    MARKDOWN = auto()
    BOTH = auto()


soil_results_config = {
    "directory":"C:\\Users\\happy\\Documents\\Obsidian Vault\\GrowBuddies_doc\\soil_science\\Soil Tests\\Results\\",
    "udp_ports": {"SP": 8196, "M3": 8195},
    "output_type": OutputType,
    "name_mapping": {
        "Sample Location": "Sample_Location",
        "Total Exchange Capacity (M. E.)": "TEC",
        "pH of Soil Sample": "pH",
        "Organic Matter, Percent": "Organic_%",
        "SULFUR (ppm)": "Sulfur_ppm",
        "SULFUR: p.p.m.": "Sulfur_ppm",
        "Bicarbonate (HCO3) ppm":"Bicarbonate_ppm",
        "Mehlich III Phosphorous: as (P O )\n2 5\nlbs / acre": "Phosphorous_lbs",
        "Desired Value\nCALCIUM:\nValue Found\nlbs / acre\nDeficit": "Calcium_lbs",
        "Desired Value\nMAGNESIUM:\nValue Found\nlbs / acre\nDeficit": "Magnesium_lbs",
        "Desired Value\nPOTASSIUM:\nlbs / acre Value Found\nDeficit": "Potassium_lbs",
        "SODIUM: lbs / acre": "Sodium_lbs",
        "Calcium (60 to 70%)": "Calcium_%",
        "Calcium": "Calcium_%",
        "Magnesium (10 to 20%)": "Magnesium_%",
        "Magnesium": "Magnesium_%",
        "Potassium (2 to 5%)": "Potassium_%",
        "Potassium": "Potassium_%",
        "Sodium (.5 to 3%)": "Sodium_%",
        "Sodium": "Sodium_%",
        "Soluble Salts ppm": "Soluble_Salts_ppm",
        "Chloride (Cl) ppm": "Chloride_ppm",
        "Bicarbonate HCO3) ppm": "Bicarbonate_ppm",
        "Other Bases (Variable)": "Other_bases",
        "Exchangable Hydrogen (10 to 15%)": "Exchangable_Hydrogen",
        "Boron (p.p.m.)": "Boron_ppm",
        "Iron (p.p.m.)": "Iron_ppm",
        "Manganese (p.p.m.)": "Manganese_(ppm",
        "Copper (p.p.m.)": "Copper_ppm",
        "Zinc (p.p.m.)": "Zinc_ppm",
        "Aluminum (p.p.m.)": "Aluminum_ppm",
        "Ammonium (p.p.m.)": "Ammonium_ppm",
        "Nitrate (p.p.m.)": "Nitrate_ppm",
        "Media Density g/cm3": "Media_Density",
        "PHOSPHORUS (ppm)": "Phosphorous_ppm",
        "CALCIUM (ppm)": "Calcium_ppm",
        "CALCIUM (meq/l)": "Calcium_meq/L",
        "MAGNESIUM (ppm)": "Magnesium_ppm",
        "MAGNESIUM (meq/l)": "Magnesium_meq/L",
        "POTASSIUM: (ppm)": "Potassium_ppm",
        "POTASSIUM: (meq/l)": "Potassium_meq/L",
        "SODIUM (ppm)": "Sodium_ppm",
        "SODIUM (meq/l)": "Sodium_meq/L",
        "Boron (p.p.m.)": "Boron_ppm",
        "Iron (p.p.m.)": "Iron_ppm",
        "Manganese (p.p.m.)": "Manganese_ppm",
    },
    "readings_to_exclude": set(
        [
            "Sample ID",
            "Lab Number",
            "Sample Depth in inches",
            "Water Used",
        ]
    ),
}
