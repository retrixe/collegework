package xyz.retrixe;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Main {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = new Job(conf, "Payment-wise MapReduce");
        job.setJarByClass(Main.class);

        if (args.length < 3) {
            throw new RuntimeException("No operation specified!");
        }
        switch (args[2]) {
            case "minPayment":
                job.setMapperClass(MinPaymentMapper.class);
                job.setReducerClass(MinReducer.class);
                break;
            case "productTotal":
                job.setMapperClass(ProductTotalMapper.class);
                job.setReducerClass(SumReducer.class);
                break;
            case "paymentTotal":
                job.setMapperClass(PaymentTotalMapper.class);
                job.setReducerClass(SumReducer.class);
                break;
            default:
                throw new RuntimeException("Invalid operation!");
        }
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
