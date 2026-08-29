# AI CUBE — Parts List (Pi 5 build)

**Owner:** Captain (Antonio) · **Date:** 2026-08-29 · **Repo:** `AGI_COMPANY/subsidiaries/AI_CUBE/`

> Links are Amazon search links (land on the exact product category). Exact ASINs/sellers
> rotate and can't be verified live, so pick the top-reviewed Prime listing on each page.
> Prices are approximate 2026 USD.

---

## Core (the brain box)

| Item | Note | ~$ |
|------|------|----|
| Raspberry Pi 5 — **16GB** | the body's brain | 120 |
| Geekworm **X735** UPS HAT | safe shutdown + battery mgmt — *don't skip* | 33 |
| 128GB NVMe SSD + M.2 HAT | or high-endurance 64GB SD | 40 |

- Pi 5 16GB → https://www.amazon.com/s?k=raspberry+pi+5+16gb
- Geekworm X735 → https://www.amazon.com/s?k=geekworm+x735+ups+hat
- NVMe + M.2 HAT → https://www.amazon.com/s?k=raspberry+pi+5+nvme+m.2+hat

## Arm (grabber)

| Item | Note | ~$ |
|------|------|----|
| 6-DOF metal arm kit | "industrial teaching" type | 60 |
| PCA9685 16-ch PWM | servo driver (I2C) | 13 |
| 2× genuine MG996R | spares (kit servos are clones) | 24 |

- Arm kit → https://www.amazon.com/s?k=6dof+metal+robotic+arm+kit+servo
- PCA9685 → https://www.amazon.com/s?k=pca9685+16+channel+pwm+servo+driver
- MG996R → https://www.amazon.com/s?k=mg996r+servo

## Sensors (eyes & ears)

| Item | Note | ~$ |
|------|------|----|
| VL53L1X ToF | distance (I2C) | 13 |
| HC-SR04 ultrasonic | redundant range | 4 |
| BNO055 IMU | 9-DOF, "which face is up" | 20 |
| Pi Camera Module 3 | vision | 28 |
| ReSpeaker 2-Mic HAT | wake word + STT | 25 |
| MAX98357A + 3W speaker | audio out | 13 |

- VL53L1X → https://www.amazon.com/s?k=vl53l1x+time+of+flight
- HC-SR04 → https://www.amazon.com/s?k=hc-sr04+ultrasonic+sensor
- BNO055 → https://www.amazon.com/s?k=bno055+imu+9+dof
- Camera Module 3 → https://www.amazon.com/s?k=raspberry+pi+camera+module+3
- ReSpeaker 2-Mic → https://www.amazon.com/s?k=respeaker+2+mic+hat
- MAX98357A → https://www.amazon.com/s?k=max98357a+i2s+amplifier

## Mobility

| Item | Note | ~$ |
|------|------|----|
| 2× DC gear motors + DRV8833 | drive | 28 |
| Tank tracks + chassis | or mecanum wheels | 25 |
| Rotary encoders | wheel odometry | 12 |

- Motors + driver → https://www.amazon.com/s?k=dc+gear+motor+drv8833+driver
- Tracks/chassis → https://www.amazon.com/s?k=robot+tank+track+chassis
- Encoders → https://www.amazon.com/s?k=rotary+encoder+motor+wheel

## Power

| Item | Note | ~$ |
|------|------|----|
| LiFePO4 or 3–4× 18650 pack | through the X735 | 40 |

- LiFePO4 pack → https://www.amazon.com/s?k=lifepo4+battery+pack+12v

## Misc

| Item | Note | ~$ |
|------|------|----|
| Jumper wires + breadboard + wiring | | 18 |
| *Make: Robotic Arms* (Matthew Eaton) | IK reference (book) | 25 |

- Jumper wires → https://www.amazon.com/s?k=jumper+wires+breadboard+kit
- Book → https://www.amazon.com/s?k=make+robotic+arms+matthew+eaton

---

**Total: ~$530–580**

**Don't cheap out on:** high-endurance storage + genuine MG996R servos (the two things that
corrupt/fail first).
