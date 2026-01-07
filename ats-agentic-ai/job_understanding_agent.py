ITI_JOBS = {
    "Fitter": [
        "fitting", "drilling", "grinding",
        "lathe", "assembly", "maintenance"
    ],
    "Welder": [
        "arc welding", "gas welding",
        "mig welding", "fabrication"
    ],
    "Electrician": [
        "wiring", "motor", "transformer",
        "switch board", "maintenance"
    ],
    "Plumber": [
        "pipe fitting", "leakage repair",
        "sanitary fitting", "water supply"
    ],
    "Machinist": [
        "lathe machine", "cnc",
        "milling", "turning", "drilling"
    ]
}

def get_job_skills(job_role):
    return ITI_JOBS.get(job_role, [])
