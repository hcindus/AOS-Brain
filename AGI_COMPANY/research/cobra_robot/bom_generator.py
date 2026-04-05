#!/usr/bin/env python3
"""
COBRA Robot BOM Generator
Complete Bill of Materials with pricing and suppliers
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum


class PartCategory(Enum):
    STRUCTURAL = "Structural"
    ELECTRONICS = "Electronics"
    ACTUATORS = "Actuators"
    SENSORS = "Sensors"
    POWER = "Power"
    FASTENERS = "Fasteners"
    CABLES = "Cables"
    TOOLS = "Tools"


@dataclass
class Part:
    """Single BOM line item"""
    part_number: str
    name: str
    category: str
    quantity: int
    unit_cost: float
    supplier: str
    supplier_sku: str
    url: str
    specs: str
    alternatives: List[str]
    
    @property
    def total_cost(self) -> float:
        return self.quantity * self.unit_cost


class COBRABOM:
    """Complete COBRA Bill of Materials"""
    
    def __init__(self, model: str = "COBRA-Standard"):
        self.model = model
        self.parts: List[Part] = []
        self.labor_hours = 8.0
        self.labor_rate = 35.0
        
    def generate_standard_bom(self):
        """Generate complete standard BOM"""
        
        # STRUCTURAL COMPONENTS
        self.parts.extend([
            Part("STR-001", "Cervical Vertebra (V1-V7)", PartCategory.STRUCTURAL.value, 
                 7, 3.50, "JLC3D", "PLA-F-GW", "https://jlc3d.com", 
                 "PLA, 20% infill, 0.2mm layer", ["PETG alternative"]),
            Part("STR-002", "Thoracic Vertebra (V8-V19)", PartCategory.STRUCTURAL.value,
                 12, 3.50, "JLC3D", "PLA-F-GW", "https://jlc3d.com",
                 "PLA, 20% infill, 0.2mm layer", ["PETG alternative"]),
            Part("STR-003", "Lumbar Vertebra (V20-V24)", PartCategory.STRUCTURAL.value,
                 5, 3.50, "JLC3D", "PLA-F-GW", "https://jlc3d.com",
                 "PLA, 20% infill, 0.2mm layer", []),
            Part("STR-004", "Sacrum Base (V25)", PartCategory.STRUCTURAL.value,
                 1, 5.00, "JLC3D", "PLA-F-GW", "https://jlc3d.com",
                 "PLA, 40% infill for rigidity", []),
            Part("STR-005", "Intervertebral Discs", PartCategory.STRUCTURAL.value,
                 25, 1.20, "McMaster", "9379K11", "https://mcmaster.com",
                 "Silicone rubber, 40A durometer", ["TPE 3D print"]),
            Part("STR-006", "Rib Segments (Thoracic)", PartCategory.STRUCTURAL.value,
                 24, 1.00, "JLC3D", "PLA-F-GW", "https://jlc3d.com",
                 "PLA, 15% infill, hollow", []),
            Part("STR-007", "Skull Housing", PartCategory.STRUCTURAL.value,
                 1, 8.00, "JLC3D", "PLA-F-GW", "https://jlc3d.com",
                 "PLA, 25% infill, glossy finish", []),
            Part("STR-008", "Phone Mount Bracket", PartCategory.STRUCTURAL.value,
                 1, 3.00, "JLC3D", "PLA-F-GW", "https://jlc3d.com",
                 "Universal phone clamp, adjustable", []),
        ])
        
        # ACTUATORS (Servos)
        self.parts.extend([
            Part("ACT-001", "MG90S Micro Servo (Pitch)", PartCategory.ACTUATORS.value,
                 25, 2.85, "Amazon", "B07MFK266B", "https://amazon.com",
                 "180°, 2.2kg/cm, metal gears", ["TowerPro SG90 ($1.50)"]),
            Part("ACT-002", "MG90S Micro Servo (Roll)", PartCategory.ACTUATORS.value,
                 25, 2.85, "Amazon", "B07MFK266B", "https://amazon.com",
                 "180°, 2.2kg/cm, metal gears", []),
            Part("ACT-003", "DS3218 Digital Servo (Base)", PartCategory.ACTUATORS.value,
                 2, 12.99, "Amazon", "B076MQ22PM", "https://amazon.com",
                 "20kg/cm, 270°, high torque", ["DS3235 for heavier loads"]),
        ])
        
        # ELECTRONICS
        self.parts.extend([
            Part("ELE-001", "Raspberry Pi 5 (8GB)", PartCategory.ELECTRONICS.value,
                 1, 80.00, "PiShop", "PI5-8GB", "https://pishop.us",
                 "8GB RAM, AI-ready", ["Pi 4 8GB ($75)"]),
            Part("ELE-002", "Raspberry Pi AI HAT+", PartCategory.ELECTRONICS.value,
                 1, 70.00, "PiShop", "AI-HAT-PLUS", "https://pishop.us",
                 "13 TOPS NPU", ["Coral USB ($60)"]),
            Part("ELE-003", "PCA9685 Servo Driver", PartCategory.ELECTRONICS.value,
                 2, 12.99, "Adafruit", "815", "https://adafruit.com",
                 "16-channel, 12-bit PWM, I2C", ["SparkFun version"]),
            Part("ELE-004", "MCP2515 CAN Controller", PartCategory.ELECTRONICS.value,
                 1, 8.99, "Amazon", "B01D1D0D5K", "https://amazon.com",
                 "SPI interface, servo bus compatible", []),
            Part("ELE-005", "Arduino Nano", PartCategory.ELECTRONICS.value,
                 1, 4.50, "Arduino", "A000005", "https://store.arduino.cc",
                 "Low-level real-time control", ["Arduino Pro Mini $3"]),
            Part("ELE-006", "Active Cooling Fan", PartCategory.ELECTRONICS.value,
                 1, 5.99, "Amazon", "B07WGCFZ4C", "https://amazon.com",
                 "40x40x10mm, 5V, quiet", []),
            Part("ELE-007", "Heat Sinks (Set)", PartCategory.ELECTRONICS.value,
                 1, 3.99, "Amazon", "B08CDMF2RS", "https://amazon.com",
                 "Aluminum, self-adhesive", []),
        ])
        
        # SENSORS
        self.parts.extend([
            Part("SEN-001", "MPU6050 IMU", PartCategory.SENSORS.value,
                 2, 4.50, "Amazon", "B07R7YXL1F", "https://amazon.com",
                 "6-axis, I2C, accelerometer + gyro", ["MPU9250 with magnetometer"]),
            Part("SEN-002", "VL53L0X ToF Distance", PartCategory.SENSORS.value,
                 1, 7.99, "Adafruit", "3317", "https://adafruit.com",
                 "2m range, obstacle detection", []),
            Part("SEN-003", "TCS34725 Color Sensor", PartCategory.SENSORS.value,
                 1, 7.95, "Adafruit", "1334", "https://adafruit.com",
                 "RGB color detection", []),
            Part("SEN-004", "IR Proximity Sensors", PartCategory.SENSORS.value,
                 4, 1.50, "Adafruit", "1568", "https://adafruit.com",
                 "Short range, 10cm", []),
            Part("SEN-005", "Current Sensors (INA219)", PartCategory.SENSORS.value,
                 2, 3.50, "Adafruit", "904", "https://adafruit.com",
                 "Power monitoring per bus", []),
        ])
        
        # POWER
        self.parts.extend([
            Part("PWR-001", "18650 Battery (3500mAh)", PartCategory.POWER.value,
                 6, 8.99, "BatterySpace", "18650-3500", "https://batteryspace.com",
                 "LG MJ1, protected cells", ["Samsung 35E"]),
            Part("PWR-002", "BMS 3S 12V 20A", PartCategory.POWER.value,
                 1, 12.99, "Amazon", "B08X2WBQN2", "https://amazon.com",
                 "Balance, overcharge, short protection", []),
            Part("PWR-003", "Step-Down Converter", PartCategory.POWER.value,
                 1, 6.99, "Amazon", "B07R4D7R8P", "https://amazon.com",
                 "LM2596, 12V to 5V", ["Buck converter module"]),
            Part("PWR-004", "Power Switch", PartCategory.POWER.value,
                 1, 2.99, "Amazon", "B07K2K4W1Y", "https://amazon.com",
                 "Rocker, 10A rated", []),
            Part("PWR-005", "XT60 Connector Pair", PartCategory.POWER.value,
                 2, 1.50, "Amazon", "B07WPHK4R9", "https://amazon.com",
                 "Gold plated, 60A rated", []),
            Part("PWR-006", "18650 Battery Holder", PartCategory.POWER.value,
                 1, 4.99, "Amazon", "B07K8QWJ6J", "https://amazon.com",
                 "3S1P configuration, PCB mount", []),
            Part("PWR-007", "Charger 12.6V 2A", PartCategory.POWER.value,
                 1, 8.99, "Amazon", "B07MFK266B", "https://amazon.com",
                 "Li-ion 3S charger, CC/CV", []),
        ])
        
        # FASTENERS
        self.parts.extend([
            Part("FAS-001", "M2x8 Machine Screws", PartCategory.FASTENERS.value,
                 100, 0.05, "McMaster", "91292A005", "https://mcmaster.com",
                 "Stainless steel, Phillips", []),
            Part("FAS-002", "M2x10 Machine Screws", PartCategory.FASTENERS.value,
                 100, 0.05, "McMaster", "91292A006", "https://mcmaster.com",
                 "Stainless steel, Phillips", []),
            Part("FAS-003", "M2 Nuts", PartCategory.FASTENERS.value,
                 200, 0.03, "McMaster", "90480A002", "https://mcmaster.com",
                 "Stainless steel, hex", []),
            Part("FAS-004", "M2 Washers", PartCategory.FASTENERS.value,
                 200, 0.02, "McMaster", "98689A101", "https://mcmaster.com",
                 "Stainless steel, flat", []),
            Part("FAS-005", "Servo Horns", PartCategory.FASTENERS.value,
                 50, 0.25, "Amazon", "Servo-Horn-Set", "https://amazon.com",
                 "Various sizes, metal + plastic", []),
            Part("FAS-006", "Servo Screws", PartCategory.FASTENERS.value,
                 50, 0.10, "Amazon", "Servo-Screw-Set", "https://amazon.com",
                 "M2x6, M2x8, included with servos", []),
        ])
        
        # CABLES
        self.parts.extend([
            Part("CBL-001", "Servo Extension Cables", PartCategory.CABLES.value,
                 25, 0.75, "Amazon", "Servo-Ext-30cm", "https://amazon.com",
                 "30cm, JR style, male-female", ["Make custom: wire + connectors"]),
            Part("CBL-002", "Dupont Wire Kit", PartCategory.CABLES.value,
                 1, 9.99, "Amazon", "B07WV4WN6Q", "https://amazon.com",
                 "120pcs, M-M, M-F, F-F, 10cm-30cm", []),
            Part("CBL-003", "I2C Cable (Qwiic/Stemma)", PartCategory.CABLES.value,
                 5, 1.95, "SparkFun", "15081", "https://sparkfun.com",
                 "4-pin JST, 50cm", []),
            Part("CBL-004", "USB-C Cable", PartCategory.CABLES.value,
                 2, 5.99, "Amazon", "USB-C-3ft", "https://amazon.com",
                 "Power + data, braided", []),
            Part("CBL-005", "Power Wire 18AWG", PartCategory.CABLES.value,
                 5, 0.50, "Amazon", "Silicone-18AWG", "https://amazon.com",
                 "Silicone insulated, flexible, per meter", []),
            Part("CBL-006", "Heat Shrink Tubing", PartCategory.CABLES.value,
                 1, 6.99, "Amazon", "Heat-Shrink-Set", "https://amazon.com",
                 "Assorted sizes, black", []),
        ])
        
        # OPTIONAL TOOLS
        self.parts.extend([
            Part("TLS-001", "Precision Screwdriver Set", PartCategory.TOOLS.value,
                 1, 12.99, "Amazon", "Screwdriver-Set", "https://amazon.com",
                 "Phillips, flat, hex, Torx", ["iFixit kit ($25)"]),
            Part("TLS-002", "Wire Strippers", PartCategory.TOOLS.value,
                 1, 8.99, "Amazon", "Wire-Stripper", "https://amazon.com",
                 "Automatic, 10-24 AWG", []),
            Part("TLS-003", "Multimeter", PartCategory.TOOLS.value,
                 1, 15.99, "Amazon", "Multimeter-Basic", "https://amazon.com",
                 "Voltage, current, continuity", ["Fluke ($100+)"]),
            Part("TLS-004", "Soldering Iron", PartCategory.TOOLS.value,
                 1, 19.99, "Amazon", "Solder-Iron-Kit", "https://amazon.com",
                 "60W, temperature controlled", []),
        ])
        
    def calculate_totals(self) -> Dict:
        """Calculate BOM totals"""
        category_totals = {}
        for part in self.parts:
            cat = part.category
            if cat not in category_totals:
                category_totals[cat] = 0
            category_totals[cat] += part.total_cost
            
        material_cost = sum(p.total_cost for p in self.parts)
        labor_cost = self.labor_hours * self.labor_rate
        total = material_cost + labor_cost
        
        # Calculate at different volumes
        volume_breaks = [1, 10, 100, 1000]
        volume_pricing = {}
        
        for vol in volume_breaks:
            if vol == 1:
                volume_pricing[vol] = total
            elif vol <= 10:
                volume_pricing[vol] = total * vol * 0.95  # 5% discount
            elif vol <= 100:
                volume_pricing[vol] = total * vol * 0.85  # 15% discount
            else:
                volume_pricing[vol] = total * vol * 0.75  # 25% discount
                
        return {
            "model": self.model,
            "material_cost": round(material_cost, 2),
            "labor_hours": self.labor_hours,
            "labor_rate": self.labor_rate,
            "labor_cost": round(labor_cost, 2),
            "total_unit_cost": round(total, 2),
            "category_breakdown": {k: round(v, 2) for k, v in category_totals.items()},
            "part_count": len(self.parts),
            "total_components": sum(p.quantity for p in self.parts),
            "volume_pricing": {f"{k}_units": round(v, 2) for k, v in volume_pricing.items()}
        }
        
    def export_csv(self, filename: str = "COBRA_BOM.csv"):
        """Export BOM to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Part Number', 'Name', 'Category', 'Qty', 
                           'Unit Cost', 'Total Cost', 'Supplier', 'SKU', 
                           'URL', 'Specs', 'Alternatives'])
            
            for part in self.parts:
                writer.writerow([
                    part.part_number, part.name, part.category, part.quantity,
                    part.unit_cost, part.total_cost, part.supplier, part.supplier_sku,
                    part.url, part.specs, '; '.join(part.alternatives)
                ])
                
        print(f"✅ BOM exported to {filename}")
        
    def export_json(self, filename: str = "COBRA_BOM.json"):
        """Export BOM to JSON"""
        data = {
            "model": self.model,
            "parts": [asdict(p) for p in self.parts],
            "totals": self.calculate_totals(),
            "export_date": "2026-03-29"
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"✅ BOM exported to {filename}")
        
    def print_summary(self):
        """Print formatted BOM summary"""
        totals = self.calculate_totals()
        
        print("\n" + "=" * 80)
        print(f"🐍 COBRA Robot BOM - {self.model}")
        print("=" * 80)
        
        print(f"\n📊 OVERVIEW")
        print(f"   Total Parts: {totals['part_count']}")
        print(f"   Total Components: {totals['total_components']}")
        
        print(f"\n💰 COST BREAKDOWN")
        print(f"   Materials: ${totals['material_cost']:.2f}")
        print(f"   Labor ({totals['labor_hours']}h @ ${totals['labor_rate']}/h): ${totals['labor_cost']:.2f}")
        print(f"   {'─' * 40}")
        print(f"   TOTAL UNIT COST: ${totals['total_unit_cost']:.2f}")
        
        print(f"\n📁 CATEGORY BREAKDOWN")
        for cat, cost in totals['category_breakdown'].items():
            pct = (cost / totals['material_cost']) * 100
            print(f"   {cat:15s}: ${cost:8.2f} ({pct:5.1f}%)")
            
        print(f"\n📦 VOLUME PRICING")
        for vol, price in totals['volume_pricing'].items():
            units = int(vol.split('_')[0])
            unit_cost = price / units
            print(f"   {units:4d} units: ${price:10,.2f} (${unit_cost:7.2f}/unit)")
            
        print("\n" + "=" * 80)
        
    def print_detailed(self):
        """Print full detailed BOM"""
        self.print_summary()
        
        print("\n📋 DETAILED PARTS LIST")
        print("─" * 80)
        
        current_category = ""
        for part in self.parts:
            if part.category != current_category:
                current_category = part.category
                print(f"\n[{current_category}]")
                
            alt_str = f" | Alt: {', '.join(part.alternatives)}" if part.alternatives else ""
            print(f"  {part.part_number:8s} | {part.name:30s} | Qty: {part.quantity:3d} | "
                  f"${part.unit_cost:6.2f} → ${part.total_cost:7.2f} | {part.supplier}{alt_str}")


def main():
    """Generate COBRA BOM"""
    print("🐍 Generating COBRA Robot BOM...")
    
    bom = COBRABOM(model="COBRA-Standard")
    bom.generate_standard_bom()
    
    # Print summary
    bom.print_detailed()
    
    # Export files
    bom.export_csv()
    bom.export_json()
    
    # Print supplier shopping lists
    print("\n" + "=" * 80)
    print("🛒 SUPPLIER SHOPPING LISTS")
    print("=" * 80)
    
    suppliers = {}
    for part in bom.parts:
        if part.supplier not in suppliers:
            suppliers[part.supplier] = []
        suppliers[part.supplier].append(part)
        
    for supplier, parts in suppliers.items():
        total = sum(p.total_cost for p in parts)
        print(f"\n{supplier}: ${total:.2f}")
        for p in parts:
            print(f"  {p.quantity}x {p.supplier_sku}: {p.name}")


if __name__ == "__main__":
    main()
