# wot-vt-converter
convert 3dsmax2012-generated obj format into WorldofTanks vt file, or extract bsp from legacy BigWorld primitives file.

python 2.7 script


* obj2vt.py is recommended, it generates a more compact vt file.
* p2vt.py will extract bsp from primitives created by 3dsmax bigworld model exporter plugin, if there is a bsp section in it. However because the way bsp is stored, all shared verts are split for each adjacent faces, causing massive duplicates.

---

## obj2vt.py  
   * Convert 3dsmax2012-generated obj format into WorldofTanks V1.x vt file. 
   * There should be only one entity in the obj file, as only the first 'g' entity is recognized by this script. If you split the collision model into pieces in 3dsmax project file, __merge them before exporting to obj__. 
   * The model in the scene should be facing scene __'back'__, with 'flip YZ-axis' option in obj export parameter. 
   * __BOTH__ display and system unit of 3dsmax set to metric meter. 
   * obj file generated by different version or different software could cause unpredictable error, for obj format has many different ways to describe the same data.
### [usage]
 python obj2vt.py input.obj  
 python obj2vt.py *.obj  
 
 ---
 
 ## p2vt.py  
* Extract bsp model from primitives file generated by bigworld 3dsmax model exporter plugin, if there is a bsp section in the file.
* aka it only works for primitives made by modders. Stock wot primitives are not supported, since they already stripped their bsp section.
* Tested with bigworld 1.91, bigoworld indie 2.1
* This script will not remove the bsp section from the input primitives.
* Because the way bsp is stored, all shared verts are split for each adjacent faces, creating a much larger vt file.
### [usage]
   python p2vt.py input.primitives  
   python p2vt.py *.primitives  
   python p2vt.py *.primitives_processed  
     
 
 
