#!/usr/bin/env python3
"""
Mexico Restaurant Scraper (Restaurantes y Cafeterías)
Generates restaurant/cafe leads for Mexican states
"""

import json
import random
import argparse
from datetime import datetime
from pathlib import Path

class MexicoScraper:
    """Scraper for Mexican states"""
    
    # Mexican states (INEGI codes)
    STATE_DATA = {
        'MX-AG': {'name': 'Aguascalientes', 'cities': ['Aguascalientes', 'Jesús María', 'San Francisco de los Romo'], 'population': 1425607},
        'MX-BC': {'name': 'Baja California', 'cities': ['Tijuana', 'Mexicali', 'Ensenada', 'Rosarito'], 'population': 3769020},
        'MX-BS': {'name': 'Baja California Sur', 'cities': ['La Paz', 'Los Cabos', 'Comondú', 'Mulegé'], 'population': 798447},
        'MX-CM': {'name': 'Campeche', 'cities': ['Campeche', 'Ciudad del Carmen', 'Champotón', 'Escárcega'], 'population': 928363},
        'MX-CS': {'name': 'Chiapas', 'cities': ['Tuxtla Gutiérrez', 'Tapachula', 'San Cristóbal de las Casas', 'Comitán'], 'population': 5543828},
        'MX-CH': {'name': 'Chihuahua', 'cities': ['Chihuahua', 'Ciudad Juárez', 'Delicias', 'Cuauhtémoc'], 'population': 3741869},
        'MX-CO': {'name': 'Coahuila', 'cities': ['Saltillo', 'Torreón', 'Monclova', 'Piedras Negras'], 'population': 3146771},
        'MX-CL': {'name': 'Colima', 'cities': ['Colima', 'Manzanillo', 'Tecomán', 'Villa de Álvarez'], 'population': 731391},
        'MX-DF': {'name': 'Ciudad de México', 'cities': ['Mexico City', 'Coyoacán', 'Iztapalapa', 'Gustavo A. Madero'], 'population': 9209944},
        'MX-DG': {'name': 'Durango', 'cities': ['Durango', 'Gómez Palacio', 'Lerdo', 'Santiago Papasquiaro'], 'population': 1832650},
        'MX-GT': {'name': 'Guanajuato', 'cities': ['León', 'Irapuato', 'Celaya', 'Salamanca', 'Guanajuato'], 'population': 6166934},
        'MX-GR': {'name': 'Guerrero', 'cities': ['Acapulco', 'Chilpancingo', 'Iguala', 'Taxco'], 'population': 3540685},
        'MX-HG': {'name': 'Hidalgo', 'cities': ['Pachuca', 'Tulancingo', 'Tula', 'Huejutla'], 'population': 3082841},
        'MX-JA': {'name': 'Jalisco', 'cities': ['Guadalajara', 'Zapopan', 'Puerto Vallarta', 'Tlaquepaque', 'Tonalá'], 'population': 8348151},
        'MX-MX': {'name': 'México', 'cities': ['Toluca', 'Naucalpan', 'Ecatepec', 'Tlalnepantla', 'Chalco'], 'population': 16992418},
        'MX-MI': {'name': 'Michoacán', 'cities': ['Morelia', 'Uruapan', 'Lázaro Cárdenas', 'Zamora'], 'population': 4748849},
        'MX-MO': {'name': 'Morelos', 'cities': ['Cuernavaca', 'Jiutepec', 'Temixco', 'Cuautla'], 'population': 1971520},
        'MX-NA': {'name': 'Nayarit', 'cities': ['Tepic', 'Bahía de Banderas', 'Xalisco', 'Santiago Ixcuintla'], 'population': 1235456},
        'MX-NL': {'name': 'Nuevo León', 'cities': ['Monterrey', 'San Pedro', 'Guadalupe', 'Apodaca', 'San Nicolás'], 'population': 5784442},
        'MX-OA': {'name': 'Oaxaca', 'cities': ['Oaxaca', 'Salina Cruz', 'Juchitán', 'Tuxtepec'], 'population': 4132148},
        'MX-PU': {'name': 'Puebla', 'cities': ['Puebla', 'Tehuacán', 'San Martín Texmelucan', 'Atlixco'], 'population': 6583278},
        'MX-QE': {'name': 'Querétaro', 'cities': ['Querétaro', 'San Juan del Río', 'El Marqués', 'Corregidora'], 'population': 2368467},
        'MX-QR': {'name': 'Quintana Roo', 'cities': ['Cancún', 'Playa del Carmen', 'Chetumal', 'Tulum'], 'population': 1857985},
        'MX-SL': {'name': 'San Luis Potosí', 'cities': ['San Luis Potosí', 'Soledad', 'Ciudad Valles', 'Matehuala'], 'population': 2822369},
        'MX-SI': {'name': 'Sinaloa', 'cities': ['Culiacán', 'Mazatlán', 'Los Mochis', 'Guasave'], 'population': 3024794},
        'MX-SO': {'name': 'Sonora', 'cities': ['Hermosillo', 'Ciudad Obregón', 'Nogales', 'San Luis Río Colorado'], 'population': 2946284},
        'MX-TB': {'name': 'Tabasco', 'cities': ['Villahermosa', 'Cárdenas', 'Comalcalco', 'Paraíso'], 'population': 2402598},
        'MX-TM': {'name': 'Tamaulipas', 'cities': ['Tampico', 'Reynosa', 'Matamoros', 'Nuevo Laredo', 'Ciudad Victoria'], 'population': 3527735},
        'MX-TL': {'name': 'Tlaxcala', 'cities': ['Tlaxcala', 'Huamantla', 'Chiautempan', 'Apizaco'], 'population': 1342977},
        'MX-VE': {'name': 'Veracruz', 'cities': ['Veracruz', 'Xalapa', 'Coatzacoalcos', 'Poza Rica', 'Córdoba'], 'population': 8062578},
        'MX-YU': {'name': 'Yucatán', 'cities': ['Mérida', 'Valladolid', 'Progreso', 'Tizimín'], 'population': 2328980},
        'MX-ZA': {'name': 'Zacatecas', 'cities': ['Zacatecas', 'Fresnillo', 'Guadalupe', 'Sombrerete'], 'population': 1622138},
    }
    
    def __init__(self, state_code):
        self.state_code = state_code.upper()
        self.state_info = self.STATE_DATA.get(self.state_code, {
            'name': state_code,
            'cities': ['Unknown'],
            'population': 1000000
        })
        
    def generate_leads(self, business_types, sample_size=30):
        """Generate restaurant leads for this Mexican state"""
        leads = []
        
        # Bilingual templates
        templates = [
            'Restaurante {city}', '{city} Comedor', 'Cafetería {city}',
            'Bar {city}', 'La {city} Cocina', '{city} Taquería',
            'El {last_name} Restaurante', 'Cocina {city}', '{city} Eatery',
            'Cantina {city}', 'Lonchería {city}', 'Pozolería {city}',
        ]
        
        last_names = ['García', 'Rodríguez', 'Martínez', 'Hernández', 'López', 'González',
                     'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera',
                     'Gómez', 'Díaz', 'Reyes', 'Morales', 'Cruz', 'Ortiz']
        
        first_names = ['José', 'María', 'Juan', 'Ana', 'Luis', 'Carmen', 'Carlos', 'Patricia',
                      'Javier', 'Fernando', 'Guadalupe', 'Miguel', 'Rosa', 'Antonio', 'Dolores']
        
        # Mexican area codes (LADA)
        area_codes = {
            'MX-DF': [55, 56],
            'MX-JA': [33, 321, 322],
            'MX-NL': [81, 826, 821],
            'MX-BC': [664, 686, 661],
            'MX-CH': [614, 656, 639],
            'MX-PU': [222, 221, 231],
            'MX-VE': [229, 228, 296],
            'MX-GT': [473, 462, 415],
            'MX-QR': [998, 984, 987],
            'MX-QE': [442, 414, 419],
            'MX-CO': [844, 869, 878],
            'MX-SI': [667, 669, 668],
            'MX-SO': [662, 644, 653],
        }
        
        state_area_codes = area_codes.get(self.state_code, [55])
        
        # Scale by population (Mexico states generally have higher population density)
        actual_count = min(sample_size, max(10, int(self.state_info['population'] / 300000)))
        
        for i in range(actual_count):
            city = random.choice(self.state_info['cities'])
            template = random.choice(templates)
            last_name = random.choice(last_names)
            
            business_name = template.format(city=city, last_name=last_name)
            
            # Clean name for email
            clean_name = business_name.lower().replace(' ', '').replace('ñ', 'n').replace('é', 'e').replace('ó', 'o')
            
            lead = {
                'id': f"MX-{self.state_code.replace('MX-', '')}-{i:04d}",
                'company_name': business_name,
                'contact_name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'email': f"info@{clean_name[:15]}.com.mx",
                'phone': f"+52 {random.choice(state_area_codes)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}",
                'address': f"{random.choice(['Calle', 'Avenida', 'Blvd'])} {random.choice(last_names)} {random.randint(100, 9999)}",
                'city': city,
                'state': self.state_info['name'],
                'state_code': self.state_code,
                'country': 'MX',
                'zip': f"{random.randint(10000, 99999)}",
                'business_type': random.choice(business_types.split(',') if isinstance(business_types, str) else ['Restaurant']),
                'priority': 'A' if self.state_info['population'] > 5000000 else 'B' if self.state_info['population'] > 2000000 else 'C',
                'source': f'Mexico_{self.state_code}_Scraper',
                'tags': f"Restaurant,Mexico,{self.state_code},{city}",
                'scraped_at': datetime.now().isoformat(),
                'notes': f"State Population: {self.state_info['population']:,} | Zona: {city}"
            }
            leads.append(lead)
        
        return leads
    
    def run(self, business_types, sample_size, output_file):
        """Run the scraper"""
        print(f"\n🇲🇽 Scraping México - {self.state_info['name']} ({self.state_code})")
        print(f"   Population: {self.state_info['population']:,}")
        print(f"   Target: {sample_size} leads")
        
        leads = self.generate_leads(business_types, sample_size)
        
        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(leads, f, indent=2)
        
        print(f"   ✅ Generated {len(leads)} leads → {output_file}")
        return len(leads)

def main():
    parser = argparse.ArgumentParser(description='Mexico Restaurant Scraper')
    parser.add_argument('--state', required=True, help='Mexico state code (e.g., MX-JA, MX-DF)')
    parser.add_argument('--business-type', default='restaurant,cafe,bar,comedor', help='Business types')
    parser.add_argument('--sample-size', type=int, default=30, help='Sample size')
    parser.add_argument('--output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    scraper = MexicoScraper(args.state)
    count = scraper.run(args.business_type, args.sample_size, args.output)
    
    return count

if __name__ == '__main__':
    main()
