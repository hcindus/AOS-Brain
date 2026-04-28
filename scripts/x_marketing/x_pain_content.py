#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) Pain-Point Content Generator
Based on Opposition Research - Highlight pain, never ascribe blame

PAIN POINTS:
1. The Inventory Panic (Friday night, out of paper)
2. The Mystery Product Problem (wrong paper, doesn't fit)
3. The Ghost Invoice (surprise charges)
4. The Shipping Calculus (math games, minimums)
5. The Health Question (BPA/phenol concerns)
6. The Support Maze (phone trees, no answers)

PRINCIPLES:
- Never bash competition
- Highlight universal pain
- Offer solution
- Same message, 3 languages
- Under 280 characters
"""

PHONE = "888-881-6834"
WEBSITE = "psdepot.com"

# PAIN-POINT BASED MESSAGES - Powerful, relatable, solution-oriented
PAIN_POINT_MESSAGES = [
    {
        # PAIN: Friday night, out of paper, line out the door
        "en": f"It's Friday 8pm. You're out of paper. Line's out the door.\n\nWe're here until 10pm with same-day delivery.\n\n{PHONE} | {WEBSITE}",
        "es": f"Viernes 8pm. Sin papel. Fila por la puerta.\n\nEstamos hasta 10pm con entrega mismo día.\n\n{PHONE} | {WEBSITE}",
        "zh": f"周五晚8点。没纸了。排队到门外。\n\n我们营业到10点，当天送达。\n\n{PHONE} | {WEBSITE}",
    },
    {
        # PAIN: Ordered paper, doesn't fit printer
        "en": f"Ordered thermal paper. Doesn't fit your printer.\n\nWe identify the right paper from a photo. Guaranteed fit.\n\n{PHONE} | {WEBSITE}",
        "es": f"Pidió papel térmico. No cabe en su impresora.\n\nIdentificamos el correcto con una foto. Garantizado.\n\n{PHONE} | {WEBSITE}",
        "zh": f"买了热敏纸。打印机装不上。\n\n发张照片，我们帮您找对型号。保证能用。\n\n{PHONE} | {WEBSITE}",
    },
    {
        # PAIN: Surprise charges on statement
        "en": f"Sunday accounting. Mystery charge appears.\n\nEvery order from us comes with text confirmation. No surprises.\n\n{PHONE} | {WEBSITE}",
        "es": f"Domingo de cuentas. Aparece cargo misterioso.\n\nCada orden nuestra incluye confirmación por texto. Sin sorpresas.\n\n{PHONE} | {WEBSITE}",
        "zh": f"周日算账。出现不明收费。\n\n我们每笔订单都有短信确认。没有意外。\n\n{PHONE} | {WEBSITE}",
    },
    {
        # PAIN: Shipping math games
        "en": f"Paper's $89. Shipping's $47. Unless you hit $150.\n\n$9.99 flat delivery. Any order size. Same day in Vegas.\n\n{PHONE} | {WEBSITE}",
        "es": f"Papel $89. Envío $47. A menos que gaste $150.\n\nEnvío plano $9.99. Cualquier tamaño. Mismo día en Vegas.\n\n{PHONE} | {WEBSITE}",
        "zh": f"纸$89。运费$47。除非满$150免邮。\n\n统一运费$9.99。任何订单。拉斯维加斯当天送达。\n\n{PHONE} | {WEBSITE}",
    },
    {
        # PAIN: Health concerns with receipts
        "en": f"Your staff handles 200+ receipts daily.\n\nPhenol-free paper. Same price. Better for their health.\n\n{PHONE} | {WEBSITE}",
        "es": f"Su personal maneja 200+ recibos diarios.\n\nPapel sin fenol. Mismo precio. Mejor para su salud.\n\n{PHONE} | {WEBSITE}",
        "zh": f"您的员工每天处理200+张收据。\n\n无酚纸。同样价格。对他们的健康更好。\n\n{PHONE} | {WEBSITE}",
    },
    {
        # PAIN: Phone trees, transfers, no answers
        "en": f"Call for support. Phone tree. Transfer. Transfer. Hang up.\n\nWhen you call us, you get a human who knows POS systems.\n\n{PHONE}",
        "es": f"Llama soporte. Árbol telefónico. Transferencia. Transferencia. Colgar.\n\nCuando nos llama, habla con humano que conoce POS.\n\n{PHONE}",
        "zh": f"打电话求助。语音菜单。转接。转接。挂断。\n\n打给我们，您直接和懂POS系统的人通话。\n\n{PHONE}",
    },
    {
        # PAIN: Supply chain delays
        "en": f"Supply chain delays hitting your stock?\n\nWe maintain consistent inventory for Vegas restaurants. Same-day available.\n\n{PHONE} | {WEBSITE}",
        "es": f"¿Retrasos en cadena de suministro afectan su stock?\n\nMantenemos inventario consistente para restaurantes Vegas. Mismo día disponible.\n\n{PHONE} | {WEBSITE}",
        "zh": f"供应链延迟影响您的库存？\n\n我们为拉斯维加斯餐厅保持稳定库存。当天送达可用。\n\n{PHONE} | {WEBSITE}",
    },
    {
        # PAIN: Opening new restaurant, POS setup stress
        "en": f"Opening a restaurant? POS setup stress?\n\nWe handle install, cabling, training. Get it right from day one.\n\n{PHONE} | {WEBSITE}",
        "es": f"¿Abriendo restaurante? ¿Estrés con configuración POS?\n\nManejamos instalación, cableado, entrenamiento. Desde día uno.\n\n{PHONE} | {WEBSITE}",
        "zh": f"开新餐厅？POS设置压力大？\n\n我们处理安装、布线、培训。从第一天就做好。\n\n{PHONE} | {WEBSITE}",
    },
    {
        # PAIN: Printer down, nobody to fix it
        "en": f"Printer down. Nobody answers. Weekend ruined.\n\nOur techs work weekends. On-site repair. We're local.\n\n{PHONE} | {WEBSITE}",
        "es": f"Impresora falla. Nadie responde. Fin de semana arruinado.\n\nNuestros técnicos trabajan fines de semana. Reparación en sitio.\n\n{PHONE} | {WEBSITE}",
        "zh": f"打印机坏了。没人接电话。周末毁了。\n\n我们技术人员周末工作。上门维修。我们是本地的。\n\n{PHONE} | {WEBSITE}",
    },
    {
        # PAIN: Inflation, supply costs up
        "en": f"Supply costs up 15-20% this year?\n\nLock in pricing with a reliable local supplier. We've served Vegas since 2005.\n\n{PHONE} | {WEBSITE}",
        "es": f"¿Costos de suministros subieron 15-20% este año?\n\nAsegure precios con proveedor local confiable. Servimos Vegas desde 2005.\n\n{PHONE} | {WEBSITE}",
        "zh": f"今年耗材成本上涨15-20%？\n\n与可靠本地供应商锁定价格。我们服务拉斯维加斯始于2005年。\n\n{PHONE} | {WEBSITE}",
    },
]

import random
import sys
from datetime import datetime

def get_daily_content():
    """Get one pain-point message in all three languages"""
    return random.choice(PAIN_POINT_MESSAGES)

def get_content_by_pain(pain_type):
    """Get content by specific pain point"""
    pain_map = {
        "inventory_panic": [0],      # Friday night, out of paper
        "wrong_product": [1],       # Ordered wrong paper
        "surprise_charges": [2],      # Ghost invoice
        "shipping_games": [3],        # Math games, minimums
        "health_concerns": [4],       # BPA/phenol
        "bad_support": [5],          # Phone trees
        "supply_delays": [6],        # Stock issues
        "new_restaurant": [7],        # Opening stress
        "printer_down": [8],         # Weekend repair
        "inflation": [9],             # Rising costs
    }
    
    if pain_type in pain_map:
        idx = pain_map[pain_type][0]
        return PAIN_POINT_MESSAGES[idx]
    return random.choice(PAIN_POINT_MESSAGES)

def main():
    if len(sys.argv) < 2:
        print("=" * 70)
        print("X Pain-Point Content Generator - Performance Supply Depot")
        print("Highlight pain, offer solution, never ascribe blame")
        print("=" * 70)
        print("\nPain Points Available:")
        print("  inventory_panic  - Friday night, out of paper")
        print("  wrong_product    - Ordered wrong paper, doesn't fit")
        print("  surprise_charges - Mystery charges on statement")
        print("  shipping_games   - Math games, free shipping thresholds")
        print("  health_concerns  - BPA/phenol-free paper")
        print("  bad_support      - Phone trees, no answers")
        print("  supply_delays    - Stock running low")
        print("  new_restaurant   - Opening stress, setup help")
        print("  printer_down     - Weekend repair needed")
        print("  inflation        - Rising supply costs")
        print("\nUsage:")
        print("  x_pain_content.py daily              # Random pain point")
        print("  x_pain_content.py [pain_type]        # Specific pain")
        print("  x_pain_content.py all                # Show all 10")
        return
    
    command = sys.argv[1]
    
    if command == "daily":
        messages = get_daily_content()
        print(f"\n📅 Pain-Point Content - {datetime.now().strftime('%Y-%m-%d')}")
        print("Strategy: Highlight pain → Offer solution → No blame\n")
        print("=" * 70)
        
        print("\n🇺🇸 ENGLISH:")
        print(f"{messages['en']}")
        print(f"\nLength: {len(messages['en'])} chars")
        
        print("\n🇪🇸 SPANISH:")
        print(f"{messages['es']}")
        print(f"\nLength: {len(messages['es'])} chars")
        
        print("\n🇨🇳 CHINESE:")
        print(f"{messages['zh']}")
        print(f"\nLength: {len(messages['zh'])} chars")
        
        print("\n" + "=" * 70)
        print("\n✅ Ready to post via browser automation")
        print("🎯 Pain-point strategy: Relatable → Solution → CTA")
        
    elif command == "all":
        print(f"\n📋 All Pain-Point Messages\n")
        print("=" * 70)
        
        pain_names = [
            ("INVENTORY PANIC", "Friday night, out of paper"),
            ("WRONG PRODUCT", "Ordered wrong paper, doesn't fit"),
            ("SURPRISE CHARGES", "Mystery charges on statement"),
            ("SHIPPING GAMES", "Math games, free shipping thresholds"),
            ("HEALTH CONCERNS", "BPA/phenol-free paper"),
            ("BAD SUPPORT", "Phone trees, no answers"),
            ("SUPPLY DELAYS", "Stock running low"),
            ("NEW RESTAURANT", "Opening stress, setup help"),
            ("PRINTER DOWN", "Weekend repair needed"),
            ("INFLATION", "Rising supply costs"),
        ]
        
        for i, (name, desc) in enumerate(pain_names):
            msg = PAIN_POINT_MESSAGES[i]
            print(f"\n{i+1}. {name}")
            print(f"   Pain: {desc}")
            print(f"\n   EN: {msg['en'][:60]}...")
            print(f"   ES: {msg['es'][:60]}...")
            print(f"   ZH: {msg['zh'][:40]}...")
            print("-" * 70)
            
    elif command in ["inventory_panic", "wrong_product", "surprise_charges", 
                     "shipping_games", "health_concerns", "bad_support", 
                     "supply_delays", "new_restaurant", "printer_down", "inflation"]:
        messages = get_content_by_pain(command)
        print(f"\n📌 Pain Point: {command.replace('_', ' ').title()}")
        print(f"\n🇺🇸 ENGLISH:\n{messages['en']}")
        print(f"\n🇪🇸 SPANISH:\n{messages['es']}")
        print(f"\n🇨🇳 CHINESE:\n{messages['zh']}")
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: daily, all, or specific pain type")

if __name__ == "__main__":
    main()
