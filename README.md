# Banana for Scale

![icon](resources/Banaan/64x64.png)

[English](#english) · [Nederlands](#nederlands)

## English

A Fusion add-in that adds a single button with a banana icon. Click it and a life-size banana (~19 cm long, ~3.7 cm thick) appears in your design, so you can see at a glance how big your model really is.

### Installation

1. Copy this folder to `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\Banaan` (Windows) or `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/Banaan` (Mac).
2. In Fusion: **Utilities → Add-Ins** (`Shift+S`), **Add-Ins** tab, select **Banaan** and click **Run**. Turn on **Run on Startup**.

### Usage

The **Banaan voor schaal** button is under **Create** in the Part environment, and in the Insert/Assemble panels of the Assembly environment.

- **Part design**: the banana becomes a body in the part.
- **Assembly/Hybrid design**: the banana gets its own component.
- Each new banana is placed 6 cm next to the previous one.

You can change the size and curvature at the top of `Banaan.py` (`SECTIONS`, `ARC_RADIUS`, `ARC_SWEEP`).

## Nederlands

Fusion add-in die één knop met een banaan-icoon toevoegt. Klik erop en er verschijnt een banaan op ware grootte (~19 cm lang, ~3,7 cm dik) in je ontwerp, zodat je meteen ziet hoe groot je model is.

### Installeren

1. Kopieer deze map naar `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\Banaan` (Windows) of `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/Banaan` (Mac).
2. In Fusion: **Utilities → Add-Ins** (`Shift+S`), tabblad **Add-Ins**, kies **Banaan** en klik **Run**. Zet **Run on Startup** aan.

### Gebruik

De knop **Banaan voor schaal** staat onder **Create** in de Part-omgeving, en in de Insert/Assemble-panelen van de Assembly-omgeving.

- **Part-ontwerp**: de banaan wordt een body in het onderdeel.
- **Assembly/Hybrid-ontwerp**: de banaan krijgt een eigen component.
- Elke volgende banaan komt 6 cm naast de vorige.

Afmetingen en kromming pas je aan bovenaan in `Banaan.py` (`SECTIONS`, `ARC_RADIUS`, `ARC_SWEEP`).
