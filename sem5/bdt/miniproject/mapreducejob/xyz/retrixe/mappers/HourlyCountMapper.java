package xyz.retrixe.mappers;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import java.util.StringTokenizer;
import java.util.regex.Matcher;

import static xyz.retrixe.mappers.ParserUtils.logPattern;

public class HourlyCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    private final static IntWritable one = new IntWritable(1);
    private final Text word = new Text();

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String file = value.toString();
        StringTokenizer tokenizer = new StringTokenizer(file, "\n");
        while (tokenizer.hasMoreTokens()) {
            Matcher matcher = logPattern.matcher(tokenizer.nextToken());
            if (matcher.matches()) {
                String timestamp = matcher.group(4); // "10/Oct/2000:13:55:36 -0700"
                String hour = timestamp.split(":")[1];
                word.set(hour); // "13"
                context.write(word, one);
            }
        }
    }
}
