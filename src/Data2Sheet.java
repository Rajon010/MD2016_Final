import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import abc.midi.TunePlayer;
import abc.notation.Tune;
import abc.parser.TuneBook;
import abc.ui.swing.JScoreComponent;

public class Data2Sheet {
	public static void main(String[] args) {		
		if(args.length < 2) {
			System.out.println("[Usage] java -cp classpath Data2Sheet DataFileName SheetFileName");
			return;
		}
		try {
			String dataFileName = args[0], sheetFileName = args[1];
			// read data and parse to ABC format
			BufferedReader br = new BufferedReader( new FileReader(dataFileName) );
			BufferedWriter bw = new BufferedWriter( new FileWriter(dataFileName + ".abc") );
			bw.write("X:1\nT:Music Data\nM:4/4\nC:MD\nK:C\n");
			String line = null;
			int count = 0;
			while( ( line = br.readLine() ) != null ) {
				String[] splitedLine = line.split(" +");
				if(splitedLine.length == 0)	continue;
				if( splitedLine[0].equals("@") )	continue;
				if( splitedLine[0].equals("C") )	bw.write("[C4E4G4");
				else if( splitedLine[0].equals("Dm") )	bw.write("[D4F4A4");
				else if( splitedLine[0].equals("F") )	bw.write("[F4A4c4");
				else if( splitedLine[0].equals("G") )	bw.write("[G4B4d4");
				else if( splitedLine[0].equals("Am") )	bw.write("[A4c4e4");
				if( splitedLine[1].equals("-") && splitedLine[2].equals("-") && splitedLine[3].equals("-") && splitedLine[4].equals("-") )
					bw.write("]");
				else {
					if( splitedLine[1].equals("-") )	bw.write("");
					else if( splitedLine[1].endsWith("4") )	bw.write( splitedLine[1].toUpperCase().charAt(0) + "," );
					else if( splitedLine[1].endsWith("5") )	bw.write( splitedLine[1].toUpperCase().charAt(0) + "" );
					else if( splitedLine[1].endsWith("6") )	bw.write( splitedLine[1].charAt(0) + "" );
					else if( splitedLine[1].endsWith("7") )	bw.write( splitedLine[1].charAt(0) + "'" );
					for(int i = 2 ; i < 5 ; i++) {
						if(i == 2) {
							if( !splitedLine[1].equals("-") && splitedLine[2].equals("-") ) {
								bw.write("2]");
								continue;
							}
							else if( splitedLine[1].equals("-") && splitedLine[2].equals("-") ) {
								bw.write("]");
								continue;
							}
							bw.write("]");
						}
						if( splitedLine[i].equals("-") ) {
							if(i == 4)	bw.write("2");
							else	bw.write("z");
						}
						else if( splitedLine[i].endsWith("4") )	bw.write( splitedLine[i].toUpperCase().charAt(0) + "," );
						else if( splitedLine[i].endsWith("5") )	bw.write( splitedLine[i].toUpperCase().charAt(0) + "" );
						else if( splitedLine[i].endsWith("6") )	bw.write( splitedLine[i].charAt(0) + "" );
						else if( splitedLine[i].endsWith("7") )	bw.write( splitedLine[i].charAt(0) + "'" );
					}
				}
				count += 1;
				if(count % 2 == 1)	bw.write(" ");
				else	bw.write("|");
				if(count % 8 == 0) {
					count = 0;
					bw.write("\n");
				}
			}
			bw.write("\n");
			br.close();
			bw.close();
			// loading from the file
			TuneBook book = new TuneBook( new File(dataFileName + ".abc") );
			// show details about the tunes that are loaded
			// System.out.println("# of tunes in itsyBitsy.abc : " + book.size());
			// retrieve the specific tune by reference number
			Tune tune = book.getTune(1);
			// display its title
			// System.out.print("Title of #1 is " + tune.getTitles()[0]);
			// and its key
			// System.out.println(" and is in the key of " + tune.getKey().toLitteralNotation());
			// can export to a file (abc notation)
			// book.saveTo(new File("out.abc"));
			// creates a simple midi player to play the melody
			TunePlayer player = new TunePlayer();
			// player.start();
			// player.play(tune);
			// creates a component that draws the melody on a musical staff
			JScoreComponent jscore = new JScoreComponent();
			jscore.setJustification(true);
			jscore.setTune(tune);
			// JFrame j = new JFrame();
			// j.add(jscore);
			// j.pack();
			// j.setVisible(true);
			// writes the score to a JPG file
			jscore.writeScoreTo( new File(sheetFileName) );
		} catch (IOException e) {
			System.err.println("[Error] I/O Exception");
			e.printStackTrace();
		}
	}
}
