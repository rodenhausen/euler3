<img src="http://euler.cs.ucdavis.edu/_/rsrc/1366832610901/home/logo_small.png" alt="The EulerX toolkit" width="100" height="88">
#e3

### Introduction
This repository is for the command line wrapper e3 of the [EulerX](https://github.com/EulerProject/EulerX) toolkit.
The [EulerX](https://github.com/EulerProject/EulerX) toolkit developed by the EulerProject team allows to solve the taxonomy alignment problem [<a href="http://www.slideshare.net/taxonbytes/ludaescher-etal-2014hybriddiagnosisconceptreasoning" target="_blank">1</a>, <a href="http://taxonbytes.org/pdf/ChenEtAl2014-HybridDiagnosisApproach.pdf" target="_blank">2</a>].
Here we created a wrapper around the [EulerX](https://github.com/EulerProject/EulerX) toolkit to achieve the following benefits.

### Benefits
* Modular commands with single responsiblities
* Refine taxonomy alignment problem on-the-go
* Reduce exposure to expert options
* Reduce required users knowledge of the euler life-cycle
* Reduce exposure to EulerX generated output data
* Re-use of existing computation results

### Demo
<a target="_blank" href="http://content.screencast.com/users/thomas.rodenhausen/folders/Jing/media/fb65bc4b-0dcf-4fce-b41c-1d4214c2aa4a/2016-10-19_1418.swf&blurover=false"><img src="https://img.youtube.com/vi/BbqY7htrY5U/0.jpg" alt="Replay a demo and inspect executed commands" 
width="180" height="120"></a>

### Prerequisites
Python 2.7.x, [EulerX](https://github.com/EulerProject/EulerX) 

### Command-Manual
Command                              | Description
-----------------------------------------------------------------|------------
bye							| Exit e3
help							| Shows this help
load tap \<cleantax file\>				| Loads a tap from a cleantax file
print tap [\<tap\>]					| Prints the current tap or the optionally provided \<tap\>
print taxonomies [\<tap\>]				| Prints the taxonomies of the current tap or the optionally provided \<tap\>
print articulations [\<tap\>]				| Prints the articulations of the current tap or the optionally provided \<tap\>
add articulation \<articulation\> [\<tap\>]			| Adds <articulation> to the current tap or the optionally provided \<tap\>
remove articulation \<articulation_index\> [\<tap\>]	| Removes articulation with index <articulation_index> from the current tap or the optionally provided \<tap\>
set sibling disjointness \<true\|false\> [\<tap\>]		| Sets the reasoning regions for the current tap or the optionally provided \<tap\>
set coverage \<true\|false\> [\<tap\>]			| Sets the reasoning coverage for the current tap or the optionally provided \<tap\>
set regions \<mnpw\|mncb\|mnve\|vrpw\|vrve\> [\<tap\>]		| Sets the reasoning regions for the current tap or the optionally provided \<tap\>
name tap \<name\> [\<tap\>]					| Names the current tap or the optionally provided \<tap\> as \<name\>
clear names						| Removes all stored named
print names						| Shows all stored names and their corresponding taps
use tap \<tap\>						| Makes \<tap\> the current tap
graph tap [\<tap\>]					| Creates a graph visualization of the current tap or the optionally provided \<tap\>
is consistent [\<tap\>]					| Checks the consistency of the current tap or the optionally provided \<tap\>
>= \<count\> worlds [\<tap\>]				| Checks if there are more than or equal than count number of possible worlds in the current tap or the optionally provided \<tap\>
graph worlds [\<tap\>]					| Creates graph visualizations of the possible worlds, if any exist, for the current tap or the optionally provided \<tap\>
print worlds [\<tap\>]					| Prints the possible worlds, if any exist, of the current tap or the optionally provided \<tap\>
graph summary [\<tap\>]					| Creates a summary visualization of the current tap or the optionally provided \<tap\>
graph four in one [\<tap\>]				| Creates a four-in-one visualization of the current tap or the optionally provided \<tap\>
graph inconsistency [\<tap\>]				|Creates a graph visualization of the inconsistency, if any exists, for the current tap or the optionally provided \<tap\>
graph ambiguity [\<tap\>]					| Creates an ambiguity visualization of the current tap or the optionally provided \<tap\>
print fix [\<tap\>]					| Prints a suggested fix of the inconsistency, if any exists, for the current tap or the optionally provided \<tap\>
create project \<name\>					| Creates a project with \<name\> including managable command history
print projects						| Print an overview of the existing projects
open project \<name\>					| Opens an existing project with \<name\>
close project						| Close the current project
remove project \<name\>					| Remove the project with \<name\>
clear projects						| Clears all the projects
print project history					| Print the project's command history
remove project history \<index\>				| Remove command with \<index\> and all dependent commands from the project's command history
set config \<key\>=\<value\>				| Sets the configiguration \<parameter\> with \<value\>
print config						| Prints the configiguration settings
reset							| Resets e3 to factory settings

