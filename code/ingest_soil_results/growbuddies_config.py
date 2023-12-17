from enum import Enum, auto


class OutputType(Enum):
    INFLUXDB = auto()
    MARKDOWN = auto()
    BOTH = auto()


soil_results_config = {
    "udp_ports": {"SP": 8196, "M3": 8195},
    "output_type": OutputType,
    "name_mapping": {
        "Total Exchange Capacity (M. E.)": "TEC",
        "pH of Soil Sample": "pH",
        "Organic Matter, Percent": "Organic_%",
        "SULFUR (ppm)": "Sulfur_(ppm)",
        "Mehlich III Phosphorous: as (P O )\n2 5\nlbs / acre": "Phosphorous_lbs",
        "Desired Value\nCALCIUM:\nValue Found\nlbs / acre\nDeficit": "Calcium_lbs",
        "Desired Value\nMAGNESIUM:\nValue Found\nlbs / acre\nDeficit": "Magnesium_lbs",
        "Desired Value\nPOTASSIUM:\nlbs / acre Value Found\nDeficit": "Potassium_lbs",
        "SODIUM: lbs / acre": "Sodium_lbs",
        "Calcium (60 to 70%)": "Calcium",
        "Magnesium (10 to 20%)": "Magnesium",
        "Potassium (2 to 5%)": "Pota,ssium",
        "Sodium (.5 to 3%)": "Sodium",
        "Soluble Salts ppm": "Soluble_Salts_(ppm)",
        "Chloride (Cl) ppm": "Chloride_(ppm)",
        "Bicarbonate (HCO3) ppm": "Bicarbonate_(ppm)",
        "Other Bases (Variable)": "Other_bases",
        "Exchangable Hydrogen (10 to 15%)": "Exchangable_Hydrogen",
        "Boron (p.p.m.)": "Boron_(ppm)",
        "Iron (p.p.m.)": "Iron_(ppm)",
        "Manganese (p.p.m.)": "Manganese_(ppm)",
        "Copper (p.p.m.)": "Copper_(ppm)",
        "Zinc (p.p.m.)": "Zinc_(ppm)",
        "Aluminum (p.p.m.)": "Aluminum_(ppm)",
        "Ammonium (p.p.m.)": "Ammonium_(ppm)",
        "Nitrate (p.p.m.)": "Nitrate_(ppm)",
        "Media Density g/cm3": "Media_Density",
        "PHOSPHORUS (ppm)": "Phosphorous_(ppm)",
        "CALCIUM (ppm)": "Calcium_(ppm)",
        "CALCIUM (meq/l)": "Calcium_(meq/L)",
        "MAGNESIUM (ppm)": "Magnesium_(ppm)",
        "MAGNESIUM (meq/l)": "Magnesium_(meq/L)",
        "POTASSIUM: (ppm)": "Potassium_(ppm)",
        "POTASSIUM: (meq/l)": "Potassium_(meq/L)",
        "SODIUM (ppm)": "Sodium_(ppm)",
        "SODIUM (meq/l)": "Sodium_(meq/L)",
        "Boron (p.p.m.)": "Boron_(ppm)",
        "Iron (p.p.m.)": "Iron_(ppm)",
        "Manganese (p.p.m.)": "Manganese_(ppm)",
    },
    "readings_to_exclude": set(
        [
            "Sample Location",
            "Sample ID",
            "Lab Number",
            "Sample Depth in inches",
            "Water Used",
        ]
    ),
}
