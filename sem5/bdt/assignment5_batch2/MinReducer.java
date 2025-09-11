package xyz.retrixe;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class MinReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        int min = Integer.MAX_VALUE;
        for (IntWritable x : values) {
            min = Math.min(min, x.get());
        }
        context.write(key, new IntWritable(min));
    }
}
