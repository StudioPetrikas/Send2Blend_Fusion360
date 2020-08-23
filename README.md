# "Send2Blend" Autodesk Fusion360 add-in

"Send2Blend" Autodesk Fusion360 add-in was creted to work in tandem with ["Send2Blend" Blender plugin.](https://github.com/StudioPetrikas/Send2Blend_Blender)

*Disclaimer: 
The code has been pieced together by a beginner coder. There will be coding mistakes, logic mistakes, naming mistakes and various other problems with the code. Please be patient and feel free to make modifications to the code as you see fit.*

# Attribution
  - App wrapper: "Apper" for Fusion360 by [Patrick Rainsberry](https://twitter.com/prrainsberry)
  - Huge chunks of code borrowed from ExportIt by WilkoV [Fusion360 ExportIt](https://github.com/WilkoV/Fusion360_ExportIt)

# Installation 
1. Download the [current release of Send2Blend for Fusion360](https://github.com/StudioPetrikas/Send2Blend_Fusion360/files/5112152/Send2Blend_Fusion360_v1.0.zip)
2. Extract the folder
3. Open Autodesk Fusion360
4. Navigate to Tools tab and click Scripts and Add-ins (Shift+S)
5. Go to Add-ins Tab
6. Click the green + sign next to "My Add-Ins"
7. Copy the extracted "Send2Blend" folder to the opened window
8. Select the copied "Send2Blend" folder and hit Open
9. Make sure "Run on Startup" is ticked
10. Restart Fusion360

*Highly Recommended: After the installation, navigate to "Tools" panel, click on Add-Ins drop down, and assingn a new keyboard shortcut for "Send To Blender". I personaly prefer CMD+B*

# Usage
1. Create a model as usual
2. Make sure to name your components appropiately. Once named, you should avoid renaming at all costs; Names are the only way to link objects with Blender (so far)
3. T-Splines, Surfaces, Meshes and bodies outside compoenets will not be exported. Convert them to B-Rep bodies for export if neccessary and make sure to create a component for any "loose" bodies.
4. Save and name your project
5. Click the Blender Icon in "Tools" panel, or hit your assigned Keyboard Shortcut.

Full workflow (Including Blender) can be found in this Youtube Video

# How it Works
1. Checks if Folder "S2B_Temp" exists on User/Desktop; Creates a Folder if it doesn't, deletes all files in the folder if it does.
2. Creates a temporary document and copies all occurrences to that temporary document.
3. Exports all occurrences to S2B_Temp folder in STL format, "High" refinement. 
4. Names the STL files: removes version, replaces spaces with dashes where appropriate.
5. Upon closing Fusion360 the S2B_Temp folder is removed.



