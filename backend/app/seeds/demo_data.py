"""Generate fictional MPLADS demonstration dataset."""
from datetime import datetime, timedelta
import random
from typing import List

# MPLADS Project Categories
CATEGORIES = [
    "Roads",
    "Education",
    "Healthcare",
    "Water Supply",
    "Sanitation",
    "Community Assets",
    "Renewable Energy",
    "Public Infrastructure",
]

# Indian States and Districts (sample)
STATES_DISTRICTS = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Pasighat", "Ziro"],
    "Assam": ["Guwahati", "Dibrugarh", "Jorhat", "Silchar"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Durg", "Korba"],
    "Goa": ["North Goa", "South Goa", "Panaji", "Mormugao"],
    "Haryana": ["Gurugram", "Faridabad", "Hisar", "Panipat"],
    "Himachal Pradesh": ["Shimla", "Kangra", "Mandi", "Kullu"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Hazaribagh"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Aurangabad"],
    "Karnataka": ["Bengaluru", "Hyderabad", "Mysore", "Belgaum"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra"],
    "Delhi": ["Central Delhi", "East Delhi", "North Delhi", "South Delhi"],
    "Manipur": ["Imphal East", "Imphal West", "Thoubal", "Churachandpur"],
    "Meghalaya": ["East Khasi Hills", "West Garo Hills", "Jaintia Hills", "Ri-Bhoi"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Kolasib"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Mon"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Puri"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Bikaner"],
    "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"],
    "Tripura": ["Agartala", "Dhalai", "Gomati", "North Tripura"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Nainital", "Almora"],
    "West Bengal": ["Kolkata", "Darjeeling", "Hooghly", "Murshidabad"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Andaman and Nicobar Islands": ["South Andaman", "North and Middle Andaman", "Nicobar", "Port Blair"],
    "Chandigarh": ["Chandigarh", "Sector 17", "Manimajra", "Dhanas"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Dadra", "Silvassa", "Daman", "Diu"],
    "Jammu and Kashmir": ["Jammu", "Srinagar", "Anantnag", "Baramulla"],
    "Ladakh": ["Leh", "Kargil", "Nubra", "Zanskar"],
    "Lakshadweep": ["Kavaratti", "Agatti", "Amini", "Andrott"],
    "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"],
}

# Project descriptions by category
PROJECT_DESCRIPTIONS = {
    "Roads": [
        "Construction of rural road connecting villages",
        "Road widening and repair project",
        "Asphalt road construction for connectivity",
        "Road surface treatment for main roads",
        "Bridge construction and rehabilitation",
    ],
    "Education": [
        "Construction of new school building",
        "School renovation and infrastructure upgrade",
        "Computer lab setup in government school",
        "Library and reading room establishment",
        "Multi-purpose school complex construction",
    ],
    "Healthcare": [
        "Health center construction and equipment",
        "Hospital renovation and upgrade",
        "Medical diagnostic center establishment",
        "Maternal health clinic setup",
        "Emergency care facility development",
    ],
    "Water Supply": [
        "Water pipeline network expansion",
        "Drinking water supply project",
        "Water treatment plant establishment",
        "Water storage tank construction",
        "Groundwater recharge pit construction",
    ],
    "Sanitation": [
        "Public toilet block construction",
        "Waste management facility setup",
        "Drainage system improvement",
        "Sewage treatment plant construction",
        "Solid waste management center",
    ],
    "Community Assets": [
        "Community center construction",
        "Multi-purpose community hall",
        "Sports complex development",
        "Recreation park development",
        "Community playground construction",
    ],
    "Renewable Energy": [
        "Solar panel installation project",
        "Street light installation with solar panels",
        "Biogas plant installation",
        "Wind turbine installation",
        "Solar water heating system setup",
    ],
    "Public Infrastructure": [
        "Bus stand construction",
        "Market complex development",
        "Parking facility construction",
        "Public restroom facility",
        "Railway platform renovation",
    ],
}

# MP Names (sample)
MP_NAMES = [
    "Rajesh Kumar", "Priya Singh", "Vikram Patel", "Deepa Sharma",
    "Ashok Reddy", "Neha Verma", "Mahendra Nath", "Divya Gupta",
    "Ravi Shankar", "Anita Desai", "Suresh Rao", "Kavya Malik",
]

# Implementing Agencies
IMPLEMENTING_AGENCIES = [
    "Public Works Department",
    "Municipal Corporation",
    "District Administration",
    "Gram Panchayat",
    "Health Department",
    "Education Department",
    "Water Supply Board",
    "Sanitation Authority",
    "Energy Department",
    "Rural Development Agency",
]


def generate_demo_projects(num_projects: int = 150) -> List[dict]:
    """Generate fictional MPLADS demonstration projects."""
    projects = []
    project_id_counter = 1000
    
    for _ in range(num_projects):
        # Random selections
        state = random.choice(list(STATES_DISTRICTS.keys()))
        district = random.choice(STATES_DISTRICTS[state])
        category = random.choice(CATEGORIES)
        description = random.choice(PROJECT_DESCRIPTIONS[category])
        mp_name = random.choice(MP_NAMES)
        agency = random.choice(IMPLEMENTING_AGENCIES)
        
        # Project financials
        base_cost = random.uniform(5_000_000, 50_000_000)  # 50L to 5Cr
        estimated_cost = base_cost
        sanctioned_amount = base_cost * random.uniform(0.8, 1.2)
        amount_released = sanctioned_amount * random.uniform(0.3, 1.0)
        
        # Add some anomalies intentionally
        if random.random() < 0.15:  # 15% cost overruns
            actual_expenditure = estimated_cost * random.uniform(1.2, 1.6)
        else:
            actual_expenditure = estimated_cost * random.uniform(0.3, 1.0)
        
        if random.random() < 0.10:  # 10% low progress high spending
            progress_percentage = random.uniform(20, 40)
            actual_expenditure = estimated_cost * random.uniform(0.7, 0.9)
        else:
            progress_percentage = random.uniform(0, 100)
        
        # Project timeline
        sanction_date = datetime.utcnow() - timedelta(days=random.randint(90, 900))
        expected_completion_date = sanction_date + timedelta(days=random.randint(180, 900))
        
        # Project status
        if progress_percentage >= 95:
            status = "Completed"
            completion_date = expected_completion_date + timedelta(days=random.randint(-30, 30))
        elif expected_completion_date < datetime.utcnow():
            status = "Delayed"
            completion_date = None
        elif progress_percentage > 30:
            status = "In Progress"
            completion_date = None
        else:
            status = "Not Started"
            completion_date = None
        
        project = {
            "project_id": f"MPLADS-{project_id_counter:06d}",
            "project_name": f"{category} Project - {district} - Phase {random.randint(1, 3)}",
            "description": description,
            "state": state,
            "district": district,
            "constituency": f"{district} Constituency",
            "category": category,
            "implementing_agency": agency,
            "mp_name": mp_name,
            "estimated_cost": float(estimated_cost),
            "sanctioned_amount": float(sanctioned_amount),
            "amount_released": float(amount_released),
            "actual_expenditure": float(actual_expenditure),
            "progress_percentage": float(progress_percentage),
            "sanction_date": sanction_date,
            "expected_completion_date": expected_completion_date,
            "completion_date": completion_date,
            "status": status,
        }
        
        projects.append(project)
        project_id_counter += 1
    
    return projects


if __name__ == "__main__":
    # Generate and print sample data for testing
    projects = generate_demo_projects(5)
    for proj in projects:
        print(f"Project: {proj['project_name']}")
        print(f"  State: {proj['state']}, District: {proj['district']}")
        print(f"  Estimated Cost: {proj['estimated_cost']:,.2f}")
        print(f"  Actual Expenditure: {proj['actual_expenditure']:,.2f}")
        print(f"  Progress: {proj['progress_percentage']:.1f}%")
        print()
