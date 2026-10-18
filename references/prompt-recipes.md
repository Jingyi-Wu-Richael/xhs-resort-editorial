# Prompt Recipes

Use these as adaptable structures. Replace bracketed fields and remove irrelevant phrases. Favor one coherent paragraph over a pile of aesthetic tags.

## Prompt Frame

Build prompts in this order:

1. Output and medium: 3:4 portrait luxury editorial photograph
2. Hero and action: product plus one human or object ritual
3. Physical setting: specific materials and depth layers
4. Light: direction, hardness, warm/cool relationship
5. Palette: one neutral, two atmosphere colors, one anchor
6. Composition and camera: viewpoint, lens family, product position and scale
7. Surface treatment: texture, grain, contrast, natural skin or material rendering
8. Exclusions: concrete errors that would invalidate the result

## Shared Base Direction

```text
3:4 portrait luxury resort editorial photograph, contemporary Mediterranean summer with a subtle 1970s magazine sensibility, hard warm afternoon sunlight from camera left and cool sky bounce, tactile limestone, natural skin and material texture, crisp product edges, moderate depth of field, restrained film grain, polished commercial art direction without looking sterile
```

Do not paste the base direction unchanged into every frame. Keep the same light and finish, then vary the action, distance, and subject.

## A. Lifestyle Hero

```text
Create a 3:4 portrait luxury editorial scene for [PRODUCT]. An adult woman in [SIMPLE WHITE OR STRIPED LOOK] relaxes beside [POOL / SEA TERRACE], performing [READING / POURING A DRINK / FASTENING JEWELRY] rather than posing for camera. Crop the face partially with [BOOK / SUNGLASSES / HAT] so the image feels editorial, not influencer-led. Place the exact [PRODUCT] on a sunlit [LIMESTONE / OAK] surface in the lower foreground, occupying about 15% of the frame and fully readable. Add only [SENSORY PROP] and [CULTURAL PROP]. Hard warm sunlight from camera left creates clean diagonal shadows; water or sky adds a cool aqua bounce. Palette: warm ivory, limestone, pool aqua, and [BRAND ANCHOR COLOR] repeated in three small points. 50 mm editorial perspective, f/5.6 visual depth, crisp texture, subtle film grain. No mobile UI, watermark, fake lettering, floating objects, warped package, distorted hands, extra fingers, direct-to-camera posing, heavy blur, or orange-teal grading.
```

## B. Editorial Still Life

```text
Create a 3:4 portrait commercial still life for [PRODUCT] on [OAK PARQUET / LIMESTONE / STRIPED LINEN], viewed from a controlled 35-degree overhead angle. Use [LARGE CULTURAL OBJECT] as the largest anchor, arrange the product group off-center in the middle third, and place one or two smaller objects just outside the group to create an editorial diagonal. A hard rectangular beam of late-afternoon sun crosses the frame from upper right to lower left, revealing wood, paper, metal, and cosmetic textures. Repeat [BRAND COLOR] in the package, one prop, and one small printed detail. Warm ivory and sunlit oak dominate, balanced by one cool reflection. 50 mm still-life photography, crisp product geometry, natural shadow falloff, restrained film grain. No perfectly centered ecommerce layout, random clutter, fake brand text, duplicate product, levitation, plastic CGI sheen, or crushed shadows.
```

## C. Architectural Poster Wall

Do this in three stages.

### Stage 1: Six Tiles

Generate six square tiles using one locked palette and sun direction:

1. Product on a bold fabric or striped ground
2. Cropped human use moment
3. Macro sensory texture
4. Simple color-and-title graphic, built with a layout tool
5. Product plus environment
6. Accessory or footwear detail

Each photographic tile should use:

```text
Square luxury campaign photograph for [PRODUCT OR BRAND], [SUBJECT AND ACTION], direct warm Mediterranean sunlight from upper left, [PALETTE], crisp commercial texture, restrained film grain, composition designed to work inside a six-panel campaign grid, no text, no watermark, no duplicate objects, no distorted anatomy or packaging
```

### Stage 2: Assemble

Use a Python executable with Pillow. In Codex desktop, use the bundled Python returned by `load_workspace_dependencies`:

```bash
<workspace-python> scripts/compose_grid.py \
  --inputs tile-01.png tile-02.png tile-03.png tile-04.png tile-05.png tile-06.png \
  --output poster-grid.png --cols 2 --rows 3 --width 1000 --height 1500 --gap 24 \
  --background '#D8CCBC'
```

### Stage 3: Place On Wall

```text
Place the supplied finished 2x3 campaign artwork as one perfectly flat printed panel on a warm limestone facade. Preserve every tile, gutter, color, and edge exactly. Add shallow classical wall molding on the left and a clean real brand wordmark beneath the panel. Hard afternoon sun comes from upper left and casts a subtle physically correct panel shadow. 3:4 portrait architectural campaign photograph, warm stone, restrained contrast, no pedestrians, no warped grid, no redrawn text, no additional posters, no mobile UI.
```

## D. Campaign Mosaic

Create eight square photographic tiles: wide environment, product still life, human torso or hands, macro product texture, ritual action, accessory detail, sensory prop, and quiet closing atmosphere. Keep the center reserved for a title card.

```bash
<workspace-python> scripts/compose_grid.py \
  --inputs tile-01.png tile-02.png tile-03.png tile-04.png tile-05.png tile-06.png tile-07.png tile-08.png \
  --output campaign-mosaic.png --cols 3 --rows 3 --width 1200 --height 1200 \
  --center-label 'BRAND' --center-bg '#AFCADC' --center-fg '#8F3433'
```

Place the most distant environment frames in corners. Keep adjacent tiles different in subject scale. If the title needs exact brand typography, create a blank center tile with the script and replace or typeset it in a design tool.

## E. Product Asset Compositing

When a real cutout or packshot exists:

1. Generate the scene with a simple placeholder matching the product's silhouette and footprint.
2. Remove the placeholder and composite the supplied product at the same perspective.
3. Add a tight contact shadow plus a broader, softer cast shadow in the locked sun direction.
4. Match highlight warmth, shadow coolness, sharpness, grain, and reflected environment color.
5. Check label geometry at 100% and thumbnail size.

Do not ask the image model to redraw a real logo or a complex jewelry setting.

## Continuity Block For A Series

Append a compact continuity block to every frame prompt:

```text
Series continuity: same hard sunlight from camera left, same warm ivory and [COASTAL COLOR] base, same [ANCHOR COLOR], same 50 mm lens family, same [RECURRING MATERIAL OR PROP], consistent product scale and label fidelity.
```

## Revision Directions

- Too generic: make the product's use ritual explicit and repeat its brand color in three physical details.
- Too beige: introduce sky or pool blue as a real environmental counterpoint; do not tint the whole image.
- Too sterile: add one tactile cultural prop and an imperfect human action, while preserving product clarity.
- Too influencer-like: crop identity, remove direct eye contact, and shift attention to gesture, material, and product.
- Product inaccurate: stop regenerating the package and composite the real packshot.
- Grid irregular: generate the tiles individually and use `compose_grid.py`.
- Text broken: generate a clean blank area and typeset the copy afterward.
