<!DOCTYPE html><html><head><meta charset="utf-8"><title>“Send2Blend” Autodesk Fusion360 add-in.md</title><style></style></head><body id="preview">
<h1 class="code-line" data-line-start=0 data-line-end=1><a id="Send2Blend_Autodesk_Fusion360_addin_0"></a>“Send2Blend” Autodesk Fusion360 add-in</h1>
<p class="has-line-data" data-line-start="2" data-line-end="3">“Send2Blend” Autodesk Fusion360 add-in was creted to work in tandem with “Send2Blend” Blender plugin.</p>
<p class="has-line-data" data-line-start="4" data-line-end="6"><em>Disclaimer:<br>
The code has been pieced together by a beginner coder. There will be coding mistakes, logic mistakes, naming mistakes and various other problems with the code. Please be patient and feel free to make modifications to the code as you see fit.</em></p>
<h1 class="code-line" data-line-start=7 data-line-end=8><a id="Attribution_7"></a>Attribution</h1>
<ul>
<li class="has-line-data" data-line-start="8" data-line-end="9">App wrapper: “Apper” for Fusion360 by <a href="https://twitter.com/prrainsberry">Patrick Rainsberry</a></li>
<li class="has-line-data" data-line-start="9" data-line-end="11">Huge chunks of code borrowed from ExportIt by WilkoV <a href="https://github.com/WilkoV/Fusion360_ExportIt">Fusion360 ExportIt</a></li>
</ul>
<h1 class="code-line" data-line-start=11 data-line-end=12><a id="Installation_11"></a>Installation</h1>
<ol>
<li class="has-line-data" data-line-start="12" data-line-end="13">Download the <a href="https://github.com/StudioPetrikas/Send2Blend_Fusion360/files/5112152/Send2Blend_Fusion360_v1.0.zip">current release of Send2Blend for Fusion360</a></li>
<li class="has-line-data" data-line-start="13" data-line-end="14">Extract the folder</li>
<li class="has-line-data" data-line-start="14" data-line-end="15">Open Autodesk Fusion360</li>
<li class="has-line-data" data-line-start="15" data-line-end="16">Navigate to Tools tab and click Scripts and Add-ins (Shift+S)</li>
<li class="has-line-data" data-line-start="16" data-line-end="17">Go to Add-ins Tab</li>
<li class="has-line-data" data-line-start="17" data-line-end="18">Click the green + sign next to “My Add-Ins”</li>
<li class="has-line-data" data-line-start="18" data-line-end="19">Copy the extracted “Send2Blend” folder to the opened window</li>
<li class="has-line-data" data-line-start="19" data-line-end="20">Select the copied “Send2Blend” folder and hit Open</li>
<li class="has-line-data" data-line-start="20" data-line-end="21">Make sure “Run on Startup” is ticked</li>
<li class="has-line-data" data-line-start="21" data-line-end="23">Restart Fusion360</li>
</ol>
<p class="has-line-data" data-line-start="23" data-line-end="24"><em>Highly Recommended: After the installation, navigate to “Tools” panel, click on Add-Ins drop down, and assingn a new keyboard shortcut for “Send To Blender”. I personaly prefer CMD+B</em></p>
<h1 class="code-line" data-line-start=25 data-line-end=26><a id="Usage_25"></a>Usage</h1>
<ol>
<li class="has-line-data" data-line-start="26" data-line-end="27">Create a model as usual</li>
<li class="has-line-data" data-line-start="27" data-line-end="28">Make sure to name your components appropiately. Once named, you should avoid renaming at all costs; Names are the only way to link objects with Blender (so far)</li>
<li class="has-line-data" data-line-start="28" data-line-end="29">T-Splines, Surfaces, Meshes will not be exported. Convert them to B-Rep bodies for export if neccessary</li>
<li class="has-line-data" data-line-start="29" data-line-end="30">Save and name your project</li>
<li class="has-line-data" data-line-start="30" data-line-end="32">Click the Blender Icon in “Tools” panel, or hit your assigned Keyboard Shortcut.</li>
</ol>
<p class="has-line-data" data-line-start="32" data-line-end="33">Full workflow (Including Blender) can be found in this Youtube Video</p>
<h1 class="code-line" data-line-start=34 data-line-end=35><a id="How_it_Works_34"></a>How it Works</h1>
<ol>
<li class="has-line-data" data-line-start="35" data-line-end="36">Checks if Folder “S2B_Temp” exists on User/Desktop; Creates a Folder if it doesn’t, deletes all files in the folder if it does.</li>
<li class="has-line-data" data-line-start="36" data-line-end="37">Creates a temporary document and copies all occurrences to that temporary document.</li>
<li class="has-line-data" data-line-start="37" data-line-end="38">Exports all occurrenced to S2B_Temp folder in STL format, “High” refinement.</li>
<li class="has-line-data" data-line-start="38" data-line-end="39">Names the STL files: removes version, replaces spaces with dashes where appropriate.</li>
<li class="has-line-data" data-line-start="39" data-line-end="40">Upon closing Fusion360 the S2B_Temp folder is removed.</li>
</ol>
</body></html>