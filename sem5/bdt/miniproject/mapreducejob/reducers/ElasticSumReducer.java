package xyz.retrixe.reducers;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.MapWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class ElasticSumReducer extends Reducer<Text, IntWritable, Text, MapWritable> {
    public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable x : values) {
            sum += x.get();
        }
        MapWritable outputDocument = new MapWritable();
        outputDocument.put(new Text("key"), key);
        outputDocument.put(new Text("count"), new IntWritable(sum));
        context.write(key, outputDocument);
    }
}
