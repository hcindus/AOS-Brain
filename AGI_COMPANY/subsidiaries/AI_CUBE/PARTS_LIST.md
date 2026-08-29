# AI CUBE — Parts List (Pi 5 build)

**Owner:** Captain (Antonio) · **Date:** 2026-08-29 · **Repo:** `AGI_COMPANY/subsidiaries/AI_CUBE/`

> Links are Amazon search links (land on the exact product category). Exact ASINs/sellers
> rotate and can't be verified live, so pick the top-reviewed Prime listing on each page.
> Prices are approximate 2026 USD. **"Look for" = the thing that separates a good buy from a dud.**

---

## Core (the brain box)

**Raspberry Pi 5 — 16GB** — ~$120
- Look for: genuine (not clone), and grab the **official 27W USB-C PSU** + an active cooler or passive metal case (Pi 5 throttles without cooling).
- → https://www.amazon.com/s?k=raspberry+pi+5+16gb

**Geekworm X735 UPS HAT** — ~$33
- Look for: the Pi 5 variant (some are Pi 4 only), includes safe-shutdown script, supports battery input.
- → https://www.amazon.com/s?k=geekworm+x735+ups+hat

**128GB NVMe SSD + M.2 HAT** — ~$40
- Look for: an **M.2 HAT specifically for Pi 5**, plus a **Gen3 NVMe 2280** drive (Gen4 just downclocks).
- → https://www.amazon.com/s?k=raspberry+pi+5+nvme+m.2+hat

## Arm (grabber)

**6-DOF metal arm kit** — ~$60
- Look for: **aluminum/steel brackets (not acrylic)**, 6 servos + gripper included, "MG996R-class" servos.
- → https://www.amazon.com/s?k=6dof+metal+robotic+arm+kit+servo

**PCA9685 16-ch PWM driver** — ~$13
- Look for: 16-channel, I2C address selectable (solder pads), **3.3V logic compatible**.
- → https://www.amazon.com/s?k=pca9685+16+channel+pwm+servo+driver

**2× genuine MG996R servos** — ~24
- Look for: **metal gears** (the #1 thing — plastic-gear clones strip in days), high-torque, "genuine MG996R."
- → https://www.amazon.com/s?k=mg996r+servo

## Sensors (eyes & ears)

**VL53L1X ToF distance** — ~$13
- Look for: I2C breakout with onboard **voltage regulator** (accepts 3.3V/5V), ~4m range.
- → https://www.amazon.com/s?k=vl53l1x+time+of+flight

**HC-SR04 ultrasonic** — ~$4
- Look for: 5V module — **pair with a voltage divider** (or 3.3V-tolerant version) for the Pi's 3.3V logic.
- → https://www.amazon.com/s?k=hc-sr04+ultrasonic+sensor

**BNO055 IMU** — ~$20
- Look for: 9-DOF **with onboard sensor fusion**, I2C, 3.3V logic.
- → https://www.amazon.com/s?k=bno055+imu+9+dof

**Pi Camera Module 3** — ~$28
- Look for: **genuine Raspberry Pi Camera Module 3**, 12MP autofocus, includes ribbon cable.
- → https://www.amazon.com/s?k=raspberry+pi+camera+module+3

**ReSpeaker 2-Mic HAT** — ~$25
- Look for: Pi 5 header compatible, 2 mics, **built-in DAC** (so audio out works too).
- → https://www.amazon.com/s?k=respeaker+2+mic+hat

**MAX98357A amp + 3W speaker** — ~$13
- Look for: I2S input, **3.3V logic**, 3W speaker included.
- → https://www.amazon.com/s?k=max98357a+i2s+amplifier

## Mobility

**DC gear motors + DRV8833** — ~$28
- Look for: gear motors **with encoders**, DRV8833 dual H-bridge, 6–12V.
- → https://www.amazon.com/s?k=dc+gear+motor+drv8833+driver

**Tank tracks + chassis** — ~$25
- Look for: matching track + drive-sprocket kit, sturdy frame.
- → https://www.amazon.com/s?k=robot+tank+track+chassis

**Rotary encoders** — ~$12
- Look for: **quadrature** output, shaft matches motor.
- → https://www.amazon.com/s?k=rotary+encoder+motor+wheel

## Power

**LiFePO4 or 3–4× 18650 pack** — ~$40
- Look for: **protected cells** / BMS, output voltage matches the X735's input.
- → https://www.amazon.com/s?k=lifepo4+battery+pack+12v

## Misc

**Jumper wires + breadboard + wiring** — ~$18
- Look for: Dupont **male + female** mix, solid-core, 20–40cm.
- → https://www.amazon.com/s?k=jumper+wires+breadboard+kit

**Make: Robotic Arms (Matthew Eaton)** — ~$25
- Look for: the Matthew Eaton edition (inverse-kinematics chapters are the value).
- → https://www.amazon.com/s?k=make+robotic+arms+matthew+eaton

---

**Total: ~$530–580**

**Don't cheap out on:** high-endurance storage + **metal-gear** servos (the two things that
corrupt/fail first).
