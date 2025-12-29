# MD302 GPS Tracker – Reverse Engineering Notes

## Overblik
Denne repo dokumenterer reverse engineering af en **MD302 GPS tracker (2017)** fundet brugt.
Formålet er at fastslå hardwarestatus, firmware-adfærd og hvorfor enheden ikke forbinder til netværk.

Alt nedenfor er verificeret via **UART boot-log**.

---

## Hardware (bekræftet)
- **SoC:** MediaTek MTK (MT62xx-serien)
- **Netværk:** 2G GSM / GPRS (ONLY)
- **GPS:** Separat GPS-modul (cold start kræver fri udsigt)
- **Strøm:**
  - VBAT (Li-ion): 3.0–4.2 V
  - Normal målt: **3.47–3.62 V (OK)**
- **UART:** 3.3 V TTL
- **SIM:** micro-SIM

---

## Bootloader (vigtigt fund)
Enheden bruger **MediaTek Bootloader V005 (siden 2005)**.

Eksempel:
Bye bye bootloader, jump to=0x1000a5b0
```

### Konklusion
- CPU OK
- RAM OK
- Flash OK
- UART OK
- Firmware starter korrekt

---

## Firmware-identifikation
```
VER: MD302_V01_GM
Build date: 2017/06/23
IMEI: 353506510240772
Server: a.gps903.net:7700
```

---

## SIM-status (kritisk erkendelse)

### Før:
```
SIM CARD--------------NG
[--- NO SIM ---]
```

### Nu:
```
SIM CARD-------------------OK
GSM Signal------------NG
[--- NO SERVICE ---]
```

### Betydning
- SIM **læses korrekt**
- SIM-holder og PIN er OK
- **Netværk registreres ikke**

➡️ **Problemet er IKKE hardware, firmware, strøm eller UART**

---

## Endelig konklusion
> **MD302 er 2G GSM-only.**
>
> Moderne SIM-kort (data-deling / LTE / VoLTE) har typisk **IKKE 2G aktiveret**.
>
> Derfor:
```
GSM Signal------------NG
SOCKET----------------NG
```

Dette er forventet adfærd i 2024+.

---

## Hvad virker
- Bootloader
- Firmware
- SIM-detektion
- Batterimåling
- UART logging
- GPS-hardware (kræver udendørs test)

---

## Hvad virker ikke
- GSM-netværk (kræver aktiv 2G)
- Socket-forbindelse til server
- Tracking via gps903-platformen

---

## Test-metode (kort)
- UART: TX + GND (3.3 V)
- Baud: 115200
- Strøm: 5 V via strøm-ind (ikke USB)
- SIM: micro-SIM, PIN OFF

---

## Mulige veje videre
1. Brug **tale-SIM med aktiv 2G** (hvis muligt)
2. Brug enheden **uden GSM** (UART/GPS logger)
3. Firmware-dump via MTK tools (SP Flash Tool)
4. Dokumentation / læringsprojekt

---

## Status
🟢 Enheden er teknisk sund  
🔴 GSM-netværk er udfaset / utilgængeligt  
🟡 Velegnet til reverse engineering / embedded learning

---

## Noter
Dette repo er ment som dokumentation og vidensdeling.
Ingen kommerciel brug.
```

## MediaTek MT62xx-serien – Teknisk overblik

**MediaTek MT62xx-serien** er en familie af ældre **System-on-a-Chip (SoC)**- og
controller-chips, primært designet til **feature phones** og trådløse
kommunikationsenheder fra midten af 2000’erne og frem.

Serien var udbredt i billige mobiltelefoner, GPS-trackere og andre
embedded GSM-enheder – især i det asiatiske marked.

---

### Nøgleinformation om MT62xx-serien

**Formål**
- MT62xx-chips fungerer som **baseband-processorer**
- Håndterer **GSM / GPRS / EDGE (2G)** kommunikation
- Integrerer CPU, DSP, hukommelsesinterfaces og periferi på én chip
- Muliggjorde produktion af meget **lavpris-mobiltelefoner**

---

**Arkitektur**
- Typisk:
  - **ARM926EJ-S** RISC-processor (ARM9)
  - Dedikeret **DSP** til signalbehandling
- Designet til lavt strømforbrug og simpel hardwareintegration

---

**Operativsystem**
- Kører MediaTeks **proprietære OS**
- Baseret på **Nucleus RTOS**
- Lukket platform (ingen officiel Linux/Android-support)

---

**Funktioner**
Afhængigt af model kunne chips understøtte:
- GSM tale og SMS
- GPRS/EDGE data
- Kamera, lyd og simpel grafik
- GPS (via eksternt modul)
- Nogle modeller (fx **MT6235**) understøttede:
  - multimedieafspilning
  - analog TV-modtagelse/optagelse  
  (sjældent uden for det asiatiske marked)

---

**Eksempler på modeller**
- MT6229  
- MT6230  
- MT6235  

Disse chips blev brugt i:
- feature phones
- GPS-trackere
- billige IoT-/telemetri-enheder
- embedded GSM-produkter

---

### Nutidig kontekst
MediaTek har siden bevæget sig videre til mere avancerede platforme som
**Helio** og **Dimensity**, der anvendes i moderne smartphones og tablets.

MT62xx-serien repræsenterer i dag:
- en **ældre generation af mobilteknologi**
- men er stadig relevant for:
  - reverse engineering
  - embedded learning
  - analyse af legacy 2G-enheder
 
    ## MediaTek (MTK) MT62xx Series – Resolved Technical Overview

### Summary
The **MediaTek MT62xx series** represents a family of controller and
baseband System-on-a-Chip (SoC) solutions designed primarily for
**feature phones** and low-cost GSM devices.

These chips were widely used before the smartphone era and formed the
technical foundation for many affordable mobile phones, GPS trackers,
and embedded GSM products.

---

## MediaTek CPU Families (Mobile Overview)

MediaTek mobile SoCs historically fall into three major families:

1. **MT62xx series** – Feature phones and embedded GSM devices  
2. **MT65xx series** – Smartphones (Android era)  
3. **MT83xx series** – Tablets and flat-panel devices  

This document focuses on the **MT62xx series**.

---

## MT62xx Series – Key Characteristics

### Purpose
- Designed for **GSM / GPRS / EDGE (2G)** communication
- Integrated **baseband processor**
- Optimized for:
  - low cost
  - low power consumption
  - high functional integration
- Widely adopted in China and emerging markets

---

### Architecture
Depending on model, MT62xx chips use:

- **ARM7**, **ARM9**, or **ARM11** CPU cores
- Instruction sets:
  - ARMv5T
  - ARMv6L
- Dedicated **DSP** for signal processing
- Integrated peripherals (audio, display, camera, SIM, GPIO)

---

### Operating System
- Runs MediaTek’s **proprietary OS**
- Based on **Nucleus RTOS**
- Closed platform (no official Linux or Android support)

---

## Design Philosophy (Important Insight)

MTK did **not** pursue raw CPU performance as the main goal.

Instead, MT62xx chips focused on:
- **feature completeness**
- **power efficiency**
- **low BOM cost**
- **long standby time**

This meant that even low-end chips could deliver:
- advanced UI effects
- multimedia features
- long battery life
- extensive phone functionality

---

## Examples by Architecture

### ARM7 (e.g. MT6250)
- Clock ~260 MHz
- Extremely low power consumption
- Very low RF radiation
- Capable of running Nucleus-based “smart-like” UI
- Representative devices:
  - Lenovo MA309

---

### ARM9 (e.g. MT6268)
- Improved data throughput
- Could handle:
  - higher GSM data rates
  - Wi-Fi (external)
  - early 3G data handling (via modem integration)
- Representative devices:
  - Lenovo I62
  - Lenovo P717
  - Lenovo P650WG

---

### ARM11 (e.g. MT6276)
- Highest-end MT62xx class
- Near-smartphone experience
- Advanced UI and software extensions
- Full 3D graphical interfaces
- Representative concept devices:
  - Lenovo ZK990

---

## Power Efficiency as a Competitive Advantage

One of MTK’s strongest advantages was **power management**.

In many cases:
- MTK designs consumed **significantly less power**
- Standby time was often superior to competing Qualcomm solutions

This design philosophy later influenced MTK’s Android-era chips, where:
- ultra-long standby
- USB-OTG
- extended peripherals
became selling points.

---

## Historical Importance

The MT62xx series demonstrates that:
- feature phones were not “weak”
- careful system integration can outperform brute-force hardware
- long battery life and usability often matter more than peak performance

---

## Modern Context
MediaTek has since moved on to modern platforms such as:
- **Helio**
- **Dimensity**

However, MT62xx chips remain relevant today for:
- reverse engineering
- embedded systems learning
- legacy GSM device analysis
- understanding early mobile SoC design

---

## Status
🟢 Legacy platform  
🟢 Technically robust for its time  
🟡 Educational and reverse-engineering value  
🔴 Obsolete for modern cellular networks (2G dependency)

