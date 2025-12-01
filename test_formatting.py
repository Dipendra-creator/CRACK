import json

# Sample API response from user
sample_response = {
    "List": {
        "HiTeckGroop.in": {
            "Data": [
                {
                    "Address": "W/O Rakesh Kumar,77rampurgabhana,gabhana,GabhanaAligarh,Uttar Pradesh,202136",      
                    "Address2": "W/O Rakesh Kumar,77,rampur, gabhana Gabhana,Aligarh,Uttar Pradesh,202136",
                    "Address3": "W/O Rakesh Kumar,rampur, gabhana Gabhana,Gabhana,Uttar Pradesh,202136 ",
                    "DocNumber": "672811474313",
                    "FatherName": "Omwati",
                    "FullName": "Rakesh Kumar",
                    "Phone": "918433220261",
                    "Phone2": "918171994779",
                    "Phone3": "917060249537",
                    "Region": "AIRTEL UPW;Airtel UP West;JIO UPW"
                },
                {
                    "Address": "77,RAMPUR Gabhana PO,GABHANA,GABHANA Gabhana Gabhana,Aligarh,Aligarh,Uttar Pradesh,202136",
                    "DocNumber": "802505846166",
                    "FatherName": "Jitendra Kumar",
                    "FullName": "Rakesh Kumar Sharma ",
                    "Phone": "918433220261",
                    "Phone2": "918171673607",
                    "Phone3": "918533001308",
                    "Region": "AIRTEL UPW;Airtel UP West"
                },
                {
                    "Address": "W/O Rakesh Kumar,77 rampur gabhana,gabhana,Gabhana Aligarh,Uttar Pradesh,202136 ",  
                    "DocNumber": "672811474313",
                    "Email": "dipu.sharma.1122@gmail.com",
                    "FatherName": "Omwati",
                    "FullName": "Rakesh Kumar",
                    "Phone": "918433220261",
                    "Region": "JIO UPE UPW"
                }
            ],
            "InfoLeak": "At the beginning of 2025, a huge leak with the data of Indian cellular operators began to spread on the network. The HITECKGROOP website is declared as a source, but this information is unverified. The data contains 1.8 billion records, however, the number of unique users below, about 300 million. Each record indicated the full name, the name of the father, and the number of the document. Most often this is the Aadhaar number, but the taxpayer's passports or numbers were also found. There were up to two phones in each line, however, since several records had several records for one user, the total number of well -known phones sometimes reached several tens. Some records also had nicknames and emails.",
            "NumOfResults": 3
        },
        "ICMR India": {
            "Data": [
                {
                    "Address": "GABHANA",
                    "Age": "18",
                    "District": "ALIGARH",
                    "FullName": "DEVENDRA",
                    "Gender": "Male",
                    "Phone": "918433220261",
                    "State": "UTTAR PRADESH"
                },
                {
                    "Address": "GABHANA",
                    "Age": "20",
                    "District": "ALIGARH",
                    "FullName": "DIPENDRA",
                    "Gender": "Male",
                    "Phone": "918433220261",
                    "State": "UTTAR PRADESH"
                }
            ],
            "InfoLeak": "In October 2023, a post appeared on the forum on the sale for 80K $ ICMR base - the largest medical restoration in India. The hacker claimed that in a leak of 815 million records. However, the base was never published until in 2025 India's leak of the same size reappeared. But the analysis revealed a fake - someone took a base of 100 million lines and inserted another 715 million randomly generated lines into the middle of this file. It is not known who the fake was performed - the first hacker or other people who tried to adjust the new leakage to the size of ICMR. The remaining 100 million records are real citizens' data. They contain phones, names, addresses and about 500 thousand Aadhaar numbers.",
            "NumOfResults": 2
        }
    },
    "NumOfDatabase": 2,
    "NumOfResults": 5,
    "free_requests_left": 50,
    "price": 0,
    "search time": 0.0155468
}


def format_value(value, indent=0):
    """
    Recursively format any value (dict, list, primitive) into readable text
    """
    indent_str = "  " * indent
    lines = []
    
    if isinstance(value, dict):
        for key, val in value.items():
            if isinstance(val, (dict, list)):
                lines.append(f"{indent_str}• {key}:")
                lines.extend(format_value(val, indent + 1))
            else:
                lines.append(f"{indent_str}• {key}: {val}")
    elif isinstance(value, list):
        for idx, item in enumerate(value, 1):
            if isinstance(item, dict):
                lines.append(f"{indent_str}[{idx}]")
                lines.extend(format_value(item, indent + 1))
            else:
                lines.append(f"{indent_str}• {item}")
    else:
        lines.append(f"{indent_str}{value}")
    
    return lines


def test_formatting():
    """Test the generic formatting with the sample response"""
    print("=" * 80)
    print("TESTING GENERIC DATA FORMATTING")
    print("=" * 80)
    
    # Extract metadata
    metadata_fields = ["NumOfDatabase", "NumOfResults", "free_requests_left", "price", "search time"]
    print("\n--- METADATA ---")
    for field in metadata_fields:
        if field in sample_response:
            print(f"{field}: {sample_response[field]}")
    
    # Process each database
    for database_name, database_data in sample_response["List"].items():
        print(f"\n{'=' * 80}")
        print(f"📊 {database_name}")
        print('=' * 80)
        
        if isinstance(database_data, dict):
            # Show InfoLeak
            if "InfoLeak" in database_data:
                print(f"\nℹ️ Info: {database_data['InfoLeak'][:100]}...")
            
            # Show NumOfResults
            if "NumOfResults" in database_data:
                print(f"\n📈 Results: {database_data['NumOfResults']}")
            
            # Process Data
            if "Data" in database_data and isinstance(database_data["Data"], list):
                for idx, record in enumerate(database_data["Data"], 1):
                    print(f"\n━━━ Record #{idx} ━━━")
                    
                    if isinstance(record, dict):
                        for field_name, field_value in record.items():
                            if isinstance(field_value, (dict, list)):
                                print(f"• {field_name}:")
                                for line in format_value(field_value, indent=1):
                                    print(line)
                            else:
                                print(f"• {field_name}: {field_value}")
                    else:
                        for line in format_value(record, indent=1):
                            print(line)
            
            # Process other fields
            for key, value in database_data.items():
                if key not in ["InfoLeak", "NumOfResults", "Data"]:
                    print(f"\n{key}:")
                    for line in format_value(value, indent=1):
                        print(line)
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE - All data displayed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    test_formatting()
