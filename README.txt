#                         .       .
#                        / `.   .' \
#                .---.  <    > <    >  .---.
#                |    \  \ - ~ ~ - /  /    |
#                 ~-..-~             ~-..-~
#             \~~~\.'                    `./~~~/
#   .-~~^-.    \__/                        \__/
# .'  O    \     /               /       \  \
#(_____,    `._.'               |         }  \/~~~/
# `----.          /       }     |        /    \__/
#       `-.      |       /      |       /      `. ,~~|
#           ~-.__|      /_ - ~ ^|      /- _      `..-'   f: f:
#                |     /        |     /     ~-.     `-. _||_||_
#                |_____|        |_____|         ~ - . _ _ _ _ _>
#
#AUTHOR
#@@UTSAID: QTQ965

---INDEX---------------------------------------------------------------------------------------------------------

FILES:

1. Stegosaurus		- python script 	- simple pvd hiding/extraction
2. broken_Stegosaurus 	- python script 	- multiway pvd hiding/extraction !!produces incorrect output!! 

3. cover_image 		- png file 		- sample cover image
4. message_file		- text file		- sample message <random strings> <utf-8>
5. output_file 		- text file 		- result of extraction on stego_image <identical to message_file>
6. README		- text file		- README
7. stego_image		- png file		- result of embedding on cover_image

FOLDERS:

1. .idea		- intellij project settings <nothing useful here>
2. venv			- python virtual enviroment tool 


---USING Stegosaurus---------------------------------------------------------------------------------------------

<message_file> must be utf-8 encoded
<cover_image> & <stego_image> must be 24-bit .png

HIDING:	'-e'
	
	SYNTAX: 	'<python invocation> Stegosaurus.py -e <message_file> <cover_image> <stego_image>'
	EXAMPLE:	'py Stegosaurus.py -e message_file.txt cover_image.png stego_image.png'

EXTRACTION: '-d'

	SYNTAX: 	'<python invocation> Stegosaurus.py -e <stego_image> <output_file>'
	EXAMPLE:	'py Stegosaurus.py -d stego_image.png output_file.txt'

ANY OTHER USE WILL THROW ERRORS


---USING broken_STEGOSAURUS--------------------------------------------------------------------------------------

<message_file> must be utf-8 encoded
<cover_image> & <stego_image> must be 24-bit .png

HIDING:	'-e'

	SYNTAX: 	'<python invocation> broken_Stegosaurus.py -e <message_file> <cover_image>'
	EXAMPLE:	'py broken_Stegosaurus.py -e message_file.txt cover_image.png'

EXTRACTION: '-d'

	!!PRINTS SLICE OF DECODED MESSAGE TO THE SCREEN!!
	!!DOES NOT PRODUCE CORRECT OUTPUT!! 

	SYNTAX: 	'<python invocation> broken_Stegosaurus.py -d <stego_image> <output_file>'
	EXAMPLE:	'py broken_Stegosaurus.py -d stego_image.png output_file.txt'

ANY OTHER USE WILL THROW ERRORS


