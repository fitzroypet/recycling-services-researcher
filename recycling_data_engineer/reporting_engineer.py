import os
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Tuple, Optional
from .database_definitions import *
from .existing_materials import EXISTING_MATERIALS

def clean_time_string(time_str: str) -> str:
    """Clean and normalize time string"""
    # Remove any duplicate AM/PM
    time_str = time_str.strip()
    time_str = time_str.replace('AM AM', 'AM').replace('PM AM', 'PM')
    time_str = time_str.replace('AM PM', 'AM').replace('PM PM', 'PM')
    
    # Ensure single space before AM/PM
    time_str = time_str.replace('AM', ' AM').replace('PM', ' PM')
    time_str = ' '.join(time_str.split())  # Normalize spaces
    
    return time_str

def convert_time_format(time_str: str) -> Optional[str]:
    """Convert 12-hour time format to 24-hour SQL format"""
    if not time_str:
        return None
    
    try:
        # Clean the time string
        time_str = clean_time_string(time_str)
        
        # Add AM/PM if missing
        if ' AM' not in time_str and ' PM' not in time_str:
            hour = int(time_str.split(':')[0])
            time_str = f"{time_str} {'AM' if hour < 12 else 'PM'}"
        
        # Parse and convert to 24-hour format
        parsed_time = datetime.strptime(time_str, '%I:%M %p')
        return parsed_time.strftime('%H:%M:00')
    except ValueError as e:
        print(f"Time conversion error for '{time_str}': {str(e)}")
        return None

def parse_opening_hours(hours_list: List[str]) -> List[Tuple]:
    """Convert opening hours from JSON format to structured data"""
    days_map = {
        'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
        'Friday': 5, 'Saturday': 6, 'Sunday': 0
    }
    parsed_hours = []
    
    for hour in hours_list:
        if not hour:
            continue
        try:
            # Split day and times
            day, times = hour.split(': ', 1)
            day_num = days_map[day]
            
            if times.lower() == 'closed':
                parsed_hours.append((day_num, None, None, True))
                continue
            
            # Handle 24-hour format
            if times.lower() == 'open 24 hours':
                parsed_hours.append((day_num, '00:00:00', '23:59:59', False))
                continue
            
            # Split and clean times
            if '–' in times:
                open_time, close_time = times.split('–')
            elif ' - ' in times:
                open_time, close_time = times.split(' - ')
            else:
                open_time, close_time = times.split('-')
            
            # Clean times
            open_time = clean_time_string(open_time)
            close_time = clean_time_string(close_time)
            
            # Handle AM/PM inheritance
            if ' AM' in close_time and ' AM' not in open_time and ' PM' not in open_time:
                open_time += ' AM'
            elif ' PM' in close_time and ' AM' not in open_time and ' PM' not in open_time:
                # Check if opening hour should be AM
                open_hour = int(open_time.split(':')[0])
                close_hour = int(close_time.split(':')[0])
                if open_hour < close_hour or close_hour == 12:
                    open_time += ' AM'
                else:
                    open_time += ' PM'
            
            # Convert to SQL format
            sql_open_time = convert_time_format(open_time)
            sql_close_time = convert_time_format(close_time)
            
            if sql_open_time and sql_close_time:
                parsed_hours.append((day_num, sql_open_time, sql_close_time, False))
            else:
                print(f"Warning: Could not parse times for {day}: {open_time} - {close_time}")
                print(f"Original format: {times}")
                print(f"Cleaned format: {open_time} - {close_time}")
                print(f"Converted: open={sql_open_time}, close={sql_close_time}")
                
        except (ValueError, KeyError) as e:
            print(f"Warning: Error parsing hours: {hour}. Error: {str(e)}")
            continue
    
    return parsed_hours

def match_materials(materials: List[str], website_materials: Dict, existing_materials: List[Dict]) -> List[Tuple]:
    """Enhanced material matching with fuzzy matching and category mapping"""
    matched_materials = []  # Initialize the list here
    material_categories = {
        'metal': [
            'iron', 'steel', 'aluminum', 'copper', 'scrap', 'metal', 'tin', 
            'brass', 'bronze', 'zinc', 'lead', 'ferrous', 'non-ferrous',
            'cans', 'wire', 'ingot'
        ],
        'plastic': [
            'plastic', 'pp', 'ps', 'pet', 'pvc', 'hdpe', 'ldpe', 'lldpe',
            'polypropylene', 'polystyrene', 'polyethylene', 'polyvinyl',
            'bottles', 'containers', 'packaging', 'pla', 'bioplastic'
        ],
        'textile': [
            'clothing', 'clothes', 'fabric', 'textile', 'garments', 'apparel',
            'fashion', 'wool', 'cotton', 'polyester', 'nylon', 'linen',
            'denim', 'silk', 'leather'
        ],
        'paper': [
            'paper', 'cardboard', 'carton', 'newspaper', 'magazine', 'mail',
            'book', 'phonebook', 'office paper', 'printing paper', 'corrugated',
            'packaging', 'box', 'document', 'catalog', 'envelope', 'receipt'
        ],
        'glass': [
            'glass', 'bottle', 'jar', 'window', 'mirror', 'container',
            'glassware', 'windscreen', 'windshield', 'pane', 'cullet'
        ]
    }
    
    # Create lookup dictionaries
    category_lookup = {mat['CategoryName']: [] for mat in existing_materials}
    for mat in existing_materials:
        category_lookup[mat['CategoryName']].append(mat['Description'].lower())
    
    def find_best_match(material: str, category: str) -> Optional[Tuple[str, str]]:
        if not material:
            return None
        material_lower = material.lower()
        
        # Direct match
        for mat in existing_materials:
            if mat['Description'].lower() == material_lower:
                return (mat['CategoryName'], mat['Description'])
        
        # Category match
        if category in category_lookup:
            if category == 'metal' and material_lower in ['iron', 'steel']:
                return ('metal', 'Mixed Metals')
            elif category == 'plastic':
                return ('plastic', 'Mixed Plastics')
            elif category == 'paper':
                return ('paper', 'Mixed Paper (general)')
        
        return None

    # Process materials from both sources
    for material in materials:
        category = next((cat for cat, keywords in material_categories.items() 
                        if any(keyword in material.lower() for keyword in keywords)), None)
        if category:
            match = find_best_match(material, category)
            if match:
                matched_materials.append(match)
    
    # Process website_materials
    for category, materials_list in website_materials.items():
        for material in materials_list:
            match = find_best_match(material, category)
            if match:
                matched_materials.append(match)
    
    return list(set(matched_materials))

def generate_sql_statements(json_data: List[Dict]) -> str:
    """Generate SQL insert statements with proper transaction handling"""
    sql_statements = [
        "SET NOCOUNT ON;",
        "SET XACT_ABORT ON;",
        "DECLARE @ErrorLog TABLE (BusinessName NVARCHAR(255), ErrorMessage NVARCHAR(MAX));",
        "BEGIN TRY",
        "    BEGIN TRANSACTION;"
    ]
    
    for i, business in enumerate(json_data):
        # Use unique variable name for each business
        business_id_var = f"@BusinessID_{i}"
        
        sql_statements.append(f"""
        BEGIN TRY
            DECLARE {business_id_var} INT;
            
            INSERT INTO recycling.Businesses (
                Name, FormattedAddress, Latitude, Longitude, PhoneNumber, 
                Website, Rating, PlaceID, ServiceKeywords
            ) VALUES (
                '{business['name'].replace("'", "''")}',
                '{business['address'].replace("'", "''")}',
                {business['coordinates']['lat']},
                {business['coordinates']['lng']},
                {f"'{business['phone']}'" if business.get('phone') else 'NULL'},
                {f"'{business['website']}'" if business.get('website') else 'NULL'},
                {business['rating'] if business.get('rating') else 'NULL'},
                '{business['place_id']}',
                '{','.join(business.get('service_keywords', [])).replace("'", "''")}'
            );
            
            SET {business_id_var} = SCOPE_IDENTITY();
            
            -- Address Components insert
            INSERT INTO recycling.AddressComponents (
                BusinessID, StreetAddress, City, State, PostalCode, Country
            ) VALUES (
                {business_id_var},
                {f"'{business.get('address_components', {}).get('route', '')}'" if business.get('address_components', {}).get('route') else 'NULL'},
                '{business.get('address_components', {}).get('postal_town', '')}',
                '{business.get('address_components', {}).get('administrative_area_level_1', '')}',
                '{business.get('address_components', {}).get('postal_code', '')}',
                '{business.get('address_components', {}).get('country', '')}'
            );
        """)
        
        # Business Hours insert
        hours = parse_opening_hours(business.get('opening_hours', []))
        for day_num, open_time, close_time, is_closed in hours:
            sql_statements.append(f"""
            INSERT INTO recycling.BusinessHours (
                BusinessID, DayOfWeek, OpenTime, CloseTime, IsClosed
            ) VALUES (
                {business_id_var}, {day_num},
                {f"'{open_time}'" if open_time else 'NULL'},
                {f"'{close_time}'" if close_time else 'NULL'},
                {1 if is_closed else 0}
            );
            """)
        
        # Business Materials insert
        materials = match_materials(
            business.get('materials', []),
            business.get('website_materials', {}),
            EXISTING_MATERIALS
        )
        
        for category, description in materials:
            sql_statements.append(f"""
            INSERT INTO recycling.BusinessMaterials (
                BusinessID, MaterialID, CategoryName, Description, IsVerified
            )
            SELECT {business_id_var}, MaterialID, '{category}', '{description}', 1
            FROM recycling.Materials
            WHERE Description = '{description}';
            """)
        
        # Business Services insert
        materials_list = business.get('materials', [])
        service_name = "Recycling Collection"
        service_desc = (f"Recycling services for {', '.join(materials_list)}" 
                       if materials_list else "General recycling services")
            
        sql_statements.append(f"""
            INSERT INTO recycling.BusinessServices (
                BusinessID, ServiceName, Description
            ) VALUES (
                {business_id_var},
                '{service_name}',
                '{service_desc.replace("'", "''")}'
            );
            
        END TRY
        BEGIN CATCH
            INSERT INTO @ErrorLog (BusinessName, ErrorMessage)
            VALUES ('{business['name'].replace("'", "''")}', ERROR_MESSAGE());
        END CATCH
        """)
    
    # Final transaction handling
    sql_statements.extend([
        "    COMMIT TRANSACTION;",
        "    SELECT * FROM @ErrorLog WHERE ErrorMessage IS NOT NULL;",
        "END TRY",
        "BEGIN CATCH",
        "    IF @@TRANCOUNT > 0",
        "        ROLLBACK TRANSACTION;",
        "    SELECT * FROM @ErrorLog WHERE ErrorMessage IS NOT NULL;",
        "    THROW;",
        "END CATCH"
    ])
    
    return "\n".join(sql_statements)

def main():
    try:
        # Load JSON data
        with open("middlesbrough_UK_20241119_055401.json", "r") as f:
            json_data = json.load(f)
        
        # Generate SQL statements
        sql_statements = generate_sql_statements(json_data)
        
        # Save to file with unique name like city country combination
        file_name = "middlesbrough_UK.sql"
        with open(file_name, "w") as f:
            f.write(sql_statements)
        
        print("SQL statements have been generated and saved to sql_statements.sql")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()