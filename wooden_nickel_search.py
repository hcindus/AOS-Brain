#!/usr/bin/env python3
"""
Search for Wooden Nickel, Silver Dollar, Silver Peso bars
"""

import csv
import json
import os
from datetime import datetime

TARGET_NAMES = [
    'wooden nickel',
    'wooden nickle',
    'silver dollar',
    'silver peso',
]

# Major cities to search (representing all 50 states)
MAJOR_CITIES = [
    # CA
    'Los Angeles', 'San Francisco', 'San Diego', 'Sacramento',
    # TX
    'Houston', 'Dallas', 'Austin', 'San Antonio',
    # NY
    'New York City', 'Buffalo', 'Rochester',
    # FL
    'Miami', 'Tampa', 'Orlando', 'Jacksonville',
    # IL
    'Chicago', 'Springfield',
    # PA
    'Philadelphia', 'Pittsburgh',
    # OH
    'Columbus', 'Cleveland', 'Cincinnati',
    # GA
    'Atlanta', 'Savannah',
    # NC
    'Charlotte', 'Raleigh',
    # MI
    'Detroit', 'Grand Rapids',
    # AZ
    'Phoenix', 'Tucson',
    # WA
    'Seattle', 'Spokane',
    # MA
    'Boston', 'Cambridge',
    # NJ
    'Newark', 'Jersey City',
    # VA
    'Richmond', 'Virginia Beach',
    # CO
    'Denver', 'Colorado Springs',
    # TN
    'Nashville', 'Memphis',
    # MO
    'Kansas City', 'St Louis',
    # IN
    'Indianapolis',
    # WI
    'Milwaukee', 'Madison',
    # NV
    'Las Vegas', 'Reno',
    # OR
    'Portland',
    # MN
    'Minneapolis', 'St Paul',
    # AL
    'Birmingham',
    # LA
    'New Orleans', 'Baton Rouge',
    # KY
    'Louisville',
    # SC
    'Charleston',
    # OK
    'Oklahoma City', 'Tulsa',
    # CT
    'Hartford',
    # UT
    'Salt Lake City',
    # IA
    'Des Moines',
    # AR
    'Little Rock',
    # MS
    'Jackson',
    # KS
    'Wichita',
    # NE
    'Omaha',
    # NM
    'Albuquerque',
    # WV
    'Charleston',
    # ID
    'Boise',
    # HI
    'Honolulu',
    # ME
    'Portland',
    # NH
    'Manchester',
    # RI
    'Providence',
    # MT
    'Billings',
    # DE
    'Wilmington',
    # SD
    'Sioux Falls',
    # ND
    'Fargo',
    # AK
    'Anchorage',
    # VT
    'Burlington',
    # WY
    'Cheyenne',
]

# Mexico cities
MEXICO_CITIES = [
    'Mexico City', 'Guadalajara', 'Monterrey', 'Tijuana',
    'Cancun', 'Puerto Vallarta', 'Cabo San Lucas', 'Acapulco',
    'Puebla', 'Leon', 'Merida', 'San Miguel de Allende',
    'Queretaro', 'Oaxaca', 'Puerto Escondido', 'Playa del Carmen',
]

print(f"Search targets: {TARGET_NAMES}")
print(f"US Cities: {len(MAJOR_CITIES)}")
print(f"Mexico Cities: {len(MEXICO_CITIES)}")
print()
print("This will search each target name in each city...")
print("Ready to begin web scraping phase.")
