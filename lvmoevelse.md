# 🧪 LVM Øvelse: Simulér fuld root og red systemet (Debian + virt-manager)

Denne øvelse demonstrerer et **realistisk LVM-fejlscenarie**:
> Root-filsystemet (`/`) bliver næsten fuldt – og reddes live med LVM.

Testet på:
- Debian 12
- LVM2
- virt-manager (KVM / QEMU)

---

## 🎯 Mål med øvelsen

Efter denne øvelse kan du:

- Forstå forskellen på **Logical Volume** og **filesystem**
- Simulere en **kritisk fuld root**
- Redde systemet **uden reinstall**
- Forstå **snapshot-begrænsninger**
- Håndtere snapshot-merge korrekt

---

## 🧠 Forudsætninger

- System installeret med LVM
- Root (`/`) ligger på et Logical Volume
- Volume Group har **ledig plads**
- Root-adgang (`sudo`)

---

## 📊 Startstatus (eksempel)

```bash
Del 1 – Simulér fuld root
Fyld root kontrolleret
sudo fallocate -l 7G /bigfile
df -h /

Pres systemet yderligere
sudo fallocate -l 600M /bigfile2
df -h /


Typisk resultat:

/ > 95 %

apt, logs og services begynder at fejle

🧯 Del 2 – Midlertidig redning
sudo rm /bigfile2
df -h /


Systemet virker igen – men root er stadig for lille.

🛠️ Del 3 – RIGTIG løsning med LVM
Udvid root (blokniveau)
sudo lvextend -L +5G /dev/debianvm-vg/root

Udvid filesystem (ext4)
sudo resize2fs /dev/debianvm-vg/root


Kontrollér:

df -h /

📸 Del 4 – Snapshot-fælde (vigtig læring)

Hvis der findes et snapshot af root:

Snapshot origin volumes can be resized only while inactive

Forklaring

Et aktivt snapshot låser origin-LV

Resize er blokeret for at beskytte data

🔁 Snapshot merge-situation

Hvis snapshot er sat til merge:

Can't remove merging snapshot logical volume

Løsning
sudo reboot


Snapshot-merge kan kun færdiggøres ved boot.

Efter reboot:

sudo lvs


Snapshot er væk, systemet er stabilt igen.

✅ Slutstatus (eksempel)
df -h /
df -h /home

/      18G  12G  5.4G  68%
/home  15G   27M   14G   1%

🧠 Vigtige læringspunkter

lvextend ≠ resize2fs

Filesystem ved intet om ny plads før resize

Snapshots låser resize af origin

Snapshot-merge kræver reboot

LVM kan redde et system uden nedetid
