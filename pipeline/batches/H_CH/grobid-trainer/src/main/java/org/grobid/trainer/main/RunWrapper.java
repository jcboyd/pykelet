package org.grobid.trainer.main;

import java.io.IOException;

import org.grobid.trainer.TrainerRunner;

public class RunWrapper {
	public static void main(String [] args) throws IOException {
		String mode = "0";
		String model = "header";
		
		/* 
		 * ['affiliation', 'chemical', 'date', 'citation', 'ebook', 'fulltext',
		 *  'header', 'name-citation', 'name-header', 'patent', 'segmentation',
		 *  'reference-segmenter']
		 */
		
		String grobid_home = "/home/joseph/Desktop/grobid/grobid-home";
		String split = "0.8";
		
		if(mode == "0" || mode == "1") {
			TrainerRunner.main(new String[] {mode, model, "-gH", grobid_home});
		}
		else {
			TrainerRunner.main(new String[] {mode, model, "-gH", grobid_home, "-s", split});
		}	
	}
}