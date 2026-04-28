#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) Content Generator for Performance Supply Depot
Same message for all communities, translated to each language.

PRINCIPLES:
- Same core message, different language
- Ethical, factual, useful for small business owners
- No false claims or exaggerated savings
- Respectful tone, no pressure tactics
"""

import random
import sys
from datetime import datetime

PHONE = "888-881-6834"
WEBSITE = "https://psdepot.com"

# Same message, translated to all three languages
MESSAGE_TEMPLATES = [
    {
        "en": f"Tip: Store thermal paper away from heat and sunlight to prevent premature darkening. Questions? {PHONE} | {WEBSITE}",
        "es": f"Consejo: Guarde el papel térmico lejos del calor y sol para evitar oscurecimiento prematuro. Preguntas? {PHONE} | {WEBSITE}",
        "zh": f"提示: 将热敏纸存放在远离热源和阳光的地方，防止过早变黑。有问题? {PHONE} | {WEBSITE}",
    },
    {
        "en": f"Receipt printer streaking? Clean the thermal head monthly with isopropyl alcohol. Need help? {PHONE} | {WEBSITE}",
        "es": f"¿Su impresora de recibos tiene rayas? Limpie la cabeza térmica mensual con alcohol isopropílico. Ayuda? {PHONE} | {WEBSITE}",
        "zh": f"收据打印机有条纹? 每月用异丙醇清洁热敏头。需要帮助? {PHONE} | {WEBSITE}",
    },
    {
        "en": f"Printer Swaps available - Trade in your old printer for a refurbished unit. Ask about options: {PHONE} | {WEBSITE}",
        "es": f"Cambio de Impresoras disponible - Cambie su impresora vieja por una reacondicionada. Pregunte opciones: {PHONE} | {WEBSITE}",
        "zh": f"打印机以旧换新服务 - 用旧打印机换翻新机。询问详情: {PHONE} | {WEBSITE}",
    },
    {
        "en": f"Cabling Services for any POS system. Professional installation and network setup. Book now: {PHONE} | {WEBSITE}",
        "es": f"Servicios de Cableado para cualquier sistema POS. Instalación profesional y configuración de red. Reserve: {PHONE} | {WEBSITE}",
        "zh": f"任何POS系统的布线服务。专业安装和网络设置。立即预约: {PHONE} | {WEBSITE}",
    },
    {
        "en": f"Sam4s POS Systems now available. Reliable hardware for restaurants and retail. Get a quote: {PHONE} | {WEBSITE}",
        "es": f"Sistemas Sam4s POS ahora disponibles. Hardware confiable para restaurantes y retail. Cotización: {PHONE} | {WEBSITE}",
        "zh": f"Sam4s POS系统现已到货。适用于餐厅和零售的可靠硬件。获取报价: {PHONE} | {WEBSITE}",
    },
    {
        "en": f"Running low on supplies? We recommend keeping a 2-week buffer. Order now: {PHONE} | {WEBSITE}",
        "es": f"¿Bajo en suministros? Recomendamos mantener reserva de 2 semanas. Ordene: {PHONE} | {WEBSITE}",
        "zh": f"耗材不足? 我们建议保持2周库存。立即下单: {PHONE} | {WEBSITE}",
    },
    {
        "en": f"Restaurant scales available: CAS, AND, Samsung models starting at $795. Calibrated and ready. {PHONE} | {WEBSITE}",
        "es": f"Básculas para restaurantes disponibles: CAS, AND, Samsung desde $795. Calibradas y listas. {PHONE} | {WEBSITE}",
        "zh": f"餐厅秤有货: CAS、AND、三星型号起价$795。已校准，即装即用。{PHONE} | {WEBSITE}",
    },
    {
        "en": f"Our technicians repair all major printer brands on-site in Las Vegas. Book service: {PHONE} | {WEBSITE}",
        "es": f"Nuestros técnicos reparan todas las marcas de impresoras en su local en Las Vegas. Reserve: {PHONE} | {WEBSITE}",
        "zh": f"我们技术人员在拉斯维加斯上门维修所有品牌打印机。预约服务: {PHONE} | {WEBSITE}",
    },
    {
        "en": f"New customers: Ask about our first-order discount and free printer diagnostic. {PHONE} | {WEBSITE}",
        "es": f"Clientes nuevos: Pregunte por descuento en primera orden y diagnóstico gratis. {PHONE} | {WEBSITE}",
        "zh": f"新客户: 询问首单优惠和免费打印机检测。{PHONE} | {WEBSITE}",
    },
    {
        "en": f"Quality POS supplies help prevent costly downtime. Stock up before the weekend rush. {PHONE} | {WEBSITE}",
        "es": f"Suministros POS de calidad ayudan a prevenir costosas interrupciones. Stock antes del finde. {PHONE} | {WEBSITE}",
        "zh": f"优质POS耗材有助于防止代价高昂的停机。周末高峰前备货。{PHONE} | {WEBSITE}",
    },
    {
        "en": f"Opening a new restaurant in Vegas? We help with POS setup, supplies, and staff training. {PHONE} | {WEBSITE}",
        "es": f"¿Abriendo restaurante nuevo en Vegas? Ayudamos con configuración POS, suministros y entrenamiento. {PHONE} | {WEBSITE}",
        "zh": f"在拉斯维加斯开新餐厅? 我们协助POS设置、耗材和员工培训。{PHONE} | {WEBSITE}",
    },
    {
        "en": f"Need help choosing the right receipt paper? Thermal for heat printers, bond for impact. Call us: {PHONE} | {WEBSITE}",
        "es": f"¿Ayuda eligiendo papel térmico correcto? Térmico para impresoras de calor, bond para impacto. Llámenos: {PHONE} | {WEBSITE}",
        "zh": f"需要帮忙选择正确的收据纸? 热敏纸用于热敏打印机，复写纸用于击打式。致电我们: {PHONE} | {WEBSITE}",
    },
]

def get_daily_content():
    """Get one message in all three languages"""
    message = random.choice(MESSAGE_TEMPLATES)
    return message

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("X Marketing Content Generator - Performance Supply Depot")
        print("Same message for all communities, translated")
        print("Phone:", PHONE)
        print("Website:", WEBSITE)
        print("=" * 60)
        print("\nUsage:")
        print("  x_content.py daily       # Generate same message in 3 languages")
        print("  x_content.py en          # Random English message")
        print("  x_content.py es          # Random Spanish message")
        print("  x_content.py zh          # Random Chinese message")
        return
    
    command = sys.argv[1]
    
    if command == "daily":
        messages = get_daily_content()
        print(f"\n📅 Daily Content - {datetime.now().strftime('%Y-%m-%d')}")
        print("Same message for all communities\n")
        print("=" * 60)
        
        print("\n🇺🇸 ENGLISH:")
        print(f"{messages['en']}")
        print(f"Length: {len(messages['en'])} chars")
        
        print("\n🇪🇸 SPANISH:")
        print(f"{messages['es']}")
        print(f"Length: {len(messages['es'])} chars")
        
        print("\n🇨🇳 CHINESE:")
        print(f"{messages['zh']}")
        print(f"Length: {len(messages['zh'])} chars")
        
        print("\n" + "=" * 60)
        print("\n✅ Ready to copy/paste into X Agent console")
        print("📋 Log file: /var/log/x_marketing.log")
        
    elif command in ["en", "es", "zh"]:
        message = random.choice(MESSAGE_TEMPLATES)[command]
        lang_name = {"en": "English", "es": "Spanish", "zh": "Chinese"}[command]
        print(f"\n🐦 {lang_name}:")
        print(f"{message}")
        print(f"\nLength: {len(message)} characters")
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: daily, en, es, or zh")

if __name__ == "__main__":
    main()
