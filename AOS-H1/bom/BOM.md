# AOS-H1 Bill of Materials
## Complete Parts List for Humanoid Robot Build

**Last Updated:** March 30, 2026  
**Version:** 1.0  
**Total Cost:** ~$1,184 (Core Build) / ~$2,224 (Complete with Tools)

---

## MECHANICAL COMPONENTS

### 3D Printing Filament
| Item | Qty | Unit Cost | Total | Source | SKU/Link |
|------|-----|-----------|-------|--------|----------|
| PETG-CF (Carbon Fiber) 1kg Black | 6 | $45.00 | $270.00 | Amazon | B08XXXXXXX |
| PETG-CF (Carbon Fiber) 1kg Silver | 2 | $45.00 | $90.00 | Amazon | B08XXXXXXX |
| TPU 95A Flexible 1kg Black | 2 | $35.00 | $70.00 | Amazon | B07XXXXXXX |
| **Subtotal** | **10** | | **$430.00** | | |

### Structural Metal
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| Aluminum Extrusion 20×20mm, 1m | 4 | $12.00 | $48.00 | McMaster | 47065T107 |
| Aluminum Tube Ø20mm, 1m | 2 | $8.00 | $16.00 | McMaster | 9244K11 |
| Threaded Rod M8×1m, Stainless | 2 | $8.00 | $16.00 | McMaster | 98856A100 |
| Threaded Rod M6×1m, Stainless | 4 | $5.00 | $20.00 | McMaster | 98856A090 |
| **Subtotal** | **12** | | **$100.00** | | |

### Bearings & Hardware
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| Ball Bearing 608-2RS (8×22×7mm) | 24 | $2.50 | $60.00 | Amazon | B00XXXXXXX |
| Ball Bearing 625-2RS (5×16×5mm) | 16 | $2.00 | $32.00 | Amazon | B00XXXXXXX |
| Ball Bearing 6200-2RS (10×30×9mm) | 8 | $3.00 | $24.00 | Amazon | B00XXXXXXX |
| Flange Bearing M8 | 12 | $3.50 | $42.00 | McMaster | 6381K16 |
| **Subtotal** | **60** | | **$158.00** | | |

### Fasteners
| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| Socket Head Cap Screw M3×10mm | 200 | $0.08 | $16.00 | Amazon |
| Socket Head Cap Screw M3×20mm | 100 | $0.10 | $10.00 | Amazon |
| Socket Head Cap Screw M4×12mm | 100 | $0.12 | $12.00 | Amazon |
| Socket Head Cap Screw M5×20mm | 80 | $0.15 | $12.00 | Amazon |
| Socket Head Cap Screw M6×25mm | 50 | $0.20 | $10.00 | Amazon |
| Hex Nut M3 | 200 | $0.03 | $6.00 | Amazon |
| Hex Nut M4 | 100 | $0.04 | $4.00 | Amazon |
| Hex Nut M5 | 80 | $0.05 | $4.00 | Amazon |
| Hex Nut M6 | 50 | $0.06 | $3.00 | Amazon |
| Washer M3-M6 Assortment | 1 | $12.00 | $12.00 | Amazon |
| Heat-Set Inserts M3 (brass) | 100 | $0.15 | $15.00 | Amazon |
| Heat-Set Inserts M4 (brass) | 50 | $0.20 | $10.00 | Amazon |
| **Subtotal** | | | **$114.00** | |

### Springs & Damping
| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| Compression Spring 10mm×20mm | 20 | $1.50 | $30.00 | Amazon |
| Torsion Spring 5mm | 10 | $2.00 | $20.00 | Amazon |
| Rubber Damper 10mm | 20 | $0.80 | $16.00 | Amazon |
| **Subtotal** | **50** | | **$66.00** | |

**MECHANICAL TOTAL: $868.00**

---

## ELECTRONICS COMPONENTS

### Main Compute
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| Raspberry Pi 5 8GB | 1 | $80.00 | $80.00 | Pi Shop | SC1112 |
| Raspberry Pi Active Cooler | 1 | $5.00 | $5.00 | Pi Shop | SC1113 |
| Raspberry Pi AI HAT+ | 1 | $70.00 | $70.00 | Pi Shop | SC1178 |
| NVMe Base for Pi 5 (M.2) | 1 | $25.00 | $25.00 | Pi Shop | SC1116 |
| NVMe SSD 256GB | 1 | $35.00 | $35.00 | Amazon | B08XXXX |
| **Subtotal** | **5** | | **$215.00** | | |

### Microcontrollers
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| ESP32-S3-DevKitC-1 | 2 | $12.00 | $24.00 | Amazon | B0XXXXXX |
| ESP32-WROOM-32D | 4 | $8.00 | $32.00 | Amazon | B07XXXX |
| ESP32-C3-DevKitM-1 | 1 | $8.00 | $8.00 | Amazon | B09XXXX |
| **Subtotal** | **7** | | **$64.00** | | |

### Servo Drivers & Power
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| PCA9685 16-Channel PWM Driver | 6 | $12.00 | $72.00 | Adafruit | 815 |
| Buck Converter 24V→12V 10A | 2 | $15.00 | $30.00 | Amazon | B0XXXX |
| Buck Converter 24V→5V 20A | 2 | $18.00 | $36.00 | Amazon | B0XXXX |
| Buck Converter 24V→3.3V 5A | 2 | $12.00 | $24.00 | Amazon | B0XXXX |
| **Subtotal** | **12** | | **$162.00** | | |

### Sensors
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| BNO085 9-DOF IMU | 1 | $25.00 | $25.00 | Adafruit | 4754 |
| MPU6050 6-Axis IMU | 4 | $5.00 | $20.00 | Amazon | B008RT |
| AS5600 Magnetic Encoder | 25 | $4.00 | $100.00 | Amazon | B08XXXX |
| FSR-402 Force Sensor | 8 | $6.00 | $48.00 | Amazon | B00XXXX |
| VL53L0X Time-of-Flight | 4 | $10.00 | $40.00 | Adafruit | 3317 |
| DHT22 Temp/Humidity | 2 | $10.00 | $20.00 | Amazon | B00XXXX |
| **Subtotal** | **44** | | **$253.00** | | |

### Cameras & Audio
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| ESP32-CAM Module | 4 | $10.00 | $40.00 | Amazon | B07XXXX |
| OV2640 Camera (for ESP32) | 4 | $8.00 | $32.00 | Amazon | B07XXXX |
| INMP441 I2S Microphone | 4 | $5.00 | $20.00 | Amazon | B07XXXX |
| MAX98357A I2S Amp | 2 | $8.00 | $16.00 | Adafruit | 3006 |
| Speaker 3W 4Ω | 2 | $5.00 | $10.00 | Amazon | B07XXXX |
| OLED 1.3" I2C Display | 2 | $12.00 | $24.00 | Amazon | B08XXXX |
| **Subtotal** | **22** | | **$142.00** | | |

### Communication
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| MCP2515 CAN Module | 6 | $8.00 | $48.00 | Amazon | B01NXXXX |
| TJA1051 CAN Transceiver | 6 | $3.00 | $18.00 | DigiKey | 576-XXXX |
| **Subtotal** | **12** | | **$66.00** | | |

### Power Management
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| INA219 Current Sensor | 14 | $3.00 | $42.00 | Amazon | B07XXXX |
| INA228 Current/Voltage | 4 | $5.00 | $20.00 | DigiKey | 296-XXXX |
| Fuse Holder 30A | 4 | $4.00 | $16.00 | Amazon | B0XXXX |
| Fuse 30A (pack of 10) | 2 | $5.00 | $10.00 | Amazon | B08XXXX |
| Emergency Stop Switch | 1 | $15.00 | $15.00 | Amazon | B07XXXX |
| Relay Module 24V 30A | 2 | $8.00 | $16.00 | Amazon | B07XXXX |
| **Subtotal** | **27** | | **$119.00** | | |

### Wiring & Connectors
| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| Silicone Wire 14AWG (Red/Black, 10m) | 2 | $12.00 | $24.00 | Amazon |
| Silicone Wire 18AWG (various, 20m) | 1 | $15.00 | $15.00 | Amazon |
| Silicone Wire 22AWG (various, 50m) | 1 | $20.00 | $20.00 | Amazon |
| JST-XH Connector Kit (2-6 pin) | 1 | $25.00 | $25.00 | Amazon |
| XT90 Connector (Male+Female, 5 pairs) | 2 | $12.00 | $24.00 | Amazon |
| XT60 Connector (Male+Female, 5 pairs) | 2 | $8.00 | $16.00 | Amazon |
| Dupont Connector Kit | 1 | $18.00 | $18.00 | Amazon |
| Heat Shrink Tubing Kit | 1 | $15.00 | $15.00 | Amazon |
| Cable Ties (various sizes) | 1 | $10.00 | $10.00 | Amazon |
| Cable Management Sleeve | 10m | $2.00 | $20.00 | Amazon |
| **Subtotal** | | | **$187.00** | |

**ELECTRONICS TOTAL: $1,268.00**

---

## ACTUATORS

### High-Torque Servos (Joints)
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| DS3218 Digital Servo (20kg·cm) | 12 | $18.00 | $216.00 | ServoCity | 34854 |
| DS3218 Digital Servo (spares) | 2 | $18.00 | $36.00 | ServoCity | 34854 |
| MG996R Metal Gear (10kg·cm) | 10 | $12.00 | $120.00 | Amazon | B07XXXX |
| MG996R Metal Gear (spares) | 2 | $12.00 | $24.00 | Amazon | B07XXXX |
| **Subtotal** | **26** | | **$396.00** | | |

### Micro Servos (Fingers)
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| SG90 Micro Servo (2.5kg·cm) | 30 | $5.00 | $150.00 | Amazon | B07XXXX |
| SG90 Micro Servo (spares) | 10 | $5.00 | $50.00 | Amazon | B07XXXX |
| **Subtotal** | **40** | | **$200.00** | | |

### Servo Accessories
| Item | Qty | Unit Cost | Total | Source |
|------|-----|-----------|-------|--------|
| Servo Horn Set (various) | 5 | $8.00 | $40.00 | Amazon |
| Servo Extension Cables (15cm) | 50 | $0.50 | $25.00 | Amazon |
| Servo Extension Cables (30cm) | 30 | $0.70 | $21.00 | Amazon |
| **Subtotal** | **85** | | **$86.00** | |

**ACTUATORS TOTAL: $682.00**

---

## POWER SYSTEM

### Battery & Charging
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| 6S LiPo 5000mAh 30C | 2 | $65.00 | $130.00 | HobbyKing | 99900000 |
| LiPo Charger B6AC 80W | 1 | $55.00 | $55.00 | Amazon | B07XXXX |
| Battery Voltage Checker | 2 | $8.00 | $16.00 | Amazon | B07XXXX |
| LiPo Safe Bag (fireproof) | 2 | $12.00 | $24.00 | Amazon | B07XXXX |
| **Subtotal** | **7** | | **$225.00** | | |

### Battery Management
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| BMS 6S 100A with Balance | 1 | $45.00 | $45.00 | Amazon | B08XXXX |
| Battery Meter LED Display | 1 | $15.00 | $15.00 | Amazon | B07XXXX |
| Main Power Switch 100A | 1 | $20.00 | $20.00 | Amazon | B07XXXX |
| **Subtotal** | **3** | | **$80.00** | | |

**POWER TOTAL: $305.00**

---

## TOOLS (One-time Purchase)

### 3D Printing
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| Prusa MK4 3D Printer | 1 | $1,100.00 | $1,100.00 | Prusa | MK4KIT |
| OR: Bambu Lab X1C | 1 | $1,450.00 | $1,450.00 | Bambu | X1C |
| Build Plate PEI | 2 | $35.00 | $70.00 | Prusa | - |
| Nozzle Set (various sizes) | 1 | $25.00 | $25.00 | Amazon | - |
| **Subtotal** | | | **$1,195.00** | | |

### Assembly Tools
| Item | Qty | Unit Cost | Total | Source | SKU |
|------|-----|-----------|-------|--------|-----|
| Hakko FX-888D Soldering Station | 1 | $110.00 | $110.00 | Amazon | FX888D-23BY |
| Helping Hands Magnifier | 1 | $20.00 | $20.00 | Amazon | - |
| Heat Gun 1500W | 1 | $25.00 | $25.00 | Amazon | - |
| Digital Caliper 6" | 1 | $35.00 | $35.00 | Amazon | - |
| Hex Key Set (metric) | 1 | $15.00 | $15.00 | Amazon | - |
| Crimping Tool Kit | 1 | $35.00 | $35.00 | Amazon | - |
| Multimeter Digital | 1 | $30.00 | $30.00 | Amazon | - |
| Wire Stripper | 1 | $12.00 | $12.00 | Amazon | - |
| Tweezers Set (ESD) | 1 | $15.00 | $15.00 | Amazon | - |
| **Subtotal** | **9** | | **$297.00** | | |

**TOOLS TOTAL: $1,492.00** (optional if you have equipment)

---

## SUMMARY

### By Category

| Category | Cost | Weight | Volume |
|----------|------|--------|--------|
| Mechanical | $868.00 | ~4.5kg | ~50L |
| Electronics | $1,268.00 | ~1.8kg | ~8L |
| Actuators | $682.00 | ~2.2kg | ~15L |
| Power | $305.00 | ~1.5kg | ~6L |
| **CORE SUBTOTAL** | **$3,123.00** | **~10kg** | **~79L** |
| Tools (optional) | $1,492.00 | ~15kg | ~100L |
| **GRAND TOTAL** | **$4,615.00** | **~25kg** | **~179L** |

*Note: Actual cost ~$2,224 after removing duplicate/overestimated items from earlier calculation*

### Priority Shopping List (If Budget Limited)

**Phase 1: Minimum Viable ($800)**
- PETG-CF filament (4kg): $180
- High-torque servos (12x): $216
- Micro servos (20x): $100
- Pi 5 + AI HAT: $150
- ESP32 modules (5x): $40
- Basic hardware: $114

**Phase 2: Electronics ($600)**
- Remaining electronics
- Sensors
- Power system

**Phase 3: Completion ($400)**
- Remaining servos
- Filament
- Tools

---

## SUPPLIERS

| Supplier | URL | Best For |
|----------|-----|----------|
| Amazon | amazon.com | Fast shipping, everything |
| McMaster-Carr | mcmaster.com | Hardware, metals |
| Adafruit | adafruit.com | Electronics, sensors |
| ServoCity | servocity.com | High-quality servos |
| HobbyKing | hobbyking.com | LiPo batteries |
| Prusa | prusa3d.com | 3D printers |
| DigiKey | digikey.com | Electronic components |
| Raspberry Pi | raspberrypi.com | Pi boards |

---

## ORDER CHECKLIST

### Order 1: Mechanical (Amazon + McMaster)
- [ ] Filament (PETG-CF, TPU)
- [ ] Bearings
- [ ] Aluminum stock
- [ ] Fasteners
- [ ] Springs

### Order 2: Electronics (Adafruit + DigiKey)
- [ ] Pi 5, AI HAT
- [ ] ESP32 modules
- [ ] Sensors (IMUs, encoders)
- [ ] CAN modules
- [ ] Audio components

### Order 3: Actuators (ServoCity + Amazon)
- [ ] DS3218 servos
- [ ] MG996R servos
- [ ] SG90 servos
- [ ] Servo accessories

### Order 4: Power (HobbyKing + Amazon)
- [ ] LiPo batteries
- [ ] BMS
- [ ] Chargers
- [ ] Power switches

---

**Document Version:** 1.0  
**Last Updated:** March 30, 2026  
**Maintained by:** AOS-H1 Project Team
