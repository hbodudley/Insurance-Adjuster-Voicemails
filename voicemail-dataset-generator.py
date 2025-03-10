import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import faker

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create Faker for generating realistic names
fake = faker.Faker()

# Define date ranges
start_date = datetime(2024, 7, 1)
end_date = datetime(2025, 3, 1)  # March 1st to exclude March data
current_date = start_date

# Define states with their weights (higher weight = more calls)
states = {
    "Florida": 0.25,
    "Georgia": 0.20,
    "North Carolina": 0.18,
    "South Carolina": 0.15,
    "Tennessee": 0.08,
    "Mississippi": 0.05,
    "Alabama": 0.05,
    "Louisiana": 0.04
}

# Define caller types and their probabilities
caller_types = {
    "Member": 0.45,
    "Claimant": 0.30,
    "Repair Shop": 0.15,
    "Other Insurance": 0.07,
    "Agero": 0.03
}

# Define message categories
message_categories = [
    "Payment Inquiry",
    "Claim Status",
    "Repair Status",
    "Rental Extension",
    "Supplement Request",
    "Towing Issue",
    "Documentation Request",
    "General Question",
    "Complaint",
    "Settlement Inquiry",
    "Coverage Question",
    "Contact Information Update"
]

# Define possible actions
actions = [
    "Called back and resolved issue",
    "Left voicemail with information",
    "Contacted repair shop",
    "Extended rental authorization",
    "Scheduled supplement inspection",
    "Updated claim notes",
    "Transferred to supervisor",
    "Sent requested documents",
    "Approved payment",
    "Requested additional information",
    "Scheduled call with member",
    "No action needed - informational only"
]

# Generate some consistent callers who will call multiple times
repeat_callers = []
for _ in range(20):
    caller_type = random.choices(list(caller_types.keys()), list(caller_types.values()))[0]
    
    if caller_type in ["Member", "Claimant"]:
        name = f"{fake.first_name()} {fake.last_name()}"
        claim_number = f"CL-{random.randint(10000000, 99999999)}"
        company = None
    else:
        name = fake.first_name()
        claim_number = f"CL-{random.randint(10000000, 99999999)}"
        if caller_type == "Repair Shop":
            company = random.choice(["Precision Auto Body", "Capital Collision", "Maaco", "ServiceKing", "Gerber Collision", "Caliber Collision", "ABRA Auto Body", "Fix Auto"])
        elif caller_type == "Other Insurance":
            company = random.choice(["State Farm", "GEICO", "Progressive", "Allstate", "Liberty Mutual", "Farmers", "Nationwide", "USAA"])
        elif caller_type == "Agero":
            company = "Agero"
        else:
            company = None
    
    repeat_callers.append({
        "name": name,
        "company": company,
        "claim_number": claim_number,
        "caller_type": caller_type,
        "state": random.choices(list(states.keys()), list(states.values()))[0],
        "phone": f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    })

# Generate repair shop supplement callers (October-December)
supplement_callers = []
for _ in range(10):
    name = fake.first_name()
    company = random.choice(["Precision Auto Body", "Capital Collision", "Maaco", "ServiceKing", "Gerber Collision", "Caliber Collision", "ABRA Auto Body", "Fix Auto"])
    claim_number = f"CL-{random.randint(10000000, 99999999)}"
    state = random.choices(list(states.keys()), list(states.values()))[0]
    phone = f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    supplement_callers.append({
        "name": name,
        "company": company,
        "claim_number": claim_number,
        "caller_type": "Repair Shop",
        "state": state,
        "phone": phone
    })

# Define holidays
holidays = {
    datetime(2024, 7, 4): "Independence Day",
    datetime(2024, 9, 2): "Labor Day",
    datetime(2024, 10, 14): "Columbus Day",
    datetime(2024, 11, 11): "Veterans Day",
    datetime(2024, 11, 28): "Thanksgiving",
    datetime(2024, 12, 25): "Christmas",
    datetime(2025, 1, 1): "New Year's Day",
    datetime(2025, 1, 20): "MLK Day",
    datetime(2025, 2, 17): "Presidents' Day"
}

# Post-holiday periods (1 week after major holidays)
post_holiday_periods = [
    (datetime(2024, 7, 5), datetime(2024, 7, 12)),  # After Independence Day
    (datetime(2024, 9, 3), datetime(2024, 9, 10)),  # After Labor Day
    (datetime(2024, 11, 29), datetime(2024, 12, 6)), # After Thanksgiving
    (datetime(2024, 12, 26), datetime(2025, 1, 2))   # After Christmas
]

# Generate voicemail data
voicemails = []

while current_date < end_date:
    # Determine weekly volume based on month
    if current_date.month == 7:
        weekly_volume = 15
    elif current_date.month in [8, 9]:
        weekly_volume = 20
    else:  # October through February
        weekly_volume = 30
    
    # Increase volume for post-holiday periods
    for start, end in post_holiday_periods:
        if start <= current_date <= end:
            weekly_volume = int(weekly_volume * 1.5)
    
    # Calculate daily calls for the next 7 days
    daily_volumes = []
    for i in range(7):
        day = (current_date + timedelta(days=i)).weekday()
        if day < 5:  # Weekday (90% of calls)
            daily_volumes.append(int(weekly_volume * 0.9 / 5))
        else:  # Weekend (10% of calls)
            daily_volumes.append(int(weekly_volume * 0.1 / 2))
    
    # Add some randomness to daily volumes
    daily_volumes = [max(1, int(v * random.uniform(0.8, 1.2))) for v in daily_volumes]
    
    # Generate calls for each day
    for i in range(7):
        day_date = current_date + timedelta(days=i)
        
        # Skip if we've gone past the end date
        if day_date >= end_date:
            break
        
        for _ in range(daily_volumes[i]):
            # Determine if this is a repeat caller
            is_repeat_caller = random.random() < 0.15  # 15% chance of repeat caller
            is_supplement_caller = (random.random() < 0.2 and  # 20% chance during supplement period
                               datetime(2024, 10, 1) <= day_date <= datetime(2024, 12, 5))
            
            # Select caller
            if is_repeat_caller:
                caller = random.choice(repeat_callers)
                caller_type = caller["caller_type"]
                name = caller["name"]
                company = caller["company"]
                claim_number = caller["claim_number"]
                state = caller["state"]
                phone = caller["phone"]
            elif is_supplement_caller:
                caller = random.choice(supplement_callers)
                caller_type = caller["caller_type"]
                name = caller["name"]
                company = caller["company"]
                claim_number = caller["claim_number"]
                state = caller["state"]
                phone = caller["phone"]
            else:
                caller_type = random.choices(list(caller_types.keys()), list(caller_types.values()))[0]
                
                if caller_type in ["Member", "Claimant"]:
                    name = f"{fake.first_name()} {fake.last_name()}"
                    company = None
                else:
                    name = fake.first_name()
                    if caller_type == "Repair Shop":
                        company = random.choice(["Precision Auto Body", "Capital Collision", "Maaco", "ServiceKing", "Gerber Collision", "Caliber Collision", "ABRA Auto Body", "Fix Auto"])
                    elif caller_type == "Other Insurance":
                        company = random.choice(["State Farm", "GEICO", "Progressive", "Allstate", "Liberty Mutual", "Farmers", "Nationwide", "USAA"])
                    elif caller_type == "Agero":
                        company = "Agero"
                    else:
                        company = None
                
                claim_number = f"CL-{random.randint(10000000, 99999999)}"
                state = random.choices(list(states.keys()), list(states.values()))[0]
                phone = f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
            # Determine call time based on caller type
            if caller_type in ["Repair Shop", "Other Insurance", "Agero"] and day_date.weekday() < 5:
                # Business hours for business callers on weekdays
                hour = random.randint(9, 16)  # 9AM to 5PM
                minute = random.randint(0, 59)
            else:
                # Wider range for members and claimants, or weekend calls
                hour = random.randint(6, 21)  # 6AM to 10PM
                minute = random.randint(0, 59)
            
            call_time = day_date.replace(hour=hour, minute=minute)
            
            # Select appropriate message category
            if is_supplement_caller:
                category = "Supplement Request"
            elif day_date in holidays or any(start <= day_date <= end for start, end in post_holiday_periods):
                # More rental extensions and repair status questions around holidays
                category = random.choice([
                    "Rental Extension", "Rental Extension", "Repair Status", "Repair Status",
                    "Payment Inquiry", "Claim Status", "General Question"
                ])
            elif caller_type == "Agero":
                category = "Towing Issue"
            elif caller_type == "Repair Shop":
                category = random.choice([
                    "Repair Status", "Supplement Request", "Payment Inquiry"
                ])
            elif caller_type == "Other Insurance":
                category = random.choice([
                    "Claim Status", "Documentation Request", "Settlement Inquiry"
                ])
            else:
                category = random.choice(message_categories)
            
            # Generate message summary
            if caller_type in ["Member", "Claimant"]:
                caller_intro = f"This is {name} calling about claim {claim_number}."
            else:
                caller_intro = f"This is {name} from {company} calling about claim {claim_number}."
            
            if category == "Payment Inquiry":
                message = f"{caller_intro} I'm checking on the status of the payment for my claim. It's been [time period] and I haven't received it yet."
            elif category == "Claim Status":
                message = f"{caller_intro} I'm calling to check on the status of my claim. Please call me back at {phone}."
            elif category == "Repair Status":
                message = f"{caller_intro} I'm wondering how much longer until my car will be repaired. Please call me back."
            elif category == "Rental Extension":
                message = f"{caller_intro} My car repairs are taking longer than expected and I need to extend my rental. Please call me back at {phone}."
            elif category == "Supplement Request":
                message = f"{caller_intro} We found additional damage during repairs and need approval for a supplement of $[amount]. Please call us back at {phone}."
            elif category == "Towing Issue":
                message = f"{caller_intro} There's an issue with the towing service for claim {claim_number}. The customer is waiting and needs immediate assistance."
            elif category == "Documentation Request":
                message = f"{caller_intro} I need a copy of [document] for my records. Could you please send it to me?"
            elif category == "General Question":
                message = f"{caller_intro} I have a question about my claim. Please call me back at {phone}."
            elif category == "Complaint":
                message = f"{caller_intro} I'm not happy with how my claim is being handled. This is taking too long and I need to speak with someone immediately."
            elif category == "Settlement Inquiry":
                message = f"{caller_intro} I'm calling about the settlement offer for claim {claim_number}. Please call me back to discuss."
            elif category == "Coverage Question":
                message = f"{caller_intro} I'm calling to verify what's covered under my policy for this claim. Please call me back."
            elif category == "Contact Information Update":
                message = f"{caller_intro} I need to update my contact information for this claim. My new phone number is {phone}."
            
            # Determine action taken
            if category == "Rental Extension":
                action = random.choice([
                    "Extended rental authorization for 3 days",
                    "Extended rental authorization for 5 days",
                    "Contacted repair shop to verify repair timeline then extended rental",
                    "Left voicemail explaining rental coverage limits"
                ])
            elif category == "Supplement Request":
                action = random.choice([
                    "Approved supplement payment",
                    "Scheduled reinspection",
                    "Requested additional documentation",
                    "Approved partial supplement amount"
                ])
            elif category == "Towing Issue":
                action = random.choice([
                    "Contacted Agero to resolve towing issue",
                    "Authorized alternate towing service",
                    "Updated pickup location in system"
                ])
            elif category == "Complaint":
                action = random.choice([
                    "Escalated to supervisor",
                    "Called back and addressed concerns",
                    "Reviewed claim for possible expediting"
                ])
            else:
                action = random.choice(actions)
            
            # Add some randomness to messages
            message = message.replace("[time period]", random.choice(["a week", "two weeks", "10 days", "over a month"]))
            message = message.replace("[amount]", f"${random.randint(500, 5000)}")
            message = message.replace("[document]", random.choice(["the estimate", "the policy declaration", "the repair authorization"]))
            
            # Create voicemail entry
            voicemail = {
                "Date/Time": call_time,
                "Number": phone,
                "Message": message,
                "Category": category,
                "Action Taken": action
            }
            
            voicemails.append(voicemail)
    
    # Move to next week
    current_date += timedelta(days=7)

# Create DataFrame and sort by date
df = pd.DataFrame(voicemails)
df = df.sort_values(by="Date/Time")

# Format the date/time column
df["Date/Time"] = df["Date/Time"].dt.strftime("%m/%d/%Y %I:%M %p")

# Export to Excel
df.to_excel("insurance_adjuster_voicemails.xlsx", index=False)

# Display sample of the data
print(f"Generated {len(df)} voicemail entries from {start_date.strftime('%m/%d/%Y')} to {end_date.strftime('%m/%d/%Y')}")
df.head()
