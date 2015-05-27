package org.grobid.trainer.evaluation;

import java.util.ArrayList;

public class ConfusionMatrix {
	
	private ArrayList<ArrayList<Integer>> matrix;
	private ArrayList<String> labels = new ArrayList<String>();
	private int numCols;
	private int numRows;
	
	public ConfusionMatrix() {
		this.matrix = new ArrayList<ArrayList<Integer>>();
		this.numRows = 0;
		this.numCols = 0;
	}
	
	public void increment(String rowLabel, String colLabel) {
		if(labels.indexOf(rowLabel) == -1) {
			addLabel(rowLabel);
		}
		if(labels.indexOf(colLabel) == -1) {
			addLabel(colLabel);
		}
		int rowIndex = labels.indexOf(rowLabel);
		int colIndex = labels.indexOf(colLabel);
		int prevValue = this.matrix.get(rowIndex).get(colIndex);
		this.matrix.get(rowIndex).set(colIndex, prevValue + 1);
	}
	
	private void addLabel(String label) {
		this.labels.add(label);
		this.addRow();
		this.addColumn();
	}
	
	private void addRow() {
		ArrayList<Integer> newRow = new ArrayList<Integer>();
		for(int i = 0; i < this.numCols; i++) {
			newRow.add(0);
		}
		matrix.add(newRow);
		numRows++;
	}
	
	private void addColumn() {
		for(int i = 0; i < this.numRows; i++) {
			matrix.get(i).add(0);
		}
		numCols++;
	}
	
	public String toString() {
		String confusionString = "";
//		for(String label : this.labels) {
//			confusionString += "\t";
//			confusionString += label;
//		}
//		confusionString += "\n";
		for(ArrayList<Integer> row : this.matrix) {
			confusionString += this.labels.get(this.matrix.indexOf(row));
			for(Integer val : row) {
				confusionString += "\t";
				confusionString += val;
			}
			confusionString += "\n";
		}
		return confusionString;
	}
}
