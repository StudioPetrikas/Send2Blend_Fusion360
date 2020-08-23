# "Send2Blend" Autodesk Fusion 360 add-in

"Send2Blend" Autodesk Fusion 360 add-in was creted to work in tandem with ["Send2Blend" Blender plugin.](https://github.com/StudioPetrikas/Send2Blend_Blender)

*Disclaimer: 
The code has been pieced together by a beginner coder. There will be coding mistakes, logic mistakes, naming mistakes and various other problems with the code. Please be patient and feel free to make modifications to the code as you see fit.*

# Attribution
  - App wrapper: "Apper" for Fusion 360 by [Patrick Rainsberry](https://twitter.com/prrainsberry)
  - Huge chunks of code borrowed from ExportIt by WilkoV [Fusion 360 ExportIt](https://github.com/WilkoV/Fusion360_ExportIt)

# Installation (MacOSX)
1. Download the [current release of Send2Blend for Fusion 360](https://github.com/StudioPetrikas/Send2Blend_Fusion360/files/5112152/Send2Blend_Fusion360_v1.0.zip)
2. Open Autodesk Fusion 360
3. Extract the folder
3. Hit Command + Space
4. Copy / Paste this location: ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns
5. Copy "Send2Blend" folder to this location
6. In Fusion 360, navigate to Tools tab.
7. Click Add-Ins (Shift + S)
8. Navigate to Add-Ins tab
9. Find "Send2Blend"
10. Make sure "Run on Startup" is ticked
11. Restart Fusion 360

Full installation proccess can also be found in this Youtube Video.

*Highly Recommended: After the installation, navigate to "Tools" panel, click on Add-Ins drop down, and assingn a new keyboard shortcut for "Send To Blender". I personaly prefer CMD+B*

# Usage
1. Create a model as usual
2. Make sure to name your components appropiately. Once named, you should avoid renaming at all costs; Names are the only way to link objects with Blender (so far)
3. T-Splines, Surfaces, Meshes and bodies outside compoenets will not be exported. Convert them to B-Rep bodies for export if neccessary and make sure to create a component for any "loose" bodies.
4. Save and name your project
5. Click the Blender Icon in "Tools" panel, or hit your assigned Keyboard Shortcut.

Full workflow (Including Blender) can be found in [this Youtube Video.](https://www.youtube.com/watch?v=HfhuiakfqBQ)

# How it Works
1. Checks if Folder "S2B_Temp" exists on User/Desktop; Creates a Folder if it doesn't, deletes all files in the folder if it does.
2. Creates a temporary document and copies all occurrences to that temporary document.
3. Exports all occurrences to S2B_Temp folder in STL format, "High" refinement. 
4. Names the STL files: removes version, replaces spaces with dashes where appropriate.
5. Upon closing Fusion360 the S2B_Temp folder is removed.



