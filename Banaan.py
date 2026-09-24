"""Banaan voor schaal - Fusion add-in.

Voegt een knop met een banaan-icoon toe aan Ontwerp > Maken. Een klik plaatst
een banaan van ware grootte (~19 cm lang, ~3,7 cm dik) als nieuw component.
"""
import math
import os
import traceback

import adsk.core
import adsk.fusion

CMD_ID = 'harmBanaanVoorSchaal'
CMD_NAME = 'Banaan voor schaal'
CMD_TOOLTIP = 'Plaats een banaan op ware grootte in je ontwerp.'
WORKSPACE_ID = 'FusionSolidEnvironment'
# Part-omgeving: Maken. Assembly-omgeving heeft geen Maken-paneel, dus ook in
# elk paneel waarvan de naam op invoegen/assembleren wijst.
PANEL_ID = 'SolidCreatePanel'
EXTRA_PANEL_WOORDEN = ('Insert', 'Assemble', 'Assembly')
RESOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'Banaan')

# Fusion rekent intern in centimeters.
ARC_RADIUS = 15.0                  # kromming van de banaan
ARC_SWEEP = math.radians(73)       # booglengte ~19 cm
# (positie langs de boog 0..1, straal van de doorsnede in cm)
SECTIONS = [
    (0.00, 0.40),   # steeltje
    (0.07, 0.45),
    (0.16, 1.20),
    (0.32, 1.75),
    (0.50, 1.85),
    (0.68, 1.75),
    (0.84, 1.25),
    (0.95, 0.60),
    (1.00, 0.25),   # puntje
]
BANAAN_GEEL = (255, 225, 53)

_app = None
_ui = None
_handlers = []


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        try:
            on_execute = CommandExecuteHandler()
            args.command.execute.add(on_execute)
            _handlers.append(on_execute)
        except Exception:
            _ui.messageBox('Fout:\n{}'.format(traceback.format_exc()))


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        try:
            maak_banaan()
        except Exception:
            _ui.messageBox('Banaan mislukt:\n{}'.format(traceback.format_exc()))


def maak_banaan():
    design = adsk.fusion.Design.cast(_app.activeProduct)
    if not design:
        _ui.messageBox('Open eerst een ontwerp in de Design-werkruimte.')
        return

    # Construction planes langs een pad werken alleen met tijdlijn.
    if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType

    root = design.rootComponent

    # Elke nieuwe banaan komt 6 cm naast de vorige te liggen.
    aantal = sum(1 for c in design.allComponents for b in c.bRepBodies if b.name.startswith('Banaan'))
    dx = aantal * 6.0

    # Part-ontwerp: geen subcomponenten toegestaan, dus de body komt in de root.
    # Assembly/Hybrid: de banaan krijgt een eigen component.
    try:
        is_part = design.designIntent == adsk.fusion.DesignIntentTypes.PartDesignIntentType
    except Exception:
        is_part = False
    if is_part:
        comp = root
    else:
        occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        comp = occ.component
        comp.name = 'Banaan'
        try:
            occ.activate()
        except Exception:
            pass

    # Gebogen hartlijn: een boog die als een glimlach ligt.
    pad_sketch = comp.sketches.add(comp.xYConstructionPlane)
    pad_sketch.name = 'Banaan hartlijn'
    start_hoek = -math.pi / 2 - ARC_SWEEP / 2
    centrum = adsk.core.Point3D.create(dx, ARC_RADIUS, 0)
    start = adsk.core.Point3D.create(dx + ARC_RADIUS * math.cos(start_hoek),
                                     ARC_RADIUS + ARC_RADIUS * math.sin(start_hoek), 0)
    boog = pad_sketch.sketchCurves.sketchArcs.addByCenterStartSweep(centrum, start, ARC_SWEEP)

    # Een cirkel per doorsnede, loodrecht op de hartlijn.
    profielen = []
    for t, straal in SECTIONS:
        plane_input = comp.constructionPlanes.createInput()
        plane_input.setByDistanceOnPath(boog, adsk.core.ValueInput.createByReal(t))
        plane = comp.constructionPlanes.add(plane_input)
        plane.isLightBulbOn = False

        hoek = start_hoek + ARC_SWEEP * t
        punt = adsk.core.Point3D.create(dx + ARC_RADIUS * math.cos(hoek),
                                        ARC_RADIUS + ARC_RADIUS * math.sin(hoek), 0)
        sketch = comp.sketches.add(plane)
        sketch.sketchCurves.sketchCircles.addByCenterRadius(sketch.modelToSketchSpace(punt), straal)
        sketch.isVisible = False
        profielen.append(sketch.profiles.item(0))

    lofts = comp.features.loftFeatures
    loft_input = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    for profiel in profielen:
        loft_input.loftSections.add(profiel)
    loft_input.isSolid = True
    loft_input.centerLineOrRails.addCenterLine(boog)
    try:
        loft = lofts.add(loft_input)
    except Exception:
        # Zonder hartlijn als geleiding lukt het altijd.
        loft_input = lofts.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        for profiel in profielen:
            loft_input.loftSections.add(profiel)
        loft_input.isSolid = True
        loft = lofts.add(loft_input)

    pad_sketch.isVisible = False
    body = loft.bodies.item(0)
    body.name = 'Banaan'
    kleur_geel(design, body)
    if not is_part:
        design.activateRootComponent()


def kleur_geel(design, body):
    """Geef de banaan een gele kleur; lukt dat niet, dan blijft hij grijs."""
    try:
        naam = 'Banaan Geel'
        uiterlijk = design.appearances.itemByName(naam)
        if not uiterlijk:
            basis = None
            for lib in _app.materialLibraries:
                for kandidaat in ('Paint - Enamel Glossy (Yellow)', 'Plastic - Glossy (Yellow)'):
                    try:
                        basis = lib.appearances.itemByName(kandidaat)
                    except Exception:
                        basis = None
                    if basis:
                        break
                if basis:
                    break
            if not basis:
                return
            uiterlijk = design.appearances.addByCopy(basis, naam)
            for prop in uiterlijk.appearanceProperties:
                kleur = adsk.core.ColorProperty.cast(prop)
                if kleur and kleur.value:
                    kleur.value = adsk.core.Color.create(*BANAAN_GEEL, 255)
                    break
        body.appearance = uiterlijk
    except Exception:
        pass


def run(context):
    global _app, _ui
    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        cmd_def = _ui.commandDefinitions.itemById(CMD_ID)
        if not cmd_def:
            cmd_def = _ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_TOOLTIP, RESOURCES)
        on_created = CommandCreatedHandler()
        cmd_def.commandCreated.add(on_created)
        _handlers.append(on_created)

        for panel in banaan_panelen():
            control = panel.controls.itemById(CMD_ID)
            if not control:
                control = panel.controls.addCommand(cmd_def)
            control.isPromoted = True
            control.isPromotedByDefault = True
        schrijf_panel_ids()
    except Exception:
        if _ui:
            _ui.messageBox('Banaan add-in starten mislukt:\n{}'.format(traceback.format_exc()))


def banaan_panelen():
    workspace = _ui.workspaces.itemById(WORKSPACE_ID)
    panelen = []
    for panel in workspace.toolbarPanels:
        if panel.id == PANEL_ID or any(w in panel.id for w in EXTRA_PANEL_WOORDEN):
            panelen.append(panel)
    return panelen


def schrijf_panel_ids():
    """Schrijf alle tabbladen en panelen naar panelen.txt, handig bij problemen."""
    try:
        regels = []
        workspace = _ui.workspaces.itemById(WORKSPACE_ID)
        for tab in workspace.toolbarTabs:
            regels.append('TAB {}  ({})'.format(tab.id, tab.name))
            for panel in tab.toolbarPanels:
                regels.append('    {}  ({})'.format(panel.id, panel.name))
        pad = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'panelen.txt')
        with open(pad, 'w', encoding='utf-8') as f:
            f.write('\n'.join(regels))
    except Exception:
        pass


def stop(context):
    try:
        for panel in banaan_panelen():
            control = panel.controls.itemById(CMD_ID)
            if control:
                control.deleteMe()
        cmd_def = _ui.commandDefinitions.itemById(CMD_ID)
        if cmd_def:
            cmd_def.deleteMe()
        _handlers.clear()
    except Exception:
        if _ui:
            _ui.messageBox('Banaan add-in stoppen mislukt:\n{}'.format(traceback.format_exc()))
