import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class RegexCount {
	public static void main(String args[]) {
		String line = args[0];

		String r_space = "[\\s]"; 
		String r_lower = "[a-z]";
		String r_upper = "[A-Z]";
		String r_numeric = "[\\d]";
		String r_punct = "[\\(\\).,?:;]";
		String r_special = "[^\\sa-zA-Z\\d\\(\\).,?:;]";

		double prop_space = (float) countOccurences(line, r_space) /
							(float) line.length();

		double prop_lower = (float) countOccurences(line, r_lower) /
							(float) line.length();

		double prop_upper = (float) countOccurences(line, r_upper) /
							(float) line.length();

		double prop_numeric = (float) countOccurences(line, r_numeric) /
							  (float) line.length();

		double prop_punct = (float) countOccurences(line, r_punct) /
							(float) line.length();

		double prop_special = (float) countOccurences(line, r_special) /
							  (float) line.length();

		System.out.print(
			"Space: " + String.format("%.2f", prop_space) + "\n" +
			"Lower: " + String.format("%.2f", prop_lower) + "\n" +
			"Upper: " + String.format("%.2f", prop_upper) + "\n" +
			"Numeric: " + String.format("%.2f", prop_numeric) + "\n" +
			"Punct: " + String.format("%.2f", prop_punct) + "\n" +
			"Special: " + String.format("%.2f", prop_special) + "\n");
	}

	private static int countOccurences(String line, String pattern) {
		int num_occurences = 0;
		Pattern r = Pattern.compile(pattern);
		Matcher m = r.matcher(line);

		while(m.find()) 
			num_occurences++;
		return num_occurences;
	}
}