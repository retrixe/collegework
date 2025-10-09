package xyz.retrixe;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class MinPaymentMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String file = value.toString();
        StringTokenizer tokenizer = new StringTokenizer(file, "\n");
        while (tokenizer.hasMoreTokens()) {
            String line = tokenizer.nextToken();
            if (line.startsWith("Transaction")) // Ignore the header
                continue;
            String[] fields = line.split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)");
            value.set(fields[3].trim());
            String sanitizedPrice = fields[2]
                    .replaceAll("\"", "")
                    .replaceAll(",", "");
            context.write(value, new IntWritable(Integer.parseInt(sanitizedPrice)));
        }
    }
}
