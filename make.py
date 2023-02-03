import os
import uuid
import json
from pathlib import Path
import shutil

skin_preset = {
  "localization_name": "",
  "geometry": "geometry.humanoid.customSlim",
  "texture": "skin.png",
  "cape": "",
  "type": "free"
}

def make_skin_preset(src):
    imp = skin_preset.copy()
    imp["localization_name"] = ".".join(src.split(".")[:-1])
    imp["cape"] = src
    return imp

title = input("Title of your pack: ")
description = input("Description of your pack: ")

path = Path(__file__).parent
out_dir = "out"
out_path = f"{path}/{out_dir}"

if os.path.exists(out_path):
    shutil.rmtree(out_path)
shutil.copytree(f"{path}/preset", out_path)
shutil.copy(f"{path}/skin.png", f"{out_path}/skin.png")

for fn in os.listdir(f"{path}/capes"):
    shutil.copy(f"{path}/capes/{fn}", f"{out_path}/{fn}")

with open(f"{out_path}/skins.json", "r+") as f:
    json_skins = json.load(f)
    # print(json_skins)
    for cape in os.listdir(f"{path}/capes"):
        imp = make_skin_preset(cape)
        # print(imp)
        json_skins["skins"].append(imp)
    f.seek(0)
    f.truncate()
    f.seek(0)
    json.dump(json_skins, f, indent=6)

with open(f"{out_path}/manifest.json", "r+") as f:
    json_manifest = json.load(f)
    json_manifest["header"]["uuid"] = str(uuid.uuid4())
    for i in range(len(json_manifest["modules"])):
        json_manifest["modules"][i]["uuid"] = str(uuid.uuid4())
    # print(json_manifest)
    f.seek(0)
    f.truncate()
    f.seek(0)
    json.dump(json_manifest, f, indent=6)

shutil.make_archive(out_path, 'zip', f"{out_path}/")
os.rename(f"{out_path}.zip", f"{out_path}/{out_path.split('/')[-1]}.mcpack")
