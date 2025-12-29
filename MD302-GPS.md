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


📌 MediaTek MT62xx-serien (verificeret info)
📍 Generel beskrivelse

MT62xx-serien er en ældre familie af GSM/GPRS baseband SoC’er fra MediaTek, brugt i feature phones og enkle mobil-/GSM-enheder. 
Full Real

📍 Én af chipsene: MT6235

Processor i mange kinesiske mobiltelefoner

Indeholder en ARM926EJ-S RISC CPU og en DSP

Brugte proprietært MediaTek-OS baseret på Nucleus RTOS 
Wikipedia

Dette understøtter, at MT62xx-platformen har en rigtig CPU + modem integreret, ikke bare en simpel mikrokontroller.

📍 Et eksempel på en baseband chip: MT6261

GSM/GPRS baseband processor til lavpris mobiltelefoner og IoT-brug

Har SIM-interface (SIM_IO, SIM_CLK, SIM_RST etc.) designet direkte i silikone

Interfaces som UART, GPIO og antenne indgår normalt i pakken 
Jotrin Electronics

Det matcher, at din MD302 har SIM-busadgang via SIM pins osv.

📍 MT62xx-chips i historisk kontekst

Serien blev brugt bredt fra omkring midten af 2000’erne til begyndelsen af 2010’erne. 
Wikipedia

Serien inkluderer mange modeller (MT6205, MT6216, MT6223, MT6235 osv.) med GSM/GPRS modem klassificeret som baseband.

🧠 Hvad denne dokumentation betyder for dit projekt

Baseret på ovenstående kilder kan du med stor sikkerhed sige:

✔️ MD302 bruger en ægte MediaTek baseband chip fra MT62xx-æraen
✔️ Den har ARM-CPU + DSP + modem på samme chip
✔️ Firmwaren kører på den integrerede processor der håndterer GSM/2G
✔️ Dette er konsistent med det du så i UART-bootloggen

📘 Eksempel på henvendelse du kan bruge i din tekstfil / README

The MD302 GPS tracker uses a MediaTek baseband SoC from the MT62xx series, a family of GSM/GPRS telecom processors used in feature phones and embedded devices in the 2000s–2010s. These chips include an ARM926EJ-S RISC processor with an integrated GSM/GPRS modem and DSP, running MediaTek’s proprietary OS based on Nucleus RTOS. One documented example is the MT6235, featuring an ARM926EJ-S core and DSP subsystem. Another is the MT6261MA, which provides GSM/GPRS connectivity and contains UART, SIM and RF interfaces on die. 
Wikipedia
+1

🧾 Henvendelser (korte facts du kan cite)

Feature phone-SoC

MediaTek MT62xx chips were used in mobile phones and embedded GSM devices, typically integrating baseband modem and processor. 
Full Real

MT6235 processor

The MT6235 is part of the MT62xx series with an ARM926EJ-S RISC CPU and DSP subsystem. 
Wikipedia

MT6261MA baseband IC

The MT6261MA is a GSM/GPRS baseband processor providing core communications functionality and peripheral interfaces such as UART and SIM. 
Jotrin Electronics


Her er en kort, skarp TL;DR, som opsummerer alt det vi nu ved – klar til README, GitHub eller deling:

TL;DR – Hvad ved vi nu (MD302 / MediaTek MT62xx)

Enheden (MD302) er fuldt funktionsdygtig hardwaremæssigt

Den er baseret på en MediaTek MT62xx-serie baseband SoC

ARM9/ARM11-klasse CPU + DSP

Integreret 2G GSM/GPRS modem

Proprietært MediaTek-OS baseret på Nucleus RTOS

Bootloader og firmware virker korrekt

MediaTek Bootloader V005 starter

Firmware loader og kører stabilt

UART-log bekræfter normal boot og drift

SIM-detektion fungerer

SIM CARD -------- OK

SIM-holder, PIN og kontakt er i orden

Problemet er udelukkende netværk

GSM Signal -------- NG

NO SERVICE

Enheden er 2G GSM-only

Moderne SIM-kort (data/LTE/VoLTE) har typisk ikke 2G aktiveret

Der er ingen hardwarefejl

Batteri (VBAT ~3.4–3.6 V) er OK

GPS, G-sensor, SOS m.m. rapporteres NG kun fordi GSM mangler

Konklusion

Enheden kan kun fungere med et SIM med aktiv 2G GSM

Alternativt kan den bruges som:

UART / embedded learning device

Reverse-engineering-case

Legacy GSM/GPS-studie

Projektets værdi

Bekræfter klassisk MT62xx-arkitektur

Dokumenterer MediaTek boot-flow

Relevans for embedded / legacy-analyse i 2025

Perfekt fund. Det her er præcis den manglende “rygende pistol”, som binder dit MD302-arbejde sammen med konkret, offentlig reverse-engineering af MT62xx-baserede implants.

Her er en stram TL;DR, som du kan bruge direkte i dit repo (fx RELATED_RESEARCH.md eller som reference-afsnit).

TL;DR – S8 Data Line Locator (MT6261) & relevans for MT62xx / MD302

S8 Data Line Locator er et lavpris GSM-spion-/tracking-implant skjult i et USB-kabel

Baseret på MediaTek MT6261(MA) – samme MT62xx-familie som MD302-trackere

Kører MediaTek proprietært OS baseret på Nucleus RTOS

Bruger 2G GSM (850/900/1800/1900 MHz) – ingen GPS, kun celle-lokation

Bekræftede tekniske facts

MTK Bootloader V005 (samme banner som i dit MD302-projekt)

UART giver boot-log, men ingen interaktiv shell

USB D+/D- går direkte til MTK-SoC (Preloader / Download Mode)

Enheden identificerer sig som:

ID 0e8d:0003 MediaTek Inc. MT6227 phone


➡️ MTK Preloader-adgang = muligt firmware-dump

Firmware & flash-analyse

ROM og SPI-flash kan dumpes

Flash indeholder:

Nucleus RTOS-strenge

MediaTek HAL / bootloader-kilde-paths

Konfigurationsdata (IMSI, controlling phone number)

Hardcoded references til gpsui.net

Flash er blok-beskyttet → skrivning svær / ikke løst

Netværk & overvågning

Enheden:

sender data via GPRS uden tydelig brugeroplysning

benytter gpsui.net som backend

gpsui.net:

gemmer lokationshistorik

tillader remote commands

havde dokumenterede IDOR-sårbarheder

Brugeren informeres ikke om login-credentials eller datalagring

➡️ Massiv privacy- og sikkerhedsrisiko

Skjulte SMS-kommandoer (uddrag)

Fundet direkte i flash:

dw / loc – lokation

1111 / 0000 – lydaktiveret callback

server – server adresse (delvist)

aqb – udleverer web-login credentials

*3646655* – version query

*reboot* – reboot

➡️ Firmware deles på tværs af flere tracker-produkter (features der ikke findes på hardware)

Relevans for dit MD302-projekt

Dette arbejde bekræfter uafhængigt:

MT62xx-baserede trackere:

har samme bootloader

samme OS-stack (Nucleus + MTK HAL)

samme netværksarkitektur

“Phone-home” adfærd er design-mæssig, ikke tilfældig

2G-afhængighed forklarer NO SERVICE i moderne net

➡️ Dit MD302-fund er teknisk konsistent med kendte MT62xx implants

Overordnet konklusion

MT62xx-baserede low-cost trackere er funktionelt robuste,
men designet med skjult remote control, central logging og svag sikkerhed.
De er uegnede til brug i 2025 uden fuld kontrol over firmware og netværk.

