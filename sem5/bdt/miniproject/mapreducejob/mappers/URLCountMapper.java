package xyz.retrixe.mappers;

import java.io.IOException;
import java.util.StringTokenizer;
import java.util.regex.Matcher;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import static xyz.retrixe.mappers.ParserUtils.logPattern;

public class URLCountMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    private final static IntWritable one = new IntWritable(1);
    private final Text word = new Text();

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String file = value.toString();
        StringTokenizer tokenizer = new StringTokenizer(file, "\n");
        while (tokenizer.hasMoreTokens()) {
            Matcher matcher = logPattern.matcher(tokenizer.nextToken());
            if (matcher.matches()) {
                String url = matcher.group(6);
                word.set(url);
                context.write(word, one);
            }
        }
    }
}
