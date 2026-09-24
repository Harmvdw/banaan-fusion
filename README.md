# Banaan voor schaal

Fusion add-in die één knop met een banaan-icoon toevoegt. Klik erop en er verschijnt een banaan op ware grootte (~19 cm lang, ~3,7 cm dik) in je ontwerp, zodat je meteen ziet hoe groot je model is.

![icoon](resources/Banaan/64x64.png)

## Installeren

1. Kopieer deze map naar `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\Banaan` (Windows) of `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/Banaan` (Mac).
2. In Fusion: **Utilities → Add-Ins** (`Shift+S`), tabblad **Add-Ins**, kies **Banaan** en klik **Run**. Zet **Run on Startup** aan.

## Gebruik

De knop **Banaan voor schaal** staat onder **Create** in de Part-omgeving, en in de Insert/Assemble-panelen van de Assembly-omgeving.

- **Part-ontwerp**: de banaan wordt een body in het onderdeel.
- **Assembly/Hybrid-ontwerp**: de banaan krijgt een eigen component.
- Elke volgende banaan komt 6 cm naast de vorige.

Afmetingen en kromming pas je aan bovenaan in `Banaan.py` (`SECTIONS`, `ARC_RADIUS`, `ARC_SWEEP`).
