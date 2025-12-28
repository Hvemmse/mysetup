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
df -h /
df -h /home
