## MD2016_Final
* python3 is used.  
* `pip3 install mido` if you want to play with midi files.  
* Convert text to midi: `python3 src/txt2Midi.py data/in midi/out 1 1`  
* Create music: `python3 src/composer.py data/data_file_list data/ inputFilename outputFilename`
* Create naive music: `python3 src/naiveComposer.py data/data_file_list data/ inputFilename outputFilename`
* Create html: `python3 src/gen_html.py sample_html_input`
* Convert data to sheet:
	* Compile(Windows): `javac -sourcepath src -d bin -cp libs\abc4j_v0.5.jar src\Data2Sheet.java`
	* Compile(Mac/Linux): `javac -sourcepath src -d bin -cp libs/abc4j_v0.5.jar src/Data2Sheet.java`
	* Run(Windows): `java -cp bin;libs\abc4j_v0.5.jar Data2Sheet data\clementi_op36_no1_mv1 image\sheet.jpg`
	* Run(Mac): `java -cp bin;libs/abc4j_v0.5.jar Data2Sheet data/clementi_op36_no1_mv1 image/sheet.jpg`
	* Run(Linux): `java -cp bin:libs/abc4j_v0.5.jar Data2Sheet data/clementi_op36_no1_mv1 image/sheet.jpg`
* Simply fill the nodes by counts: `python3 src/simple_fill.py data/data_file_list data/ test/in3 test/simple_out3`

