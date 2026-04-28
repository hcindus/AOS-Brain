#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X (Twitter) Content Generator for Performance Supply Depot
Ethical, factual content designed to help small business owners succeed.

PRINCIPLES:
- No false claims or exaggerated savings
- Actual product prices and services offered
- Educational content that adds value
- Respectful tone, no pressure tactics
- Clear contact information for genuine inquiries
"""

import random
import sys
from datetime import datetime

PHONE = "888-881-6834"
WEBSITE = "https://psdepot.com"

# Ethical Content Templates - Focused on value and education
TEMPLATES = {
    "en": {
        "educational": [
            f"Tip: Thermal paper darkens when exposed to heat/sunlight. Store in a cool, dry place to extend shelf life. Questions? {PHONE} | {WEBSITE}",
            f"Receipt printer streaking? Try cleaning the thermal head monthly with isopropyl alcohol on a lint-free cloth. {WEBSITE} | {PHONE}",
            f"Did you know? Bond paper for impact printers lasts longer when stored flat, not on its side. More tips: {WEBSITE} | {PHONE}",
            f"Regular printer maintenance can prevent costly breakdowns during rush hour. We offer on-site service in Vegas. {PHONE} | {WEBSITE}",
            f"Choosing the right receipt paper matters. Thermal for heat-based printers, bond for impact printers. Need help? {PHONE} | {WEBSITE}",
        ],
        "service_info": [
            f"We service Samsung, Clover, Square, and most major POS systems. Local technicians available in Las Vegas. {PHONE} | {WEBSITE}",
            f"Same-day delivery available for in-stock items when ordered by 2 PM. Serving Las Vegas restaurants. {PHONE} | {WEBSITE}",
            f"POS system questions? Our team has 15+ years experience with restaurant point-of-sale equipment. Call us: {PHONE} | {WEBSITE}",
            f"From receipt paper to full POS setups — we help Vegas restaurants keep operations running smoothly. {PHONE} | {WEBSITE}",
        ],
        "pricing_transparent": [
            f"Samsung POS systems: Starting at $495 with professional installation available. Get a quote: {PHONE} | {WEBSITE}",
            f"Thermal receipt paper rolls in stock. Competitive pricing with volume discounts available. Inquire: {PHONE} | {WEBSITE}",
            f"Restaurant scales (CAS, AND, Samsung) starting at $795. Calibrated and ready for commercial use. {PHONE} | {WEBSITE}",
            f"Printer repair service: Diagnostic fee applies, credited toward repair. No surprises. Vegas local: {PHONE} | {WEBSITE}",
        ],
        "helpful": [
            f"Running low on supplies? We recommend keeping a 2-week buffer to avoid weekend stockouts. Order: {PHONE} | {WEBSITE}",
            f"Q3 planning time. Evaluating your POS supply costs? We're happy to provide a comparison quote. {PHONE} | {WEBSITE}",
            f"New restaurant opening in Vegas? We help with POS setup, supply planning, and staff training. {PHONE} | {WEBSITE}",
            f"Questions about printer compatibility? Send us your model number — we'll confirm the right supplies. {PHONE} | {WEBSITE}",
        ],
    },
    "es": {
        "educational": [
            f"Consejo: El papel térmico se oscurece con el calor y sol. Guárdelo en lugar fresco y seco. Preguntas? {PHONE} | {WEBSITE}",
            f"¿Su impresora de recibos tiene rayas? Limpie la cabeza térmica mensual con alcohol isopropílico. {PHONE} | {WEBSITE}",
            f"El papel bond para impresoras de impacto dura más si se guarda plano, no de lado. Más consejos: {PHONE} | {WEBSITE}",
            f"El mantenimiento regular de impresoras evita fallas costosas durante las horas pico. Servicio en Las Vegas: {PHONE} | {WEBSITE}",
            f"Papel térmico para impresoras de calor, papel bond para impresoras de impacto. ¿Necesita ayuda? {PHONE} | {WEBSITE}",
        ],
        "service_info": [
            f"Serviciamos Samsung, Clover, Square y la mayoría de sistemas POS. Técnicos locales en Las Vegas. {PHONE} | {WEBSITE}",
            f"Entrega mismo día disponible para artículos en stock si ordena antes de las 2 PM. {PHONE} | {WEBSITE}",
            f"¿Preguntas sobre sistemas POS? Nuestro equipo tiene 15+ años de experiencia. Llámenos: {PHONE} | {WEBSITE}",
            f"Desde papel térmico hasta configuraciones POS completas — ayudamos a restaurantes en Las Vegas. {PHONE} | {WEBSITE}",
        ],
        "pricing_transparent": [
            f"Sistemas POS Samsung: Desde $495 con instalación profesional disponible. Cotización: {PHONE} | {WEBSITE}",
            f"Rollos de papel térmico en stock. Precios competitivos con descuentos por volumen. Pregunte: {PHONE} | {WEBSITE}",
            f"Básculas para restaurantes (CAS, AND, Samsung) desde $795. Calibradas para uso comercial. {PHONE} | {WEBSITE}",
            f"Servicio de reparación: Aplica cuota de diagnóstico, acreditada a la reparación. {PHONE} | {WEBSITE}",
        ],
        "helpful": [
            f"¿Se le acaban los suministros? Recomendamos mantener reserva de 2 semanas. Ordene: {PHONE} | {WEBSITE}",
            f"Temporada de planificación Q3. ¿Evaluando costos de suministros POS? Cotización sin compromiso: {PHONE} | {WEBSITE}",
            f"¿Abriendo restaurante nuevo en Las Vegas? Ayudamos con configuración POS y capacitación. {PHONE} | {WEBSITE}",
            f"¿Preguntas sobre compatibilidad de impresoras? Envíenos el modelo — confirmamos los suministros. {PHONE} | {WEBSITE}",
        ],
    },
    "zh": {
        "educational": [
            f"提示: 热敏纸遇热和阳光会变黑。存放在阴凉干燥处可延长保质期。咨询: {PHONE} | {WEBSITE}",
            f"收据打印机有条纹? 每月用异丙醇和无绒布清洁热敏头。{PHONE} | {WEBSITE}",
            f"击打式打印机的债券纸平放比侧放更耐用。更多提示: {PHONE} | {WEBSITE}",
            f"定期打印机维护可防止繁忙时段的昂贵故障。拉斯维加斯上门服务: {PHONE} | {WEBSITE}",
            f"热敏纸用于热敏打印机，债券纸用于击打式打印机。需要帮助? {PHONE} | {WEBSITE}",
        ],
        "service_info": [
            f"我们维修三星、Clover、Square及大多数POS系统。拉斯维加斯本地技术人员。{PHONE} | {WEBSITE}",
            f"下午2点前下单的现货可当日送达。服务拉斯维加斯餐厅。{PHONE} | {WEBSITE}",
            f"POS系统问题? 我们的团队有15年以上餐厅收银设备经验。致电: {PHONE} | {WEBSITE}",
            f"从收据纸到完整POS系统 — 我们帮助拉斯维加斯餐厅顺利运营。{PHONE} | {WEBSITE}",
        ],
        "pricing_transparent": [
            f"三星POS系统: $495起，提供专业安装。获取报价: {PHONE} | {WEBSITE}",
            f"热敏收据纸卷有货。价格竞争力强，量大优惠。咨询: {PHONE} | {WEBSITE}",
            f"餐厅秤(CAS、AND、三星) $795起。校准完毕，商用就绪。{PHONE} | {WEBSITE}",
            f"打印机维修服务: 收取诊断费，维修时抵扣。无隐藏费用。{PHONE} | {WEBSITE}",
        ],
        "helpful": [
            f"耗材不足? 我们建议保持2周库存避免周末缺货。下单: {PHONE} | {WEBSITE}",
            f"Q3规划时间。评估POS耗材成本? 我们很乐意提供对比报价。{PHONE} | {WEBSITE}",
            f"在拉斯维加斯开新餐厅? 我们提供POS设置、供应规划和员工培训。{PHONE} | {WEBSITE}",
            f"打印机兼容性问题? 发送型号给我们 — 我们确认正确的耗材。{PHONE} | {WEBSITE}",
        ],
    }
}

def get_tweet(lang="en", category=None):
    """Get a tweet in specified language"""
    if lang not in TEMPLATES:
        lang = "en"
    
    if category and category in TEMPLATES[lang]:
        return random.choice(TEMPLATES[lang][category])
    
    category = random.choice(list(TEMPLATES[lang].keys()))
    return random.choice(TEMPLATES[lang][category])

def generate_trilingual_daily():
    """Generate 1 tweet in each language - balanced across categories"""
    return {
        "en": get_tweet("en", "educational"),
        "es": get_tweet("es", "service_info"),
        "zh": get_tweet("zh", "helpful")
    }

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("X Marketing Content Generator - Performance Supply Depot")
        print("Ethical, factual content for small business owners")
        print("Phone:", PHONE)
        print("Website:", WEBSITE)
        print("=" * 60)
        print("\nCategories: educational, service_info, pricing_transparent, helpful")
        print("\nUsage:")
        print("  x_content.py daily       # Generate 1 tweet per language")
        print("  x_content.py en          # Random English tweet")
        print("  x_content.py es          # Random Spanish tweet")
        print("  x_content.py zh          # Random Chinese tweet")
        return
    
    command = sys.argv[1]
    
    if command == "daily":
        tweets = generate_trilingual_daily()
        print(f"\n📅 Ethical Marketing Content - {datetime.now().strftime('%Y-%m-%d')}\n")
        print("=" * 60)
        print("Ethical Guidelines: Factual • Educational • No Pressure • Transparent")
        print("=" * 60)
        
        print("\n🇺🇸 ENGLISH (Educational Focus):")
        print(f"{tweets['en']}")
        print(f"Length: {len(tweets['en'])} chars")
        
        print("\n🇪🇸 SPANISH (Service Focus):")
        print(f"{tweets['es']}")
        print(f"Length: {len(tweets['es'])} chars")
        
        print("\n🇨🇳 CHINESE (Helpful Focus):")
        print(f"{tweets['zh']}")
        print(f"Length: {len(tweets['zh'])} chars")
        
        print("\n" + "=" * 60)
        print("\n✅ Ready to copy/paste into X Agent console")
        print("📋 Log file: /var/log/x_marketing.log")
        
    elif command in ["en", "es", "zh"]:
        tweet = get_tweet(command)
        lang_name = {"en": "English", "es": "Spanish", "zh": "Chinese"}[command]
        print(f"\n🐦 {lang_name} Tweet:")
        print(f"{tweet}")
        print(f"\nLength: {len(tweet)} characters")
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: daily, en, es, or zh")

if __name__ == "__main__":
    main()
