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
