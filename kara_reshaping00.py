# generate_kara_masks.py
import os, numpy as np
import geopandas as gpd
from shapely.geometry import Point
from icenet.data.sic.mask import Masks

hemi = "north"                          # Kara è nell’emisfero nord
mask_dir = f"./data/masks/{hemi}/masks" # cartella già usata da IceNet
os.makedirs(mask_dir, exist_ok=True)

#  Leggi lo shapefile e proiettalo sul CRS EASE‑2‑North (EPSG:6931)
kara = gpd.read_file("Kara_sea_iho.zip").to_crs("EPSG:6931")
kara_poly = kara.unary_union            # (multi)poligono unico

# ➋ Costruisci il reticolo delle 432 × 432 celle IceNet
m = Masks(north=True, south=False)
xc, yc = np.meshgrid(m.xc, m.yc, indexing="xy")   # coordinate proiettate (EPSG:6931)

# ➌ Verifica se il centro di ogni cella cade nel poligono Kara
flat = [kara_poly.contains(Point(x, y)) for x, y in zip(xc.ravel(), yc.ravel())]
kara_mask = np.array(flat, dtype=bool).reshape(m._shape)

# ➍ Interseca con le maschere mensili esistenti e sovrascrivi
for mm in range(1, 13):
    p = os.path.join(mask_dir, f"active_grid_cell_mask_{mm:02d}.npy")
    base_mask = np.load(p)
    np.save(p, base_mask & kara_mask)   # 1 = “cella valida del Kara”
print("Maschere Kara pronte.")
