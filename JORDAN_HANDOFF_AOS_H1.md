# AOS-H1 Production Handoff
## Jordan Assignment: Robot Production Coordination

**Assigned By:** Captain  
**Handed Off By:** Miles (Dark Factory AOS)  
**Date:** March 30, 2026  
**Status:** Ready for Production

---

## 🎯 MISSION: Build AOS-H1 in Stages

### Stage 1: Virtual Model (Week 1-2)
- [ ] Review CAD files in `/AOS-H1/cad/`
- [ ] Run STL generator script
- [ ] Validate all 102 parts fit together
- [ ] Create assembly animation/video

### Stage 2: Vendor Sourcing (Week 2-3)
**Priority Vendors Needed:**

| Category | Vendor Type | Quantity | Notes |
|----------|-------------|----------|-------|
| **PCB Fabrication** | Circuit board manufacturer | 7 boards | ESP32 nodes, power distribution |
| **3D Printing** | PETG-CF/TPU printing service | 102 parts | 280 hours print time |
| **CNC Machining** | Aluminum parts | 12 parts | Precision bearings, brackets |
| **Actuators** | Servo distributor | 42 servos | DS3218, MG996R, SG90 |
| **Electronics** | Component distributor | 200+ components | Full BOM |
| **Power** | Battery/BMS supplier | 2 batteries + BMS | 6S LiPo 5000mAh |

**Snap-Together Preferred:**
- Design parts for minimal assembly
- Heat-set inserts pre-installed
- Plug-and-play electronics
- Tool-less where possible

### Stage 3: In-House Assembly (Week 4-6)
- [ ] Receive all parts
- [ ] Inventory check against BOM
- [ ] Test fit virtual model
- [ ] Assembly according to guide
- [ ] Calibration and testing

### Stage 4: Production Handoff (Week 7+)
- [ ] Document lessons learned
- [ ] Refine BOM based on actual costs
- [ ] Prepare production package for vendors
- [ ] Scale to 5-10 units

---

## 📋 VENDOR REQUIREMENTS

### PCB Fabrication Vendor
**Requirements:**
- 2-layer and 4-layer boards
- Lead-free assembly
- Quick turnaround (1-2 weeks)
- Assembly service preferred
- Budget: ~$500 for 7 boards

**Suggested Vendors:**
- PCBWay (pcbway.com)
- JLCPCB (jlcpcb.com)
- OSH Park (oshpark.com)

### 3D Printing Vendor
**Requirements:**
- PETG-CF filament capability
- TPU flexible filament
- Large build volume (200mm+)
- Tight tolerances (±0.1mm)
- Batch pricing for 102 parts
- Budget: ~$600

**Suggested Vendors:**
- Craftcloud (craftcloud3d.com) - aggregator
- Xometry (xometry.com)
- Local makerspaces

### CNC Machining Vendor
**Requirements:**
- Aluminum 6061
- 20×20mm extrusions
- Threaded rod cutting
- Budget: ~$100

**Suggested Vendors:**
- Xometry
- SendCutSend
- Local machine shops

### Servo Supplier
**Requirements:**
- Bulk pricing (10+ units)
- DS3218 (20kg) - 12 units
- MG996R (10kg) - 10 units
- SG90 micro - 30 units
- Budget: ~$486

**Suggested Vendors:**
- ServoCity (bulk pricing)
- Amazon (quick delivery)
- HobbyKing (international)

---

## 💰 BUDGET SUMMARY

| Category | Estimated | Vendor |
|----------|-----------|--------|
| PCBs | $500 | TBD |
| 3D Printing | $600 | TBD |
| CNC | $100 | TBD |
| Servos | $486 | TBD |
| Electronics | $824 | TBD |
| Power | $251 | TBD |
| **TOTAL** | **$2,761** | |

---

## 🔧 SNAP-TOGETHER DESIGN MODIFICATIONS

**If vendors can't do snap-fit, consider:**

1. **Heat-set inserts** - Pre-install threaded inserts
2. **Press-fit bearings** - Tight tolerances for friction fit
3. **Alignment pins** - Guide assembly visually
4. **Cable management** - Pre-routed channels
5. **Modular sub-assemblies** - Build torso/arms/legs separately

**Assembly time target:**
- Expert: 20 hours
- First-time builder: 40-60 hours

---

## 📞 TEAM RESOURCES

**Technical Support:**
- STACKTRACE (Chief Software Architect)
- TAPTAP (Mobile/Frontend)
- PIPELINE (Backend/DevOps)
- BUGCATCHER (QA)

**Questions?**
- Full docs: `/AOS-H1/`
- BOM: `/AOS-H1/bom/BOM.md`
- Assembly: `/AOS-H1/docs/ASSEMBLY_GUIDE.md`
- CAD: `/AOS-H1/cad/stl_generator.py`

---

## ✅ JORDAN'S CHECKLIST

**Week 1:**
- [ ] Review AOS-H1 documentation
- [ ] Generate STLs
- [ ] Get quotes from 3 PCB vendors
- [ ] Get quotes from 3 3D printing vendors

**Week 2:**
- [ ] Compare quotes, select vendors
- [ ] Place orders for long-lead items (PCBs, 3D printing)
- [ ] Order servos and electronics

**Week 3:**
- [ ] Receive first parts
- [ ] Quality check
- [ ] Begin virtual assembly

**Week 4-6:**
- [ ] Physical assembly
- [ ] Testing
- [ ] Documentation

**Week 7+:**
- [ ] Production package ready
- [ ] Scale to multiple units

---

## 💬 FROM CAPTAIN

> "Jordan is turning out to be quite effective. She's doing a great job."

**You've got this, Jordan!** The AOS-H1 is a big project, but we've done the hard work - full documentation, BOM, assembly guide. Now it's about coordination and execution.

**Need help?** Loop in the Technical team. They've got your back.

**Questions?** Captain said he may touch base tomorrow from the field.

---

*Handoff complete. Jordan, you're up!* 🤖

*Miles - Dark Factory AOS*  
*March 30, 2026*
